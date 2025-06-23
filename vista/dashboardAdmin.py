from PyQt5.QtWidgets import (QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton,QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QDate
import sqlite3
from vista.formTurno import FormTurno
from vista.todosLosTurnos import TodosLosTurnos
from controladores.estadisticas.obtenerDatosTurnos import obtenerDatosTurnos, estadisticasLocalidad
from vista.estadisticasPorLocalidad import EstadisticasLocalidadWidget

class DashboardAdmin(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

        self.setWindowTitle("Ventana dashboard de turnos para Admin")
        self.setGeometry(200,200,800,500)

        mainLayout = QVBoxLayout()

        titulo = QLabel("Turnos del dia")
        titulo.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(titulo)

        #Tabla de turnos del dia.
        self.tablaTurnos = QTableWidget()
        self.tablaTurnos.setColumnCount(4)
        self.tablaTurnos.setHorizontalHeaderLabels(["Nombre", "Servicio", "Hora", "Localidad"])
        mainLayout.addWidget(self.tablaTurnos)

        botonesLayout = QHBoxLayout()
        
        self.botonNuevo = QPushButton("Nuevo turno")
        self.botonNuevo.clicked.connect(self.abrirFormTurnos)
        botonesLayout.addWidget(self.botonNuevo)

        self.botonVerTodos= QPushButton("Ver todos los turnos")
        self.botonVerTodos.clicked.connect(self.verTodosLosTurnos)
        botonesLayout.addWidget(self.botonVerTodos)

        self.botonVolver = QPushButton("← Volver")
        self.botonVolver.clicked.connect(self.volver)
        botonesLayout.addWidget(self.botonVolver)

        self.botonEstadisticas = QPushButton("Ver estadísticas")
        self.botonEstadisticas.clicked.connect(self.mostrarEstadisticas)
        botonesLayout.addWidget(self.botonEstadisticas)

        botonesWidget = QWidget()
        botonesWidget.setLayout(botonesLayout)
        mainLayout.addWidget(botonesWidget)

        self.setLayout(mainLayout)
        self.cargarTurnosDelDia()

    def cargarTurnosDelDia(self):
        conn = sqlite3.connect("models/turnosCompletos.db")
        cursor = conn.cursor()

        hoy = QDate.currentDate().toString("yyyy-MM-dd")
        cursor.execute("""SELECT nombre, servicio, hora, localidad FROM turnos WHERE fecha = ?""", (hoy,))

        turnos = cursor.fetchall()
        conn.close()

        self.tablaTurnos.setRowCount(len(turnos))

        for rowIndex, turno in enumerate(turnos):
            for colIndex, dato in enumerate(turno):
                self.tablaTurnos.setItem(rowIndex,colIndex, QTableWidgetItem(str(dato)))

    def abrirFormTurnos(self):
        self.formTurno = FormTurno()
        self.formTurno.show()

    def verTodosLosTurnos(self):
        self.fullTurnos = TodosLosTurnos()
        self.fullTurnos.show()

    def volver(self):
        self.mainWindow.stack.setCurrentWidget(self.mainWindow.loginScreen)

    def mostrarEstadisticas(self):
        df = obtenerDatosTurnos()
        conteo = estadisticasLocalidad(df)
        self.estadisticasWidget = EstadisticasLocalidadWidget(conteo)
        self.estadisticasWidget.show()

     


