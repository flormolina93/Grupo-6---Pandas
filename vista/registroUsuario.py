from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QComboBox, QHBoxLayout) 
from PyQt5.QtCore import Qt
# Asegurate de que tu modelo acepte los argumentos nuevos (calle, numero)
from models.insertarUsuario import insertarUsuario
from vista.estilosCss import estiloBoton, estiloInput

class RegistroUsuario(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

        self.setWindowTitle("Registro de Personal")
        self.setGeometry(300, 300, 350, 500) 

        layout = QVBoxLayout()
        
        # --- Título ---
        lbl_titulo = QLabel("Nuevo Usuario")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(lbl_titulo)

        # --- DNI ---
        self.inputDni = QLineEdit()
        self.inputDni.setPlaceholderText("DNI (Solo números)")
        layout.addWidget(self.inputDni)

        # --- Nombre ---
        self.inputNombre = QLineEdit()
        self.inputNombre.setPlaceholderText("Nombre")
        layout.addWidget(self.inputNombre)

        # --- Apellido ---
        self.inputApellido = QLineEdit()
        self.inputApellido.setPlaceholderText("Apellido")
        layout.addWidget(self.inputApellido)

        # --- DIRECCIÓN (Calle y Número en la misma línea) ---
        layoutDireccion = QHBoxLayout() 
        
        self.inputCalle = QLineEdit()
        self.inputCalle.setPlaceholderText("Calle")
        
        self.inputNumero = QLineEdit()
        self.inputNumero.setPlaceholderText("Altura/Nro")
        self.inputNumero.setMaximumWidth(80) 

        layoutDireccion.addWidget(self.inputCalle)
        layoutDireccion.addWidget(self.inputNumero)
        layout.addLayout(layoutDireccion) 

        # --- Rol ---
        self.comboRol = QComboBox()
        self.comboRol.addItems(["Empleado", "Administrador"])
        # self.comboRol.setStyleSheet(estiloInput) # A veces conviene dejar el estilo nativo en combos
        layout.addWidget(self.comboRol)

        # --- Email ---
        self.inputEmail = QLineEdit()
        self.inputEmail.setPlaceholderText("Correo electrónico")
        layout.addWidget(self.inputEmail)

        # --- Teléfono ---
        self.inputTelefono = QLineEdit()
        self.inputTelefono.setPlaceholderText("Teléfono / Celular")
        layout.addWidget(self.inputTelefono)

        # --- Password ---
        self.inputPass = QLineEdit()
        self.inputPass.setPlaceholderText("Contraseña")
        self.inputPass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.inputPass)

        # --- Botón Registrar ---
        self.botonRegistrar = QPushButton("Registrar Usuario")
        self.botonRegistrar.clicked.connect(self.registrar)
        layout.addWidget(self.botonRegistrar)

        # --- Mensaje ---
        self.mensaje = QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mensaje)
        
        # --- Botón Volver ---
        self.botonVolver = QPushButton("Volver")
        self.botonVolver.setStyleSheet("background-color: #555; color: white; padding: 5px;")
        self.botonVolver.clicked.connect(self.volver)
        layout.addWidget(self.botonVolver)

        self.setLayout(layout)
        self.darStilos()

    def registrar(self):
        # 1. Obtenemos datos
        dni = self.inputDni.text().strip()
        nombre = self.inputNombre.text().strip()
        apellido = self.inputApellido.text().strip()
        calle = self.inputCalle.text().strip() 
        numero = self.inputNumero.text().strip() 
        email = self.inputEmail.text().strip()
        telefono = self.inputTelefono.text().strip()
        password = self.inputPass.text()
        rol_texto = self.comboRol.currentText()

        # 2. Validaciones visuales
        if not dni or not nombre or not apellido or not password:
            self.mensaje.setText("DNI, Nombre, Apellido y Pass son obligatorios")
            self.mensaje.setStyleSheet("color: red;")
            return
        
        if not dni.isdigit():
            self.mensaje.setText("El DNI debe contener solo números")
            self.mensaje.setStyleSheet("color: red;")
            return

        # 3. Preparar llamada
        es_admin_booleano = 1 if rol_texto == "Administrador" else 0

        # 4. LLAMADA AL MODELO
        try:
            exito, mensaje_resultado = insertarUsuario(
                nombre, 
                apellido, 
                dni, 
                email, 
                telefono, 
                calle,   
                numero,  
                password, 
                es_admin_booleano
            )

            if exito:
                self.mensaje.setText("Usuario registrado con éxito")
                self.mensaje.setStyleSheet("color: green;")
                # Limpiar todo
                self.inputDni.clear()
                self.inputNombre.clear()
                self.inputApellido.clear()
                self.inputCalle.clear()
                self.inputNumero.clear()
                self.inputEmail.clear()
                self.inputTelefono.clear()
                self.inputPass.clear()
            else:
                self.mensaje.setText(mensaje_resultado)
                self.mensaje.setStyleSheet("color: red;")
                
        except Exception as e:
             self.mensaje.setText(f"Error técnico: {e}")
             self.mensaje.setStyleSheet("color: red;")

    def volver(self):
        # --- CORRECCIÓN AQUÍ ---
        # Usamos 'bienvenida' que es el nombre correcto en MainWindow
        if hasattr(self.mainWindow, 'bienvenida'):
            self.mainWindow.stack.setCurrentWidget(self.mainWindow.bienvenida)

    def darStilos(self):
        lista_widgets = [self.inputDni, self.inputNombre, self.inputApellido, 
                         self.inputCalle, self.inputNumero,
                         self.inputEmail, self.inputTelefono, self.inputPass, 
                         self.comboRol, self.botonRegistrar]
        
        for widget in lista_widgets:
            # Quitamos el MaxWidth fijo para calle y numero para que usen el layout horizontal mejor
            if widget not in [self.inputCalle, self.inputNumero]:
                 widget.setMaximumWidth(400)
            
            if isinstance(widget, QPushButton):
                widget.setStyleSheet(estiloBoton)
            else:
                # Ojo: A veces aplicar estiloInput al Combo rompe la flecha, probá si queda bien
                widget.setStyleSheet(estiloInput)