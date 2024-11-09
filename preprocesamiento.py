from database import connect_to_db

def preprocess_incident_comisaria_map():
    db = connect_to_db()
    cursor = db.cursor()

    # Consulta SQL para obtener la relación entre incidentes y comisarías, incluyendo patrullas
    cursor.execute("""
        SELECT ic.id_incidente, ic.id_comisaria, MIN(ic.tiempo) as tiempo, ic.distancia, c.patrullas 
        FROM incidentes_comisarias ic
        JOIN comisarias c ON ic.id_comisaria = c.id
        GROUP BY ic.id_incidente, ic.id_comisaria
    """)
    data = cursor.fetchall()

    # Crear el diccionario incident_comisaria_map con tiempo, distancia y patrullas
    incident_comisaria_map = {}
    for row in data:
        incident_id, comisaria_id, min_time, distance, patrullas = row
        if incident_id not in incident_comisaria_map:
            incident_comisaria_map[incident_id] = []
        # Añadir tiempo, distancia y patrullas al diccionario
        incident_comisaria_map[incident_id].append((comisaria_id, min_time, distance, patrullas))

    cursor.close()
    db.close()

    return incident_comisaria_map