# Proyecto de Tesis - Optimización de Patrullaje con Algoritmos Genéticos

Este proyecto es parte de una tesis que utiliza algoritmos genéticos para optimizar la distribución de patrulleras en Ciudad del Este. Este repositorio contiene el código fuente y la configuración necesaria para ejecutar el proyecto, incluyendo la base de datos y el archivo `database.py` para conectarse a ella.

## Requisitos

- Python 3.x
- MySQL (o MariaDB)
- Librerías de Python

## Configuración de la Base de Datos

1. **Instala MySQL o MariaDB** en tu computadora. Puedes descargar MySQL desde [aquí](https://dev.mysql.com/downloads/) o MariaDB desde [aquí](https://mariadb.org/download/).

2. **Crea la base de datos**. Abre tu terminal o línea de comandos y accede a MySQL:

    ```bash
    mysql -u root -p
    ```

   Luego, crea la base de datos:

    ```sql
    CREATE DATABASE tesis;
    ```

3. **Importa las tablas y datos**. Si tienes un archivo `tesis.sql` con las tablas y datos necesarios, puedes importarlo usando:

    ```bash
    mysql -u root -p tesis < /ruta/al/archivo.sql
    ```

   Asegúrate de ajustar la ruta al archivo `tesis.sql` que contiene los datos de tu proyecto.

## Configuración del Archivo de Conexión (`database.py`)

En el archivo `database.py`, se configura la conexión con la base de datos. Este archivo contiene una función `connect_to_db()` que establece la conexión a la base de datos `tesis`.

El código en `database.py` se ve así:

```python
import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tesis"
    )


Configuración de Parámetros

Es posible que necesites ajustar algunos parámetros en database.py para conectarte a tu base de datos de MySQL:

    host: Deja "localhost" si la base de datos está en tu propia máquina. Cambia esto a una dirección IP o nombre de host si la base de datos está en un servidor remoto.
    user: Reemplaza "root" con el nombre de usuario de MySQL que tengas configurado.
    password: Introduce aquí la contraseña de tu usuario de MySQL.
    database: Asegúrate de que el nombre de la base de datos (tesis) coincida con el nombre que creaste.

Ejemplo de configuración:

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="tu_usuario",
        password="tu_contraseña",
        database="tesis"
    )

Instalación de Dependencias

Las siguientes librerías son necesarias para ejecutar el proyecto. Puedes instalarlas usando pip:

pip install -r requirements.txt

Aquí tienes un ejemplo del archivo requirements.txt con las librerías necesarias:

numpy
deap
multiprocessing
functools
folium
mysql-connector-python
pandas
matplotlib

Ejecución del Proyecto

    Asegúrate de que el servidor de MySQL esté corriendo.
    Configura la base de datos como se indicó en las instrucciones anteriores.
    Ejecuta el archivo principal main.py para iniciar el proceso de optimización.

python main.py

Estructura del Proyecto

    main.py: Archivo principal que ejecuta la optimización de patrullaje.
    bd.py: Configuración de conexión a la base de datos.
    genetic_operations.py: Funciones de inicialización, mutación y cruce para el algoritmo genético.
    evaluation.py: Función de evaluación de fitness para el algoritmo genético.
    evaluation_deterministic.py: Función de evaluación determinista.
    preprocesamiento.py: Preprocesamiento de los datos de incidentes y comisarías.
    generate_map.py: Generación de mapas para visualización de la distribución de patrulleras.
    visualization.py: Funciones para visualizar y comparar tiempos de respuesta.
