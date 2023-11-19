import joblib
from sklearn.linear_model import LinearRegression

class ModeloRegresionLineal:
    def __init__(self, modelo, variable_x, variable_y):
        self.modelo = modelo
        self.variable_x = variable_x
        self.variable_y = variable_y
        self.ecuacion_recta = f"y = {self.modelo.intercept_:.2f} + {self.modelo.coef_[0][0]:.2f} * {self.variable_x}"

    def guardar_modelo(self, mse, filename):
        try:
            # Guardar el modelo y los datos relevantes
            joblib.dump({'modelo': self.modelo, 'variable_x': self.variable_x, 'variable_y': self.variable_y, 'mse': mse}, filename)
            print(f"Modelo guardado exitosamente en: {filename}")
        except Exception as e:
            print(f"Error al guardar el modelo: {str(e)}")

def cargar_modelo(filename):
    try:
        # Cargar el modelo y los datos relevantes desde el archivo
        data = joblib.load(filename)
        modelo = ModeloRegresionLineal(data['modelo'], data['variable_x'], data['variable_y'])
        return modelo
    except Exception as e:
        print(f"Error al cargar el modelo: {str(e)}")
        return None
