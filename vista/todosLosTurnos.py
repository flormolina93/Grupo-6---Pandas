from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QPushButton, QLabel, QHeaderView, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from models.conectarBase import conectarBase
from vista.estilosCss import estiloTabla

# Importamos la lógica de edición y borrado
from models.accionesTurnos import cambiarEstadoTurno, eliminarTurno
from vista.ventanaEditarTurno import VentanaEditarTurno

class TodosLosTurnos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial Completo de Turnos")
        self.setGeometry(150, 150, 1100, 600) # Un poco más ancha

        layout = QVBoxLayout()

        # --- Título ---
        titulo = QLabel("Historial Completo de Turnos")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; margin: 15px;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # --- Tabla ---
        self.tabla = QTableWidget()
        
        # Columnas: Fecha | Hora | Cliente | Servicio | Localidad | Estado | Borrar | ID (Oculto)
        self.tabla.setColumnCount(8)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Hora", "Cliente", "Servicio", "Localidad", "Estado", "Borrar", "ID"])
        
        # Ajuste de columnas
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents) # Columna borrar chiquita
        
        # OCULTAMOS LA COLUMNA ID (Índice 7)
        self.tabla.setColumnHidden(7, True)

        # Conectar Doble Click para editar
        self.tabla.doubleClicked.connect(self.abrirEditorDeTurno)
        
        layout.addWidget(self.tabla)

        # --- Botón Cerrar ---
        self.botonCerrar = QPushButton("Cerrar Historial")
        self.botonCerrar.clicked.connect(self.close)
        self.botonCerrar.setStyleSheet("background-color: #555; color: white; padding: 10px;")
        layout.addWidget(self.botonCerrar)

        self.setLayout(layout)
        
        # Estilos y Carga
        self.tabla.setStyleSheet(estiloTabla)
        self.cargarDatos()

    def cargarDatos(self):
        self.tabla.setRowCount(0)
        conn = conectarBase()
        
        try:
            cursor = conn.cursor()
            
            # --- SQL ACTUALIZADO: Traemos el ID del turno (T.idTurno) ---
            sql = """
                SELECT 
                    T.fecha,
                    T.hora, 
                    C.nombre, 
                    C.apellido, 
                    S.nombreDeServicio, 
                    C.localidad, 
                    T.estado, 
                    T.observaciones,
                    C.idCliente,
                    T.idTurno  -- IMPORTANTE
                FROM turnosTomados T
                JOIN clientes C ON T.fkIdCliente = C.idCliente
                JOIN servicios S ON T.fkIdServicio = S.idServicio
                ORDER BY T.fecha DESC, T.hora ASC
            """
            
            cursor.execute(sql)
            datos = cursor.fetchall()
            
            self.tabla.setRowCount(len(datos))

            for row, turno in enumerate(datos):
                # Desempaquetamos
                fecha, hora, nom, ape, servicio, loc, estado_db, obs, id_cliente, id_turno = turno

                # --- Lógica Nombre ---
                if id_cliente == 1:
                    nombre_final = obs if obs else "Consumidor Final"
                    localidad_final = "-" 
                else:
                    nombre_final = f"{nom} {ape}"
                    localidad_final = loc

                # --- Items de Texto ---
                self.tabla.setItem(row, 0, QTableWidgetItem(str(fecha)))
                self.tabla.setItem(row, 1, QTableWidgetItem(str(hora)))
                self.tabla.setItem(row, 2, QTableWidgetItem(str(nombre_final)))
                self.tabla.setItem(row, 3, QTableWidgetItem(str(servicio)))
                self.tabla.setItem(row, 4, QTableWidgetItem(str(localidad_final)))

                # --- COMBOBOX ESTADO ---
                comboEstado = QComboBox()
                opciones = ["Pendiente", "Finalizado", "Cancelado"]
                comboEstado.addItems(opciones)
                
                estado_visual = estado_db.capitalize()
                comboEstado.setCurrentText(estado_visual)
                comboEstado.setProperty("estado_anterior", estado_visual)
                self.aplicarColorCombo(comboEstado, estado_visual)
                
                comboEstado.activated.connect(lambda _, c=comboEstado, id=id_turno: self.confirmarCambioEstado(c, id))
                self.tabla.setCellWidget(row, 5, comboEstado)

                # --- BOTÓN BORRAR ---
                btnEliminar = QPushButton("❌")
                btnEliminar.setStyleSheet("color: red; font-weight: bold; border: none;")
                btnEliminar.setCursor(Qt.PointingHandCursor)
                btnEliminar.clicked.connect(lambda _, id=id_turno: self.borrarTurno(id))
                self.tabla.setCellWidget(row, 6, btnEliminar)

                # --- ID OCULTO ---
                self.tabla.setItem(row, 7, QTableWidgetItem(str(id_turno)))

        except Exception as e:
            print(f"Error cargando historial: {e}")
        finally:
            conn.close()

    # --- FUNCIONES DE LÓGICA (Idénticas al Dashboard) ---

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
            "¿Estás seguro de que querés borrar este turno del historial?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            if eliminarTurno(id_turno):
                self.cargarDatos() # Recargamos la tabla
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar")

    def abrirEditorDeTurno(self, index):
        row = index.row()
        try:
            # Recuperamos datos de la fila
            fecha_actual = self.tabla.item(row, 0).text() # Col 0
            hora_actual = self.tabla.item(row, 1).text()  # Col 1
            servicio_actual = self.tabla.item(row, 3).text() # Col 3
            
            # Recuperamos ID Oculto (Col 7)
            id_turno = int(self.tabla.item(row, 7).text())

            # Abrimos la ventana
            editor = VentanaEditarTurno(id_turno, fecha_actual, hora_actual, servicio_actual, self)
            if editor.exec_():
                self.cargarDatos() # Si guardó, recargamos
        except Exception as e:
            print(f"Error abriendo editor: {e}")