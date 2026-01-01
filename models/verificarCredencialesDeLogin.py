from models.conectarBase import conectarBase
import bcrypt
from typing import Tuple, Union, Dict
import bcrypt
from models.conectarBase import conectarBase

def verificarCredencialesDeLogin(dni: int, password: str) -> Tuple[bool, Union[Dict, str]]:
    """
    Verifica las credenciales de un empleado.
    
    Args:
        dni (int): DNI del empleado.
        password (str): Contraseña en texto plano ingresada por el usuario.
        
    Returns:
        Tuple[bool, Union[Dict, str]]: 
            - (True, dict_datos_usuario) si es exitoso.
            - (False, mensaje_error) si falla.
    """
    conn = None
    try:
        conn = conectarBase()
        cursor = conn.cursor()

        sql = "SELECT idEmpleado, password, nombre, apellido, rol FROM empleados WHERE dni = ?"
        cursor.execute(sql, (dni,))
        resultado = cursor.fetchone()

        # 1. Validación temprana: Si no existe el usuario, cortamos acá.
        if not resultado:
            return False, "El DNI no está registrado en el sistema."

        id_empleado, hash_guardado, nombre, apellido, rol = resultado

        # 2. Validación de seguridad: Usuario sin pass en BD
        if not hash_guardado:
            return False, "Este usuario no tiene contraseña configurada."

        # 3. Preparar bytes para Bcrypt (Manejo robusto de tipos)
        # Aseguramos que el hash sea bytes, por si SQLite lo devuelve como string
        hash_bytes = hash_guardado.encode('utf-8') if isinstance(hash_guardado, str) else hash_guardado
        password_bytes = password.encode('utf-8')

        if bcrypt.checkpw(password_bytes, hash_bytes):
            datos_usuario = {
                "id": id_empleado,
                "nombre_completo": f"{nombre} {apellido}",
                "rol": rol,
                "esAdmin": (rol == 'admin')
            }
            return True, datos_usuario
        else:
            return False, "Contraseña incorrecta."

    except Exception as e:
        # En producción acá meterías un log del error real (print(e) o logging.error(e))
        return False, f"Error crítico del sistema: {str(e)}"

    finally:
        # 4. CIERRE SEGURO: Esto se ejecuta SIEMPRE, haya return, éxito o error.
        if conn:
            conn.close()