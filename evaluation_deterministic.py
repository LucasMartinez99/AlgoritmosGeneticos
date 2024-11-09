
def evaluate_deterministic(individual, crime_data, comisarias_data, incident_comisaria_map,
                           max_time=15, mes_seleccionado=None, periodo_seleccionado=None):
    """Evaluar el individuo de manera determinista, manteniendo las mismas 
    penalizaciones y recompensas que la función original."""
    
    # Aplicar filtros
    if mes_seleccionado is not None:
        crime_data = crime_data[crime_data['mes'] == mes_seleccionado]

    if periodo_seleccionado is not None:
        crime_data = crime_data[crime_data['periodo_del_dia'] == periodo_seleccionado]
    
    total_response_time = 0
    total_penalty = 0
    patrulleras_asignadas = [0] * len(comisarias_data)
    incidentes_manejados_por_comisaria = [0] * len(comisarias_data)
    
    total_patrullas_asignadas = 0  # Controlar el número total de patrulleras asignadas

    # Calcular la cantidad máxima de incidentes que puede manejar cada patrullera
    incidentes_por_patrullera = max(1, len(crime_data) // 39)

    # Evaluación de cada incidente
    for idx, incident in crime_data.iterrows():
        incident_id = incident['id']
        if incident_id in incident_comisaria_map:
            # Obtener la comisaría más cercana
            nearest_comisaria = min(incident_comisaria_map[incident_id], key=lambda x: x[1])
            nearest_comisaria_idx = nearest_comisaria[0]
            response_time = nearest_comisaria[1]

            # Acumular tiempo de respuesta y asignar incidente a una patrullera
            if response_time <= max_time * 60:
                current_patrulleras = patrulleras_asignadas[nearest_comisaria_idx - 1]
                max_incidentes_manejables = current_patrulleras * incidentes_por_patrullera

                if incidentes_manejados_por_comisaria[nearest_comisaria_idx 
                                                      - 1] < max_incidentes_manejables:
                    incidentes_manejados_por_comisaria[nearest_comisaria_idx - 1] += 1
                else:
                    if total_patrullas_asignadas < 39:
                        patrulleras_asignadas[nearest_comisaria_idx - 1] += 1
                        total_patrullas_asignadas += 1
                        incidentes_manejados_por_comisaria[nearest_comisaria_idx - 1] += 1
                        # Penalización por exceder sin asignar patrullas suficientes
                        total_penalty += (500 + 100 * incidentes_manejados_por_comisaria[nearest_comisaria_idx 
                                                                                         - 1])
                    else:
                        # Penalización por exceder el límite de patrulleras asignadas
                        total_penalty += 5000

            else:
                # Penalización por exceso de tiempo de respuesta
                total_penalty += (response_time - max_time * 60) * 1000

            # Acumular el tiempo de respuesta
            total_response_time += response_time

    # Asegurarse de que el total de patrulleras sea exactamente 39
    if total_patrullas_asignadas < 39:
        remaining_patrullas = 39 - total_patrullas_asignadas
        for i in range(remaining_patrullas):
            idx = random.randint(0, len(patrulleras_asignadas) - 1)
            patrulleras_asignadas[idx] += 1
    elif total_patrullas_asignadas > 39:
        excess_patrullas = total_patrullas_asignadas - 39
        for i in range(excess_patrullas):
            idx = random.choice([i for i, val in enumerate(patrulleras_asignadas) 
                                 if val > 1])
            patrulleras_asignadas[idx] -= 1

    # Penalización por capacidad excedida sin asignar patrullera extra
    for idx, incidentes in enumerate(incidentes_manejados_por_comisaria):
        capacidad_actual = patrulleras_asignadas[idx] * incidentes_por_patrullera
        if incidentes > capacidad_actual:
            exceso_incidentes = incidentes - capacidad_actual
            total_penalty += exceso_incidentes * (1000 + 390 * exceso_incidentes)

    # Penalización por uso ineficiente de patrulleras
    for idx, num_patrullas in enumerate(patrulleras_asignadas):
        if num_patrullas > 0:
            capacidad_necesaria = (incidentes_manejados_por_comisaria[idx] + 
                                   incidentes_por_patrullera - 1) // incidentes_por_patrullera
            if num_patrullas > capacidad_necesaria:
                exceso_patrulleras = num_patrullas - capacidad_necesaria
                total_penalty += exceso_patrulleras * (390 + 50 * exceso_patrulleras)

    # Penalización por incidentes no cubiertos
    total_incidentes_cubiertos = sum(incidentes_manejados_por_comisaria)
    incidentes_no_cubiertos = len(crime_data) - total_incidentes_cubiertos
    if incidentes_no_cubiertos > 0:
        total_penalty += incidentes_no_cubiertos * (3900 + 500 * incidentes_no_cubiertos)

    # Recompensa por uso eficiente de las patrulleras
    for idx, incidentes in enumerate(incidentes_manejados_por_comisaria):
        if incidentes == patrulleras_asignadas[idx] * incidentes_por_patrullera:
            total_penalty -= 500 + 100 * incidentes

    # Recompensa por cubrir todos los incidentes con menos patrulleras
    if total_incidentes_cubiertos == len(crime_data):
        total_penalty -= 1000 * (len(crime_data) - total_patrullas_asignadas)

    # Penalización por patrulleras sin uso
    for idx, num_patrullas in enumerate(patrulleras_asignadas):
        if incidentes_manejados_por_comisaria[idx] == 0 and num_patrullas > 0:
            total_penalty += 3900

    # Calcular el valor de fitness (determinista, sin ruido aleatorio)
    fitness_value = total_response_time + total_penalty

    return fitness_value,






