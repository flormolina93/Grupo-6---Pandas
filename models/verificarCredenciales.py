from models.conectarBase import conectarBase
import bcrypt

def verificarCredenciales(email, password):
    try:
        conn = conectarBase()
        cursor = conn.cursor()

        cursor.execute("""SELECT password, nombre, esAdmin FROM usuarios WHERE email = ?""", (email,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            hashGuardado, nombre, esAdmin = resultado
            if bcrypt.checkpw(password.encode('utf-8'), hashGuardado.encode('utf-8')):
                return True, {"nombre": nombre, "esAdmin": esAdmin}
            else:
                return False, "Contraseña incorrecta"
        else:
            return False, "El correo no esta registrado"  
    except Exception as e:
        return False, f"Error en la verificacion: {e}"
