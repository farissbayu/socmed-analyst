import json
from sqlmodel import Session, create_engine
from app.models.database import OrganisasiPerangkatDaerah

# Setup engine database
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)


def seed_opd_from_json(filepath="seed_data/opd.json"):
    """
    Extract OPD (Organisasi Perangkat Daerah) data from JSON and seed into database.

    Args:
        filepath: Path to opd.json
    """

    opd_list = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"📊 Total OPD dalam JSON: {len(data)}")

        # 1. Ekstrak data OPD dari JSON
        for item in data:
            try:
                id_opd = item.get("id_opd")
                nama_opd = item.get("nama_opd", "")
                singkatan = item.get("singkatan")
                deskripsi_tugas = item.get("deskripsi_tugas")
                kategori_tugas = item.get("kategori_tugas")
                tiktok_user_id = item.get("tiktok_user_id")

                if id_opd and nama_opd:
                    opd_data = {
                        "id_opd": id_opd,
                        "nama_opd": nama_opd,
                        "singkatan": singkatan,
                        "deskripsi_tugas": deskripsi_tugas,
                        "kategori_tugas": kategori_tugas,
                        "tiktok_user_id": tiktok_user_id,
                    }

                    opd_list.append(opd_data)

            except (KeyError, ValueError, AttributeError):
                # Skip items with missing required fields
                pass

        print(f"✅ Extracted {len(opd_list)} OPD records\n")

        # 2. Masukkan ke Database
        if opd_list:
            with Session(engine) as session:
                for opd_data in opd_list:
                    opd_db = OrganisasiPerangkatDaerah(**opd_data)
                    # Use merge to avoid duplicate errors if running seeder multiple times
                    session.merge(opd_db)

                session.commit()

            print(
                f"✅ Berhasil mengekstrak dan menyimpan {len(opd_list)} OPD records ke database!"
            )
            return opd_list
        else:
            print("⚠️  Tidak ada OPD records yang valid untuk diseed")
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
    opd_records = seed_opd_from_json(filepath="seed_data/opd.json")
