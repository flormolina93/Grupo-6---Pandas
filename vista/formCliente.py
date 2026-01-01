from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt
from models.insertarCliente import insertarNuevoCliente
from vista.estilosCss import estilosForm

class FormCliente(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.setWindowTitle("Nuevo Cliente")
        
        layout = QVBoxLayout()

        # --- Título ---
        titulo = QLabel("Registrar Nuevo Cliente")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # --- Inputs ---
        self.inputNombre = QLineEdit()
        self.inputNombre.setPlaceholderText("Nombre (Obligatorio)")
        layout.addWidget(self.inputNombre)

        self.inputApellido = QLineEdit()
        self.inputApellido.setPlaceholderText("Apellido (Obligatorio)")
        layout.addWidget(self.inputApellido)

        # --- Dirección (Calle y Número en una misma fila) ---
        layoutDireccion = QHBoxLayout()
        
        self.inputCalle = QLineEdit()
        self.inputCalle.setPlaceholderText("Calle")
        layoutDireccion.addWidget(self.inputCalle)

        self.inputNumero = QLineEdit()
        self.inputNumero.setPlaceholderText("Altura/N°")
        self.inputNumero.setMaximumWidth(100) # Que sea cortito
        layoutDireccion.addWidget(self.inputNumero)
        
        layout.addLayout(layoutDireccion)

        self.inputLocalidad = QLineEdit()
        self.inputLocalidad.setPlaceholderText("Localidad")
        layout.addWidget(self.inputLocalidad)

        self.inputCelular = QLineEdit()
        self.inputCelular.setPlaceholderText("Celular (Obligatorio)")
        layout.addWidget(self.inputCelular)

        # --- Botones ---
        self.botonGuardar = QPushButton("Guardar Cliente")
        self.botonGuardar.clicked.connect(self.guardar)
        layout.addWidget(self.botonGuardar)

        self.botonVolver = QPushButton("Volver")
        self.botonVolver.clicked.connect(self.volver)
        layout.addWidget(self.botonVolver)

        # --- Mensajes ---
        self.mensaje = QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mensaje)

        self.setLayout(layout)
        self.darEstilos()

    def guardar(self):
        # Obtener datos
        nombre = self.inputNombre.text().strip()
        apellido = self.inputApellido.text().strip()
        calle = self.inputCalle.text().strip()
        numero = self.inputNumero.text().strip()
        localidad = self.inputLocalidad.text().strip()
        celular = self.inputCelular.text().strip()

        # Validaciones (Segun tu base de datos: Nombre y Apellido son NOT NULL)
        if not nombre or not apellido or not celular:
            self.mensaje.setText("Nombre, Apellido y Celular son obligatorios")
            self.mensaje.setStyleSheet("color: red;")
            return

        # Validación extra para que el número de calle sea numérico si escribieron algo
        if numero and not numero.isdigit():
             self.mensaje.setText("El número de calle debe ser numérico")
             self.mensaje.setStyleSheet("color: red;")
             return

        # Llamada al Modelo
        exito, resultado = insertarNuevoCliente(nombre, apellido, calle, numero, localidad, celular)

        if exito:
            self.mensaje.setText(resultado)
            self.mensaje.setStyleSheet("color: green;")
            # Limpiar todo
            self.inputNombre.clear()
            self.inputApellido.clear()
            self.inputCalle.clear()
            self.inputNumero.clear()
            self.inputLocalidad.clear()
            self.inputCelular.clear()
            self.inputNombre.setFocus()
        else:
            self.mensaje.setText(resultado)
            self.mensaje.setStyleSheet("color: red;")

    def volver(self):
        if hasattr(self.mainWindow, 'dashboardScreen'):
            self.mainWindow.stack.setCurrentWidget(self.mainWindow.dashboardScreen)

    def darEstilos(self):
        self.setStyleSheet(estilosForm)