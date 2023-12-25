import tkinter as tk
from tkinter import Label, Button, filedialog, Frame, ttk, Radiobutton, Scrollbar, StringVar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from regresionlineal import RegresionLineal
from clase_modelo import ModeloInfo
from file_operations import cargar_archivo_csv, cargar_archivo_excel, cargar_archivo_db

class RegresionLinealApp:
    def __init__(self, master):
        self.master = master
        master.title("Aplicación de Regresión Lineal")
        self.regresion_lineal = RegresionLineal(self)

        self.modelo = None
        self.df = None
        self.radiobuttons_x = []  # Inicializar como lista vacía
        self.radiobuttons_y = []  # Inicializar como lista vacía

        self.figure = None
        self.canvas = None

        self.frame_contenedor_ruta = Frame(master)
        self.frame_contenedor_ruta.pack(fill=tk.X)  # Ocupa todo el ancho horizontal
        self.frame_contenedor_ruta.columnconfigure(0, weight=20)
        self.frame_contenedor_ruta.columnconfigure(1, weight=1)
        self.frame_contenedor_ruta.columnconfigure(2, weight=1)
        self.frame_contenedor_ruta.columnconfigure(3, weight=10)

        self.etiqueta_ruta = Label(self.frame_contenedor_ruta, text="RUTA:")
        self.etiqueta_ruta.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.boton_examinar = Button(self.frame_contenedor_ruta, text="Examinar", command=self.cargar_datos)
        self.boton_examinar.grid(row=0, column=1, padx=0, pady=5, sticky=tk.W)

        self.boton_cargar_modelo = Button(self.frame_contenedor_ruta, text="Cargar Modelo", command=self.cargar_modelo)
        self.boton_cargar_modelo.grid(row=0, column=2, padx=(0, 10), pady=5, sticky=tk.W)

        self.frame_variables = Frame(self.master)
        self.frame_variables.pack(side="top", fill="both", expand=True)

        self.tabla_frame = Frame(self.frame_variables)

        self.etiqueta_seleccionar = None
        self.etiqueta_variable_x = None
        self.etiqueta_variable_y = None
        self.boton_realizar_regresion = None

        self.variable_x = None
        self.variable_y = None

        self.frame_prediccion = Frame(self.frame_variables)

        self.ecuacion = None
        self.mse = None
        self.r2 = None
        self.etiqueta_ecuacion = None
        self.etiqueta_datos = None

        self.etiqueta_descripcion = None
        self.entrada_descripcion = None
        self.texto_descripcion = None
        self.boton_guardar_modelo = None

        self.info_modelo = None
        self.modelo_cargado = None

        self.valor_x = None
        self.valor_y = None
        self.nueva_ecuacion = None
        self.etiqueta_nueva_ecuacion = None
        self.crear_widgets()

    def crear_widgets(self):
        # Agrega aquí la configuración de tus widgets
        pass

    def cargar_datos(self):
        # Llama al método cargar_datos de la instancia de RegresionLineal
        self.regresion_lineal.cargar_datos()

    def realizar_regresion(self):
        # Llama al método realizar_regresion de la instancia de RegresionLineal
        self.regresion_lineal.realizar_regresion()

    def realizar_prediccion(self):
        # Llama al método realizar_prediccion de la instancia de RegresionLineal
        valor_x = self.texto_valor_x.get()
        self.regresion_lineal.realizar_prediccion(valor_x)

    def actualizar_etiqueta_ruta(self, ruta):
        self.etiqueta_ruta.config(text=f"RUTA: {ruta}")

    def mostrar_tabla(self, df):
        # Limpiar el contenido actual del Frame
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()

        # Configurar columnas
        columns = df.columns
        clean_columns = [col.replace(" ", "_") for col in columns]  # Reemplazar espacios en nombres de columnas

        # Crear un Treeview en el Frame
        self.tabla = ttk.Treeview(self.tabla_frame, show="headings", columns=clean_columns, height=6)
        
        # Configurar columnas
        for col, clean_col in zip(columns, clean_columns):
            self.tabla.heading(clean_col, text=col)
            self.tabla.column(clean_col, anchor="center", width=150) 

        self.scrollbar_y = Scrollbar(self.tabla_frame, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scrollbar_y.set)

        # Empaquetar el Treeview y la barra de desplazamiento en el Frame
        self.tabla.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")

        # Agregar filas sin incluir el índice
        for row in df.itertuples(index=False):
            values = [str(getattr(row, col)) for col in df.columns]
            self.tabla.insert("", "end", values=values)

        self.tabla_frame.grid(row=0, column=0, columnspan=12, padx=10, pady=5, sticky=tk.W)

        self.etiqueta_seleccionar = Label(self.frame_variables, text="Seleccionar variables:")
        self.etiqueta_seleccionar.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.etiqueta_variable_x = Label(self.frame_variables, text="Variable x:")
        self.etiqueta_variable_x.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.etiqueta_variable_y = Label(self.frame_variables, text="Variable y:")
        self.etiqueta_variable_y.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.boton_realizar_regresion = Button(self.frame_variables, text="Realizar regresión", command=self.realizar_regresion)
        self.boton_realizar_regresion.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)


    def mostrar_variables(self, columnas):
        self.variable_x = StringVar(value=" ")
        self.variable_y = StringVar(value=" ")
        for radiobutton in self.radiobuttons_x:
            radiobutton.destroy()
        for radiobutton in self.radiobuttons_y:
            radiobutton.destroy()
        self.radiobuttons_x = self.crear_radiobuttons(self.frame_variables, columnas, self.variable_x, row=2, column=1)
        self.radiobuttons_y = self.crear_radiobuttons(self.frame_variables, columnas, self.variable_y, row=3, column=1)


    def actualizar_grafico(self, X, y, y_pred, variable_x, variable_y, ecuacion, mse, r2):
        # Agrega aquí la lógica para actualizar el gráfico en la interfaz
        pass

    def actualizar_interfaz_prediccion(self):
        # Agrega aquí la lógica para actualizar la interfaz después de la regresión
        pass

    def mostrar_ecuacion_prediccion(self, ecuacion):
        # Agrega aquí la lógica para mostrar la ecuación de predicción en la interfaz
        pass

    def establecer_info_modelo(self, info_modelo):
        # Agrega aquí la lógica para establecer la información del modelo en la interfaz
        pass

    
    def show_error(self, mensaje):
        top = tk.Toplevel()
        top.title("Error")
        text = tk.Text(top)
        text.insert(tk.INSERT, mensaje)
        text.pack()# Función para obtener el valor ingresado en el cuadro de texto

    def show_info(self, mensaje):
        top = tk.Toplevel()
        top.title("Información")
        text = tk.Text(top)
        text.insert(tk.INSERT, mensaje)
        text.pack()# Función para obtener el valor ingresado en el cuadro de texto

# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    app = RegresionLinealApp(root)
    root.mainloop()

