import pandas as pd


def mostrar_archivocsv():
    ruta_csv = input('Añade la ruta de tu archivo CSV: ')
    df = pd.read_csv(ruta_csv)
    print(df.head(10))
mostrar_archivocsv()

def mostrar_archivoexcel():
    ruta_xlsx = input('Añade la ruta de tu archivo XLSX: ')
    df = pd.read_excel(ruta_xlsx)
    print(df.head(10))
mostrar_archivoexcel()

