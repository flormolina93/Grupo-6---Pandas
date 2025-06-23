from models.conectarBase import conectarBase

def crearTablaTurnos():
    conn = conectarBase()
    cursor = conn.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS turnos (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nombre TEXT NOT NULL,
                   servicio TEXT NOT NULL,
                   localidad TEXT NOT NULL,
                   celular TEXT NOT NULL,
                   fecha TEXT NOT NULL,
                   hora TEXT NOT NULL)""")
    
    conn.commit()
    conn.close()