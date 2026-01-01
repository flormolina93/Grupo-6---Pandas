from models.conectarBase import conectarBase

def obtenerServicios():
    """
    Devuelve una lista de strings con los nombres de los servicios disponibles.
    Ej: ['Peluqueria', 'Manicuria', ...]
    """
    lista_servicios = []
    conn = conectarBase()
    try:
        cursor = conn.cursor()
        # OJO: Respetamos el nombre de la columna que pusiste en el PDF ("nombre De Servicio")
        cursor.execute('SELECT nombreDeServicio FROM servicios')
        resultados = cursor.fetchall()
        
        # resultados viene como una lista de tuplas: [('Peluqueria',), ('Masajes',)]
        # Lo limpiamos para que sea una lista simple: ['Peluqueria', 'Masajes']
        for fila in resultados:
            lista_servicios.append(fila[0])
            
    except Exception as e:
        print(f"Error cargando servicios: {e}")
    finally:
        if conn:
            conn.close()
            
    return lista_servicios