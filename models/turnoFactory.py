from models.turno import Turno

class TurnoFactory:
    @staticmethod
    def crearTurno(nombre, servicio, localidad, celular, fecha, hora):
        nombre = nombre.strip().title()
        servicio = servicio.strip().capitalize()
        localidad = localidad.strip().title()  # <- Normalización acá
        celular = celular.strip()
        fecha = fecha.strip()
        hora = hora.strip()

        return Turno(nombre, servicio, localidad, celular, fecha, hora)
