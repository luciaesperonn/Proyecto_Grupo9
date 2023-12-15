import joblib

class ModeloInfo:
    def __init__(self, x, y, intercept, slope, ecuacion_recta, mse):
        """
        Inicia una instancia de la clase ModeloInfo.

        Parámetros:
        - x: Valor de la variable predictora.
        - y: Valor de la variable objetivo.
        - intercept: Intercepto del modelo de regresión lineal.
        - slope: Pendiente del modelo de regresión lineal.
        - ecuacion_recta: Ecuación de la recta del modelo.
        - mse: Error cuadrático medio del modelo.
        """
        self.x = x
        self.y = y
        self.intercept = intercept
        self.slope = slope
        self.ecuacion_recta = ecuacion_recta
        self.mse = mse

    def guardar_modelo(self, file_path):
        """
        Guarda la instancia de la clase en un archivo utilizando joblib.

        Parámetros:
        - file_path (str): Ruta del archivo donde se guardará la instancia.
        """
        # Utilizar joblib.dump para guardar la instancia de la clase
        joblib.dump(self, file_path)