from PyQt5.QtWidgets import QMainWindow, QStackedWidget,QPushButton
from vista.loginWindow import LoginWindow
from vista.dashboardAdmin import DashboardAdmin
from vista.registroAdmin import RegistroAdmin
from vista.bienvenida import Bienvenida

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Turnos")
        self.setGeometry(200, 200, 800, 500)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.loginScreen = LoginWindow(self)
        self.registroScreen = RegistroAdmin(self)
        self.dashboardScreen = DashboardAdmin(self)
        self.bienvenida = Bienvenida(self)

        self.stack.addWidget(self.bienvenida)     # index 0
        self.stack.addWidget(self.loginScreen)     #Index 1
        self.stack.addWidget(self.registroScreen)  # index 2
        self.stack.addWidget(self.dashboardScreen) # index 3

        self.stack.setCurrentWidget(self.bienvenida)  # Mostrar login al inicio

    def mostrarLogin(self):
        self.stack.setCurrentIndex(1)

    def mostrarRegistro(self):
        self.stack.setCurrentIndex(2)

    def mostrarDashboard(self):
        self.stack.setCurrentIndex(3)

    def reemplazarLogin(self, NuevaClaseLogin):
    # Eliminar del stack y liberar memoria
        self.stack.removeWidget(self.loginScreen)
        self.loginScreen.deleteLater()

    # Crear nueva instancia
        self.loginScreen = NuevaClaseLogin(self)
        self.stack.insertWidget(1, self.loginScreen)

    # Mostrar login nuevo
        self.stack.setCurrentIndex(1)
