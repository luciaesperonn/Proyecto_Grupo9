from tkinter import Tk 
from InterfazNueva import RegresionLinealApp

if __name__ == "__main__":
    root = Tk()
    root.state('zoomed')  # Para abrir la ventana maximizada con barra de título y botones
    app = RegresionLinealApp(root)
    root.mainloop()