import folium
import json

def generate_map(individual, crime_data, comisarias_data, incident_comisaria_map, mes_seleccionado=None, periodo_seleccionado=None):
    """
    Esta función genera el mapa con los incidentes y calcula el tiempo de respuesta
    total y promedio por comisaría para un individuo optimizado o la distribución actual.
    """
    # Aplicar filtros
    if mes_seleccionado is not None:
        crime_data = crime_data[crime_data['mes'] == mes_seleccionado]

    if periodo_seleccionado is not None:
        crime_data = crime_data[crime_data['periodo_del_dia'] == periodo_seleccionado]

    # Crear un mapa centrado en la primera comisaría
    m = folium.Map(location=[comisarias_data.iloc[0]['latitud'], comisarias_data.iloc[0]['longitud']], zoom_start=12)

    # Variables para calcular tiempos de respuesta
    total_response_time = 0
    response_times_per_comisaria = {comisaria['id']: [] for _, comisaria in comisarias_data.iterrows()}

    # Agregar leyenda en la parte superior centrada
    total_incidentes = len(crime_data)
    legend_html = f'''
     <div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: 225px; height: 65px; 
     background-color: white;
     border:2px solid grey; z-index:9999; font-size:14px;
     ">
     &nbsp; <b>Total Incidentes:</b> {total_incidentes} <br>
     &nbsp; <b>Mes Seleccionado:</b> {mes_seleccionado if mes_seleccionado else 'Todos'} <br>
     &nbsp; <b>Periodo Seleccionado:</b> {periodo_seleccionado if periodo_seleccionado else 'Todos'} 
     </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Cargar el archivo JSON con los límites de Ciudad del Este
    with open('cde.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extraer las coordenadas del polígono y agregarlo al mapa
    coordinates = data['geometry']['coordinates'][0][0]
    coordinates = [(coord[1], coord[0]) for coord in coordinates]
    folium.Polygon(locations=coordinates, color="blue", weight=2.5, fill=True, fill_opacity=0.2).add_to(m)

    # Agregar marcadores de comisarías
    for i, row in comisarias_data.iterrows():
        lat = row['latitud']
        lon = row['longitud']
        patrullas = individual[i]
        icon = folium.DivIcon(html=f"""
        <div style="font-family: Arial; color: white; background-color: black; border-radius: 50%; width: 30px; height: 30px; text-align: center; line-height: 30px;">
        {patrullas}
        </div>
        """)
        folium.Marker([lat, lon], icon=icon).add_to(m)

    # Agregar marcadores de incidentes y calcular tiempos de respuesta según la cantidad de patrulleras
    for i, row in crime_data.iterrows():
        lat = row['latitud']
        lon = row['longitud']
        categoria = row['categoria']
        tipo_delito = row['tipo_delito']

        if row['id'] in incident_comisaria_map:
            nearest_comisaria = min(incident_comisaria_map[row['id']], key=lambda x: x[1])
            nearest_comisaria_idx = nearest_comisaria[0]
            response_time = nearest_comisaria[1]

            # Obtener la cantidad de patrulleras asignadas a la comisaría
            num_patrulleras = individual[nearest_comisaria_idx - 1]

            if num_patrulleras > 0:
                # Si hay patrulleras, distribuir los incidentes para que el tiempo se reduzca
                adjusted_response_time = response_time / num_patrulleras
            else:
                # Si no hay patrulleras, el tiempo de respuesta es el mismo (sin penalización)
                adjusted_response_time = response_time

            # Acumular el tiempo de respuesta
            total_response_time += adjusted_response_time
            response_times_per_comisaria[nearest_comisaria_idx].append(adjusted_response_time)

            # Crear el popup con la información del incidente
            popup_text = f"""
            Coordenadas: ({lat}, {lon})<br>
            Categoría: {categoria}<br>
            Tipo de Delito: {tipo_delito}<br>
            Tiempo de Respuesta: {adjusted_response_time:.2f} minutos
            """
        else:
            popup_text = f"Coordenadas: ({lat}, {lon})<br> Categoría: {categoria}<br>Tipo de Delito: {tipo_delito}"

        # Agregar el marcador del incidente
        folium.CircleMarker(location=(lat, lon), radius=5, color='red', fill=True, fill_color='red', fill_opacity=0.7,
                            popup=folium.Popup(popup_text, max_width=300)).add_to(m)

        # Conectar incidentes con la comisaría asignada
        if row['id'] in incident_comisaria_map:
            nearest_comisaria_idx = nearest_comisaria[0] - 1
            folium.PolyLine([(lat, lon), 
                             (comisarias_data.iloc[nearest_comisaria_idx]['latitud'], comisarias_data.iloc[nearest_comisaria_idx]['longitud'])],
                            color="gray", weight=2.5, opacity=1).add_to(m)

    # Cálculo del tiempo promedio por comisaría
    avg_response_times_per_comisaria = []
    for comisaria_id, times in response_times_per_comisaria.items():
        if times:  # Evitar dividir por 0 si una comisaría no maneja incidentes
            avg_response_time = sum(times) / len(times)
        else:
            avg_response_time = 0  # Si la comisaría no maneja incidentes

        avg_response_times_per_comisaria.append(avg_response_time)
        print(f"Comisaría {comisaria_id}: Tiempo promedio de respuesta: {avg_response_time:.2f} minutos")

    # Imprimir el tiempo total de respuesta
    print(f"Tiempo de respuesta total para este individuo: {total_response_time:.2f} minutos")

    # Guardar el mapa
    m.save('mapa_con_tiempos.html')

    # Devolver tiempos de respuesta totales y por comisaría
    return total_response_time, avg_response_times_per_comisaria
