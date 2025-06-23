from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from models.verificarCredenciales import verificarCredenciales
from vista.dashboardAdmin import DashboardAdmin

class LoginWindow(QWidget):

    def __init__(self, mainWindow):

        super().__init__()
        self.mainWindow = mainWindow

        self.setWindowTitle("Login")
        self.setGeometry(300,300,350,200)
        self.setStyleSheet("""
            QLineEdit { padding: 8px; font-size: 14px; }
            QPushButton { padding: 8px; font-size: 14px; }
            QLabel { font-size: 13px; }
        """)

        layout = QVBoxLayout()

        self.inputEmail = QLineEdit()
        self.inputEmail.setPlaceholderText("Correo electrónico")
        layout.addWidget(self.inputEmail)

        self.inputPass = QLineEdit()
        self.inputPass.setPlaceholderText("Contraseña")
        self.inputPass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.inputPass)

        self.botonLogin = QPushButton("Iniciar sesión")
        self.botonLogin.clicked.connect(self.login)
        layout.addWidget(self.botonLogin)

        self.botonVolver = QPushButton("← Volver")
        self.botonVolver.clicked.connect(self.volver)
        layout.addWidget(self.botonVolver)


        self.mensaje = QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mensaje)

        self.setLayout(layout)
    
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


    

        

