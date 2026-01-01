from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
# Importamos la lógica de verificación
from models.verificarCredencialesDeLogin import verificarCredencialesDeLogin
# 1. IMPORTAMOS EL GESTOR DE SESIÓN (NUEVO)
from models.sesionManager import guardarSesion
# Importamos estilos
from vista.loginStylosFondo import LoginStyloFondo
from vista.estilosCss import estiloBoton, estiloInput

class LoginWindow(QWidget):

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

        # Aplicamos el fondo con imagen (si tenés la clase configurada)
        LoginStyloFondo().aplicarEstilo(self)

        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 350, 250)
        
        # Estilos locales base para asegurar legibilidad
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

        # --- LOGO ---
        self.logo = QLabel()
        try:
            # Asegurate que la ruta "img/logo.jpeg" sea correcta
            pixmap = QPixmap("img/logo.jpeg")
            if not pixmap.isNull():
                self.logo.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                self.logo.setAlignment(Qt.AlignCenter)
                layoutCentrado.addWidget(self.logo)
        except:
            pass 

        # --- INPUT DNI ---
        self.inputDni = QLineEdit()
        self.inputDni.setPlaceholderText("Ingrese su DNI")
        layoutCentrado.addWidget(self.inputDni)

        # --- INPUT PASSWORD ---
        self.inputPass = QLineEdit()
        self.inputPass.setPlaceholderText("Contraseña")
        self.inputPass.setEchoMode(QLineEdit.Password)
        layoutCentrado.addWidget(self.inputPass)

        # --- BOTONES ---
        self.botonLogin = QPushButton("Iniciar sesión")
        self.botonLogin.clicked.connect(self.login)
        layoutCentrado.addWidget(self.botonLogin)

        self.botonVolver = QPushButton("← Volver")
        self.botonVolver.clicked.connect(self.volver)
        layoutCentrado.addWidget(self.botonVolver)

        # --- MENSAJE DE ESTADO ---
        self.mensaje = QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)
        layoutCentrado.addWidget(self.mensaje)

        layoutPrincipal.addWidget(contenedor)

        self.setLayout(layoutPrincipal)
        self.aplicarEstilos()

    def login(self):
        dni_texto = self.inputDni.text().strip()
        password = self.inputPass.text()

        # 1. Validación de campos vacíos
        if not dni_texto or not password:
            self.mensaje.setText("Por favor complete todos los campos")
            self.mensaje.setStyleSheet("color: red; font-weight: bold;")
            return 
        
        # 2. Validación numérica para DNI
        if not dni_texto.isdigit():
            self.mensaje.setText("El DNI debe contener solo números")
            self.mensaje.setStyleSheet("color: red; font-weight: bold;")
            return

        try:
            dni_int = int(dni_texto)
            
            # 3. Llamada al Backend (Modelo)
            exito, resultado = verificarCredencialesDeLogin(dni_int, password)

            if exito:
                # Login exitoso: 'resultado' es el diccionario con datos del usuario
                nombre_usuario = resultado.get('nombre_completo', 'Usuario')
                
                self.mensaje.setText(f"¡Bienvenido {nombre_usuario}!")
                self.mensaje.setStyleSheet("color: green; font-weight: bold;")

                # --- 2. GUARDAMOS LA SESIÓN EN DISCO (NUEVO) ---
                guardarSesion(resultado)
                
                # GUARDAR SESIÓN EN MAIN WINDOW (Memoria)
                self.mainWindow.usuario_logueado = resultado 
                
                # NAVEGAR AL DASHBOARD
                # Verificamos si existe 'dashboardScreen' en el main
                if hasattr(self.mainWindow, 'dashboardScreen'):
                    self.mainWindow.stack.setCurrentWidget(self.mainWindow.dashboardScreen)
                else:
                    self.mensaje.setText("Login OK (Error: No encuentro el Dashboard)")
            
            else:
                # Login fallido: 'resultado' es el mensaje de error
                self.mensaje.setText(resultado)
                self.mensaje.setStyleSheet("color: red; font-weight: bold;")

        except Exception as e:
            self.mensaje.setText(f"Error técnico: {str(e)}")
            self.mensaje.setStyleSheet("color: red;")

    def volver(self):
        # Buscamos 'bienvenida', que es el nombre real en tu MainWindow
        if hasattr(self.mainWindow, 'bienvenida'):
            self.mainWindow.stack.setCurrentWidget(self.mainWindow.bienvenida)
        else:
            print("Error: No se encuentra la pantalla de Bienvenida en MainWindow")

    def aplicarEstilos(self):
        # Ajustamos anchos y estilos desde el archivo CSS externo
        self.inputDni.setMaximumWidth(400)
        self.inputPass.setMaximumWidth(400) 
        
        self.inputDni.setStyleSheet(estiloInput)
        self.inputPass.setStyleSheet(estiloInput)
        
        self.botonLogin.setStyleSheet(estiloBoton)
        self.botonVolver.setStyleSheet(estiloBoton)