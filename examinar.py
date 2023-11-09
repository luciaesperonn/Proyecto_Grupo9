import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import sqlite3
from tkinter import *
from leer_archivos import mostrar_archivos

# Variable global para el botón "Atrás"
button_back = None

def browse_files():
    filename = filedialog.askopenfilename(initialdir="/", title="Examinar", filetypes=(("Text files", "*.txt*"), ("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("SQLite databases", "*.db"), ("all files", "*.*")))

    if filename:  # Verificar si se seleccionó un archivo
        label_file_explorer.configure(text="Archivo abierto: ")
        button_exit.config(state=tk.NORMAL)  # Habilitar el botón "Salir"

        df = mostrar_archivos(filename)
        show_data_popup(df)

        # Crear el botón "Examinar" después de abrir un archivo
        button_examine = tk.Button(window, text="Examinar", command=lambda: toggle_examine(filename), height=1, width=16)
        button_examine.place(x=200, y=230)

# Nueva función para alternar la visibilidad de la ruta del archivo
def toggle_examine(filename):
    label_file_explorer.configure(text=filename)
    global button_back
    button_back = tk.Button(window, text="Atrás", command=back_to_previous_state, height=1, width=6)
    button_back.place(x=300, y=230)

def back_to_previous_state():
    label_file_explorer.configure(text="Explorador de Archivos usando Tkinter")
    button_exit.config(state=tk.DISABLED)  # Deshabilitar el botón "Salir"
    
    # Eliminar el botón "Examinar" y el botón "Atrás"
    button_examine.place_forget()
    button_back.place_forget()

# Resto de tu código...




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

# Crear la ventana raíz
window = tk.Tk()
window.title('EXPLORADOR DE ARCHIVOS')
window.geometry("500x500")
window.config(bg="#d9ffdf")

# Crear elementos de la interfaz gráfica

label_file_explorer = tk.Label(window, text="Explorador de Archivos usando Tkinter", width=200, height=5, fg="black", bg="#87a1ab")
button_explore = tk.Button(window, text="Buscar Archivos", command=browse_files, height=1, width=16)
#button_examine = tk.Button(window, text="Examinar", command=browse_files, height=1, width=16)
button_exit = tk.Button(window, text="Salir", command=window.quit, height=1, width=6)

# Organizar elementos en la ventana
label_file_explorer.place(y=50)
button_explore.place(x=200, y=230)
button_exit.place(x=230, y=260)

#Mostrar la lista con las variables del archivo
listbox_resultado = tk.Listbox(window, selectmode=tk.SINGLE, height=1, width=250, bg="#dfe9f5")
listbox_resultado.place(y=300)

#Función para seleccionar las columnas de los datos que se usarán como entradas y salida del modelo
def Seleccionar():
   print(var1.get())
   print(var2.get())
   print()

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

# Creación de los Radiobutton
var1 = StringVar()
var2 = StringVar()

values = ["longitude", "latitude", "housing_median_age", "total_rooms", "total_bedrooms", "population", "households", "median_income", "median_house_value"]
    
for i, value in enumerate(values):
    
        rad1 = Radiobutton(window, variable=var1, value=value, text=i, command=Seleccionar)
        rad2 = Radiobutton(window, variable=var2, value=value, text=i, command=Seleccionar)
        
        rad1.pack(side=LEFT)
        rad2.pack(side=LEFT)
        
        rad1.place(x=80 + 120 * i, y=380)
        rad2.place(x=80 + 120 * i, y=440)
        
        rad1.config(bg="#d9ffdf")
        rad2.config(bg="#d9ffdf")

var1.set(' ')
var2.set(' ')

# Iniciar la aplicación
window.mainloop()