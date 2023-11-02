import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


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
        
def crear_modelo_regresion_lineal(archivo, columna_predictora, columna_objetivo):
    datos = cargar_datos(archivo)
    verificar_columnas_numericas(datos, [columna_predictora[0]] + [columna_objetivo[0]])

    X = datos[columna_predictora]
    y = datos[columna_objetivo]

    modelo = LinearRegression()
    modelo.fit(X, y)

    y_pred = modelo.predict(X)
    # Calcular el error cuadrático medio
    mse = mean_squared_error(y, y_pred)
    # Calcular el coeficiente de determinación (R²)
    r2 = r2_score(y, y_pred)
    
    print("Coeficientes del modelo:")
    print("Pendiente (coeficiente):", modelo.coef_)
    print("Intercepto:", modelo.intercept_)
    print("Error cuadrático medio (MSE):", mse)
    print("Coeficiente de determinación (R²):", r2)

    return modelo

def visualizar_modelo(modelo, X, y):
    y_pred = modelo.predict(X)

    plt.figure(figsize=(8, 6))
    plt.scatter(X, y, color='lightblue', label='Datos reales')
    plt.plot(X, y_pred, color='purple', linewidth=2, label='Ajuste del modelo')
    plt.xlabel('Variable Independiente')
    plt.ylabel('Variable Dependiente')
    plt.legend()
    plt.title('Modelo de Regresión Lineal')
    plt.show()

if __name__ == "__main__":
    archivo = input("Introduce el nombre del archivo de datos (csv o xlsx): ")
    columna_predictora = input("Introduce la columna predictora: ")
    columna_predictora = columna_predictora.split(',')  # Convierte la entrada en una lista
    columna_objetivo = input("Introduce la columna objetivo: ")
    columna_objetivo = columna_objetivo.split(',')  # Convierte la entrada en una lista

    datos = cargar_datos(archivo)
    modelo = crear_modelo_regresion_lineal(archivo, columna_predictora, columna_objetivo)

    X = datos[columna_predictora]
    y = datos[columna_objetivo]

    visualizar_modelo(modelo, X, y)




