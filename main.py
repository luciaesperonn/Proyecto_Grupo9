from singleton import SingletonTk
from tkinter import Tk
from gui_app import *

if __name__ == "__main__":
    # Crear una instancia de la clase SingletonTk(), que representa la ventana principal de la aplicación.
    root = SingletonTk()  
    root.state('zoomed')  
    # Crear una instancia de la clase RegresionLinealApp, que probablemente represente la interfaz gráfica de la aplicación.
    app = RegresionLinealApp(root)
    # Iniciar el bucle principal de la interfaz gráfica, permitiendo la interactividad del usuario.
    root.mainloop()