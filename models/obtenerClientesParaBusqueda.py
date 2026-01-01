from models.conectarBase import conectarBase

def obtenerClientesParaBusqueda():
    """
    Retorna una lista de diccionarios con los datos de los clientes
    para usar en el autocompletado.
    """
    lista_clientes = []
    conn = conectarBase()
    try:
        cursor = conn.cursor()
        # Traemos Nombre, Apellido, Localidad y Teléfono
        sql = """
            SELECT c.nombre, c.apellido, c.localidad, t.telefono 
            FROM clientes c
            JOIN telefonosCliente t ON c.idCliente = t.fkIdCliente
        """
        cursor.execute(sql)
        datos = cursor.fetchall()

        for fila in datos:
            nombre, apellido, localidad, telefono = fila
            
            # Armamos una etiqueta bonita para el buscador
            # Ej: "Marta Perez - 11223344"
            texto_mostrar = f"{nombre} {apellido} - {telefono}"
            
            cliente_dict = {
                "label": texto_mostrar, # Lo que se ve en la lista
                "nombre_real": f"{nombre} {apellido}",
                "localidad": localidad,
                "telefono": telefono
            }
            lista_clientes.append(cliente_dict)

    except Exception as e:
        print(f"Error obteniendo clientes: {e}")
    finally:
        conn.close()
        
    return lista_clientes