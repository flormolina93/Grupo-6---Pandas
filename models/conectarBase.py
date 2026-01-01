import os
import sqlite3

def conectarBase():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
    
    
    DB_PATH = os.path.join(BASE_DIR, "bdTurnos.db") 
    
    print("📂 Conectando a:", DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    
    conn.execute("PRAGMA foreign_keys = 1")
    
    return conn