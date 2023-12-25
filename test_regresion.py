import unittest
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
from file_operations import verificar_columnas_numericas
from regresionlineal import realizar_regresion

class TestVerificarColumnasNumericas(unittest.TestCase):

    def setUp(self):
        # Crear un DataFrame de prueba
        data = {'ColumnaNumerica': [1, 2, 3, 4, 5], 'OtraColumnaNumerica': [2.0, 4.5, 5.2, 4.8, 5.0]}
        self.df_numeric = pd.DataFrame(data)

        data_no_numeric = {'ColumnaNoNumerica': ['a', 'b', 'c', 'd', 'e']}
        self.df_no_numeric = pd.DataFrame(data_no_numeric)

    def test_verificar_columnas_numericas_con_columnas_numericas(self):
        # No debería lanzar una excepción para un DataFrame con columnas numéricas
        try:
            verificar_columnas_numericas(self.df_numeric, ['ColumnaNumerica', 'OtraColumnaNumerica'])  # Corregir aquí
        except ValueError:
            self.fail("verificar_columnas_numericas lanzó un ValueError de manera incorrecta.")

    def test_verificar_columnas_numericas_con_columnas_no_numericas(self):
        # Debería lanzar una excepción para un DataFrame con columnas no numéricas
        with self.assertRaises(ValueError):
            verificar_columnas_numericas(self.df_no_numeric, ['ColumnaNoNumerica'])
