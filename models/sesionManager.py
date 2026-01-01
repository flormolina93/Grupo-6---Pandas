import json
import os

# Nombre del archivo donde guardaremos la info (se crea en la carpeta del proyecto)
ARCHIVO_SESION = "sesion_activa.json"

def guardarSesion(datos_usuario):
    """Guarda el diccionario del usuario en un archivo JSON."""
    try:
        with open(ARCHIVO_SESION, 'w') as f:
            json.dump(datos_usuario, f)
        return True
    except Exception as e:
        print(f"Error guardando sesión: {e}")
        return False

def cargarSesion():
    """Devuelve los datos del usuario si existe el archivo, sino devuelve None."""
    if not os.path.exists(ARCHIVO_SESION):
        return None
    
    try:
        with open(ARCHIVO_SESION, 'r') as f:
            datos = json.load(f)
            return datos
    except Exception as e:
        print(f"Error leyendo sesión: {e}")
        return None

def eliminarSesion():
    """Borra el archivo para cerrar sesión."""
    if os.path.exists(ARCHIVO_SESION):
        try:
            os.remove(ARCHIVO_SESION)
        except Exception as e:
            print(f"Error eliminando sesión: {e}")