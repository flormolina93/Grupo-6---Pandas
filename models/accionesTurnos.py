from models.conectarBase import conectarBase

def cambiarEstadoTurno(id_turno, nuevo_estado):
    """Actualiza el estado de un turno en la BD"""
    
    # DEBUG: Para ver si llegan bien los datos
    print(f"---- INTENTANDO CAMBIAR ESTADO ----")
    print(f"ID Turno: {id_turno} (Tipo: {type(id_turno)})")
    print(f"Nuevo Estado: {nuevo_estado}")

    conn = conectarBase()
    try:
        cursor = conn.cursor()
        
        # Consulta SQL Directa
        sql = "UPDATE turnosTomados SET estado = ? WHERE idTurno = ?"
        
        # Ejecutamos
        cursor.execute(sql, (nuevo_estado, id_turno))
        
        # IMPORTANTE: Forzamos el guardado manual
        conn.commit() 
        
        print("✅ ¡Base de datos actualizada con éxito!")
        return True

    except Exception as e:
        # ACÁ VAMOS A VER EL ERROR REAL
        print(f"❌ ERROR SQL FATAL: {e}")
        return False
        
    finally:
        conn.close()

def eliminarTurno(id_turno):
    """Elimina definitivamente el turno de la BD"""
    conn = conectarBase()
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM turnosTomados WHERE idTurno = ?"
        cursor.execute(sql, (id_turno,))
        conn.commit() # Agregamos commit manual acá también por las dudas
        return True
    except Exception as e:
        print(f"Error eliminando turno: {e}")
        return False
    finally:
        conn.close()
    
def editarDatosDelTurno(id_turno, nueva_fecha, nueva_hora, nuevo_servicio_texto):
    """
    Busca el ID del servicio por nombre y hace el Update del turno.
    """
    conn = conectarBase()
    try:
        cursor = conn.cursor()
        
        # 1. Necesitamos el ID del servicio nuevo (porque recibimos el texto "Corte")
        cursor.execute("SELECT idServicio FROM servicios WHERE nombreDeServicio = ?", (nuevo_servicio_texto,))
        resultado_serv = cursor.fetchone()
        
        if not resultado_serv:
            return False # No existe ese servicio
            
        id_servicio = resultado_serv[0]

        # 2. Hacemos el UPDATE
        sql = """
            UPDATE turnosTomados 
            SET fecha = ?, hora = ?, fkIdServicio = ?
            WHERE idTurno = ?
        """
        cursor.execute(sql, (nueva_fecha, nueva_hora, id_servicio, id_turno))
        conn.commit()
        return True

    except Exception as e:
        print(f"Error editando turno: {e}")
        return False
    finally:
        conn.close()