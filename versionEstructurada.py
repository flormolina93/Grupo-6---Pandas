from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
import sys

def abrir_login():
    print("Ir a login (esto cambiaría la pantalla)")

def abrir_registro():
    print("Ir a registro (esto cambiaría la pantalla)")

def mostrar_pantalla_bienvenida():
    ventana = QWidget()
    ventana.setWindowTitle("Bienvenida a la App de Turnos")
    ventana.setGeometry(300, 300, 300, 200)

    layout_principal = QVBoxLayout()
    layout_principal.setAlignment(Qt.AlignCenter)

    titulo = QLabel("¡Bienvenido/a!")
    titulo.setAlignment(Qt.AlignCenter)
    titulo.setStyleSheet("font-weight: bold; font-size: 18px; color: #444;")
    layout_principal.addWidget(titulo)

    boton_login = QPushButton("Iniciar sesión")
    boton_login.setStyleSheet("background-color: #2e86de; color: white; padding: 10px; border-radius: 5px;")
    boton_login.clicked.connect(abrir_login)
    layout_principal.addWidget(boton_login)

    boton_registro = QPushButton("Registrarse como Admin")
    boton_registro.setStyleSheet("background-color: #2e86de; color: white; padding: 10px; border-radius: 5px;")
    boton_registro.clicked.connect(abrir_registro)
    layout_principal.addWidget(boton_registro)

    ventana.setLayout(layout_principal)
    ventana.show()
    return ventana

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pantalla = mostrar_pantalla_bienvenida()
    sys.exit(app.exec_())
