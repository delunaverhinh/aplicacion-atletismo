import os
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Carpeta donde se guardarán las imágenes
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def get_conn():
    return sqlite3.connect("entrenamientos.db")

@app.route("/")
def home():
    return """
    <h2>Bienvenido al sistema de entrenamientos</h2>
    <p>
        <a href='/nueva_carrera'>Registrar carrera</a> |
        <a href='/panel'>Panel</a>
    </p>
    """

@app.route("/nueva_carrera", methods=["GET", "POST"])
def nueva_carrera():
    if request.method == "POST":
        usuario_id = request.form.get("usuario_id")
        fecha = request.form.get("fecha")
        distancia = request.form.get("distancia")
        duracion = request.form.get("duracion")  # formato min:seg
        notas = request.form.get("notas")

        # Manejo de imagen
        imagen_file = request.files.get("imagen")
        imagen_path = None
        if imagen_file and imagen_file.filename != "":
            imagen_path = os.path.join(app.config["UPLOAD_FOLDER"], imagen_file.filename)
            imagen_file.save(imagen_path)

        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO carreras (usuario_id, fecha, distancia, duracion, notas, imagen)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (usuario_id, fecha, distancia, duracion, notas, imagen_path))
        conn.commit()
        conn.close()
        return redirect("/panel")
    return render_template("nueva_carrera.html")

@app.route("/panel")
def panel():
    view = request.args.get("view", "general")

    conn = get_conn()
    c = conn.cursor()

    carreras = []
    fechas = []
    atletas = []

    if view == "general":
        fecha = request.args.get("fecha")
        usuario_id = request.args.get("usuario_id")

        if fecha and usuario_id:
            c.execute("SELECT * FROM carreras WHERE fecha = ? AND usuario_id = ?", (fecha, usuario_id))
        elif fecha:
            c.execute("SELECT * FROM carreras WHERE fecha = ?", (fecha,))
        elif usuario_id:
            c.execute("SELECT * FROM carreras WHERE usuario_id = ?", (usuario_id,))
        else:
            c.execute("SELECT * FROM carreras")
        carreras = c.fetchall()

    elif view == "dia":
        fecha = request.args.get("fecha")
        if fecha:
            c.execute("SELECT * FROM carreras WHERE fecha = ?", (fecha,))
            carreras = c.fetchall()
        else:
            c.execute("SELECT DISTINCT fecha FROM carreras ORDER BY fecha DESC")
            fechas = c.fetchall()

    elif view == "atleta":
        usuario_id = request.args.get("usuario_id")
        if usuario_id:
            c.execute("SELECT * FROM carreras WHERE usuario_id = ?", (usuario_id,))
            carreras = c.fetchall()
        else:
            c.execute("SELECT DISTINCT usuario_id FROM carreras ORDER BY usuario_id")
            atletas = c.fetchall()

    conn.close()

    return render_template(
        "panel.html",
        view=view,
        carreras=carreras,
        fechas=fechas,
        atletas=atletas
    )

if __name__ == "__main__":
    # Escucha en todas las interfaces, accesible desde cualquier navegador
    app.run(host="0.0.0.0", port=5000, debug=True)
