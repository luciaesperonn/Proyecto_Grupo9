import tkinter as tk
from tkinter import StringVar, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Scrollbar
from matplotlib.figure import Figure

class WidgetFactory:
    """
    Clase WidgetFactory que proporciona métodos estáticos para crear diferentes widgets y componentes 
    de la biblioteca Tkinter y Matplotlib.

    Atributos:
    - WIDGET_TYPES (dict): Un diccionario que mapea tipos de widgets a sus clases correspondientes de Tkinter.

    Métodos estáticos:
    - crear_widget(tipo, master, **kwargs): Crea un widget del tipo especificado con los argumentos adicionales proporcionados.
    - crear_stringvar(valor_inicial=" "): Crea y devuelve una instancia de StringVar con un valor inicial.
    - crear_treeview(master, show="headings", columns=None, height=6): Crea y devuelve un Treeview con las opciones dadas.
    - crear_scrollbar(master, orient, command): Crea y devuelve un Scrollbar con la orientación y comando especificados.
    - crear_figure(figsize=(6, 4)): Crea y devuelve una instancia de Figure de Matplotlib con el tamaño especificado.
    - crear_figure_canvas(master, figure): Crea y devuelve una instancia de FigureCanvasTkAgg con la figura dada.

    Uso típico:
    >>> factory = WidgetFactory()
    >>> boton = factory.crear_widget('boton', master, text="Click me")
    >>> string_var = factory.crear_stringvar("Hola")
    >>> tree = factory.crear_treeview(master)
    >>> scrollbar = factory.crear_scrollbar(master, orient="vertical", command=callback_function)
    >>> figure = factory.crear_figure(figsize=(8, 6))
     canvas = factory.crear_figure_canvas(master, figure)
    """
    WIDGET_TYPES = {
        'boton': tk.Button,
        'entrada': tk.Entry,
        'frame': tk.Frame,
        'etiqueta': tk.Label
    }

    @staticmethod
    def crear_widget(tipo, master, **kwargs):
        """
        Crea y devuelve un widget del tipo especificado con los argumentos adicionales proporcionados.

        Parámetros:
        - tipo (str): Tipo de widget a crear.
        - master: Widget padre al que se agregará el nuevo widget.
        - **kwargs: Argumentos adicionales específicos para el widget.

        Retorna:
        - Widget: Una instancia del widget especificado.
        
        Lanza:
        - ValueError: Si el tipo de widget no es válido.
        """
        widget_class = WidgetFactory.WIDGET_TYPES.get(tipo)
        if not widget_class:
            raise ValueError("Tipo de widget no válido")
        return widget_class(master, **kwargs)

    @staticmethod
    def crear_stringvar(valor_inicial=" "):
        """
        Crea y devuelve una instancia de StringVar con un valor inicial.

        Parámetros:
        - valor_inicial (str): Valor inicial para el StringVar. Por defecto es un espacio en blanco.

        Retorna:
        - StringVar: Una instancia de StringVar con el valor inicial especificado.
        """
        return StringVar(value=valor_inicial)

    @staticmethod
    def crear_treeview(master, show="headings", columns=None, height=6):
        """
        Crea y devuelve una instancia de ttk.Treeview con las opciones proporcionadas.

        Parámetros:
        - master: Widget padre al que se agregará el Treeview.
        - show (str): Opción para mostrar solo los encabezados en el Treeview. Por defecto es "headings".
        - columns (list): Lista de columnas para el Treeview.
        - height (int): Altura del Treeview. Por defecto es 6.

        Retorna:
        - ttk.Treeview: Una instancia de Treeview con las opciones especificadas.
        """
        return ttk.Treeview(master, show=show, columns=columns, height=height)

    @staticmethod
    def crear_scrollbar(master, orient, command):
        """
        Crea y devuelve una instancia de Scrollbar con las opciones proporcionadas.

        Parámetros:
        - master: Widget padre al que se agregará el Scrollbar.
        - orient (str): Orientación del Scrollbar ("vertical" o "horizontal").
        - command: Comando que se asociará con el Scrollbar.

        Retorna:
        - Scrollbar: Una instancia de Scrollbar con las opciones especificadas.
        """
        return Scrollbar(master, orient=orient, command=command)

    @staticmethod
    def crear_figure(figsize=(6, 4)):
        """
        Crea y devuelve una instancia de Figure de Matplotlib con el tamaño especificado.

        Parámetros:
        - figsize (tuple): Dimensiones de la figura (ancho, alto). Por defecto es (6, 4).

        Retorna:
        - Figure: Una instancia de Figure con el tamaño especificado.
        """
        return Figure(figsize=figsize)

    @staticmethod
    def crear_figure_canvas(master, figure):
        """
        Crea y devuelve una instancia de FigureCanvasTkAgg con la figura dada.

        Parámetros:
        - master: Widget padre al que se agregará el FigureCanvasTkAgg.
        - figure: Figura de Matplotlib que se mostrará en el FigureCanvasTkAgg.

        Retorna:
        - FigureCanvasTkAgg: Una instancia de FigureCanvasTkAgg con la figura proporcionada.
        """
        return FigureCanvasTkAgg(figure, master=master)