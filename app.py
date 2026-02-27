from flask import Flask, render_template, request, redirect, session, flash 
from manager import ManagerMahasiswa
from database import get_db
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("login"):
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            return "akses ditolak"
        return f(*args, **kwargs)
    return wrapper

app = Flask(__name__)
app.secret_key = "rahasia"

manager = ManagerMahasiswa()

@app.route("/")
def index():
    db = get_db()
    
    page = int(request.args.get("page", 1))
    per_page = 5

    offset = (page - 1) * per_page

    data = db.execute(
        "SELECT *FROM mahasiswa LIMIT ? OFFSET ?",
        (per_page, offset)
    ).fetchall()
    
    total = db.execute("SELECT COUNT(*) " \
    "FROM mahasiswa").fetchone()[0]
    total_page = (total + per_page - 1) // per_page

    return render_template("index.html", data=data, page=page, total_page=total_page)

@app.route("/tambah", methods=["GET","POST"])
@login_required
@admin_required
def tambah():
    if request.method == "POST":
        nama = request.form["nama"]
        nilai = int(request.form["nilai"])
        
        if nilai < 0 or nilai > 100:
            return render_template("tambah.html",
            error="nilai harus diantar 0 sampai 100")
        
        manager.tambah(nama, nilai)
        flash("data berhasil ditambahkan")

        return redirect("/")
    
    return render_template("tambah.html")

@app.route("/hapus/<nama>")
@login_required
@admin_required
def hapus(nama):
    if session.get("role") != "admin":
        return "tidak punya akses"
    manager.hapus(nama)
    flash("data berhasil dihapus")
    return redirect("/")  

@app.route("/edit/<nama>", methods=["GET", "POST"])
@login_required
@admin_required
def edit(nama):
    if session.get("role") != "admin":
        return "tidak punya akses"    

    mhs = manager.cari(nama)

    if not mhs:
        return "Data tidak ditemukan"
    
    if request.method == "POST":
        nilai = int(request.form["nilai"])

        if nilai < 0 or nilai > 100:
            return render_template("edit.html",
            mhs = mhs, error="nilai harus antara 0 sampai 100") 

        db = get_db()
        db.execute(
            "UPDATE mahasiswa SET nilai=? WHERE nama=?",
            (nilai, nama)
        )
        db.commit()

        flash("data berhasil diupdate")
        return redirect("/")

    return render_template("edit.html", mhs=mhs)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = manager.login(username, password)

        if user:
            session["login"] = True
            session["role"] = user["role"]
            session["username"] = user["username"]
            return redirect("/")
        else:
            return render_template("login.html", error="login gagal")
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/cari", methods=["GET", "POST"])
def cari():
    hasil = None

    if request.method == "POST":
        nama = request.form["nama"]
        hasil = manager.cari(nama)
        
        return render_template("cari.html", 
hasil=hasil)
    
    return render_template("cari.html",
hasil = None)
    
@app.route("/api/mahasiswa", methods=["GET"])
def api_semua():
    data = manager.semua()

    hasil = []
    for mhs in data:
        hasil.append({
            "nama" : mhs.nama,
            "nilai" : mhs.nilai,
            "status" : mhs.cek_lulus()
        })
    return jsonify(hasil)

@app.route("/api/mahasiswa/<nama>", methods = ["GET"])
def api_detail(nama):
    mhs = manager.cari(nama)

    if not mhs:
        return jsonify({"error": "tidak ditemukan"})
    
    return jsonify({
        "nama" : mhs.nama,
        "nilai" : mhs.nilai,
        "status" : mhs.cek_lulus()
    })

@app.route("/api/mahasiswa", methods = ["POST"])
def api_tambah():
    data = request.get_json()

    nama = data["nama"]
    nilai = data["nilai"]

    if nilai < 0 or nilai > 100:
        return jsonify({"error" : "nilai harus 0-100"})
    
    manager.tambah(nama, nilai)

    return jsonify({"message": "berhasil ditambahkan"})

@app.route("/api/mahasiswa/<nama>", methods = ["PUT"])
def api_edit(nama):
    data = request.get_json()
    nilai = data["nilai"]

    if nilai < 0 or nilai > 100:
        return jsonify({"error": "nilai tidak valid"})
    
    db = get_db()
    db.execute(
        "UPDATE mahasiswa SET nilai=? WHERE nama=?",
        (nilai, nama)
    )
    db.commit()

    return jsonify({"message": "berhasil diupdate"})

@app.route("/api/mahasiswa/<nama>", methods = ["DELETE"])
def api_hapus(nama):
    manager.hapus(nama)
    return jsonify({"message": "berhasil dihapus"})

@app.route("/api/lulus", methods = ["GET"])
def api_lulus():
    data = manager.semua()

    hasil = []

    for mhs in data:
        if mhs.nilai >= 75:
            hasil.append({
                "nama": mhs.nama,
                "nilai": mhs.nilai,
                "status": "lulus"
            })

    return jsonify(hasil)
        
if __name__== "__main__":
    app.run(host="0.0.0.0", port=5000)