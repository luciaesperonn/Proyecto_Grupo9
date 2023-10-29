import sqlite3
import pandas as pd

# Función para cargar y mostrar todos los datos de la tabla
def cargar_datos_sqlite(base_datos, tabla):
    # Conectarse a la base de datos SQLite
    conn = sqlite3.connect(base_datos)
    
    # Construir una consulta SQL para seleccionar todos los datos de la tabla
    consulta = f"SELECT * FROM {tabla}"
    
    # Leer todos los datos de la tabla en un DataFrame de pandas
    datos = pd.read_sql_query(consulta, conn)
    
    # Mostrar los datos en la consola
    print(datos)
    
    # Cerrar la conexión a la base de datos
    conn.close()

# Nombre de la base de datos SQLite
base_datos = 'housing.db'

# Nombre de la tabla en la base de datos
tabla = 'california_housing_dataset'

# Cargar y mostrar todos los datos de la tabla
cargar_datos_sqlite(base_datos, tabla)
