from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPalette, QBrush

class LoginStyloFondo:
    def aplicarEstilo(self, widget: QWidget):
        # Fondo
        background = QPixmap("img/fondo.png")
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(background))
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)

        # Podés aplicar otros estilos al widget entero acá si querés
