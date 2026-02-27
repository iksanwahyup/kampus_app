from mahasiswa import Mahasiswa
from database import get_db

db = get_db()

db.execute("""
CREATE TABLE IF NOT EXISTS mahasiswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    nilai INTEGER
)
""")

db.commit()


class ManagerMahasiswa:
    def __init__(self):
        self.data = []

    def tambah(self, nama, nilai):
        db = get_db()
        db.execute(
            "INSERT INTO mahasiswa (nama, nilai) VALUES (?, ?)",
            (nama, nilai)
        )
        db.commit()
    
    def lihat(self):
        db = get_db()
        hasil = db.execute("SELECT nama, nilai FROM mahasiswa")

        for nama, nilai in hasil:
            mhs = Mahasiswa(nama, nilai)
            print(mhs)
    
    def cari(self, nama):
        db = get_db()
        hasil = db.execute(
            "SELECT nama, nilai FROM mahasiswa WHERE nama=?",
            (nama,)
        ).fetchone()

        if hasil:
            return Mahasiswa(hasil[0], hasil[1])
        return None
    
    def hapus(self, nama):
        db = get_db()
        db.execute("DELETE FROM mahasiswa WHERE nama=?", (nama,))
        db.commit()

    def semua(self):
        db = get_db()
        hasil = db.execute("SELECT nama, nilai FROM mahasiswa").fetchall()

        data = []
        for nama, nilai in hasil:
            data.append(Mahasiswa(nama, nilai))
        return data
    
    def login(self, username, password):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username=? AND password=?"
            (username, password)
        ).fetchone()
        return user