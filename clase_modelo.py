import joblib
import json
import os

class ModeloInfo:
    def __init__(self, x, y, intercept, slope, ecuacion_recta, mse, descripcion):
        self.x = x
        self.y = y
        self.intercept = intercept
        self.slope = slope
        self.ecuacion_recta = ecuacion_recta
        self.mse = mse
        self.descripcion = descripcion

    def guardar_modelo(self, file_path):
        # Guardar la instancia de la clase utilizando joblib
        joblib.dump(self, file_path)
        
        # Guardar la descripción en un archivo JSON
        descripcion_file_path = file_path + ".json"
        with open(descripcion_file_path, 'w') as f:
            json.dump({"descripcion": self.descripcion}, f)

    @classmethod
    def cargar_modelo(cls, file_path):
        # Cargar la instancia de la clase utilizando joblib
        loaded_model = joblib.load(file_path)
        
        # Cargar la descripción desde el archivo JSON
        descripcion_file_path = file_path + ".json"
        with open(descripcion_file_path, 'r') as f:
            data = json.load(f)
            loaded_model.descripcion = data["descripcion"]

        return loaded_model

