import pandas as pd
import sqlite3

def mostrar_archivos(archivo):
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
        print(f"Se produjo un error al cargar el archivo: {str(e)}")
        return None


print(mostrar_archivos('housing.db'))