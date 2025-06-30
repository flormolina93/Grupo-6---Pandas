from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from models.crearTablaUsuarios import crearTablaUsuarios
from models.insertarUsuario import insertarUsuario
from vista.estilosCss import estiloBoton, estiloInput

class RegistroAdmin(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

        self.setWindowTitle("Estetica Turnos")
        self.setGeometry(300,300,350,250)

        crearTablaUsuarios() #Esto te asegura que la tabla exista

        layout = QVBoxLayout()

        self.inputEmail = QLineEdit()
        self.inputEmail.setPlaceholderText("Correo electronico")
        layout.addWidget(self.inputEmail)

        self.inputPass = QLineEdit()
        self.inputPass.setPlaceholderText("Contraseña")
        self.inputPass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.inputPass)

        self.inputNombre = QLineEdit()
        self.inputNombre.setPlaceholderText("Nombre completo")
        layout.addWidget(self.inputNombre)      

        self.botonRegistrar = QPushButton("Registrar")
        self.botonRegistrar.clicked.connect(self.registrar)
        layout.addWidget(self.botonRegistrar)

        self.mensaje= QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mensaje)

        self.setLayout(layout)
        self.darStilos()

    def registrar(self):
        email = self.inputEmail.text().strip()
        password = self.inputPass.text()
        nombre = self.inputNombre.text()

        if not email or not password or not nombre:
            self.mensaje.setText("Complete todos los datos")
            self.mensaje.setStyleSheet("color: red;")
            return
        
        exito, mensaje = insertarUsuario(email, password, nombre, esAdmin = 1)  

        if exito:
            self.mensaje.setText(mensaje)
            self.mensaje.setStyleSheet("color: green;")
            self.inputEmail.clear()
            self.inputPass.clear()
            self.inputNombre.clear()
            self.mensaje.setText("Usuario registrado")
        else:
            self.mensaje.setText(mensaje)
            self.mensaje.setStyleSheet("color: red;")

    def darStilos(self):
        self.inputEmail.setMaximumWidth(400)
        self.inputPass.setMaximumWidth(400)
        self.inputNombre.setMaximumWidth(400)
        self.botonRegistrar.setMaximumWidth(400)
        
        self.botonRegistrar.setStyleSheet(estiloBoton)
        self.inputPass.setStyleSheet(estiloInput)
        self.inputEmail.setStyleSheet(estiloInput)
        self.inputNombre.setStyleSheet(estiloInput)

            

        






