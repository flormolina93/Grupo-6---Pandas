from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from vista.loginWindow import LoginWindow
from vista.dashboardAdmin import DashboardAdmin
from vista.registroUsuario import RegistroUsuario
from vista.bienvenida import Bienvenida
from vista.formCliente import FormCliente 

# 1. IMPORTAMOS EL GESTOR DE SESIÓN
from models.sesionManager import cargarSesion

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Turnos")
        self.setGeometry(200, 200, 800, 500)
        
        self.usuario_logueado = None 

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Instancias
        self.loginScreen = LoginWindow(self)
        self.registroScreen = RegistroUsuario(self)
        self.dashboardScreen = DashboardAdmin(self)
        self.bienvenida = Bienvenida(self)
        self.formClienteScreen = FormCliente(self)

        # Agregamos al Stack
        self.stack.addWidget(self.bienvenida)        # Index 0
        self.stack.addWidget(self.loginScreen)       # Index 1
        self.stack.addWidget(self.registroScreen)    # Index 2
        self.stack.addWidget(self.dashboardScreen)   # Index 3
        self.stack.addWidget(self.formClienteScreen) # Index 4

        # --- LÓGICA DE AUTO-LOGIN (NUEVO) ---
        # Verificamos si existe el archivo 'sesion_activa.json'
        usuario_guardado = cargarSesion()

        if usuario_guardado:
            # CASO A: SI HAY SESIÓN GUARDADA
            print(f"Sesión restaurada para: {usuario_guardado.get('nombre_completo')}")
            
            # 1. Cargamos el usuario en la memoria de la App
            self.usuario_logueado = usuario_guardado
            
            # 2. Saltamos directo al Dashboard (Index 3)
            self.stack.setCurrentWidget(self.dashboardScreen)
        else:
            # CASO B: NO HAY SESIÓN (Flujo normal)
            self.stack.setCurrentWidget(self.bienvenida)

    def mostrarLogin(self):
        self.stack.setCurrentIndex(1)

    def mostrarRegistro(self):
        self.stack.setCurrentIndex(2)

    def mostrarDashboard(self):
        self.stack.setCurrentIndex(3)

    def mostrarFormCliente(self):
        self.stack.setCurrentWidget(self.formClienteScreen)