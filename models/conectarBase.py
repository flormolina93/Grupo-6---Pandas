import os
import sqlite3


def conectarBase():
    BASE_DIR = "C/Users/migue/Documents/nuevoProyectoPyqtTurnos/models"
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Ruta del script actual
    DB_PATH = os.path.join(BASE_DIR, "turnosCompletos.db")  # Archivo DB en esa carpeta
    print("📂 Usando base de datos en:", DB_PATH)
    return sqlite3.connect(DB_PATH)
