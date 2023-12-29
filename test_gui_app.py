import os
import unittest
import tempfile
import pandas as pd
import pandas as pd
import tkinter as tk
from tkinter import Tk
from unittest.mock import Mock
from tkinter import StringVar
from gui_app import RegresionLinealApp


class TestCargarDatos(unittest.TestCase):

    def setUp(self):
        # Crear archivos temporales para las pruebas
        self.csv_file = tempfile.NamedTemporaryFile(
            suffix=".csv", delete=False)
        self.xlsx_file = tempfile.NamedTemporaryFile(
            suffix=".xlsx", delete=False)
        self.db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)

        # Establecer los paths de los archivos temporales
        self.csv_path = self.csv_file.name
        self.xlsx_path = self.xlsx_file.name
        self.db_path = self.db_file.name

    def tearDown(self):
        # Cerrar y eliminar los archivos temporales después de cada prueba
        self.csv_file.close()
        self.xlsx_file.close()
        self.db_file.close()

        os.unlink(self.csv_file.name)
        os.unlink(self.xlsx_file.name)
        os.unlink(self.db_file.name)

    def test_cargar_datos_csv(self):
        root = tk.Tk()
        app = RegresionLinealApp(root)

        # Llamar a cargar_datos sin argumentos
        app.cargar_datos()

        # Aserciones para verificar que los datos se cargaron correctamente.
        self.assertIsNotNone(app.df)  # Verifica que el DataFrame no sea None
        # Verifica que el DataFrame sea del tipo correcto
        self.assertIsInstance(app.df, pd.DataFrame)

        # Verificar que el DataFrame tenga algún dato (por ejemplo, más de 0 filas)
        self.assertGreater(len(app.df), 0)

        # Verificar que las variables se muestren correctamente
        self.assertIsNotNone(app.radiobuttons_x)
        self.assertIsNotNone(app.radiobuttons_y)

    def test_cargar_datos_excel(self):
        root = tk.Tk()
        app = RegresionLinealApp(root)

        # Llamar a cargar_datos sin argumentos
        app.cargar_datos()

        # Aserciones para verificar que los datos se cargaron correctamente.
        self.assertIsNotNone(app.df)  # Verifica que el DataFrame no sea None
        # Verifica que el DataFrame sea del tipo correcto
        self.assertIsInstance(app.df, pd.DataFrame)

        # Verificar que el DataFrame tenga algún dato (por ejemplo, más de 0 filas)
        self.assertGreater(len(app.df), 0)

        # Verificar que las variables se muestren correctamente
        self.assertIsNotNone(app.radiobuttons_x)
        self.assertIsNotNone(app.radiobuttons_y)

    def test_cargar_datos_db(self):
        root = tk.Tk()
        app = RegresionLinealApp(root)

        # Llamar a cargar_datos sin argumentos
        app.cargar_datos()

        # Aserciones para verificar que los datos se cargaron correctamente.
        self.assertIsNotNone(app.df)  # Verifica que el DataFrame no sea None
        # Verifica que el DataFrame sea del tipo correcto
        self.assertIsInstance(app.df, pd.DataFrame)

        # Verificar que el DataFrame tenga algún dato (por ejemplo, más de 0 filas)
        self.assertGreater(len(app.df), 0)

        # Verificar que las variables se muestren correctamente
        self.assertIsNotNone(app.radiobuttons_x)
        self.assertIsNotNone(app.radiobuttons_y)


class TestMostrarVariables(unittest.TestCase):

    def setUp(self):
        # Creando un objeto maestro real
        self.master_real = Tk()

        # Creando una instancia de RegresionLinealApp con el maestro real
        self.instance = RegresionLinealApp(self.master_real)
        # Ejemplo de lista de variables
        self.variables = ["Variable1", "Variable2", "Variable3"]

    def test_mostrar_variables(self):
        # Antes de llamar a la función, verifica que no haya radio buttons inicialmente
        self.assertEqual(len(self.instance.radiobuttons_x), 0)
        self.assertEqual(len(self.instance.radiobuttons_y), 0)

        # Llama a la función con las variables
        self.instance.mostrar_variables(self.variables)

        # Verifica que los radio buttons se hayan creado
        self.assertNotEqual(len(self.instance.radiobuttons_x), 0)
        self.assertNotEqual(len(self.instance.radiobuttons_y), 0)

        radiobutton_texts_x = [rb["text"]
                               for rb in self.instance.radiobuttons_x]
        radiobutton_texts_y = [rb["text"]
                               for rb in self.instance.radiobuttons_y]

        # Verificar que los textos de los radio buttons coinciden con las variables
        self.assertListEqual(radiobutton_texts_x, self.variables)
        self.assertListEqual(radiobutton_texts_y, self.variables)

        # Verificar el valor inicial de las StringVar
        self.assertEqual(self.instance.variable_x.get(), " ")
        self.assertEqual(self.instance.variable_y.get(), " ")


