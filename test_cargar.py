import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from gui_app import RegresionLinealApp

class TestCargarModelo(unittest.TestCase):
    def setUp(self):
        # Crear una instancia de la aplicación
        self.root = Tk()
        self.app = RegresionLinealApp(self.root)

    def tearDown(self):
        # Cierra la aplicación después de cada prueba
        self.root.destroy()

    @patch("tkinter.filedialog.askopenfilename", return_value="modelo.joblib")
    @patch("joblib.load", return_value=MagicMock(
        variable_x="x",
        variable_y="y",
        intercepto=1.0,
        coeficiente=2.0,
        ecuacion_recta="y = 2x + 1",
        mse=0.5,
        descripcion="Modelo de prueba"
    ))
    def test_cargar_modelo_exitoso(self, mock_load, mock_askopenfilename):
        # Simular la selección de un archivo para cargar
        self.app.cargar_modelo()

        # Verificar que la etiqueta de la ruta se actualiza
        self.assertEqual(self.app.etiqueta_ruta.cget("text"), "RUTA: modelo.joblib")

        # Verificar que se carga el modelo correctamente
        self.assertIsNotNone(self.app.modelo_cargado)
        self.assertEqual(self.app.modelo_cargado.variable_x, "x")
        self.assertEqual(self.app.modelo_cargado.variable_y, "y")
        self.assertEqual(self.app.modelo_cargado.intercepto, 1.0)
        self.assertEqual(self.app.modelo_cargado.coeficiente, 2.0)
        self.assertEqual(self.app.modelo_cargado.ecuacion_recta, "y = 2x + 1")
        self.assertEqual(self.app.modelo_cargado.mse, 0.5)
        self.assertEqual(self.app.modelo_cargado.descripcion, "Modelo de prueba")

if __name__ == '__main__':
    unittest.main()
