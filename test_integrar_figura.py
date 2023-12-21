import unittest
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from interfaz import integrar_figura_en_canvas  # Reemplaza 'tu_modulo' con el nombre real de tu módulo

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
