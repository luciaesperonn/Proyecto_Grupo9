import unittest
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
from regresion_lineal import verificar_columnas_numericas, crear_modelo_regresion_lineal, visualizar_modelo





class TestCrearModeloRegresionLineal(unittest.TestCase):

    def setUp(self):
        # Crear un DataFrame de prueba
        data = {'VariableX': [1, 2, 3, 4, 5], 'VariableY': [2, 4, 5, 4, 5]}
        self.df = pd.DataFrame(data)

        # Guardar el DataFrame en un archivo CSV temporal
        self.file_path = 'temp_file.csv'
        self.df.to_csv(self.file_path, index=False)

    def tearDown(self):
        # Eliminar el archivo temporal después de las pruebas
        os.remove(self.file_path)

    def test_crear_modelo_regresion_lineal(self):
        # Llamar a la función que se está probando
        modelo = crear_modelo_regresion_lineal('temp_file.csv', ['VariableX'], ['VariableY'])

        # Verificar que el modelo es una instancia de LinearRegression
        self.assertIsInstance(modelo, LinearRegression)

        # Verificar que el modelo se ha ajustado correctamente
        modelo.fit(self.df[['VariableX']], self.df['VariableY'])
        self.assertAlmostEqual(modelo.coef_[0], 0.6, places=2)  # Ajustar según el comportamiento esperado
        self.assertAlmostEqual(modelo.intercept_, 2.2, places=2)  # Ajustar según el comportamiento esperado

class TestVisualizarModelo(unittest.TestCase):

    def setUp(self):
        # Crear un DataFrame de prueba
        data = {'VariableX': [1, 2, 3, 4, 5], 'VariableY': [2, 4, 5, 4, 5]}
        self.df = pd.DataFrame(data)

        # Crear un modelo de regresión lineal
        modelo = LinearRegression()
        modelo.fit(self.df[['VariableX']], self.df['VariableY'])

        # Guardar el modelo y datos relevantes
        self.modelo = modelo
        self.X = self.df[['VariableX']]
        self.y = self.df['VariableY']
        self.etiqueta_x = 'VariableX'
        self.etiqueta_y = 'VariableY'

    def test_visualizar_modelo(self):
        # Llamar a la función que se está probando
        figura_generada = visualizar_modelo(self.modelo, self.X, self.y, self.etiqueta_x, self.etiqueta_y)

        # Verificar que la figura generada sea una instancia de matplotlib.figure.Figure
        self.assertIsInstance(figura_generada, Figure)

if __name__ == '__main__':
    unittest.main()
