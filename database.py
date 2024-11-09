import mysql.connector
import pandas as pd

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tesis"
    )

def categorize_period_of_day(hour):
    if 6 <= hour < 12:
        return 'mañana'
    elif 12 <= hour < 18:
        return 'tarde'
    else:
        return 'noche'

def load_data_from_db():
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            i.id, 
            tipo_delito, 
            latitud, 
            longitud, 
            fecha_hora, 
            id_categoria, 
            id_barrio, 
            b.descripcion AS barrio, 
            c.descripcion AS categoria 
        FROM incidentes i 
        JOIN barrios b ON i.id_barrio = b.id 
        JOIN categorias c ON i.id_categoria = c.id
    """)
    incidentes = cursor.fetchall()

    # Actualiza las columnas del DataFrame para que coincidan con la consulta
    incidentes_df = pd.DataFrame(incidentes, columns=['id', 'tipo_delito', 'latitud', 'longitud', 'FECHA_HORA', 'id_categoria', 'id_barrio', 'barrio', 'categoria'])

    # Convertir FECHA_HORA a un tipo de dato datetime si no lo es
    incidentes_df['FECHA_HORA'] = pd.to_datetime(incidentes_df['FECHA_HORA'])
    
    # Crear una nueva columna con el mes extraído de FECHA_HORA
    incidentes_df['mes'] = incidentes_df['FECHA_HORA'].dt.month

    # Clasificar el incidente según la hora del día
    incidentes_df['periodo_del_dia'] = incidentes_df['FECHA_HORA'].dt.hour.apply(categorize_period_of_day)

    cursor.execute("SELECT id, latitud, longitud, id_barrio, patrullas FROM comisarias")
    comisarias = cursor.fetchall()
    comisarias_df = pd.DataFrame(comisarias, columns=['id', 'latitud', 'longitud', 'id_barrio', 'patrullas'])

    cursor.close()
    db.close()

    return incidentes_df, comisarias_df