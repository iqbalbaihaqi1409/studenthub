
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.environ.get("VERCEL"):
    DATABASE = "/tmp/studenthub.db"
else:
    DATABASE = os.path.join(BASE_DIR, "studenthub.db")


def get_db():
    koneksi = sqlite3.connect(DATABASE)
    koneksi.row_factory = sqlite3.Row
    return koneksi


def buat_database():
    with get_db() as koneksi:
        koneksi.execute("""
            CREATE TABLE IF NOT EXISTS tugas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                matkul TEXT NOT NULL,
                deadline TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Belum selesai'
            )
        """)


buat_database()


@app.route("/")
def home():
    with get_db() as koneksi:
        total = koneksi.execute(
            "SELECT COUNT(*) FROM tugas"
        ).fetchone()[0]

        selesai = koneksi.execute(
            "SELECT COUNT(*) FROM tugas WHERE status = 'Selesai'"
        ).fetchone()[0]

        belum_selesai = total - selesai

        tugas_terbaru = koneksi.execute(
            "SELECT * FROM tugas ORDER BY id DESC LIMIT 5"
        ).fetchall()

    return render_template(
        "index.html",
        total=total,
        selesai=selesai,
        belum_selesai=belum_selesai,
        tugas_terbaru=tugas_terbaru
    )


@app.route("/jadwal")
def jadwal():
    return render_template("jadwal.html")


@app.route("/tugas", methods=["GET", "POST"])
def tugas():
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        matkul = request.form.get("matkul", "").strip()
        deadline = request.form.get("deadline", "").strip()

        if nama and matkul and deadline:
            with get_db() as koneksi:
                koneksi.execute(
                    """
                    INSERT INTO tugas (nama, matkul, deadline)
                    VALUES (?, ?, ?)
                    """,
                    (nama, matkul, deadline)
                )

        return redirect(url_for("tugas"))

    with get_db() as koneksi:
        tugas_list = koneksi.execute(
            "SELECT * FROM tugas ORDER BY id DESC"
        ).fetchall()

    return render_template("tugas.html", tugas_list=tugas_list)


@app.route("/tugas/selesai/<int:id>", methods=["POST"])
def tugas_selesai(id):
    with get_db() as koneksi:
        koneksi.execute(
            "UPDATE tugas SET status = 'Selesai' WHERE id = ?",
            (id,)
        )

    return redirect(url_for("tugas"))


@app.route("/tugas/hapus/<int:id>", methods=["POST"])
def hapus_tugas(id):
    with get_db() as koneksi:
        koneksi.execute(
            "DELETE FROM tugas WHERE id = ?",
            (id,)
        )

    return redirect(url_for("tugas"))


@app.route("/materi")
def materi():
    return render_template("materi.html")


@app.route("/nilai")
def nilai():
    return render_template("nilai.html")


@app.route("/keuangan")
def keuangan():
    return render_template("keuangan.html")


@app.route("/pengaturan")
def pengaturan():
    return render_template("pengaturan.html")


if __name__ == "__main__":
    app.run(debug=True)
