from conectarBase import conectarBase

conn = conectarBase()
cursor = conn.cursor()

# Le preguntamos a la base de datos cómo está formada la tabla
cursor.execute("PRAGMA table_info(servicios)")
columnas = cursor.fetchall()

print("--- TUS COLUMNAS SON ---")
for col in columnas:
    print(f"ID: {col[0]} | Nombre: {col[1]} | Tipo: {col[2]}")

conn.close()