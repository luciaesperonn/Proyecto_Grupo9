import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from csv_excel import mostrar_archivocsv, mostrar_archivoexcel

# Función para crear y entrenar un modelo de regresión lineal
def entrenar_modelo(datos, columnas_entradas, columna_salida):
    X = datos[columnas_entradas]
    y = datos[columna_salida]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    return modelo, X_test, y_test

# Nombre del archivo CSV o Excel
archivo_datos = 'housing.csv'

# Columnas que se utilizarán como entradas del modelo
columnas_entradas = ['total_rooms', 'total_bedrooms']

# Columna que se utilizará como salida del modelo
columna_salida = 'median_house_value'

# Cargar los datos
if archivo_datos.endswith('.csv'):
    datos = mostrar_archivocsv(archivo_datos)
elif archivo_datos.endswith('xlsx'):
    datos = mostrar_archivoexcel(archivo_datos)
else:
    raise ('ERROR. Archivo en formato no válido')

# Entrenar el modelo
modelo, X_test, y_test = entrenar_modelo(datos, columnas_entradas, columna_salida)

# Realizar predicciones
predicciones = modelo.predict(X_test)

