import joblib
from regresion_lineal import crear_modelo_regresion_lineal
# Supongamos que 'model' es tu modelo entrenado
model = crear_modelo_regresion_lineal('housing.csv', ['longitude'], ['latitude'])  # Ejemplo, utiliza tu propio modelo

# Guardar el modelo en un archivo
joblib.dump(model, 'modelo_guardado.joblib')

