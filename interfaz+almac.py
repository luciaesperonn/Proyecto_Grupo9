import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import sqlite3
from tkinter import *
from leer_archivos import mostrar_archivos
from regresion_lineal import crear_modelo_regresion_lineal, visualizar_modelo

# Variables globales
button_explore = None
button_back = None
button_examine = None

def browse_files():
    global archivo_seleccionado

    filename = filedialog.askopenfilename(initialdir="/", title="Examinar", filetypes=(("Text files", "*.txt*"), ("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("SQLite databases", "*.db"), ("all files", "*.*")))

    if filename:  # Verificar si se seleccionó un archivo
        archivo_seleccionado=filename
        label_file_explorer.configure(text="Archivo abierto:  ")
        
        # Habilitar el botón "Salir"
        button_exit.config(state=tk.NORMAL)
        
        df = mostrar_archivos(filename)
        show_data_popup(df)

        # Crear el botón "Examinar" después de abrir un archivo
        global button_examine
        button_examine = tk.Button(window, text="Examinar", command=lambda: toggle_examine(filename), height=1, width=16)
        button_examine.place(x=200, y=230)

        #Llamar a la función para crear los Radiobuttons
        radiobuttons_var1 = create_radiobuttons(window, var1, filename, 380, Seleccionar)
        radiobuttons_var2 = create_radiobuttons(window, var2, filename, 440, Seleccionar)


# Nueva función para alternar la visibilidad de la ruta del archivo
def toggle_examine(filename):
    label_file_explorer.configure(text=filename)
    global button_back
    button_back = tk.Button(window, text="Atrás", command=back_to_previous_state, height=1, width=6)
    button_back.place(x=300, y=230)

def back_to_previous_state():
    label_file_explorer.configure(text="Explorador de Archivos usando Tkinter")
    
    # Eliminar el botón "Examinar" y el botón "Atrás"
    button_examine.place_forget()
    button_back.place_forget()

    # Crear el botón "Buscar Archivos"
    global button_explore
    button_explore = tk.Button(window, text="Buscar Archivos", command=browse_files, height=1, width=16)
    button_explore.place(x=200, y=230)


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
   global archivo_seleccionado
   variable_x = var1.get()
   variable_y = var2.get()

   if variable_x != ' ' and variable_y != ' ' and archivo_seleccionado:
       try:
           modelo = crear_modelo_regresion_lineal(archivo_seleccionado, [variable_x], [variable_y])

           # Obtener los datos correspondientes a las variables seleccionadas
           datos_seleccionados = mostrar_archivos(archivo_seleccionado)
           datos_seleccionados = datos_seleccionados.dropna(subset=[variable_x, variable_y])
           X_seleccionado = datos_seleccionados[[variable_x]]
           y_seleccionado = datos_seleccionados[variable_y]

           visualizar_modelo(modelo, X_seleccionado, y_seleccionado, [variable_x])
       except Exception as e:
           show_error(f"Error al crear o visualizar el modelo: {str(e)}")

def create_radiobuttons(window,variable, filename, y_position, command_callback):
    radiobuttons = []
    #Obtener la primera fila del DataFrame
    primera_fila = get_first_row(filename)
    if primera_fila is not None:
        for i, (columna,value) in enumerate(primera_fila.items()):
            rad = Radiobutton(window, variable=variable, value=columna, text=i, command=command_callback)
            rad.pack(side=LEFT)
            rad.place(x=80+120*i, y=y_position)
            rad.config(bg="#d9ffdf")
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
label_file_explorer = tk.Label(window, text="Explorador de Archivos usando Tkinter", width=250, height=5, fg="black", bg="#d9ffdf")
button_explore = tk.Button(window, text="Buscar Archivos", command=browse_files, height=1, width=16)
button_exit = tk.Button(window, text="Salir", command=window.quit, height=1, width=6)

# Organizar elementos en la ventana
label_file_explorer.place(y=50)
button_explore.place(x=200, y=230)
button_exit.place(x=230, y=260)

#Mostrar la lista con las variables del archivo
listbox_resultado = tk.Listbox(window, selectmode=tk.SINGLE, height=1, width=250, bg="#dfe9f5")
listbox_resultado.place(y=300)

button_regression = tk.Button(window, text="Realizar Regresión Lineal", command=Seleccionar, height=1, width=20)
button_regression.place(x=180, y=470)

#Etiquetas
etiqueta_seleccionar = tk.Label(window, text="Selecciona una variable x y una variable y:")
etiqueta_seleccionar.place(y = 330)
etiqueta_seleccionar.config(bg="#d9ffdf")

etiqueta_variable_x = tk.Label(window, text="VARIABLE X:")
etiqueta_variable_x.place(y = 380)
etiqueta_variable_x.config(bg="#d9ffdf")

etiqueta_variable_y = tk.Label(window, text="VARIABLE Y:")
etiqueta_variable_y.place(y = 440)
etiqueta_variable_y.config(bg="#d9ffdf")

# Iniciar la aplicación
window.mainloop() 