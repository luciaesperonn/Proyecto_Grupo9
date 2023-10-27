# Regresion Lineal Simple
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def cargar_datos(archivo):
    if archivo.endswith('.csv'):
        datos = pd.read_csv(archivo)
    elif archivo.endswith('.xlsx'):
        datos = pd.read_excel(archivo)
    else:
        raise ValueError("Formato de archivo no compatible")

    return datos

def verificar_columnas_numericas(datos, columnas):
    for col in columnas:
        if not pd.api.types.is_numeric_dtype(datos[col]):
            raise ValueError(f"La columna '{col}' no es numérica.")
        
archivo = 'housing.csv'  
dataset = cargar_datos(archivo)

# Función para crear y entrenar un modelo de HistGradientBoostingRegressor
def entrenar_modelo(columna_x, columna_y):
    x = dataset[[columna_x]].values  # Usar las variables 'columna_x' y 'columna_y' en lugar de cadenas
    y = dataset[[columna_y]].values  

    modelo = LinearRegression()
    modelo.fit(x, y)

    return modelo

columna_x = 'NombreDeTuColumnaX','NombreOtraColumna'  
columna_y = 'median_house_value' 


regressor = entrenar_modelo(columna_x, columna_y)

y_pred = regressor.predict(x_test)


plt.scatter(x_test[:, 0], y_test, color='red')
plt.plot(x_test[:, 0], y_pred, color='blue')
plt.title(f'{columna_y} vs. {columna_x} (Conjunto de prueba)')
plt.xlabel(columna_x)
plt.ylabel(columna_y)
plt.show()

