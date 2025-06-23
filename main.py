import sys
from PyQt5.QtWidgets import QApplication
from vista.bienvenida import Bienvenida
from models.crearTablaTurnos import crearTablaTurnos
from models.crearTablaUsuarios import crearTablaUsuarios
import os
from models.conectarBase import conectarBase
from vista.mainWindow import MainWindow

def main():
    crearTablaUsuarios()
    crearTablaTurnos()
    
    app = QApplication(sys.argv)

    ventanaPrincipal = MainWindow()
    ventanaPrincipal.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()