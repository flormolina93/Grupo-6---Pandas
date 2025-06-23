from models.conectarBase import conectarBase
from models.turno import Turno

def insertarTurno(turno: Turno):

    try:
        conn = conectarBase()
        cursor = conn.cursor()

        #Validar si ya existe un turno para el mismo dia y hora
        cursor.execute("SELECT * FROM turnos WHERE fecha= ? AND hora = ?",
            (turno.fecha, turno.hora))
        if cursor.fetchone():
            return False, "Ya hay un turno para ese horario."
        
        cursor.execute("""INSERT INTO turnos(nombre,servicio, localidad, celular, fecha,hora ) VALUES (?,?,?,?,?,?)""", (turno.nombre, turno.servicio,turno.localidad, turno.celular,turno.fecha,turno.hora))

        conn.commit()
        conn.close()

        return True, "Turno registrado con exito"
    except Exception as e:
        return False, f"Error al guardar el turno: {e}"
    
    

