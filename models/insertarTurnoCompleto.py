from models.conectarBase import conectarBase

def insertarTurnoCompleto(nombre_cliente, servicio_texto, localidad, celular, fecha, hora, id_empleado_logueado):
    conn = conectarBase()
    try:
        with conn: 
            cursor = conn.cursor()

            # --- 1. Buscamos el ID del Servicio ---
            cursor.execute("SELECT idServicio FROM servicios WHERE nombreDeServicio = ?", (servicio_texto,))
            res_servicio = cursor.fetchone()
            if not res_servicio:
                return False, f"El servicio '{servicio_texto}' no existe."
            id_servicio = res_servicio[0]

            # --- 2. Lógica del Cliente (SIN CREAR NADA NUEVO) ---
            id_cliente = None
            observaciones = "" 

            # Paso A: ¿Puso celular? Buscamos si existe.
            if celular and celular.strip() != "":
                cursor.execute("SELECT fkIdCliente FROM telefonosCliente WHERE telefono = ?", (celular,))
                res_tel = cursor.fetchone()

                if res_tel:
                    # ¡ENCONTRADO! Usamos el ID del cliente registrado
                    id_cliente = res_tel[0]
                    # Si querés, podés agregar algo a observaciones, o dejarlo vacío
                    # observaciones = "" 
                else:
                    # NO EXISTE: No lo creamos. Lo tratamos como Consumidor Final (ID 1)
                    # Y guardamos TODOS los datos en observaciones para no perder contacto
                    id_cliente = 1
                    observaciones = f"{nombre_cliente} ({localidad}) - Cel: {celular}"
            
            else:
                # Paso B: No puso celular. Es Consumidor Final (ID 1) directo.
                id_cliente = 1
                observaciones = f"{nombre_cliente} ({localidad})"

            # --- 3. Validar Disponibilidad ---
            cursor.execute("SELECT idTurno FROM turnosTomados WHERE fecha = ? AND hora = ?", (fecha, hora))
            if cursor.fetchone():
                return False, "Ese horario ya está ocupado."

            # --- 4. Insertar el Turno ---
            # Guardamos el ID (real o 1) y las observaciones con los datos visuales
            sql = """
                INSERT INTO turnosTomados 
                (fkIdCliente, fkIdEmpleado, fkIdServicio, fecha, hora, estado, observaciones) 
                VALUES (?, ?, ?, ?, ?, 'pendiente', ?)
            """
            cursor.execute(sql, (id_cliente, id_empleado_logueado, id_servicio, fecha, hora, observaciones))
            
            return True, "Turno registrado exitosamente."

    except Exception as e:
        return False, f"Error técnico: {str(e)}"
    finally:
        if conn: conn.close()