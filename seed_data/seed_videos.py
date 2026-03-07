import json
from datetime import datetime
from sqlmodel import Session
from app.models.database import TikTokVideo
from app.models.engine import engine


def extract_video_id_from_url(url):
    if url and "/video/" in url:
        return url.split("/video/")[-1]
    return None


def seed_videos_from_json(filepath="seed_data/videos.json", min_date_str="2026-01-01"):
    min_date = datetime.strptime(min_date_str, "%Y-%m-%d")
    videos_list = []
    total_comments = 0

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            date_str = item.get("createTimeISO")

            if date_str:
                try:
                    video_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

                    if video_date.date() >= min_date.date():
                        video_url = item.get("webVideoUrl")
                        video_id = extract_video_id_from_url(video_url)

                        if video_id and video_url:
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

                            comment_count = item.get("commentCount", 0)
                            if isinstance(comment_count, int):
                                total_comments += comment_count

                except (ValueError, AttributeError):
                    pass

        if videos_list:
            with Session(engine) as session:
                for video_data in videos_list:
                    video_db = TikTokVideo(**video_data)
                    session.merge(video_db)

                session.commit()

            return videos_list, total_comments
        else:
            return [], 0

    except FileNotFoundError:
        return [], 0
    except json.JSONDecodeError:
        return [], 0
    except Exception:
        return [], 0


if __name__ == "__main__":
    videos, total_comments = seed_videos_from_json(
        filepath="seed_data/videos.json", min_date_str="2026-01-01"
    )
