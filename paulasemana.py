#Programa de Python para crear un explorador de archivos utilizando la librería Tkinter
#Importamos todos los componenentes de la librería tkinter
from tkinter import *
#importamos el módulo filedialog
from tkinter import filedialog
#importamos el módulo ttk
from tkinter import ttk

#Función para abrir la ventana del explorador de archivos
def browseFiles():
    filename = filename.askopenfilename(initialdir= "/", title = "Examinar", filetypes=(("Text files", "*.txt*"), ("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("SQLite databases", "*.db"), ("all files", "*.*")))
    label_file_explorer.configure(text = "Archivo abierto: " + filename)

#Creamos la ventana raíz
window = Tk()

#Escribimos el título de la ventana
window.title('File Explorer')

#Establecemos el tamaño de la ventana
window.geometry("500x500")

#Establecemos el color de fondo de la ventana
window.config(background= "#dfe9f5")

#Creamos el Explorador de Archivos
label_file_explorer = Label(window, text = "Explorador de Archivos usando Tkinter", width = 75, height = 5, fg = "black")
button_explore = Button(window, text = "Buscar Archivos", command = browseFiles, height = 1, width = 16)
button_exit = Button(window, text = "Salir", command = exit, height = 1, width = 6)

#Establecemos el color de fondo de la etiqueta explorador de archivos
label_file_explorer.config(background = "#c5d4eb")

"""# Cargar imagen del disco.
image = PhotoImage(file="carpeta.png")
# Insertarla en una etiqueta.
carpeta = ttk.Label(image=image)
carpeta.pack()"""

#Establecemos la posición de los botones 
button_explore.place(x=200, y=230)
button_exit.place(x=230, y=260)
label_file_explorer.place(y=100)
#carpeta.place(x =240, y=200)

window.mainloop()