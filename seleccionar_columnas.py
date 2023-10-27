import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor

# Función para cargar los datos desde un archivo CSV o Excel
def cargar_datos(archivo):
    if archivo.endswith('.csv'):
        datos = pd.read_csv(archivo)
    elif archivo.endswith('.xlsx'):
        datos = pd.read_excel(archivo)
    else:
        raise ValueError("Formato de archivo no compatible")

    return datos

# Función para crear y entrenar un modelo de HistGradientBoostingRegressor
def entrenar_modelo(datos, columnas_entradas, columna_salida):
    X = datos[columnas_entradas]
    y = datos[columna_salida]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = HistGradientBoostingRegressor()
    modelo.fit(X_train, y_train)

    return modelo, X_test, y_test

# Función para verificar si las columnas son numéricas
def verificar_columnas_numericas(datos, columnas):
    for col in columnas:
        if not pd.api.types.is_numeric_dtype(datos[col]):
            raise ValueError(f"La columna '{col}' no es numérica.")

# Nombre del archivo CSV o Excel
tipo_archivo = 2
if tipo_archivo == 1:
    archivo_datos = 'housing.csv'
elif tipo_archivo == 2:
    archivo_datos = 'housing.xlsx'

# Cargar los datos
datos = cargar_datos(archivo_datos)

# Columna que se utilizará como salida del modelo (elige la que corresponda)
columna_salida = 'median_house_value'

# Especificar manualmente las columnas de entrada
columnas_entradas = ['total_rooms', 'total_bedrooms']

# Verificar si las columnas de entrada son numéricas
verificar_columnas_numericas(datos, columnas_entradas)

# Entrenar el modelo
modelo, X_test, y_test = entrenar_modelo(datos, columnas_entradas, columna_salida)

# Realizar predicciones
predicciones = modelo.predict(X_test)

print(predicciones)


