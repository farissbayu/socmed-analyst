import json
from datetime import datetime
from sqlmodel import Session, create_engine, select
from app.models.database import TikTokComment, TikTokUser

# Setup engine database
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)


def extract_video_id_from_url(url):
    """
    Extract video ID from TikTok URL.
    Example: https://www.tiktok.com/@pemkab_pasuruan/video/7605445736410533128
    Returns: 7605445736410533128
    """
    if url and "/video/" in url:
        return url.split("/video/")[-1]
    return None


def seed_comments_from_json(filepath="seed_data/comments.json"):
    """
    Extract comment data from JSON and seed into database.
    Also creates missing users with is_priority=False if they don't exist.

    Args:
        filepath: Path to comments.json
    """

    comments_list = []
    users_dict = {}  # Store unique users: {user_id: {username, avatar_url}}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"📊 Total comments dalam JSON: {len(data)}")

        # 1. Ekstrak data comments dan users dari JSON
        for item in data:
            try:
                # Extract video ID from URL
                video_url = item.get("videoWebUrl")
                video_id = extract_video_id_from_url(video_url)

                # Get user ID - use uid from comment
                user_id = item.get("uid")

                # Get comment ID
                comment_id = item.get("cid")

                if comment_id and video_id and user_id:
                    # Collect user data (only once per user)
                    if user_id not in users_dict:
                        users_dict[user_id] = {
                            "username": item.get("uniqueId", ""),
                            "avatar_thumbnail": item.get("avatarThumbnail", ""),
                        }

                    # Parse ISO date to datetime
                    create_time_iso_str = item.get("createTimeISO")
                    create_time_iso = None

                    if create_time_iso_str:
                        try:
                            create_time_iso = datetime.fromisoformat(
                                create_time_iso_str.replace("Z", "+00:00")
                            )
                        except (ValueError, AttributeError):
                            pass

                    comment_data = {
                        "id_tiktok_comment": comment_id,
                        "video_id": video_id,
                        "user_id": user_id,
                        "input_url": item.get("input", video_url),
                        "create_time": item.get("createTime") or 0,
                        "create_time_iso": create_time_iso,
                        "text": item.get("text") or "",
                        "digg_count": item.get("diggCount") or 0,
                        "liked_by_author": item.get("likedByAuthor") or False,
                        "pinned_by_author": item.get("pinnedByAuthor") or False,
                        "replies_to_id": item.get("repliesToId"),
                        "reply_comment_total": item.get("replyCommentTotal") or 0,
                    }

                    comments_list.append(comment_data)

            except (KeyError, ValueError, AttributeError):
                # Skip items with missing required fields
                pass

        print(f"✅ Extracted {len(comments_list)} comments")
        print(f"📊 Found {len(users_dict)} unique users in comments\n")

        # 2. Masukkan users dan comments ke Database
        if comments_list:
            with Session(engine) as session:
                # First, handle users
                users_created = 0
                users_skipped = 0

                for user_id, user_data in users_dict.items():
                    # Check if user already exists
                    statement = select(TikTokUser).where(
                        TikTokUser.id_tiktok_user == user_id
                    )
                    existing_user = session.exec(statement).first()

                    if existing_user:
                        # User exists - skip if is_priority is True, otherwise we can update
                        if existing_user.is_priority:
                            users_skipped += 1
                            print(
                                f"  ⏭️  User {user_data['username']} already exists with is_priority=True"
                            )
                        else:
                            # User exists but is_priority is False, update it with new data if available
                            if user_data["avatar_thumbnail"]:
                                existing_user.avatar_thumbnail = user_data[
                                    "avatar_thumbnail"
                                ]
                            session.add(existing_user)
                            users_skipped += 1
                    else:
                        # Create new user with is_priority=False
                        new_user = TikTokUser(
                            id_tiktok_user=user_id,
                            username=user_data["username"] or "",
                            avatar_thumbnail=user_data["avatar_thumbnail"],
                            is_priority=False,
                        )
                        session.add(new_user)
                        users_created += 1

                session.commit()
                print(
                    f"✅ Created {users_created} new users, skipped {users_skipped} existing users"
                )

                # Then, handle comments
                for comment_data in comments_list:
                    comment_db = TikTokComment(**comment_data)
                    session.merge(comment_db)

                session.commit()

            print(
                f"✅ Berhasil mengekstrak dan menyimpan {len(comments_list)} comments ke database!"
            )
            return comments_list
        else:
            print("⚠️  Tidak ada comments yang valid untuk diseed")
            return []

    except FileNotFoundError:
        print(f"❌ File {filepath} tidak ditemukan!")
        return []
    except json.JSONDecodeError:
        print("❌ Format JSON tidak valid. Pastikan formatnya array [...]")
        return []
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


if __name__ == "__main__":
    comments = seed_comments_from_json(filepath="seed_data/comments.json")
