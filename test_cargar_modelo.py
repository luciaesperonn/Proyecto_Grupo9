import unittest
import tempfile
import os
import shutil
from unittest.mock import patch, mock_open
from interfaz import cargar_modelo, show_error, introducir_valor_x, limpiar_interfaz, mostrar_info_modelo

class TestCargarModelo(unittest.TestCase):

    def setUp(self):
        # Crear un directorio temporal
        self.temp_dir = tempfile.mkdtemp()

        # Crear un archivo temporal
        _, self.temp_file_path = tempfile.mkstemp(suffix=".joblib", dir=self.temp_dir)

    def tearDown(self):
        def cleanup():
            try:
                os.unlink(self.temp_file_path)
            except Exception as e:
                print(f"Error al eliminar el archivo: {str(e)}")

            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                print(f"Error al eliminar el directorio temporal: {str(e)}")

        self.addCleanup(cleanup)

    @patch("interfaz.filedialog.askopenfilename", return_value="/ruta/del/archivo.joblib")
    @patch("interfaz.joblib.load", return_value="Información del modelo cargado")
    @patch("interfaz.mostrar_info_modelo")
    @patch("interfaz.limpiar_interfaz")
    @patch("interfaz.introducir_valor_x")
    def test_cargar_modelo_exitoso(
            self, mock_introducir_valor_x, mock_limpiar_interfaz, mock_mostrar_info_modelo,
            mock_joblib_load, mock_askopenfilename):

        # Llamar a la función que estás probando
        cargar_modelo()

        mock_askopenfilename.assert_called_once()
        mock_joblib_load.assert_called_once_with("/ruta/del/archivo.joblib")
        mock_mostrar_info_modelo.assert_called_once_with("/ruta/del/archivo.joblib", "Información del modelo cargado")
        mock_limpiar_interfaz.assert_called_once()
        mock_introducir_valor_x.assert_called_once()

    @patch("interfaz.filedialog.askopenfilename", return_value="/ruta/del/archivo_fallido.joblib")
    @patch("interfaz.joblib.load", side_effect=Exception("Error al cargar el modelo"))
    @patch("interfaz.show_error")
    def test_cargar_modelo_fallido(self, mock_show_error, mock_joblib_load, mock_askopenfilename):
        # Llamar a la función que estás probando
        cargar_modelo()

        # Aquí puedes realizar tus aserciones o verificar que las funciones mock hayan sido llamadas correctamente

if __name__ == '__main__':
    unittest.main()
