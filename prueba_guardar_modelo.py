import joblib
from regresion_lineal import crear_modelo_regresion_lineal

modelo = crear_modelo_regresion_lineal('housing.csv', ['longitude'], ['latitude'])  # Ejemplo

# Guardar el modelo en un archivo
joblib.dump(modelo, 'modelo_guardado.joblib')

