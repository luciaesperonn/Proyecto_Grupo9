# Importar los módulos necesarios
import unittest
import tempfile
import os
import sqlite3
import pandas as pd
from leer_archivos import mostrar_archivos

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
        df = mostrar_archivos(self.csv_file.name)
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (2, 2))

    def test_cargar_xlsx(self):
        # Crear contenido Excel para la prueba
        xlsx_content = {"columna1": [1, 3], "columna2": [2, 4]}
        df = pd.DataFrame(xlsx_content)
        df.to_excel(self.xlsx_file.name, index=False)

        # Probar cargar un archivo Excel
        df_loaded = mostrar_archivos(self.xlsx_file.name)
        pd.testing.assert_frame_equal(df, df_loaded)

    def test_cargar_db(self):
        # Crear contenido de base de datos para la prueba
        db_content = {"columna1": [1, 3], "columna2": [2, 4]}
        df = pd.DataFrame(db_content)
        conn = sqlite3.connect(self.db_file.name)
        df.to_sql("tabla_prueba", conn, index=False)
        conn.close()

        # Probar cargar un archivo de base de datos
        df_loaded = mostrar_archivos(self.db_file.name)
        pd.testing.assert_frame_equal(df, df_loaded)

    def test_formato_no_compatible(self):
        with self.assertRaises(ValueError, msg="Formato de archivo no compatible"):
            mostrar_archivos("archivo.txt")


if __name__ == "__main__":
    unittest.main()

