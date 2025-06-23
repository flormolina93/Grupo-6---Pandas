from models.conectarBase import conectarBase

def crearTablaUsuarios():
    conn = conectarBase()
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS usuarios(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   email TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL,
                   nombre TEXT NOT NULL,
                   esAdmin INTEGER NOT NULL DEFAULT 0)""")
    
    conn.commit()
    conn.close()