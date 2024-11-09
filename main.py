import numpy as np
from deap import base, creator, tools, algorithms
from deap.tools import Statistics, Logbook
import multiprocessing
from functools import partial
from database import load_data_from_db
from genetic_operations import initialize_individual, mutate, cxUniformKeepSum
from evaluation import evaluate
from preprocesamiento import preprocess_incident_comisaria_map
from generate_map import generate_map
import folium
from evaluation_deterministic import evaluate_deterministic
from visualization import plot_total_response_time_comparison, plot_response_time_by_comisaria

def format_fitness_values(value):
    """Convertir valores a string sin notación científica."""
    return f"{value:.0f}"

def main():
    global MES_SELECCIONADO, PERIODO_SELECCIONADO

    MES_SELECCIONADO = None 
    PERIODO_SELECCIONADO = None

    crime_data, comisarias_data = load_data_from_db()
    incident_comisaria_map = preprocess_incident_comisaria_map()

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("individual", initialize_individual, creator.Individual, 
        crime_data=crime_data,
        comisarias_data=comisarias_data)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", cxUniformKeepSum)
    toolbox.register("mutate", mutate)
    toolbox.register("select", tools.selRoulette)
    toolbox.register("evaluate", partial(evaluate, crime_data=crime_data, 
        comisarias_data=comisarias_data, 
        incident_comisaria_map=incident_comisaria_map, 
        max_time=15, mes_seleccionado=MES_SELECCIONADO, 
        periodo_seleccionado=PERIODO_SELECCIONADO))

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

    population = toolbox.population(n=1000)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda x: format_fitness_values(np.mean(x)))
    stats.register("std", lambda x: format_fitness_values(np.std(x)))
    stats.register("min", lambda x: format_fitness_values(np.min(x)))
    stats.register("max", lambda x: format_fitness_values(np.max(x)))

    logbook = Logbook()
    logbook.header = ["gen", "nevals"] + stats.fields

    hof = tools.HallOfFame(10)

    # Definir variables para el mejor individuo global
    best_global_individual = None
    best_global_fitness = float('inf')  # Inicialmente un valor muy alto

    # Correr el algoritmo genético con MuPlusLambda para mayor diversidad
    for gen in range(40):  # Suponiendo 40 generaciones
        population, log = algorithms.eaMuPlusLambda(
            population, toolbox, mu=1000, lambda_=1500, cxpb=0.7, mutpb=0.3, ngen=1, 
            stats=stats, halloffame=hof, verbose=False  # No imprimir cada generación
        )
        
        # Imprimir el progreso de la generación actual
        record = stats.compile(population)
        logbook.record(gen=gen, nevals=len(population), **record)
        print(logbook.stream)  # Esto imprime cada generación

        # Obtener el mejor individuo de la generación actual
        best_individual_gen = tools.selBest(population, k=1)[0]
        fitness_best_gen = best_individual_gen.fitness.values[0]
        
        # Comparar si este individuo es mejor que el mejor global hasta ahora
        if fitness_best_gen < best_global_fitness:
            best_global_individual = best_individual_gen
            best_global_fitness = fitness_best_gen

    # Mostrar el mejor individuo global al final de todas las generaciones
    print(f"\nFitness global mínimo: {best_global_fitness}")
    print(f"Mejor individuo global: {best_global_individual}")

    total_patrulleras = sum(best_global_individual)
    print(f"Total de patrulleras: {total_patrulleras}")
    
    # Obtener el individuo que representa la distribución actual
    current_allocation = comisarias_data['patrullas'].tolist()
    
    # Crear el individuo actual
    current_individual = creator.Individual(current_allocation)
    
    print(f"Solución actual: {current_individual}")
    
    # Evaluar el individuo actual de manera determinista
    current_fitness_deterministic = evaluate_deterministic(current_individual, 
        crime_data, comisarias_data, 
        incident_comisaria_map, 
        mes_seleccionado=MES_SELECCIONADO, 
        periodo_seleccionado=PERIODO_SELECCIONADO)

    print(f"Fitness determinista de la distribución actual: {current_fitness_deterministic[0]:,.2f}")

    
    # Comparación final
    if best_global_fitness < current_fitness_deterministic[0]:
        print("La solución optimizada es mejor que la distribución actual.")
    else:
        print("La distribución actual es mejor o igual que la solución optimizada.")

    # Obtener tiempos de respuesta para la distribución actual y el mejor individuo
    current_total_time, current_times_per_comisaria =generate_map(current_individual, 
        crime_data, comisarias_data, 
        incident_comisaria_map, 
        mes_seleccionado=MES_SELECCIONADO, 
        periodo_seleccionado=PERIODO_SELECCIONADO)
    best_total_time, best_times_per_comisaria = generate_map(best_global_individual, 
        crime_data, comisarias_data, 
        incident_comisaria_map, 
        mes_seleccionado=MES_SELECCIONADO, 
        periodo_seleccionado=PERIODO_SELECCIONADO)

    # Graficar comparaciones
    plot_total_response_time_comparison(best_total_time, current_total_time)
    plot_response_time_by_comisaria(best_times_per_comisaria, current_times_per_comisaria, 
        comisarias_data['id'].tolist())

if __name__ == "__main__":
    main()