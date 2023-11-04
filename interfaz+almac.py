import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import sqlite3

# Función para abrir la ventana del explorador de archivoss
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
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        
        # Obtener el nombre de la primera tabla en la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table = cursor.fetchone()[0]
        
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
window.config(bg="#d9ffdf")

# Crear elementos de la interfaz gráfica
label_file_explorer = tk.Label(window, text="Explorador de Archivos usando Tkinter", width=75, height=5, fg="black", bg="#87a1ab")
button_explore = tk.Button(window, text="Buscar Archivos", command=browse_files, height=1, width=16)
button_exit = tk.Button(window, text="Salir", command=window.quit, height=1, width=6)

# Organizar elementos en la ventana
label_file_explorer.place(x=40, y=50)
button_explore.place(x=200, y=230)
button_exit.place(x=230, y=260)

# Iniciar la aplicación
window.mainloop()

