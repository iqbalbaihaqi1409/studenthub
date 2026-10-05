from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/jadwal")
def jadwal():
    return render_template("jadwal.html")


@app.route("/tugas")
def tugas():
    return render_template("tugas.html")


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