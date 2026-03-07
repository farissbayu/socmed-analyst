import json
from datetime import datetime
from sqlmodel import Session, create_engine
from app.models.database import TikTokVideo  # Sesuaikan path import-nya jika berbeda

# Setup engine database
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)


def extract_video_id_from_url(url):
    """
    Extract video ID from TikTok URL.
    Example: https://www.tiktok.com/@pemkab_pasuruan/video/7614341245522939144
    Returns: 7614341245522939144
    """
    if url and "/video/" in url:
        return url.split("/video/")[-1]
    return None


def seed_videos_from_json(filepath="seed_data/videos.json", min_date_str="2026-01-01"):
    """
    Extract video data from JSON and seed into database.

    Args:
        filepath: Path to videos.json
        min_date_str: Minimum date filter (YYYY-MM-DD format)
    """

    min_date = datetime.strptime(min_date_str, "%Y-%m-%d")
    videos_list = []
    total_comments = 0

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"📊 Total video dalam JSON: {len(data)}")
        print(f"🎯 Filter: Video dengan release date >= {min_date_str}\n")

        # 1. Ekstrak data video dari JSON
        for item in data:
            # Extract and parse date from createTimeISO field
            date_str = item.get("createTimeISO")

            if date_str:
                try:
                    # Parse ISO 8601 format (e.g., "2026-03-07T02:52:58.000Z")
                    video_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

                    # Filter by date - only include videos from min_date onwards
                    if video_date.date() >= min_date.date():
                        # Extract video ID from URL
                        video_url = item.get("webVideoUrl")
                        video_id = extract_video_id_from_url(video_url)

                        if video_id and video_url:
                            # Parse video creation timestamp
                            video_created_at = None
                            try:
                                video_created_at = datetime.fromisoformat(
                                    date_str.replace("Z", "+00:00")
                                )
                            except (ValueError, AttributeError):
                                pass

                            video_data = {
                                "id_tiktok_video": video_id,
                                "tiktok_user_id": item.get("authorMeta.name"),
                                "video_web_url": video_url,
                                "submitted_video_url": video_url,
                                "video_created_at": video_created_at,
                            }

                            videos_list.append(video_data)

                            # Sum comments
                            comment_count = item.get("commentCount", 0)
                            if isinstance(comment_count, int):
                                total_comments += comment_count

                except (ValueError, AttributeError):
                    # If date parsing fails, skip this item
                    pass

        print(f"✅ Total video setelah filter: {len(videos_list)}")
        print(f"💬 Total comments dari semua video yang difilter: {total_comments}\n")

        # 2. Masukkan ke Database
        if videos_list:
            with Session(engine) as session:
                for video_data in videos_list:
                    # Unpacking dictionary langsung ke model TikTokVideo
                    video_db = TikTokVideo(**video_data)

                    # Pakai merge agar aman dari error duplicate Primary Key
                    session.merge(video_db)

                session.commit()

            print(
                f"✅ Berhasil mengekstrak dan menyimpan {len(videos_list)} video ke database!"
            )
            return videos_list, total_comments
        else:
            print("⚠️  Tidak ada video yang sesuai dengan filter tanggal")
            return [], 0

    except FileNotFoundError:
        print(f"❌ File {filepath} tidak ditemukan!")
        return [], 0
    except json.JSONDecodeError:
        print("❌ Format JSON tidak valid. Pastikan formatnya array [...]")
        return [], 0
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return [], 0


if __name__ == "__main__":
    videos, total_comments = seed_videos_from_json(
        filepath="seed_data/videos.json", min_date_str="2026-01-01"
    )
