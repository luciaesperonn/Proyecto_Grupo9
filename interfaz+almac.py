 #Importación de librerías
import sqlite3
import joblib
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from matplotlib.figure import Figure
from sklearn.impute import SimpleImputer
from leer_archivos import mostrar_archivos
from clase_modelo import ModeloInfo
from sklearn.metrics import mean_squared_error
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from regresion_lineal import crear_modelo_regresion_lineal, visualizar_modelo

# Variables globales
button_explore = None
selected_variable_x = None
selected_variable_y = None
label_coeficientes = None
label_intercepto = None
label_mse = None
label_r2 = None
text_data_display = None
modelo_info = None

def browse_files():
    global selected_variable_x, selected_variable_y, filename

    filename = filedialog.askopenfilename(initialdir="/", title="Examinar", filetypes=(("Text files", "*.txt*"), 
                                                                                       ("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("SQLite databases", "*.db"), ("all files", "*.*")))

    if filename:  # Verificar si se seleccionó un archivo
        label_file_explorer.config(text=f"Archivo seleccionado: {filename}")
        
        df = mostrar_archivos(filename)
        show_data_popup(df)

        radiobuttons_var1 = create_radiobuttons(window, var1, filename, 300, Seleccionar)
        radiobuttons_var2 = create_radiobuttons(window, var2, filename, 320, Seleccionar)

     # Crear el botón "Realizar Regresión Lineal"
    button_regresion = tk.Button(window, text="Realizar Regresión Lineal", height=1, width=20)
    button_regresion["command"] = lambda: realizar_regresion_lineal(filename, selected_variable_x, selected_variable_y)
    button_regresion.place(x=600, y=360)

    
def show_data_popup(df):
    global text_data_display  # Para acceder al widget Text desde otras funciones
    text_data_display.delete(1.0, tk.END)  # Limpiar el contenido actual

    # Obtener información sobre los datos
    headers = df.columns
    max_column_widths = [max(len(str(header)), df[header].astype(str).apply(len).max()) for header in headers]
    
    # Agregar encabezados al Text
    header_text = " | ".join(f"{header:<{width}}" for header, width in zip(headers, max_column_widths)) + "\n"
    text_data_display.insert(tk.END, header_text)

    # Agregar separador de columnas
    separator_line = "-" * sum(max_column_widths + [len(headers) - 1]) + "\n"
    text_data_display.insert(tk.END, separator_line)

    # Agregar filas al Text
    for _, row in df.iterrows():
        row_text = " | ".join(f"{str(value)[:width].center(width)}" for value, width in zip(row, max_column_widths)) + "\n"
        text_data_display.insert(tk.END, row_text)

def show_first_row(df):
    primera_fila = df.iloc[0]
    row_text = "     ".join(f"{columna}" for columna, valor in primera_fila.items())

def show_error(message):
    top = tk.Toplevel()
    top.title("Error")
    text = tk.Text(top)
    text.insert(tk.INSERT, message)
    text.pack()

#Función para seleccionar las columnas de los datos que se usarán como entradas y salida del modelo
def Seleccionar():
    global selected_variable_x, selected_variable_y
    selected_variable_x = var1.get()
    selected_variable_y = var2.get()
    print(selected_variable_x)
    print(selected_variable_y)
    print()

    
 
# Nueva función para realizar la regresión lineal
modelo_regresion = None

def realizar_regresion_lineal(filename, variable_x, variable_y):
    global label_mse, button_guardar_modelo, modelo_info

    try:
        modelo = crear_modelo_regresion_lineal(filename, [variable_x], [variable_y])
        datos = mostrar_archivos(filename)

        # Imputar valores NaN
        imputer = SimpleImputer(strategy='mean')
        datos[[variable_x, variable_y]] = imputer.fit_transform(datos[[variable_x, variable_y]])

        X = datos[[variable_x]]
        y = datos[[variable_y]]
        fig = visualizar_modelo(modelo, X, y, [variable_x])

        # Crear o actualizar las etiquetas con los resultados
        if label_mse is None:
            label_mse = tk.Label(window, text="")
            label_mse.place(x=400, y=395)
        label_mse.config(text=f"El error cuadrático medio (MSE) es: {mean_squared_error(y, modelo.predict(X))} y la bondad de ajuste (R²) es: {r2_score(y, modelo.predict(X))}")
        window.update()

        # Integrar la figura en un Canvas de Tkinter
        graph_canvas = FigureCanvasTkAgg(fig, master=window)
        graph_canvas_widget = graph_canvas.get_tk_widget()
        graph_canvas_widget.place(x=380, y=420)

        # Crear una instancia de ModeloInfo
        ecuacion_recta = f"y = {float(modelo.intercept_)} + {float(modelo.coef_[0][0])} * {variable_x}"
        mse = mean_squared_error(y, modelo.predict(X))
        modelo_info = ModeloInfo(ecuacion_recta, mse)

        # Crear el botón "Realizar Regresión Lineal"
        button_guardar_modelo = tk.Button(window, text="Guardar Modelo", height=1, width=20, command=guardar_modelo)
        button_guardar_modelo.place(x=750, y=360)


    except Exception as e:
        show_error(f"Error al realizar la regresión lineal: {str(e)}")


def guardar_modelo():
    global modelo_info

    if modelo_info is None:
        show_error("Realiza la regresión lineal antes de intentar guardar el modelo.")
        return

    try:
        # Obtener la ruta y nombre de archivo seleccionados por el usuario
        file_path = filedialog.asksaveasfilename(defaultextension=".joblib", filetypes=[("Archivos joblib", "*.joblib")])

        if file_path:
            # Guardar la información del modelo en el archivo
            modelo_info.guardar_modelo(file_path)

            show_error(f"Modelo guardado en: {file_path}")

    except Exception as e:
        show_error(f"Error al guardar el modelo: {str(e)}")


       
def create_radiobuttons(window, variable, filename, y_position, command_callback):
    radiobuttons = []
    # Obtener la primera fila del DataFrame
    primera_fila = get_first_row(filename)
    texto = ["longitude", 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'median_house_value', 'ocean_proximity']
    if primera_fila is not None:
        for i, (columna, value) in enumerate(primera_fila.items()):
            if i < len(texto):  # Asegurarse de que hay elementos en la lista 'texto'
                rad = Radiobutton(window, variable=variable, value=columna, text=texto[i], command=command_callback, font=("Helvetica", 8))
                rad.pack(side=LEFT)
                rad.place(x=120 + 125 * i, y=y_position)
                rad.config(bg="#bcdbf3")
                radiobuttons.append(rad)
    else:
        print("Error al obtener la primera fila del archivo.")
    return radiobuttons

def get_first_row(filename):
    df = mostrar_archivos(filename)
    if df is not None:
        primera_fila = df.iloc[0]
        return primera_fila
    else:
        return None

# Crear la ventana raíz
window = tk.Tk()
window.title('EXPLORADOR DE ARCHIVOS')
window.geometry("500x500")
window.config(bg="#bcdbf3")

# Creación de los Radiobutton
var1 = StringVar()
var2 = StringVar()
# Establecer valores predeterminados
var1.set(' ')
var2.set(' ')

# Crear elementos de la interfaz gráfica
label_file_explorer = tk.Label(window, text="", width=150, height=2, fg="black", bg="#d9ffdf")
button_explore = tk.Button(window, text="Buscar Archivos", command=browse_files, height=1, width=16)

# Organizar elementos en la ventana
label_file_explorer.place(x=100, y=50)
button_explore.place(x=1175, y=55)

# Crear un widget Text para mostrar los datos
text_data_display = tk.Text(window, wrap=tk.NONE, height=9, width=158)
text_data_display.place(x=50, y=120)  

#Etiquetas
etiqueta_seleccionar = tk.Label(window, text="RUTA")
etiqueta_seleccionar.place(x= 30, y = 60)
etiqueta_seleccionar.config(bg="#bcdbf3")

etiqueta_seleccionar = tk.Label(window, text="Selecciona una variable x y una variable y:")
etiqueta_seleccionar.place(x=20, y = 280)
etiqueta_seleccionar.config(bg="#bcdbf3")

etiqueta_variable_x = tk.Label(window, text="VARIABLE X:")
etiqueta_variable_x.place(x=20, y = 300)
etiqueta_variable_x.config(bg="#bcdbf3")

etiqueta_variable_y = tk.Label(window, text="VARIABLE Y:")
etiqueta_variable_y.place(x=20, y = 320)
etiqueta_variable_y.config(bg="#bcdbf3")


# Iniciar la aplicación
window.mainloop() 