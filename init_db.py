import sqlite3

# Conectar (crea el archivo si no existe)
conn = sqlite3.connect("entrenamientos.db")
c = conn.cursor()

# Crear tabla de usuarios
c.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    rol TEXT CHECK(rol IN ('atleta','entrenador'))
)
""")

# Crear tabla de carreras
c.execute("""
CREATE TABLE IF NOT EXISTS carreras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    fecha DATE,
    distancia REAL,
    duracion INTEGER,
    notas TEXT,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
)
""")

conn.commit()
conn.close()
print("Base de datos inicializada correctamente.")
