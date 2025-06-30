from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from models.verificarCredenciales import verificarCredenciales
from vista.dashboardAdmin import DashboardAdmin
from vista.loginStylosFondo import LoginStyloFondo
from vista.estilosCss import estiloBoton, estiloInput
from PyQt5.QtGui import QPixmap

class LoginWindow(QWidget):

    def __init__(self, mainWindow):

        super().__init__()
        self.mainWindow = mainWindow

        LoginStyloFondo().aplicarEstilo(self)

        self.setWindowTitle("Login")
        self.setGeometry(300,300,350,200)
        self.setStyleSheet("""
            QLineEdit { padding: 8px; font-size: 14px; }
            QPushButton { padding: 8px; font-size: 14px; }
            QLabel { font-size: 13px; }
        """)

        layoutPrincipal = QVBoxLayout()
        layoutPrincipal.setAlignment(Qt.AlignCenter)

        contenedor = QWidget()
        layoutCentrado = QVBoxLayout()
        layoutCentrado.setAlignment(Qt.AlignCenter)
        contenedor.setLayout(layoutCentrado)


        self.logo = QLabel()
        pixmap = QPixmap("img/logo.jpeg")
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        layoutCentrado.addWidget(self.logo)

        self.inputEmail = QLineEdit()
        self.inputEmail.setPlaceholderText("Correo electrónico")
        layoutCentrado.addWidget(self.inputEmail)

        self.inputPass = QLineEdit()
        self.inputPass.setPlaceholderText("Contraseña")
        self.inputPass.setEchoMode(QLineEdit.Password)
        layoutCentrado.addWidget(self.inputPass)

        self.botonLogin = QPushButton("Iniciar sesión")
        self.botonLogin.clicked.connect(self.login)
        layoutCentrado.addWidget(self.botonLogin)

        self.botonVolver = QPushButton("← Volver")
        self.botonVolver.clicked.connect(self.volver)
        layoutCentrado.addWidget(self.botonVolver)


        self.mensaje = QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)
        layoutCentrado.addWidget(self.mensaje)

        layoutPrincipal.addWidget(contenedor)

        self.setLayout(layoutPrincipal)
        self.aplicarEstilos()
    def login(self):
        email = self.inputEmail.text().strip()
        password = self.inputPass.text()

        if not email or not password:
            self.mensaje.setText("Complete todos los campos")
            self.mensaje.setStyleSheet("color: red;")
            return 
    
        exito, resultado = verificarCredenciales(email, password)

        if exito:
            self.mensaje.setText(f"!Bienvenido {resultado['nombre']}¡")
            self.mensaje.setStyleSheet("color: green;")
            self.mainWindow.usuarioActual = resultado  # Guarda el dict con nombre, email, etc.
            self.mainWindow.stack.setCurrentWidget(self.mainWindow.dashboardScreen)
            

        else:
            self.mensaje.setText(resultado)
            self.mensaje.setStyleSheet("color: red;")

    def volver(self):
        self.mainWindow.stack.setCurrentWidget(self.mainWindow.bienvenida)

    def aplicarEstilos(self):
        self.inputEmail.setMaximumWidth(400)
        self.inputPass.setMaximumWidth(400) 
        self.inputEmail.setStyleSheet(estiloInput)
        self.inputPass.setStyleSheet(estiloInput)
        self.botonLogin.setStyleSheet(estiloBoton)
        self.botonVolver.setStyleSheet(estiloBoton)
        
        



    

        

