from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QTimeEdit, QCompleter)
from PyQt5.QtCore import QDate, QTime, Qt
from models.insertarTurnoCompleto import insertarTurnoCompleto 
from models.obtenerServicios import obtenerServicios 
from models.obtenerClientesParaBusqueda import obtenerClientesParaBusqueda
from vista.estilosCss import estilosForm

class FormTurno(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow 
        self.setWindowTitle("Registro de turnos")

        self.datos_clientes = [] 

        layout = QVBoxLayout()

        # --- Input Nombre con Autocompletado ---
        self.inputNombre = QLineEdit()
        self.inputNombre.setPlaceholderText("Nombre del Cliente (Escriba para buscar)")
        layout.addWidget(self.inputNombre)
        
        self.configurarAutocompletado()

        # --- Combo Servicios ---
        self.comboServicio = QComboBox()
        lista_de_servicios = obtenerServicios()
        if lista_de_servicios:
            self.comboServicio.addItems(lista_de_servicios)
        else:
            self.comboServicio.addItem("Sin servicios cargados")
        layout.addWidget(self.comboServicio)

        # --- Inputs Restantes ---
        self.inputLocalidad = QLineEdit()
        self.inputLocalidad.setPlaceholderText("Localidad")
        layout.addWidget(self.inputLocalidad)

        self.inputWpp = QLineEdit()
        self.inputWpp.setPlaceholderText("Celular (Ej: 1122334455)")
        layout.addWidget(self.inputWpp)

        self.fechaTurno = QDateEdit()
        self.fechaTurno.setCalendarPopup(True)
        self.fechaTurno.setDate(QDate.currentDate())
        layout.addWidget(self.fechaTurno)

        self.horaTurno = QTimeEdit()
        self.horaTurno.setTime(QTime.currentTime())
        layout.addWidget(self.horaTurno)

        # --- BOTONES (En fila horizontal) ---
        layoutBotones = QHBoxLayout()

        self.botonGuardar = QPushButton("Guardar turno")
        self.botonGuardar.clicked.connect(self.guardarTurno)
        self.botonGuardar.setStyleSheet("background-color: #4CAF50; color: white;") # Verde para guardar
        layoutBotones.addWidget(self.botonGuardar)

        self.botonVolver = QPushButton("Volver / Cancelar")
        self.botonVolver.clicked.connect(self.volver)
        self.botonVolver.setStyleSheet("background-color: #f44336; color: white;") # Rojo para cancelar
        layoutBotones.addWidget(self.botonVolver)

        layout.addLayout(layoutBotones)

        # --- Mensaje ---
        self.mensaje = QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mensaje)

        self.setLayout(layout)
        # self.darStilos() # (Ojo: tus estilos generales pueden pisar los colores de los botones de arriba)

    def configurarAutocompletado(self):
        self.datos_clientes = obtenerClientesParaBusqueda()
        lista_nombres = [c['label'] for c in self.datos_clientes]
        
        completer = QCompleter(lista_nombres)
        completer.setCaseSensitivity(Qt.CaseInsensitive) 
        completer.setFilterMode(Qt.MatchContains) 
        
        self.inputNombre.setCompleter(completer)
        completer.activated.connect(self.rellenarDatosCliente)

    def rellenarDatosCliente(self, texto_seleccionado):
        for cliente in self.datos_clientes:
            if cliente['label'] == texto_seleccionado:
                self.inputNombre.setText(cliente['nombre_real'])
                self.inputLocalidad.setText(cliente['localidad'])
                self.inputWpp.setText(cliente['telefono'])
                self.mensaje.setText("✓ Cliente encontrado")
                self.mensaje.setStyleSheet("color: blue")
                break

    def guardarTurno(self):
        nombre = self.inputNombre.text().strip()
        servicio_texto = self.comboServicio.currentText()
        localidad = self.inputLocalidad.text().strip()
        celular = self.inputWpp.text().strip()
        fecha = self.fechaTurno.date().toString("yyyy-MM-dd")
        hora = self.horaTurno.time().toString("HH:mm")

        if not nombre or not localidad or not celular:
            self.mensaje.setText("Completa todos los campos obligatorios")
            self.mensaje.setStyleSheet("color: red")
            return 
        
        if servicio_texto == "Sin servicios cargados":
            self.mensaje.setText("No hay servicios disponibles")
            self.mensaje.setStyleSheet("color: red")
            return

        id_empleado_actual = 1 
        if hasattr(self.mainWindow, 'usuario_logueado') and self.mainWindow.usuario_logueado:
            id_empleado_actual = self.mainWindow.usuario_logueado.get('id', 1) 
        
        try:
            exito, resultado_mensaje = insertarTurnoCompleto(
                nombre, servicio_texto, localidad, celular, fecha, hora, id_empleado_actual
            )

            if exito:
                self.mensaje.setText(resultado_mensaje)
                self.mensaje.setStyleSheet("color: green")
                self.inputNombre.clear()
                self.inputLocalidad.clear()
                self.inputWpp.clear()
                self.inputNombre.setFocus()
            else:
                self.mensaje.setText(resultado_mensaje)
                self.mensaje.setStyleSheet("color: red;")
        
        except Exception as e:
            self.mensaje.setText(f"Error técnico: {e}")
            self.mensaje.setStyleSheet("color: red;")

    def volver(self):
        # Esta función usa el Stack del MainWindow para volver atrás
        if hasattr(self.mainWindow, 'dashboardScreen'):
            self.mainWindow.stack.setCurrentWidget(self.mainWindow.dashboardScreen)

    def darStilos(self):
        self.setStyleSheet(estilosForm)