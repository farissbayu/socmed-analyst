from app.models.engine import engine
import json
from sqlmodel import Session
from app.models.database import TikTokUser


def seed_user_from_json(filepath="seed_data/user_videos.json"):
    unique_users = {}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            uid = item.get("authorMeta.id")
            username = item.get("authorMeta.name")
            avatar = item.get("authorMeta.avatar")

            if uid and uid not in unique_users:
                unique_users[uid] = {
                    "id_tiktok_user": uid,
                    "username": username,
                    "avatar_thumbnail": avatar,
                    "is_priority": True,
                }

        hasil_ekstrak = list(unique_users.values())

        with Session(engine) as session:
            for user_data in hasil_ekstrak:
                user_db = TikTokUser(**user_data)
                session.merge(user_db)

            session.commit()

        return hasil_ekstrak

    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception:
        return []


if __name__ == "__main__":
    seed_user_from_json("seed_data/user_videos.json")
