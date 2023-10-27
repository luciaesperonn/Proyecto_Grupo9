import pandas as pd


def mostrar_archivocsv():
    try:
        ruta_csv = input('Añade la ruta de tu archivo CSV: ')
        df = pd.read_csv(ruta_csv)
        print(df.head(10))
    except FileNotFoundError:
        print('El archivo CSV no se encuentra en la ruta elegida')
    except Exception as j:
        print(f"Se produjo un error al cargar el archivo CSV: {str(j)}")
mostrar_archivocsv()

def mostrar_archivoexcel():
    try:
        ruta_xlsx = input('Añade la ruta de tu archivo XLSX: ')
        df = pd.read_excel(ruta_xlsx)
        print(df.head(10))
    except FileNotFoundError:
        print('El archivo XLSX no se encuentra en la ruta elegida')
    except Exception as j:
        print(f"Se produjo un error al cargar el archivo XLSX: {str(j)}")

mostrar_archivoexcel() 



