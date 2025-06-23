from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class EstadisticasLocalidadWidget(QWidget):
    def __init__(self, conteoLocalidades):
        super().__init__()
        self.setWindowTitle("Estadísticas por Localidad")
        self.setGeometry(400, 300, 300, 200)

        layout = QVBoxLayout()

        titulo = QLabel("Conteo de turnos por localidad")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Mostrar resultados en un label simple
        texto = "\n".join([f"{loc}: {cant}" for loc, cant in conteoLocalidades.items()])
        etiqueta = QLabel(texto)
        etiqueta.setAlignment(Qt.AlignLeft)
        layout.addWidget(etiqueta)

        self.setLayout(layout)

        self.plot(conteoLocalidades)

    def plot(self, conteoLocalidades):
        ax = self.figure.add_subplot(111)
        ax.clear()

        localidades = list(conteoLocalidades.index)
        cantidades = list(conteoLocalidades.values)

        ax.bar(localidades, cantidades, color='red')
        ax.set_title("Cantidad de turnos por localidad")
        ax.set_ylabel("Cantidad")
        ax.set_xlabel("Localidad")
        ax.tick_params(axis='x', rotation=45)

        self.canvas.draw()