class TestMostrarTabla(unittest.TestCase):

    def setUp(self):
        # Configuración inicial para las pruebas
        self.root = tk.Tk()
        # Instancia de la clase RegresionLinealApp
        self.app = RegresionLinealApp(self.root)

        # Crear un DataFrame de prueba
        data = {'Columna1': [1, 2, 3], 'Columna2': ['a', 'b', 'c']}
        self.df = pd.DataFrame(data)

    def tearDown(self):
        # Limpieza después de las pruebas
        self.root.destroy()

    def test_mostrar_tabla_creacion_correcta(self):
        # Llamar al método mostrar_tabla de la instancia de la clase RegresionLinealApp
        self.app.mostrar_tabla(self.df)

        # Asegurarse de que el Treeview tenga el mismo número de columnas que el DataFrame
        self.assertEqual(len(self.app.tabla["columns"]), len(self.df.columns))

        # Verificar si todos los widgets esperados se crean dentro de self.tabla_frame
        children_widgets = [widget.winfo_class()
                            for widget in self.app.tabla_frame.winfo_children()]
        expected_widgets = ['Scrollbar', 'Treeview']
        for widget in expected_widgets:
            self.assertIn(widget, children_widgets,
                          f"Se esperaba el widget {widget} dentro de self.tabla_frame")

        # Comprobar si las etiquetas se han creado correctamente dentro de self.frame_variables
        expected_labels = ["Seleccionar variables:",
                           "Variable x:", "Variable y:"]
        actual_labels = [label.cget("text") for label in self.app.frame_variables.winfo_children(
        ) if label.winfo_class() == "Label"]
        for label in expected_labels:
            self.assertIn(
                label, actual_labels, f"Se esperaba la etiqueta {label} en self.frame_variables")

        # Confirmar que el botón "Realizar regresión" se crea correctamente dentro de self.frame_variables
        button_texts = [button.cget("text") for button in self.app.frame_variables.winfo_children(
        ) if button.winfo_class() == "Button"]
        self.assertIn("Realizar regresión", button_texts,
                      "Se esperaba el botón 'Realizar regresión' en self.frame_variables")

        # Asumiendo que tienes un número específico de filas en el DataFrame de prueba, como 3 en este caso.
        num_rows_expected = len(self.df)

        # Contar el número de filas en el Treeview
        num_rows_actual = len(self.app.tabla.get_children())

        # Asegurarse de que el número de filas en el Treeview sea el esperado
        self.assertEqual(num_rows_actual, num_rows_expected,
                         f"Se esperaban {num_rows_expected} filas en el Treeview, pero se encontraron {num_rows_actual}")

        # Verificar que los valores en las filas del Treeview sean correctos
        for i, row in enumerate(self.df.itertuples(index=False)):
            values_expected = [str(getattr(row, col))
                               for col in self.df.columns]
            values_actual = list(self.app.tabla.item(
                self.app.tabla.get_children()[i], "values"))
            self.assertEqual(values_actual, values_expected,
                             f"Los valores en la fila {i+1} del Treeview no coinciden con los valores esperados")


class TestCrearRadiobuttons(unittest.TestCase):

    def setUp(self):
        # Crear una ventana de Tkinter para las pruebas
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.options = ['Opción 1', 'Opción 2', 'Opción 3']
        self.variable = tk.StringVar()

        # Instancia de la clase que contiene el método
        self.mi_clase_instance = RegresionLinealApp(master=self.root)

    def tearDown(self):
        # Destruir la ventana de Tkinter después de cada prueba
        self.root.destroy()

    def test_crear_radiobuttons_crea_botones_correctamente(self):
        # Llamar al método desde la instancia y obtener los botones de radio creados
        radiobuttons = self.mi_clase_instance.crear_radiobuttons(
            self.frame, self.options, self.variable, 0, 0)

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


if __name__ == '__main__':
    unittest.main()
