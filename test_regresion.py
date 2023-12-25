import unittest
import pandas as pd
import os
import tkinter as tk
from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
from file_operations import verificar_columnas_numericas
from regresionlineal import realizar_regresion, crear_radiobuttons

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

class TestCrearRadiobuttons(unittest.TestCase):

    def setUp(self):
        # Crear una ventana de Tkinter para las pruebas
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.options = ['Opción 1', 'Opción 2', 'Opción 3']
        self.variable = tk.StringVar()

    def tearDown(self):
        # Destruir la ventana de Tkinter después de cada prueba
        self.root.destroy()

    def test_crear_radiobuttons_crea_botones_correctamente(self):
        # Llamar a la función y obtener los botones de radio creados
        radiobuttons = crear_radiobuttons(self.frame, self.options, self.variable, 0, 0)
        
        # Verificar si se crearon la cantidad correcta de botones de radio
        self.assertEqual(len(radiobuttons), len(self.options))
        
        # Verificar si los textos de los botones coinciden con las opciones
        for i, radiobutton in enumerate(radiobuttons):
            self.assertEqual(radiobutton['text'], self.options[i])
            
        # Verificar si los botones están en el marco correcto
        for i, radiobutton in enumerate(radiobuttons):
            self.assertEqual(radiobutton.master, self.frame)
            
        # Verificar las posiciones de los botones en el marco
        # Aquí se asume que todos los botones se colocan en la misma fila (row=0) pero en diferentes columnas.
        for i, radiobutton in enumerate(radiobuttons):
            self.assertEqual(radiobutton.grid_info()['row'], 0)
            self.assertEqual(radiobutton.grid_info()['column'], i)