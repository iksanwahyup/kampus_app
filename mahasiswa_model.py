from database import get_db

class MahasiswaModel:

    @staticmethod
    def tambah(nama, nilai):
        db = get_db()
        db.execute(
            "INSERT INTO mahasiswa(nama, nilai) VALUES (?, ?)",
            (nama, nilai)
        )
        db.commit()

    @staticmethod
    def semua():
        db = get_db()
        return db.execute("SELECT * FROM mahasiswa").fetchall()
    
    @staticmethod
    def hapus(id):
        db = get_db()
        db.execute("DELETE FROM mahasiswa WHERE id = ?", (id,))
        db.commit()