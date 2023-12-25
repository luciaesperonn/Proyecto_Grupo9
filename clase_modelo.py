import joblib
 
class ModeloInfo:
    def __init__(self, x, y, intercepto, coeficiente, ecuacion_recta, mse, descripcion):
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
        self.variable_x = x
        self.variable_y = y
        self.intercepto = intercepto
        self.coeficiente = coeficiente
        self.ecuacion_recta = ecuacion_recta
        self.mse = mse
        self.descripcion = descripcion
 
    def guardar_modelo(self, file_path):
        """
        Guarda la instancia de la clase en un archivo utilizando joblib.
 
        Parámetros:
        - file_path (str): Ruta del archivo donde se guardará la instancia.
        """
        # Utilizar joblib.dump para guardar la instancia de la clase
        joblib.dump(self, file_path)
 
    def cargar_modelo(self, file_path):
        """
        Carga una instancia de la clase desde un archivo utilizando joblib.
 
        Parámetros:
        - file_path (str): Ruta del archivo desde donde se cargará la instancia.
        """
        # Utilizar joblib.load para cargar la instancia de la clase desde el archivo
        loaded_model = joblib.load(file_path)
 
        # Actualizar los atributos de la instancia actual con los cargados desde el archivo
        self.x = loaded_model.x
        self.y = loaded_model.y
        self.intercepto = loaded_model.intercepto
        self.coeficiente = loaded_model.coeficiente
        self.ecuacion_recta = loaded_model.ecuacion_recta
        self.mse = loaded_model.mse
        self.descripcion = loaded_model.descripcion