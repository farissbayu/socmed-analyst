import json
from sqlmodel import Session, create_engine
from app.models.database import TikTokUser  # Sesuaikan path import-nya jika berbeda

# Setup engine database
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)


def seed_user_from_json(filepath="seed_data/user_videos.json"):
    # Kita pakai dictionary untuk menyimpan user unik berdasarkan ID
    unique_users = {}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1. Ekstrak data unik dari JSON
        for item in data:
            uid = item.get("authorMeta.id")
            username = item.get("authorMeta.name")
            avatar = item.get("authorMeta.avatar")

            # Kalau ID-nya ada dan belum masuk ke dictionary, kita tambahkan
            if uid and uid not in unique_users:
                unique_users[uid] = {
                    "id_tiktok_user": uid,
                    "username": username,
                    "avatar_thumbnail": avatar,
                    "is_priority": True,  # Kita set True karena ini akun target utama (Bupati)
                }

        hasil_ekstrak = list(unique_users.values())

        # 2. Masukkan ke Database
        with Session(engine) as session:
            for user_data in hasil_ekstrak:
                # Unpacking dictionary langsung ke model TikTokUser
                user_db = TikTokUser(**user_data)

                # Pakai merge agar aman dari error duplicate Primary Key
                session.merge(user_db)

            session.commit()

        print(
            f"✅ Berhasil mengekstrak dan menyimpan {len(hasil_ekstrak)} user unik ke database!"
        )
        return hasil_ekstrak

    except FileNotFoundError:
        print(f"❌ File {filepath} tidak ditemukan!")
        return []
    except json.JSONDecodeError:
        print("❌ Format JSON tidak valid.")
        return []
    except Exception as e:
        print(f"❌ Error seeding users: {str(e)}")
        return []


if __name__ == "__main__":
    seed_user_from_json("seed_data/user_videos.json")
