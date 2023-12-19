import sqlite3
import pandas as pd

def mostrar_archivos(archivo):
    """
    Carga datos desde diferentes tipos de archivos y retorna un DataFrame de pandas.

    Parámetros:
    - archivo (str): Ruta del archivo a cargar.

    Devuelve:
    - pd.DataFrame: DataFrame que contiene los datos cargados desde el archivo.
    - None: Si hay un error al cargar el archivo.
    """
    try:
        if archivo.endswith('.csv'):
            df = pd.read_csv(archivo)
        elif archivo.endswith('.xlsx'):
            df = pd.read_excel(archivo)
        elif archivo.endswith('.db'):
            conn = sqlite3.connect(archivo)
            
            # Obtener la lista de tablas en la base de datos
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if len(tables) != 1:
                raise ValueError("La base de datos contiene más de una tabla o está vacía.")
            
            tabla = tables[0][0]
            consulta = f"SELECT * FROM {tabla}"
            
            df = pd.read_sql_query(consulta, conn)
            conn.close()
        else:
            raise ValueError("Formato de archivo no compatible")
        return df
    except Exception as e:
        # Cambia esta línea para lanzar la excepción en lugar de imprimir el mensaje
        raise ValueError(f"Se produjo un error al cargar el archivo: {str(e)}")
        return None