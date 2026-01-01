from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from models.conectarBase import conectarBase 
from vista.formTurno import FormTurno
from vista.todosLosTurnos import TodosLosTurnos 
from vista.estilosCss import estiloBoton, estiloTabla
from models.sesionManager import eliminarSesion
from models.accionesTurnos import cambiarEstadoTurno, eliminarTurno

# --- IMPORTS DE VENTANAS SECUNDARIAS ---
from vista.ventanaEditarTurno import VentanaEditarTurno
from vista.vistaEstadisticas import VistaEstadisticas 

class DashboardAdmin(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow 
        self.setWindowTitle("Panel de Administración")
        self.setGeometry(200, 200, 1050, 550) 

        mainLayout = QVBoxLayout()

        # --- HEADER CON USUARIO ---
        self.lblUsuario = QLabel("Cargando...")
        self.lblUsuario.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; margin: 10px;")
        self.lblUsuario.setAlignment(Qt.AlignRight) 
        mainLayout.addWidget(self.lblUsuario)

        # --- TÍTULO ---
        fecha_hoy = QDate.currentDate().toString('dd/MM/yyyy')
        titulo = QLabel(f"Turnos del día: {fecha_hoy}")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; margin: 5px; color: #333;")
        titulo.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(titulo)

        # --- TABLA DE TURNOS ---
        self.tablaTurnos = QTableWidget()
        # 7 Columnas: Hora | Cliente | Servicio | Localidad | Estado | Borrar | ID (Oculto)
        self.tablaTurnos.setColumnCount(7) 
        self.tablaTurnos.setHorizontalHeaderLabels(["Hora", "Cliente", "Servicio", "Localidad", "Estado", "Borrar", "ID"])
        
        # Ajuste de columnas
        header = self.tablaTurnos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Borrar chiquito
        
        # Ocultamos la columna ID (Indice 6)
        self.tablaTurnos.setColumnHidden(6, True)

        # Conectamos Doble Click para editar
        self.tablaTurnos.doubleClicked.connect(self.abrirEditorDeTurno)
        
        mainLayout.addWidget(self.tablaTurnos)
        
        # --- MENSAJE DE AYUDA ---
        lblAyuda = QLabel("💡 Tip: Hacé doble click en un turno para editar fecha, hora o servicio.")
        lblAyuda.setStyleSheet("color: #777; font-style: italic;")
        lblAyuda.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(lblAyuda)

        # --- BOTONERA ---
        self.botonesLayout = QHBoxLayout()
        
        # 1. Nuevo Turno
        self.botonNuevo = QPushButton("+ Nuevo Turno")
        self.botonNuevo.clicked.connect(self.abrirFormTurnos)
        self.botonesLayout.addWidget(self.botonNuevo)
        
        # 2. Nuevo Cliente
        self.botonNuevoCliente = QPushButton("+ Nuevo Cliente")
        self.botonNuevoCliente.clicked.connect(self.mainWindow.mostrarFormCliente)
        self.botonesLayout.addWidget(self.botonNuevoCliente)

        # 3. Historial
        self.botonVerTodos = QPushButton("Historial Completo")
        self.botonVerTodos.clicked.connect(self.verTodosLosTurnos) 
        self.botonesLayout.addWidget(self.botonVerTodos)

        # 4. Estadísticas (Inicialmente oculto)
        self.botonEstadisticas = QPushButton("📊 Estadísticas")
        self.botonEstadisticas.clicked.connect(self.verEstadisticas)
        self.botonEstadisticas.setVisible(False) 
        self.botonesLayout.addWidget(self.botonEstadisticas)

        # 5. Cerrar Sesión
        self.botonVolver = QPushButton("Cerrar Sesión")
        self.botonVolver.clicked.connect(self.volver)
        self.botonesLayout.addWidget(self.botonVolver)

        botonesWidget = QWidget()
        botonesWidget.setLayout(self.botonesLayout)
        mainLayout.addWidget(botonesWidget)

        self.setLayout(mainLayout)
        self.darStilos()
        
        # Carga inicial (aunque showEvent lo hará de nuevo)
        self.cargarTurnosDelDia()

    def showEvent(self, event):
        """
        Se ejecuta cada vez que se muestra la pantalla.
        Controla los permisos de admin y el nombre de usuario.
        """
        if self.mainWindow.usuario_logueado:
            nombre = self.mainWindow.usuario_logueado.get('nombre_completo', 'Usuario')
            rol = self.mainWindow.usuario_logueado.get('rol', 'empleado') 
            
            self.lblUsuario.setText(f"👤 Hola, {nombre} ({rol})")
            
            # --- SEGURIDAD: Solo Admin ve el botón ---
            if rol == 'admin':
                self.botonEstadisticas.setVisible(True)
            else:
                self.botonEstadisticas.setVisible(False)
        else:
            self.lblUsuario.setText("👤 Usuario: -")
            self.botonEstadisticas.setVisible(False)

        self.cargarTurnosDelDia()

    def verEstadisticas(self):
        # Abre la ventana con el gráfico de torta
        self.ventanaStats = VistaEstadisticas()
        self.ventanaStats.show()

    def cargarTurnosDelDia(self):
        self.tablaTurnos.setRowCount(0)
        conn = conectarBase()
        try:
            cursor = conn.cursor()
            hoy = QDate.currentDate().toString("yyyy-MM-dd")
            
            sql = """
                SELECT 
                    T.hora, C.nombre, C.apellido, S.nombreDeServicio, 
                    C.localidad, T.estado, T.observaciones, C.idCliente, T.idTurno, T.fecha
                FROM turnosTomados T
                JOIN clientes C ON T.fkIdCliente = C.idCliente
                JOIN servicios S ON T.fkIdServicio = S.idServicio
                WHERE T.fecha = ?
                ORDER BY T.hora ASC
            """
            cursor.execute(sql, (hoy,))
            turnos = cursor.fetchall()

            self.tablaTurnos.setRowCount(len(turnos))

            for row, datos in enumerate(turnos):
                hora, nom, ape, serv, loc, estado_db, obs, id_cli, id_turno, fecha = datos

                # --- Lógica Nombre ---
                if id_cli == 1:
                    nombre_final = obs if obs else "Consumidor Final"
                    localidad_final = "-"
                else:
                    nombre_final = f"{nom} {ape}"
                    localidad_final = loc
                
                # --- Items de Texto ---
                self.tablaTurnos.setItem(row, 0, QTableWidgetItem(str(hora)))
                self.tablaTurnos.setItem(row, 1, QTableWidgetItem(str(nombre_final)))
                self.tablaTurnos.setItem(row, 2, QTableWidgetItem(str(serv)))
                self.tablaTurnos.setItem(row, 3, QTableWidgetItem(str(localidad_final)))

                # --- ComboBox Estado ---
                comboEstado = QComboBox()
                opciones = ["Pendiente", "Finalizado", "Cancelado"]
                comboEstado.addItems(opciones)
                
                # Transformar de BD (minúscula) a Visual (Capitalize)
                estado_visual = estado_db.capitalize() 
                comboEstado.setCurrentText(estado_visual)
                comboEstado.setProperty("estado_anterior", estado_visual)
                
                self.aplicarColorCombo(comboEstado, estado_visual)
                
                # Conectar señal
                comboEstado.activated.connect(lambda _, c=comboEstado, id=id_turno: self.confirmarCambioEstado(c, id))
                self.tablaTurnos.setCellWidget(row, 4, comboEstado)

                # --- Botón Eliminar ---
                btnEliminar = QPushButton("❌")
                btnEliminar.setStyleSheet("color: red; font-weight: bold; border: none;")
                btnEliminar.setCursor(Qt.PointingHandCursor)
                btnEliminar.clicked.connect(lambda _, id=id_turno: self.borrarTurno(id))
                self.tablaTurnos.setCellWidget(row, 5, btnEliminar)

                # --- ID Oculto ---
                self.tablaTurnos.setItem(row, 6, QTableWidgetItem(str(id_turno)))
                # Guardamos fecha para el editor
                self.tablaTurnos.item(row, 6).setData(Qt.UserRole, fecha) 

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    def abrirEditorDeTurno(self, index):
        """Doble click para editar"""
        row = index.row()
        try:
            hora_actual = self.tablaTurnos.item(row, 0).text()
            servicio_actual = self.tablaTurnos.item(row, 2).text()
            
            # Recuperar datos ocultos
            id_turno = int(self.tablaTurnos.item(row, 6).text())
            fecha_actual = self.tablaTurnos.item(row, 6).data(Qt.UserRole)

            editor = VentanaEditarTurno(id_turno, fecha_actual, hora_actual, servicio_actual, self)
            if editor.exec_(): 
                self.cargarTurnosDelDia() # Recargar si guardó cambios
        except Exception as e:
            print(f"Error abriendo editor: {e}")

    # --- LÓGICA DE ESTADOS Y COLORES ---
    def aplicarColorCombo(self, combo, texto_estado):
        if texto_estado == "Finalizado":
            combo.setStyleSheet("color: green; font-weight: bold;")
        elif texto_estado == "Cancelado":
            combo.setStyleSheet("color: red;")
        else:
            combo.setStyleSheet("color: black;")

    def confirmarCambioEstado(self, combo, id_turno):
        nuevo_estado_visual = combo.currentText()
        estado_anterior = combo.property("estado_anterior")

        respuesta = QMessageBox.question(
            self, "Confirmar Cambio", 
            f"¿Desea cambiar el estado a '{nuevo_estado_visual}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            estado_para_bd = nuevo_estado_visual.lower()
            exito = cambiarEstadoTurno(id_turno, estado_para_bd)
            if exito:
                combo.setProperty("estado_anterior", nuevo_estado_visual)
                self.aplicarColorCombo(combo, nuevo_estado_visual)
            else:
                QMessageBox.warning(self, "Error", "No se pudo guardar.")
                self.revertirCombo(combo, estado_anterior)
        else:
            self.revertirCombo(combo, estado_anterior)

    def revertirCombo(self, combo, estado_anterior):
        combo.blockSignals(True)
        combo.setCurrentText(estado_anterior)
        self.aplicarColorCombo(combo, estado_anterior)
        combo.blockSignals(False)

    def borrarTurno(self, id_turno):
        respuesta = QMessageBox.question(
            self, "Confirmar Eliminación", 
            "¿Estás seguro de que querés borrar este turno permanentemente?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            if eliminarTurno(id_turno):
                self.cargarTurnosDelDia()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar")

    # --- NAVEGACIÓN ---
    def abrirFormTurnos(self):
        self.formTurno = FormTurno(self.mainWindow) 
        self.mainWindow.stack.addWidget(self.formTurno)
        self.mainWindow.stack.setCurrentWidget(self.formTurno)

    def verTodosLosTurnos(self):
        self.fullTurnos = TodosLosTurnos()
        self.fullTurnos.show()

    def volver(self):
        eliminarSesion()
        self.mainWindow.mostrarLogin()
        self.mainWindow.usuario_logueado = None

    def darStilos(self):
        self.tablaTurnos.setStyleSheet(estiloTabla)
        self.botonNuevo.setStyleSheet(estiloBoton)
        self.botonNuevoCliente.setStyleSheet(estiloBoton)
        self.botonVerTodos.setStyleSheet(estiloBoton)
        self.botonVolver.setStyleSheet(estiloBoton)
        
        # Estilo especial para el botón de estadísticas
        self.botonEstadisticas.setStyleSheet("""
            QPushButton {
                background-color: #673AB7; 
                color: white; 
                font-size: 14px; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover { background-color: #512DA8; }
        """)