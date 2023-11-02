import pandas as pd
import sqlite3

def mostrar_archivos(archivo, base_datos=None, tabla=None):
    try:
        if archivo.endswith('.csv'):
            df = pd.read_csv(archivo)
            print(df)
        elif archivo.endswith('.xlsx'):
            df = pd.read_excel(archivo)
            print(df)
        elif archivo.endswith('.db'):
            if not base_datos or not tabla:
                raise ValueError("Debes proporcionar el nombre de la base de datos y la tabla para cargar los datos.")
            
            # Conectarse a la base de datos SQLite
            conn = sqlite3.connect(base_datos)
            
            # Construir una consulta SQL para seleccionar todos los datos de la tabla
            consulta = f"SELECT * FROM {tabla}"
            
            # Leer todos los datos de la tabla en un DataFrame de pandas
            df = pd.read_sql_query(consulta, conn)
                        
            # Cerrar la conexión a la base de datos
            conn.close()
        else:
            raise ValueError("Formato de archivo no compatible")
        return datos
    except Exception as e:
        print(f"Se produjo un error al cargar el archivo: {str(e)}")
        return df
    
