import pandas as pd


def mostrar_archivos(archivo):
    try:
        if archivo.endswith('.csv'):
            df = pd.read_csv(archivo)
            print(df)
        elif archivo.endswith('.xlsx'):
            df = pd.read_excel(archivo)
            print(df)
        else:
            raise ValueError("Formato de archivo no compatible")
    except Exception as j:
        print(f"Se produjo un error al cargar el archivo CSV: {str(j)}")
    
print('hola') 

