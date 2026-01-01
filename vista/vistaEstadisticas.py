from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Importamos las 3 funciones del modelo
from models.reportes import obtenerRankingServicios, obtenerTurnosPorHora, obtenerTurnosPorLocalidad

class VistaEstadisticas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Estadísticas del Negocio")
        self.setGeometry(100, 100, 900, 650)
        self.setStyleSheet("background-color: #f5f5f5;") # Fondo gris clarito

        mainLayout = QVBoxLayout()

        # --- TÍTULO ---
        titulo = QLabel("Panel de Métricas")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin: 10px;")
        titulo.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(titulo)

        # --- PESTAÑAS (TABS) ---
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #ccc; background: white; }
            QTabBar::tab { background: #e0e0e0; padding: 10px; margin: 2px; border-radius: 4px; }
            QTabBar::tab:selected { background: #673AB7; color: white; font-weight: bold; }
        """)

        # Pestaña 1: Servicios
        self.tabServicios = QWidget()
        self.setupTabServicios()
        self.tabs.addTab(self.tabServicios, "🍕 Por Servicio")

        # Pestaña 2: Horarios
        self.tabHorarios = QWidget()
        self.setupTabHorarios()
        self.tabs.addTab(self.tabHorarios, "⏰ Por Horario")

        # Pestaña 3: Localidades
        self.tabLocalidades = QWidget()
        self.setupTabLocalidades()
        self.tabs.addTab(self.tabLocalidades, "📍 Por Localidad")

        mainLayout.addWidget(self.tabs)

        # --- BOTÓN CERRAR ---
        btnCerrar = QPushButton("Cerrar")
        btnCerrar.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-weight: bold;")
        btnCerrar.clicked.connect(self.close)
        mainLayout.addWidget(btnCerrar)

        self.setLayout(mainLayout)

    # --- PESTAÑA 1: GRÁFICO DE TORTA (SERVICIOS) ---
    def setupTabServicios(self):
        layout = QVBoxLayout()
        datos = obtenerRankingServicios()
        
        if not datos:
            layout.addWidget(QLabel("No hay datos suficientes."))
        else:
            etiquetas = [fila[0] for fila in datos]
            valores = [fila[1] for fila in datos]

            fig, ax = plt.subplots(figsize=(5, 4))
            colores = ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0', '#FF5722']
            
            ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores)
            ax.set_title("Distribución de Servicios Vendidos")
            
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)
        
        self.tabServicios.setLayout(layout)

    # --- PESTAÑA 2: GRÁFICO DE BARRAS (HORARIOS) ---
    def setupTabHorarios(self):
        layout = QVBoxLayout()
        datos = obtenerTurnosPorHora() # [('09', 5), ('10', 8)...]
        
        if not datos:
            layout.addWidget(QLabel("No hay datos de horarios."))
        else:
            horas = [fila[0] + ":00" for fila in datos] # Agregamos :00 para que quede lindo
            cantidad = [fila[1] for fila in datos]

            fig, ax = plt.subplots(figsize=(5, 4))
            
            # Gráfico de Barras Vertical
            ax.bar(horas, cantidad, color='#3F51B5')
            
            ax.set_xlabel("Hora del día")
            ax.set_ylabel("Cantidad de Turnos")
            ax.set_title("Horas Pico de Atención")
            ax.grid(axis='y', linestyle='--', alpha=0.7) # Rejilla horizontal suave

            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)
        
        self.tabHorarios.setLayout(layout)

    # --- PESTAÑA 3: BARRAS HORIZONTALES (LOCALIDADES) ---
    def setupTabLocalidades(self):
        layout = QVBoxLayout()
        datos = obtenerTurnosPorLocalidad()
        
        if not datos:
            layout.addWidget(QLabel("No hay datos de localidades."))
        else:
            # Matplotlib dibuja de abajo hacia arriba, así que invertimos la lista 
            # para que el Top 1 quede arriba visualmente
            datos = datos[::-1] 
            
            localidades = [fila[0] for fila in datos]
            cantidad = [fila[1] for fila in datos]

            fig, ax = plt.subplots(figsize=(5, 4))
            
            # Gráfico de Barras Horizontal (barh)
            ax.barh(localidades, cantidad, color='#009688')
            
            ax.set_xlabel("Cantidad de Clientes")
            ax.set_title("Clientes por Localidad")
            ax.grid(axis='x', linestyle='--', alpha=0.7)

            # Ajustamos el margen para que entren los nombres largos
            plt.tight_layout()

            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)
        
        self.tabLocalidades.setLayout(layout)