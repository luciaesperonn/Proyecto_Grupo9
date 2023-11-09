import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import sqlite3
from leer_archivos import mostrar_archivos

# Función para abrir la ventana del explorador de archivoss
def browse_files():
    filename = filedialog.askopenfilename(initialdir="/", title="Examinar", filetypes=(("Text files", "*.txt*"), ("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("SQLite databases", "*.db"), ("all files", "*.*")))
    label_file_explorer.configure(text="Archivo abierto: " + filename)

    df=mostrar_archivos(filename)
    show_data_popup(df)
    
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
    row_text = ", ".join(f"{columna}" for columna in primera_fila.keys())
    listbox_resultado.insert(tk.END, row_text)    

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
window.config(bg="#d9ffdf")

# Crear elementos de la interfaz gráfica
label_file_explorer = tk.Label(window, text="Explorador de Archivos usando Tkinter", width=75, height=5, fg="black", bg="#87a1ab")
button_explore = tk.Button(window, text="Buscar Archivos", command=browse_files, height=1, width=16)
button_exit = tk.Button(window, text="Salir", command=window.quit, height=1, width=6)

# Organizar elementos en la ventana
label_file_explorer.place(x=40, y=50)
button_explore.place(x=200, y=230)
button_exit.place(x=230, y=260)

#Mostrar la lista con las variables del archivo
listbox_resultado = tk.Listbox(window, selectmode=tk.SINGLE, height=1, width=150, bg="#dfe9f5")
listbox_resultado.place(x=0, y=300)

# Iniciar la aplicación
window.mainloop()

