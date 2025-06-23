from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3
from models.conectarBase import conectarBase

def cargarTurnos(tabla):
        conn = conectarBase()
        cursor = conn.cursor()

        cursor.execute("SELECT nombre, servicio, localidad, celular, fecha, hora FROM turnos")
        turnos = cursor.fetchall()
        conn.close()

        tabla.setRowCount(len(turnos))

        for rowIndex, turno in enumerate(turnos):
            for colIndex, dato in enumerate(turno):
                tabla.setItem(rowIndex, colIndex, QTableWidgetItem(str(dato)))