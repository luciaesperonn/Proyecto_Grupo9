import unittest
import os
import joblib
from clase_modelo import ModeloInfo


class TestGuardarModelo(unittest.TestCase):

    def setUp(self):
        # Crea una instancia de ModeloInfo con valores ficticios para la prueba
        self.modelo = ModeloInfo(
            x=0.5,
            y=1.0,
            modelo="Regresión Lineal",
            intercepto=0.2,
            coeficiente=0.3,
            ecuacion_recta="y = 0.3x + 0.2",
            mse=0.05,
            descripcion="Esta es una descripción de prueba"
        )

    def tearDown(self):
        # Elimina el archivo después de la prueba si existe
        if os.path.exists("test_modelo.pkl"):
            os.remove("test_modelo.pkl")

    def test_guardar_modelo(self):
        # Define la ruta del archivo de prueba
        file_path = "test_modelo.pkl"

        # Llama al método guardar_modelo
        self.modelo.guardar_modelo(file_path)

        # Verifica si el archivo se ha creado
        self.assertTrue(os.path.exists(file_path),
                        "El archivo no se creó correctamente")

        # Verifica si el archivo no está vacío
        self.assertGreater(os.path.getsize(file_path),
                           0, "El archivo está vacío")

        # Carga el modelo desde el archivo
        modelo_cargado = joblib.load(file_path)

        # Verifica si la descripción cargada coincide con la descripción original
        self.assertEqual(self.modelo.descripcion, modelo_cargado.descripcion,
                         "La descripción cargada no coincide")
        self.assertEqual(self.modelo.variable_x,
                         modelo_cargado.variable_x, "El valor de x no coincide")
        self.assertEqual(self.modelo.variable_y,
                         modelo_cargado.variable_y, "El valor de y no coincide")
        self.assertEqual(self.modelo.modelo,
                         modelo_cargado.modelo, "El modelo no coincide")
        self.assertEqual(self.modelo.intercepto,
                         modelo_cargado.intercepto, "El intercepto no coincide")
        self.assertEqual(self.modelo.coeficiente,
                         modelo_cargado.coeficiente, "El coeficiente no coincide")
        self.assertEqual(self.modelo.ecuacion_recta,
                         modelo_cargado.ecuacion_recta, "La ecuación de la recta no coincide")
        self.assertEqual(self.modelo.mse, modelo_cargado.mse,
                         "El MSE no coincide")


class TestCargarModelo(unittest.TestCase):

    def setUp(self):
        # Crear una instancia de ModeloInfo con valores ficticios para la prueba
        self.modelo = ModeloInfo(
            x=0.5,
            y=1.0,
            modelo="RegresionLineal",
            intercepto=0.2,
            coeficiente=0.3,
            ecuacion_recta="y = 0.3x + 0.2",
            mse=0.05,
            descripcion="Esta es una descripción de prueba"
        )

    def tearDown(self):
        # Elimina el archivo después de la prueba si existe
        if os.path.exists("test_modelo.pkl"):
            os.remove("test_modelo.pkl")

    def test_cargar_modelo(self):
        # Guarda el modelo primero para luego cargarlo
        file_path = "test_modelo.pkl"
        self.modelo.guardar_modelo(file_path)

        # Asegúrate de que el archivo exista antes de cargarlo
        self.assertTrue(os.path.exists(file_path),
                        "El archivo no se creó correctamente")

        # Llama al método cargar_modelo para cargar el modelo
        self.modelo.cargar_modelo(file_path)

        # Verifica si los atributos cargados coinciden con los originales
        self.assertEqual(self.modelo.variable_x, 0.5)
        self.assertEqual(self.modelo.variable_y, 1.0)
        self.assertEqual(self.modelo.modelo, "RegresionLineal")
        self.assertEqual(self.modelo.intercepto, 0.2)
        self.assertEqual(self.modelo.coeficiente, 0.3)
        self.assertEqual(self.modelo.ecuacion_recta, "y = 0.3x + 0.2")
        self.assertEqual(self.modelo.mse, 0.05)
        self.assertEqual(self.modelo.descripcion,
                         "Esta es una descripción de prueba")

        # Además, verifica el tipo de datos de algunos atributos
        self.assertIsInstance(self.modelo.variable_x, float)
        self.assertIsInstance(self.modelo.variable_y, float)
        self.assertIsInstance(self.modelo.intercepto, float)
        self.assertIsInstance(self.modelo.coeficiente, float)
        self.assertIsInstance(self.modelo.ecuacion_recta, str)
        self.assertIsInstance(self.modelo.mse, float)
        self.assertIsInstance(self.modelo.descripcion, str)


if __name__ == '__main__':
    unittest.main()
