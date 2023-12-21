import unittest
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from interfaz import crear_modelo_info
from clase_modelo import ModeloInfo

class TestCrearModeloInfo(unittest.TestCase):

    def setUp(self):
        # Crear un DataFrame de prueba
        data = {'VariableX': [1, 2, 3, 4, 5], 'VariableY': [2, 4, 5, 4, 5]}
        self.df = pd.DataFrame(data)

        # Crear un modelo de regresión lineal
        modelo = LinearRegression()
        modelo.fit(self.df[['VariableX']], self.df['VariableY'])

        # Guardar el modelo y datos relevantes
        self.modelo = modelo
        self.variable_x = 'VariableX'
        self.variable_y = 'VariableY'
        self.X = self.df[[self.variable_x]]
        self.y = self.df[self.variable_y]

    def test_crear_modelo_info(self):
        # Llamar a la función que se está probando
        modelo_info = crear_modelo_info(self.modelo, self.variable_x, self.variable_y, self.X, self.y)

        # Verificar que el resultado es una instancia de ModeloInfo
        self.assertIsInstance(modelo_info, ModeloInfo)

        # Verificar que los atributos de ModeloInfo son correctos
        self.assertEqual(modelo_info.variable_x, self.variable_x)
        self.assertEqual(modelo_info.variable_y, self.variable_y)
        self.assertEqual(modelo_info.intercept, float(self.modelo.intercept_))
        self.assertEqual(modelo_info.slope, float(self.modelo.coef_[0]))  # Ajustar según la forma real de los coeficientes
        self.assertIsInstance(modelo_info.ecuacion_recta, str)
        self.assertIsInstance(modelo_info.mse, float)

if __name__ == '__main__':
    unittest.main()
