from tkinter import *
import tkinter as tk
import pandas as pd
import sqlite3

# Función para abrir la ventana del explorador de archivos
def browse_files():
    filename = filedialog.askopenfilename(initialdir="/", title="Examinar", filetypes=(("Text files", "*.txt*"), ("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("SQLite databases", "*.db"), ("all files", "*.*")))
    label_file_explorer.configure(text="Archivo abierto: " + filename)
    
    if filename.endswith((".csv", ".xlsx")):
        show_data(filename)
    elif filename.endswith(".db"):
        show_data_sqlite(filename)

def show_data(filename):
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(filename)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filename)
        
        show_data_popup(df)
    except Exception as e:
        error_message = f"Error al cargar el archivo: {str(e)}"
        show_error(error_message)

def show_data_sqlite(filename):
    database = filename
    table = input("Introduce el nombre de la tabla en la base de datos SQLite: ")
    try:
        conn = sqlite3.connect(database)
        query = f"SELECT * FROM {table}"
        df = pd.read_sql_query(query, conn)
        show_data_popup(df)
        conn.close()
    except Exception as e:
        error_message = f"Error al cargar los datos desde la base de datos SQLite: {str(e)}"
        show_error(error_message)

def show_data_popup(df):
    top = tk.Toplevel()
    top.title("Datos")
    text = tk.Text(top)
    text.insert(tk.INSERT, df.to_string())
    text.pack()

def show_error(message):
    top = tk.Toplevel()
    top.title("Error")
    text = tk.Text(top)
    text.insert(tk.INSERT, message)
    text.pack()

# Crear la ventana raíz
window = tk.Tk()
window.title('File Explorer')
window.geometry("500x500")
window.config(bg="#dfe9f5")

# Crear elementos de la interfaz gráfica
label_file_explorer = tk.Label(window, text="Explorador de Archivos usando Tkinter", width=75, height=5, fg="black", bg="#c5d4eb")
button_explore = tk.Button(window, text="Buscar Archivos", command=browse_files, height=1, width=16)
button_exit = tk.Button(window, text="Salir", command=window.quit, height=1, width=6)

# Organizar elementos en la ventana
label_file_explorer.place(x=40, y=50)
button_explore.place(x=200, y=230)
button_exit.place(x=230, y=260)

#Función para seleccionar las columnas de los datos que se usarán como entradas y salida del modelo
def Seleccionar():
   print(var1.get())
   print(var2.get())
   print()

#Etiquetas
etiqueta_seleccionar = tk.Label(window, text="Selecciona una variable x y una variable y:")
etiqueta_seleccionar.place(y = 300)
etiqueta_seleccionar.config(bg="#dfe9f5")

etiqueta_variable_x = tk.Label(window, text="Variable x:")
etiqueta_variable_x.place(y = 350)
etiqueta_variable_x.config(bg="#dfe9f5")

etiqueta_variable_y = tk.Label(window, text="Variable y:")
etiqueta_variable_y.place(y = 400)
etiqueta_variable_y.config(bg="#dfe9f5")

#Creación de los Radiobutton
var1 = StringVar()
var2 = StringVar()

values = ["longitude", "latitude", "housing_median_age", "total_rooms", "total_bedrooms", "population", "households", "median_income", "median_house_value"]

for i, value in enumerate(values):
    rad1 = Radiobutton(window, variable=var1, value=value, command=Seleccionar)
    rad2 = Radiobutton(window, variable=var2, value=value, command=Seleccionar)
    
    rad1.pack(side=LEFT)
    rad2.pack(side=LEFT)
    
    rad1.place(x=80 + 20 * i, y=350)
    rad2.place(x=80 + 20 * i, y=400)
    
    rad1.config(bg="#dfe9f5")
    rad2.config(bg="#dfe9f5")

var1.set(' ')
var2.set(' ')

# Iniciar la aplicación
window.mainloop()