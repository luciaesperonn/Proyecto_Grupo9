import pandas as pd
import sqlite3

def cargar_archivo_csv(archivo):
    """
    Carga un archivo CSV y devuelve un DataFrame de pandas.

    Parámetros:
    - archivo (str): Ruta del archivo CSV.

    Return:
    - pd.DataFrame: DataFrame con los datos del archivo CSV.

    Lanza:
    - FileNotFoundError: Si el archivo no se encuentra.
    - ValueError: Si el archivo CSV está vacío o hay un error al leerlo.
    """    
    try:
        df = pd.read_csv(archivo)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {archivo}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"El archivo CSV está vacío: {archivo}")
    except pd.errors.ParserError:
        raise ValueError(f"Error al leer el archivo CSV: {archivo}")

def cargar_archivo_excel(archivo):
    """
    Carga un archivo Excel y devuelve un DataFrame de pandas.

    Parámetros:
    - archivo (str): Ruta del archivo Excel.

    Devuelve:
    - pd.DataFrame: DataFrame con los datos del archivo Excel.

    Lanza:
    - FileNotFoundError: Si el archivo no se encuentra.
    - ValueError: Si el archivo Excel está vacío o hay un error al leerlo.
    """
    try:
        df = pd.read_excel(archivo)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {archivo}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"El archivo Excel está vacío: {archivo}")
    except pd.errors.ParserError:
        raise ValueError(f"Error al leer el archivo Excel: {archivo}")

def cargar_archivo_db(archivo):
    """
    Carga datos desde una base de datos SQLite y devuelve un DataFrame de pandas.

    Parámetros:
    - archivo (str): Ruta del archivo de base de datos SQLite.

    Devuelve:
    - pd.DataFrame: DataFrame con los datos de la tabla de la base de datos.

    Lanza:
    -ValueError: si la base de datos contiene más de una tabla o está vacía.
    -sqlite.Error: si se produce un error al leer la base de datos
    """
    try:
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
        return df
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error al leer la base de datos: {str(e)}")

def verificar_columnas_numericas(datos, columnas):
    """
    Verifica que las columnas especificadas en el DataFrame sean de tipo numérico.

    Parámetros:
    - datos (pd.DataFrame): DataFrame de pandas que contiene los datos.
    - columnas (list): Lista de nombres de columnas a verificar.

    Lanza:
    - ValueError: Si alguna columna no es numérica.
    """
    for col in columnas:
        if not pd.api.types.is_numeric_dtype(datos[col]):
            raise ValueError(f"La columna '{col}' no es numérica.")
