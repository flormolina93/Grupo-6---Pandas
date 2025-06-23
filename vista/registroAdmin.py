from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from models.crearTablaUsuarios import crearTablaUsuarios
from models.insertarUsuario import insertarUsuario

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
        self.botonRegistrar.clicked.connect(insertarUsuario)
        layout.addWidget(self.botonRegistrar)

        self.mensaje= QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mensaje)

        self.setLayout(layout)

    

            

        






