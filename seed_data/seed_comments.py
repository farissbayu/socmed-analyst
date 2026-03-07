from app.models.engine import engine
import json
from datetime import datetime
from sqlmodel import Session, select
from app.models.database import TikTokComment, TikTokUser


def extract_video_id_from_url(url):
    if url and "/video/" in url:
        return url.split("/video/")[-1]
    return None


def seed_comments_from_json(filepath="seed_data/comments.json"):
    comments_list = []
    users_dict = {}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            try:
                video_url = item.get("videoWebUrl")
                video_id = extract_video_id_from_url(video_url)
                user_id = item.get("uid")
                comment_id = item.get("cid")

                if comment_id and video_id and user_id:
                    if user_id not in users_dict:
                        users_dict[user_id] = {
                            "username": item.get("uniqueId", ""),
                            "avatar_thumbnail": item.get("avatarThumbnail", ""),
                        }

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
                pass

        if comments_list:
            with Session(engine) as session:
                for user_id, user_data in users_dict.items():
                    statement = select(TikTokUser).where(
                        TikTokUser.id_tiktok_user == user_id
                    )
                    existing_user = session.exec(statement).first()

                    if existing_user:
                        if (
                            not existing_user.is_priority
                            and user_data["avatar_thumbnail"]
                        ):
                            existing_user.avatar_thumbnail = user_data[
                                "avatar_thumbnail"
                            ]
                            session.add(existing_user)
                    else:
                        new_user = TikTokUser(
                            id_tiktok_user=user_id,
                            username=user_data["username"] or "",
                            avatar_thumbnail=user_data["avatar_thumbnail"],
                            is_priority=False,
                        )
                        session.add(new_user)

                session.commit()

                for comment_data in comments_list:
                    comment_db = TikTokComment(**comment_data)
                    session.merge(comment_db)

                session.commit()

            return comments_list
        else:
            return []

    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception:
        return []


if __name__ == "__main__":
    comments = seed_comments_from_json(filepath="seed_data/comments.json")
