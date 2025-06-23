from models.insertarUsuario import insertarUsuario

def registrar(self):
        email = self.inputEmail.text().strip()
        password = self.inputPass.text()
        nombre = self.inputNombre.text()

        if not email or not password or not nombre:
            self.mensaje.setText("Complete todos los datos")
            self.mensaje.setStyleSheet("color: red;")
            return
        
        exito, mensaje = insertarUsuario(email, password, nombre, esAdmin = 1)  

        if exito:
            self.mensaje.setText(mensaje)
            self.mensaje.setStyleSheet("color: green;")
            self.inputEmail.clear()
            self.inputPass.clear()
            self.inputNombre.clear()
            self.mensaje.setText("SELECT * FROM usuarios")
        else:
            self.mensaje.setText(mensaje)
            self.mensaje.setStyleSheet("color: red;")