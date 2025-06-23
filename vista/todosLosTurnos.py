from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
import sqlite3
from controladores.cargarTurnos import cargarTurnos

class TodosLosTurnos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todos los turnos")
        self.setGeometry(300, 300, 800, 400)

        layout = QVBoxLayout()

        titulo = QLabel("Listado de todos los turnos")
        layout.addWidget(titulo)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Servicio", "Localidad", "Celular", "Fecha", "Hora"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        cargarTurnos(self.tabla)

    

