import joblib

class ModeloInfo:
    def __init__(self, ecuacion_recta, mse):
        self.ecuacion_recta = ecuacion_recta
        self.mse = mse

    def guardar_modelo(self, file_path):
        # Utilizar joblib.dump para guardar la instancia de la clase
        joblib.dump(self, file_path)

