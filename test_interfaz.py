import unittest
import pandas as pd
import tkinter as tk
from matplotlib.figure import Figure
from interfaz import get_first_row, integrar_figura_en_canvas

class TestGetFirstRow(unittest.TestCase):

    def test_get_first_row_valid_file(self):
        # Crear un DataFrame de prueba
        data = {'Columna1': [1, 2, 3], 'Columna2': ['A', 'B', 'C']}
        df = pd.DataFrame(data)

        # Guardar el DataFrame en un archivo CSV temporal
        file_path = 'temp_file.csv'
        df.to_csv(file_path, index=False)

        # Llamar a la función que se está probando
        first_row = get_first_row(file_path)

        # Verificar que la primera fila sea la correcta
        expected_first_row = pd.Series({'Columna1': 1, 'Columna2': 'A'})
        self.assertTrue(first_row.equals(expected_first_row))

        # Eliminar el archivo temporal después de la prueba
        import os
        os.remove(file_path)

class TestIntegrarFiguraEnCanvas(unittest.TestCase):

    def test_integrar_figura_en_canvas(self):
        # Crear una figura de ejemplo
        figura = Figure(figsize=(5, 4), dpi=100)
        ax = figura.add_subplot(111)
        ax.plot([1, 2, 3, 4], [2, 3, 5, 10])

        # Crear una ventana de tkinter
        ventana = tk.Tk()

        # Llamar a la función que se está probando
        integrar_figura_en_canvas(figura, ventana)

        # Mostrar la ventana (importante para que los widgets se coloquen correctamente)
        ventana.update_idletasks()

        # Verificar que la ventana se actualiza correctamente
        self.assertTrue(ventana.winfo_ismapped())


if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
