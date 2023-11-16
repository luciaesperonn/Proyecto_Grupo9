import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from leer_archivos import mostrar_archivos


def verificar_columnas_numericas(datos, columnas):
    for col in columnas:
        if not pd.api.types.is_numeric_dtype(datos[col]):
            raise ValueError(f"La columna '{col}' no es numérica.")
        
def crear_modelo_regresion_lineal(archivo, columna_predictora, columna_objetivo):
    datos = mostrar_archivos(archivo)
    verificar_columnas_numericas(datos, [columna_predictora[0]] + [columna_objetivo[0]])

    # Eliminar filas con valores NaN en las columnas relevantes
    datos = datos.dropna(subset=columna_predictora + columna_objetivo)
    
    X = datos[columna_predictora]
    y = datos[columna_objetivo]

    modelo = LinearRegression()
    modelo.fit(X, y)

    y_pred = modelo.predict(X)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    print("Coeficientes del modelo:")
    print("Pendiente (coeficiente):", modelo.coef_)
    print("Intercepto:", modelo.intercept_)
    print("Error cuadrático medio (MSE):", mse)
    print("Bondad de ajuste (R²):", r2)

   # Mostrar la ecuación de la recta
    print("\nEcuación de la recta:")
    print(f"y = {modelo.intercept_} + {modelo.coef_[0]} * {columna_predictora[0]}")
    
    return modelo

def visualizar_modelo(modelo, X, y, columna_predictora):
    y_pred = modelo.predict(X)

    plt.figure(figsize=(8, 6))
    plt.scatter(X, y, color='lightblue', label='Datos reales')
    plt.plot(X, y_pred, color='purple', linewidth=2, label='Ajuste del modelo')
    
    # Convertir los coeficientes y el intercepto a tipos de datos numéricos
    intercepto = float(modelo.intercept_)
    coeficiente = float(modelo.coef_[0][0])

    # Agregar texto con la ecuación de la recta
    equation_text = f"Ecuación de la recta:\n y = {intercepto:.2f} + {coeficiente:.2f} * X"
    plt.text(X.min(), y.max(), equation_text, fontsize=10, verticalalignment='top')
    
    plt.xlabel('Variable Independiente')
    plt.ylabel('Variable Dependiente')
    plt.legend()
    plt.title('Modelo de Regresión Lineal')
    plt.show()






