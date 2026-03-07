import re
from sqlmodel import Session, create_engine
from app.models.database import WilayahKecamatan, WilayahDesa  # Sesuaikan path-nya

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)


def seed_from_sql_files():
    with Session(engine) as session:
        print("Mulai seeding data...")

        try:
            with open("seed_data/wilayah_kecamatan.sql", "r", encoding="utf-8") as f:
                content = f.read()
                matches = re.findall(r"\((\d+),\s*\d+,\s*'([^']+)'\)", content)

                kecamatan_list = [
                    WilayahKecamatan(id_kecamatan=int(id_kec), nama_kecamatan=nama)
                    for id_kec, nama in matches
                ]
                for kecamatan in kecamatan_list:
                    session.merge(kecamatan)
                session.commit()
                print(f"Berhasil memproses {len(kecamatan_list)} data Kecamatan.")
        except FileNotFoundError:
            print("File wilayah_kecamatan.sql tidak ditemukan!")

        try:
            with open("seed_data/wilayah_desa.sql", "r", encoding="utf-8") as f:
                content = f.read()
                matches = re.findall(r"\((\d+),\s*(\d+),\s*'([^']+)'\)", content)

                desa_list = [
                    WilayahDesa(
                        id_desa=int(id_desa), kecamatan_id=int(kec_id), nama_desa=nama
                    )
                    for id_desa, kec_id, nama in matches
                ]
                for desa in desa_list:
                    session.merge(desa)
                session.commit()
                print(f"Berhasil memproses {len(desa_list)} data Desa.")
        except FileNotFoundError:
            print("File desa.sql tidak ditemukan!")

        session.commit()
        print("Seeding selesai dan berhasil disimpan ke database!")


if __name__ == "__main__":
    seed_from_sql_files()
