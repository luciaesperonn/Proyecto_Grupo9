import unittest
import pandas as pd
import tkinter as tk
from gui_app import RegresionLinealApp

class TestMostrarTabla(unittest.TestCase):

    def setUp(self):
        # Configuración inicial para las pruebas
        self.root = tk.Tk()
        self.app = RegresionLinealApp(self.root)  # Instancia de la clase RegresionLinealApp

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
    children_widgets = [widget.winfo_class() for widget in self.app.tabla_frame.winfo_children()]
    expected_widgets = ['Scrollbar', 'Treeview']
    for widget in expected_widgets:
        self.assertIn(widget, children_widgets, f"Se esperaba el widget {widget} dentro de self.tabla_frame")

    # Comprobar si las etiquetas se han creado correctamente dentro de self.frame_variables
    expected_labels = ["Seleccionar variables:", "Variable x:", "Variable y:"]
    actual_labels = [label.cget("text") for label in self.app.frame_variables.winfo_children() if label.winfo_class() == "Label"]
    for label in expected_labels:
        self.assertIn(label, actual_labels, f"Se esperaba la etiqueta {label} en self.frame_variables")

    # Confirmar que el botón "Realizar regresión" se crea correctamente dentro de self.frame_variables
    button_texts = [button.cget("text") for button in self.app.frame_variables.winfo_children() if button.winfo_class() == "Button"]
    self.assertIn("Realizar regresión", button_texts, "Se esperaba el botón 'Realizar regresión' en self.frame_variables")

    # Asumiendo que tienes un número específico de filas en el DataFrame de prueba, como 3 en este caso.
    num_rows_expected = len(self.df)

    # Contar el número de filas en el Treeview
    num_rows_actual = len(self.app.tabla.get_children())
    
    # Asegurarse de que el número de filas en el Treeview sea el esperado
    self.assertEqual(num_rows_actual, num_rows_expected, 
                     f"Se esperaban {num_rows_expected} filas en el Treeview, pero se encontraron {num_rows_actual}")
    
    # Verificar que los valores en las filas del Treeview sean correctos
    for i, row in enumerate(self.df.itertuples(index=False)):
        values_expected = [str(getattr(row, col)) for col in self.df.columns]
        values_actual = self.app.tabla.item(self.app.tabla.get_children()[i], "values")
        self.assertEqual(values_actual, values_expected, 
                         f"Los valores en la fila {i+1} del Treeview no coinciden con los valores esperados")

if __name__ == '__main__':
    unittest.main()