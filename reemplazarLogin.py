def reemplazarLogin(self, nuevoLoginClass):
    # Elimina el viejo login del stack
    self.stack.removeWidget(self.loginScreen)
    self.loginScreen.deleteLater()

    # Crea una nueva instancia del login (con estilos, etc.)
    self.loginScreen = nuevoLoginClass(self)
    self.stack.insertWidget(1, self.loginScreen)  # index 1 = login

    # Mostrar el nuevo login
    self.stack.setCurrentIndex(1)
