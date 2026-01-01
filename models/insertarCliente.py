from models.conectarBase import conectarBase

def insertarNuevoCliente(nombre, apellido, calle, numero, localidad, telefono):
    conn = conectarBase()
    try:
        with conn: # Transacción de seguridad
            cursor = conn.cursor()

            # 1. Validar si el teléfono ya existe (para no duplicar)
            cursor.execute("SELECT fkIdCliente FROM telefonosCliente WHERE telefono = ?", (telefono,))
            if cursor.fetchone():
                return False, "Ese número de celular ya está registrado."

            # 2. Insertar en tabla 'clientes' (Respetando tu estructura)
            # Nota: Si calle o numero vienen vacíos, guardamos None (NULL en la base)
            sql_cliente = """
                INSERT INTO clientes (nombre, apellido, calle, numeroCalle, localidad) 
                VALUES (?, ?, ?, ?, ?)
            """
            
            # Ajuste para que se guarde NULL si el campo está vacío
            val_calle = calle if calle else None
            val_numero = int(numero) if numero and numero.isdigit() else None
            
            cursor.execute(sql_cliente, (nombre, apellido, val_calle, val_numero, localidad))
            
            # 3. Recuperar el ID nuevo
            id_nuevo_cliente = cursor.lastrowid

            # 4. Insertar el teléfono vinculado
            sql_telefono = "INSERT INTO telefonosCliente (fkIdCliente, telefono) VALUES (?, ?)"
            cursor.execute(sql_telefono, (id_nuevo_cliente, telefono))

            return True, "Cliente registrado exitosamente."

    except Exception as e:
        return False, f"Error técnico: {str(e)}"
    finally:
        if conn: conn.close()