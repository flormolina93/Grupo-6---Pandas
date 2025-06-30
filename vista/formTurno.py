from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QTimeEdit)
from PyQt5.QtCore import QDate, QTime, Qt
from models.turnoFactory import TurnoFactory
from models.insertarTurno import insertarTurno
from vista.estilosCss import estilosForm
class FormTurno(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de turnos")

        layout = QVBoxLayout()

        self.inputNombre = QLineEdit()
        self.inputNombre.setPlaceholderText("Nombre")
        layout.addWidget(self.inputNombre)

        self.comboServicio =QComboBox()
        self.comboServicio.addItems(["Peluqueria", "Pedicuria", "Manicuria", "Masajes", "Depilacion"])
        layout.addWidget(self.comboServicio)

        self.inputLocalidad = QLineEdit()
        self.inputLocalidad.setPlaceholderText("Localidad")
        layout.addWidget(self.inputLocalidad)

        self.inputWpp = QLineEdit()
        self.inputWpp.setPlaceholderText("Celular")
        layout.addWidget(self.inputWpp)

        self.fechaTurno = QDateEdit()
        self.fechaTurno.setCalendarPopup(True)
        self.fechaTurno.setDate(QDate.currentDate())
        layout.addWidget(self.fechaTurno)

        self.horaTurno = QTimeEdit()
        self.horaTurno.setTime(QTime.currentTime())
        layout.addWidget(self.horaTurno)

        self.botonGuardar = QPushButton("Guardar turno")
        self.botonGuardar.clicked.connect(self.guardarTurno)
        layout.addWidget(self.botonGuardar)

        self.mensaje = QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mensaje)

        self.setLayout(layout)
        self.darStilos()
        
    def guardarTurno(self):
        nombre = self.inputNombre.text().strip()
        servicio = self.comboServicio.currentText()
        localidad = self.inputLocalidad.text().strip()
        celular = self.inputWpp.text().strip()
        fecha = self.fechaTurno.date().toString("yyyy-MM-dd")
        hora = self.horaTurno.time().toString("HH:mm")

        if not nombre or not localidad or not celular:
            self.mensaje.setText("Completa todos los campos obligatorios")
            self.mensaje.setStyleSheet("color: red")
            return 
        
        turno = TurnoFactory.crearTurno(nombre, servicio, localidad, celular, fecha, hora)
        exito, mensaje = insertarTurno(turno)

        if exito:
            self.mensaje.setText("Turno registrado correctamente")
            self.mensaje.setStyleSheet("color: green")
            self.inputNombre.clear()
            self.inputLocalidad.clear()
            self.inputWpp.clear()
        else:
            self.mensaje.setText(mensaje)
            self.mensaje.setStyleSheet("color: red;")

    def volver(self):
        self.mainWindow.stack.setCurrentWidget(self.mainWindow.loginScreen)

    def darStilos(self):
        self.setStyleSheet(estilosForm)



        





