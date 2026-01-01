from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDateEdit, QTimeEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QDate, QTime, Qt
from models.obtenerServicios import obtenerServicios
from models.accionesTurnos import editarDatosDelTurno

class VentanaEditarTurno(QDialog):
    def __init__(self, id_turno, fecha_actual, hora_actual, servicio_actual, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Turno")
        self.setGeometry(300, 300, 300, 250)
        
        self.id_turno = id_turno
        
        layout = QVBoxLayout()
        
        # --- FECHA ---
        layout.addWidget(QLabel("Fecha:"))
        self.inputFecha = QDateEdit()
        self.inputFecha.setCalendarPopup(True)
        # Convertimos string "2025-12-31" a objeto QDate
        self.inputFecha.setDate(QDate.fromString(fecha_actual, "yyyy-MM-dd"))
        layout.addWidget(self.inputFecha)

        # --- HORA ---
        layout.addWidget(QLabel("Hora:"))
        self.inputHora = QTimeEdit()
        # Convertimos string "14:30" a objeto QTime
        self.inputHora.setTime(QTime.fromString(hora_actual, "HH:mm"))
        layout.addWidget(self.inputHora)

        # --- SERVICIO ---
        layout.addWidget(QLabel("Servicio:"))
        self.comboServicio = QComboBox()
        self.comboServicio.addItems(obtenerServicios())
        self.comboServicio.setCurrentText(servicio_actual)
        layout.addWidget(self.comboServicio)

        # --- BOTONES ---
        self.btnGuardar = QPushButton("Guardar Cambios")
        self.btnGuardar.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.btnGuardar.clicked.connect(self.guardar)
        layout.addWidget(self.btnGuardar)
        
        self.setLayout(layout)

    def guardar(self):
        nueva_fecha = self.inputFecha.date().toString("yyyy-MM-dd")
        nueva_hora = self.inputHora.time().toString("HH:mm")
        nuevo_servicio = self.comboServicio.currentText()

        # Llamamos al modelo
        exito = editarDatosDelTurno(self.id_turno, nueva_fecha, nueva_hora, nuevo_servicio)

        if exito:
            QMessageBox.information(self, "Éxito", "Turno modificado correctamente")
            self.accept() # Cierra la ventana devolviendo "True" (Accepted)
        else:
            QMessageBox.warning(self, "Error", "No se pudo modificar el turno")