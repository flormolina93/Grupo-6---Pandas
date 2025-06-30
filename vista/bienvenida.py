from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from vista.loginWindow import LoginWindow
from vista.registroAdmin import RegistroAdmin
from vista.loginStylosFondo import LoginStyloFondo
from vista.estilosCss import estiloBoton,estilosContenedorPrincipal, estiloTitulo

class Bienvenida(QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        self.mainWindow = MainWindow

        LoginStyloFondo().aplicarEstilo(self)

        self.setWindowTitle("Bienvenida a la App de Turnos")
        self.setGeometry(300, 300, 300, 200)

        self.contenedorPrincipal = QWidget()

        layoutVentana = QVBoxLayout()
        layoutVentana.setAlignment(Qt.AlignCenter)

        self.contenedorPrincipal=QWidget()
        layoutPrincipal = QVBoxLayout(self.contenedorPrincipal)
        layoutPrincipal.setAlignment(Qt.AlignCenter)

        self.titulo = QLabel("¡Bienvenido/a!")
        self.titulo.setAlignment(Qt.AlignCenter)
        layoutPrincipal.addWidget(self.titulo)

        self.botonLogin = QPushButton("Iniciar sesión")
        self.botonLogin.clicked.connect(self.abrirLogin)
        layoutPrincipal.addWidget(self.botonLogin)

        self.botonRegistro = QPushButton("Registrarse como Admin")
        self.botonRegistro.clicked.connect(self.abrirRegistro)
        layoutPrincipal.addWidget(self.botonRegistro)

        layoutVentana.addWidget(self.contenedorPrincipal)
        self.setLayout(layoutVentana)
        self.darEstilos()

    def abrirLogin(self):
        self.mainWindow.stack.setCurrentWidget(self.mainWindow.loginScreen)

    def abrirRegistro(self):
        self.mainWindow.stack.setCurrentWidget(self.mainWindow.registroScreen)

    def irLogin(self):
        self.mainWindow.reemplazarLogin(LoginWindow)

    def darEstilos(self):
        

        self.contenedorPrincipal.setStyleSheet(estilosContenedorPrincipal)
        self.botonLogin.setStyleSheet(estiloBoton)
        self.botonRegistro.setStyleSheet(estiloBoton)
        self.titulo.setStyleSheet(estiloTitulo)
    
