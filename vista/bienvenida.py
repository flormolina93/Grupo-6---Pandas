from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from vista.loginWindow import LoginWindow
from vista.registroAdmin import RegistroAdmin


class Bienvenida(QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        self.mainWindow = MainWindow

        self.setWindowTitle("Bienvenida a la App de Turnos")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        titulo = QLabel("¡Bienvenido/a!")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px;")
        layout.addWidget(titulo)

        botonLogin = QPushButton("Iniciar sesión")
        botonLogin.clicked.connect(self.abrirLogin)
        layout.addWidget(botonLogin)

        botonRegistro = QPushButton("Registrarse como Admin")
        botonRegistro.clicked.connect(self.abrirRegistro)
        layout.addWidget(botonRegistro)

        self.setLayout(layout)

    def abrirLogin(self):
        self.mainWindow.stack.setCurrentWidget(self.mainWindow.loginScreen)

    def abrirRegistro(self):
        self.mainWindow.stack.setCurrentWidget(self.mainWindow.registroScreen)
    
