from models.conectarBase import conectarBase
import bcrypt
import sqlite3

# Agregamos calle y numero a los parámetros
def insertarUsuario(nombre, apellido, dni, email, telefono, calle, numero, password, esAdmin=0):
    conn = conectarBase()
    
    try:
        with conn:
            cursor = conn.cursor()

            # 1. Hashear password
            passwordBytes = password.encode('utf-8')
            hashed = bcrypt.hashpw(passwordBytes, bcrypt.gensalt())
            hashedStr = hashed.decode('utf-8')

            rol = "admin" if esAdmin else "empleado"

            # 2. Insertar en tabla EMPLEADOS (Ahora con Calle y Numero)
            # Nota: Si el numero viene vacío, guardamos NULL (None en Python)
            val_numero = int(numero) if numero and numero.isdigit() else None

            sql_empleado = """
                INSERT INTO empleados (nombre, apellido, dni, calle, numeroCalle, rol, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sql_empleado, (nombre, apellido, dni, calle, val_numero, rol, hashedStr))
            
            id_nuevo_empleado = cursor.lastrowid 

            # 3. Insertar Email
            if email:
                sql_email = "INSERT INTO emailEmpleado (fkIdEmpleado, email) VALUES (?, ?)"
                cursor.execute(sql_email, (id_nuevo_empleado, email))

            # 4. Insertar Teléfono
            if telefono:
                sql_tel = "INSERT INTO telefonosEmpleado (fkIdEmpleado, telefono) VALUES (?, ?)"
                cursor.execute(sql_tel, (id_nuevo_empleado, telefono))

        return True, "Empleado registrado con éxito."

    except sqlite3.IntegrityError as e:
        errores = str(e)
        if "dni" in errores:
            return False, "Error: El DNI ya está registrado."
        elif "email" in errores:
            return False, "Error: El Email ya está registrado."
        elif "telefono" in errores:
            return False, "Error: El Teléfono ya está registrado."
        else:
            return False, f"Error de duplicados: {errores}"
        
    except Exception as e:
        return False, f"Error técnico: {e}"
    
    finally:
        conn.close()