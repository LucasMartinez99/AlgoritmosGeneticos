import numpy as np
import matplotlib.pyplot as plt

def plot_total_response_time_comparison(best_total_time, current_total_time):
    labels = ['Mejor Individuo', 'Distribución Actual']
    times = [best_total_time, current_total_time]

    plt.bar(labels, times, color=['blue', 'orange'])
    plt.ylabel('Tiempo de Respuesta Total (minutos)')
    plt.title('Comparación de Tiempo de Respuesta Total')

    # Añadir rango
    plt.yticks(np.arange(0, max(times) + 50, 50))

    # Calcular y mostrar la diferencia
    difference = current_total_time - best_total_time

    # Ajustar márgenes para que se vea la diferencia
    plt.subplots_adjust(bottom=0.2)  # Ajustar el margen inferior
    plt.figtext(0.5, 0.02, f'Diferencia en tiempo de respuesta: {difference:.2f} minutos', ha='center', fontsize=12)

    plt.tight_layout()
    plt.show()
    
def plot_response_time_by_comisaria(best_times, current_times, comisaria_ids):
    bar_width = 0.35
    index = np.arange(len(comisaria_ids))

    plt.bar(index, best_times, bar_width, label='Mejor Individuo', color='blue')
    plt.bar(index + bar_width, current_times, bar_width, label='Distribución Actual', color='orange')

    plt.xlabel('Dependencias')
    plt.ylabel('Tiempo de Respuesta Promedio (minutos)')
    plt.title('Comparación de Tiempo de Respuesta por Dependencias')

    plt.xticks(index + bar_width / 2, comisaria_ids)
    plt.legend()
    plt.tight_layout()
    plt.show()
