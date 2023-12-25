import pandas as pd
import sqlite3

def cargar_archivo_csv(archivo):
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
