import pandas as pd
from clase_modelo import ModeloInfo
from matplotlib.figure import Figure
from leer_archivos import mostrar_archivos
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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

def crear_modelo_regresion_lineal(archivo, columna_predictora, columna_objetivo):
    """
    Crea un modelo de regresión lineal utilizando scikit-learn.

    Parámetros:
    - archivo (str): Ruta del archivo que contiene los datos.
    - columna_predictora (list): Lista con el nombre de la columna predictora.
    - columna_objetivo (list): Lista con el nombre de la columna objetivo.

    Devuelve:
    - sklearn.linear_model.LinearRegression: Modelo entrenado de regresión lineal.
    """
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
    print(f"Pendiente (coeficiente): {modelo.coef_[0][0]}")
    print(f"Intercepto: {modelo.intercept_}")
    print(f"Error cuadrático medio (MSE): {mse}")
    print(f"Bondad de ajuste (R²): {r2}")

    return modelo

def visualizar_modelo(modelo, X, y, etiqueta_x, etiqueta_y):
    """
    Visualiza un modelo de regresión lineal utilizando matplotlib.

    Parámetros:
    - modelo (sklearn.linear_model.LinearRegression): Modelo entrenado de regresión lineal.
    - X (pd.DataFrame): DataFrame de pandas con la variable predictora.
    - y (pd.Series): Serie de pandas con la variable objetivo.
    - etiqueta_x (str): Etiqueta para el eje X.
    - etiqueta_y (str): Etiqueta para el eje Y.

    Devuelve:
    - matplotlib.figure.Figure: Figura generada por matplotlib.
    """
    y_pred = modelo.predict(X)

    figure = Figure(figsize=(6, 4))
    ax = figure.add_subplot(111)
    ax.scatter(X, y, color='lightblue', label='Datos reales')
    ax.plot(X, y_pred, color='purple', linewidth=2, label='Ajuste del modelo')
   
    # Convertir los coeficientes y el intercepto a tipos de datos numéricos
    intercepto = float(modelo.intercept_)
    coeficiente = float(modelo.coef_[0][0])

    ax.set_xlabel(etiqueta_x)  # Utiliza la etiqueta de la variable X
    ax.set_ylabel(etiqueta_y)  # Utiliza la etiqueta de la variable Y
    ax.legend()
    ax.set_title('Modelo de Regresión Lineal')
    
    return figure