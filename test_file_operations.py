# Importar los módulos necesarios
import unittest
import tempfile
import os
import sqlite3
import pandas as pd
from file_operations import cargar_archivo_csv, cargar_archivo_excel, cargar_archivo_db, verificar_columnas_numericas

class TestLeerArchivos(unittest.TestCase):
    def setUp(self):
        # Crear archivos temporales para las pruebas
        self.csv_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
        self.xlsx_file = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        self.db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.txt_file = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)

    def tearDown(self):
        #Cerrar los archivos antes de eliminarlos
        self.csv_file.close()
        self.xlsx_file.close()
        self.db_file.close()
        self.txt_file.close()

        # Eliminar los archivos temporales después de cada prueba
        os.unlink(self.csv_file.name)
        os.unlink(self.xlsx_file.name)
        os.unlink(self.db_file.name)
        os.unlink(self.txt_file.name)

    def test_cargar_csv(self):
        # Crear contenido CSV para la prueba
        csv_content = "columna1,columna2\n1,2\n3,4\n"
        self.csv_file.write(csv_content.encode())
        self.csv_file.flush()

    # Probar cargar un archivo CSV
        df = cargar_archivo_csv(self.csv_file.name)
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (2, 2))

    def test_cargar_xlsx(self):
        # Crear contenido Excel para la prueba
        xlsx_content = {"columna1": [1, 3], "columna2": [2, 4]}
        df = pd.DataFrame(xlsx_content)
        df.to_excel(self.xlsx_file.name, index=False)

        # Probar cargar un archivo Excel
        df_loaded = cargar_archivo_excel(self.xlsx_file.name)
        pd.testing.assert_frame_equal(df, df_loaded)

    def test_cargar_db(self):
        # Crear contenido de base de datos para la prueba
        db_content = {"columna1": [1, 3], "columna2": [2, 4]}
        df = pd.DataFrame(db_content)
        conn = sqlite3.connect(self.db_file.name)
        df.to_sql("tabla_prueba", conn, index=False)
        conn.close()

        # Probar cargar un archivo de base de datos
        df_loaded = cargar_archivo_db(self.db_file.name)
        pd.testing.assert_frame_equal(df, df_loaded)

class TestVerificarColumnasNumericas(unittest.TestCase):

    def test_columnas_numericas(self):
        # Crear un DataFrame de ejemplo
        data = {
            'A': [1, 2, 3],
            'B': [1.1, 2.2, 3.3],
            'C': ['a', 'b', 'c']
        }
        df = pd.DataFrame(data)

        # Llamar a la función con columnas numéricas
        columnas_numericas = ['A', 'B']
        verificar_columnas_numericas(df, columnas_numericas)

        # Si la función no arroja un ValueError, entonces la prueba pasa
        self.assertTrue(True)

    def test_columnas_no_numericas(self):
        # Crear un DataFrame de ejemplo
        data = {
            'A': [1, 2, 3],
            'B': ['a', 'b', 'c'],
            'C': ['x', 'y', 'z']
        }
        df = pd.DataFrame(data)

        # Llamar a la función con columnas no numéricas
        columnas_no_numericas = ['A', 'B']
        
        with self.assertRaises(ValueError) as context:
            verificar_columnas_numericas(df, columnas_no_numericas)
        
        # Verificar el mensaje de error
        self.assertEqual(str(context.exception), "La columna 'B' no es numérica.")

    def test_columnas_inexistentes(self):
        # Crear un DataFrame de ejemplo
        data = {
            'A': [1, 2, 3],
            'B': [1.1, 2.2, 3.3],
            'C': ['a', 'b', 'c']
        }
        df = pd.DataFrame(data)

        # Llamar a la función con una columna inexistente
        columnas_inexistentes = ['A', 'D']
        
        with self.assertRaises(KeyError) as context:
            verificar_columnas_numericas(df, columnas_inexistentes)
        
        # Verificar el mensaje de error
        self.assertEqual(str(context.exception), "'D'")

if __name__ == "__main__":
    unittest.main()