import tkinter as Tk

class SingletonTk:
    """
    Clase SingletonTk que garantiza que solo exista una instancia de la ventana principal de Tkinter.

    Atributos:
    - _instance: Almacena la única instancia de la ventana principal.

    Métodos:
    - __new__(cls): Método especial que se encarga de crear una nueva instancia si no existe, 
                    o devolver la instancia existente si ya se ha creado.
    """

    _instance = None

    def __new__(cls):
        """
        Crea una instancia única de la ventana principal si aún no existe. Si ya existe, devuelve esa instancia.

        Retorna:
        - Tk.Tk: Instancia única de la ventana principal de Tkinter.
        """
        if cls._instance is None:
            cls._instance = Tk.Tk()  
            cls._instance.state('zoomed')
        return cls._instance
