import sqlite3
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
from sklearn.metrics import mean_squared_error
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from regresion_lineal import crear_modelo_regresion_lineal, visualizar_modelo

# VARIABLES GLOBALES
button_explore = None
selected_variable_x = None
selected_variable_y = None
label_coeficientes = None
label_intercepto = None
label_mse = None
label_r2 = None

def browse_files():
    global selected_variable_x, selected_variable_y

    filename = filedialog.askopenfilename(initialdir="/", title="Examinar", filetypes=(("Text files", "*.txt*"), ("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("SQLite databases", "*.db"), ("all files", "*.*")))

    if filename:  # Verificar si se seleccionó un archivo
        df = mostrar_archivos(filename)
        show_data_popup(df)

        radiobuttons_var1 = create_radiobuttons(window, var1, filename, 240, Seleccionar)
        radiobuttons_var2 = create_radiobuttons(window, var2, filename, 260, Seleccionar)
 
    



def show_data_popup(df):
    top = tk.Toplevel()
    top.title("Datos")
    text = tk.Text(top)
    text.insert(tk.INSERT, df.to_string())
    text.pack()

    show_first_row(df)

def show_first_row(df):
    primera_fila = df.iloc[0]
    listbox_resultado.delete(0, tk.END)  # Limpiar la lista antes de agregar elementos
    row_text = "                      ".join(f"{columna}" for columna, valor in primera_fila.items())
    listbox_resultado.insert(tk.END, row_text)  

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
def realizar_regresion_lineal(filename, variable_x, variable_y):
    global label_coeficientes, label_intercepto, label_mse, label_r2

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
        if label_coeficientes is None:
            label_coeficientes = tk.Label(window, text="")
            label_coeficientes.place(x=10, y=310)
        label_coeficientes.config(text=f"Pendiente (coeficiente): {modelo.coef_}")
        window.update()

        if label_intercepto is None:
            label_intercepto = tk.Label(window, text="")
            label_intercepto.place(x=10, y=330)
        label_intercepto.config(text=f"Intercepto: {modelo.intercept_}")
        window.update()

        if label_mse is None:
            label_mse = tk.Label(window, text="")
            label_mse.place(x=10, y=350)
        label_mse.config(text=f"Error cuadrático medio (MSE): {mean_squared_error(y, modelo.predict(X))}")
        window.update()

        if label_r2 is None:
            label_r2 = tk.Label(window, text="")
            label_r2.place(x=10, y=370)
        label_r2.config(text=f"Bondad de ajuste (R²): {r2_score(y, modelo.predict(X))}")
        window.update()
       
        # Integrar la figura en un Canvas de Tkinter
        graph_canvas = FigureCanvasTkAgg(fig, master=window)
        graph_canvas_widget = graph_canvas.get_tk_widget()
        graph_canvas_widget.place(x=500, y=350)

    except Exception as e:
        show_error(f"Error al realizar la regresión lineal: {str(e)}")
       
def create_radiobuttons(window,variable, filename, y_position, command_callback):
    radiobuttons = []
    #Obtener la primera fila del DataFrame
    primera_fila = get_first_row(filename)
    if primera_fila is not None:
        for i, (columna,value) in enumerate(primera_fila.items()):
            rad = Radiobutton(window, variable=variable, value=columna, text=i, command=command_callback)
            rad.pack(side=LEFT)
            rad.place(x=80+120*i, y=y_position)
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
label_file_explorer = tk.Label(window, text="", width=180, height=2, fg="black", bg="#d9ffdf")
button_explore = tk.Button(window, text="Buscar Archivos", command=browse_files, height=1, width=16)

# Organizar elementos en la ventana
label_file_explorer.place(x=100, y=50)
button_explore.place(x=1375, y=55)

#Mostrar la lista con las variables del archivo
listbox_resultado = tk.Listbox(window, selectmode=tk.SINGLE, height=1, width=250, bg="#dfe9f5")
listbox_resultado.place(y=200)

# Crear el botón "Realizar Regresión Lineal"
button_regresion = tk.Button(window, text="Realizar Regresión Lineal", height=1, width=20)
button_regresion["command"] = lambda: realizar_regresion_lineal(filename, selected_variable_x, selected_variable_y)
button_regresion.place(x=630, y=290)

#Etiquetas
etiqueta_seleccionar = tk.Label(window, text="RUTA")
etiqueta_seleccionar.place(x= 30, y = 60)
etiqueta_seleccionar.config(bg="#bcdbf3")

etiqueta_seleccionar = tk.Label(window, text="Selecciona una variable x y una variable y:")
etiqueta_seleccionar.place(y = 220)
etiqueta_seleccionar.config(bg="#bcdbf3")

etiqueta_variable_x = tk.Label(window, text="VARIABLE X:")
etiqueta_variable_x.place(y = 240)
etiqueta_variable_x.config(bg="#bcdbf3")

etiqueta_variable_y = tk.Label(window, text="VARIABLE Y:")
etiqueta_variable_y.place(y = 260)
etiqueta_variable_y.config(bg="#bcdbf3")

# Iniciar la aplicación
window.mainloop() 