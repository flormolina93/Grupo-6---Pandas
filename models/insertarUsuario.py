from models.conectarBase import conectarBase
import bcrypt
import sqlite3

def insertarUsuario(email, password, nombre, esAdmin=0):
    try:
        conn = conectarBase()
        cursor = conn.cursor()

        #Hashear la contraseña
        passwordBytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(passwordBytes, bcrypt.gensalt())
        hashedStr = hashed.decode('utf-8')

        cursor.execute(""" INSERT INTO usuarios(email, password, nombre, esAdmin)
                       VALUES (?,?,?,?)""", (email, hashedStr, nombre, esAdmin))
        
        conn.commit()
        conn.close()
        return True, "Usuario registrado con exito."
    except sqlite3.IntegrityError:
        return False, "El correo ya esta registrado."
    except Exception as e:
        return False, f"Error al registrar usuario: {e}"