from app.models.engine import engine
import json
from sqlmodel import Session
from app.models.database import OrganisasiPerangkatDaerah


def seed_opd_from_json(filepath="seed_data/opd.json"):
    opd_list = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

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
                pass

        if opd_list:
            with Session(engine) as session:
                for opd_data in opd_list:
                    opd_db = OrganisasiPerangkatDaerah(**opd_data)
                    session.merge(opd_db)

                session.commit()

            return opd_list
        else:
            return []

    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception:
        return []


if __name__ == "__main__":
    opd_records = seed_opd_from_json(filepath="seed_data/opd.json")
