from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class Logo:
    def aplicarLogo(self,widget:)
        self.logo = QLabel()
        pixmap = QPixmap("recursos/logo.png")
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)

        layoutCentrado.addWidget(self.logo)
