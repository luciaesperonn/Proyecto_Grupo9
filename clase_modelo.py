import joblib

class ModeloInfo:
    def __init__(self, x, y, ecuacion_recta, mse):
        self.x = x
        self.y = y
        self.ecuacion_recta = ecuacion_recta
        self.mse = mse

    def guardar_modelo(self, file_path):
        # Utilizar joblib.dump para guardar la instancia de la clase
        joblib.dump(self, file_path)

