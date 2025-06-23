import pandas as pd
from models.conectarBase import conectarBase
def obtenerDatosTurnos():
    conn = conectarBase()
    query = "SELECT * FROM turnos"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def estadisticasLocalidad(df):
    conteo = df['localidad'].value_counts()
    print(conteo)
    return conteo

