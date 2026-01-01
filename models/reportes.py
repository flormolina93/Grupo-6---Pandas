from models.conectarBase import conectarBase

def obtenerRankingServicios():
    """Retorna: [('Corte', 15), ('Barba', 5)]"""
    conn = conectarBase()
    try:
        cursor = conn.cursor()
        sql = """
            SELECT S.nombreDeServicio, COUNT(T.idTurno) as cantidad
            FROM turnosTomados T
            JOIN servicios S ON T.fkIdServicio = S.idServicio
            WHERE T.estado != 'cancelado'
            GROUP BY S.nombreDeServicio
            ORDER BY cantidad DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error reporte servicios: {e}")
        return []
    finally:
        conn.close()

def obtenerTurnosPorHora():
    """
    Agrupa por la hora (ej: las 14:00, 14:30 cuentan como '14')
    Retorna: [('09', 5), ('10', 8), ...] ordenado por hora.
    """
    conn = conectarBase()
    try:
        cursor = conn.cursor()
        # Usamos substr para agarrar los primeros 2 caracteres de la hora (HH)
        sql = """
            SELECT substr(hora, 1, 2) as bloque_hora, COUNT(idTurno) as cantidad
            FROM turnosTomados
            WHERE estado != 'cancelado'
            GROUP BY bloque_hora
            ORDER BY bloque_hora ASC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error reporte horas: {e}")
        return []
    finally:
        conn.close()

def obtenerTurnosPorLocalidad():
    """Retorna: [('Lomas de Zamora', 20), ('Banfield', 12)]"""
    conn = conectarBase()
    try:
        cursor = conn.cursor()
        sql = """
            SELECT C.localidad, COUNT(T.idTurno) as cantidad
            FROM turnosTomados T
            JOIN clientes C ON T.fkIdCliente = C.idCliente
            WHERE T.estado != 'cancelado' 
            AND C.idCliente != 1 -- Opcional: Excluir 'Consumidor Final' si ensucia el gráfico
            GROUP BY C.localidad
            ORDER BY cantidad DESC
            LIMIT 10 -- Top 10 localidades para no saturar
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error reporte localidades: {e}")
        return []
    finally:
        conn.close()