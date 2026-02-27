import sqlite3

conn = sqlite3.connect("kampus.db")
db = conn.cursor()

db.execute("""
CREATE TABLE IF NOT EXISTS mahasiswa(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           nama TEXT,
           nilai INTEGER
           )
""")

conn.commit()
conn.close()

print("Database & dan tabel siap!")