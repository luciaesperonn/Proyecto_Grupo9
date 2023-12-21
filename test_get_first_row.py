import unittest
import pandas as pd
from interfaz import get_first_row 

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

if __name__ == '__main__':
    unittest.main()
