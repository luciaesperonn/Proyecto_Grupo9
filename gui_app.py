import pandas as pd
import sqlite3
from sklearn.linear_model import LinearRegression
import joblib
import tkinter as tk
from tkinter import Tk, Label, Button, filedialog, Frame, ttk, Radiobutton, Scrollbar, StringVar
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.metrics import mean_squared_error, r2_score
from clase_modelo import ModeloInfo
import joblib
from file_operations import cargar_archivo_csv, cargar_archivo_excel, cargar_archivo_db,verificar_columnas_numericas

class RegresionLinealApp:
    def __init__(self, master):
        """
        Inicializa la aplicación de Regresión Lineal.

        Parámetros:
        - master: Ventana principal de la aplicación.
        """
        """
        Inicializa la aplicación de Regresión Lineal.

        Parámetros:
        - master: Ventana principal de la aplicación.
        """
        self.master = master
        master.title("Aplicación de Regresión Lineal")

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
    
    def cargar_datos(self):
        """
        Carga los datos desde un archivo seleccionado por el usuario.

        Lanza:
        - ValueError: Si no se selecciona un archivo o hay un problema al cargar los datos.
        """
        """
        Carga los datos desde un archivo seleccionado por el usuario.

        Lanza:
        - ValueError: Si no se selecciona un archivo o hay un problema al cargar los datos.
        """
        self.ocultar_elementos_interfaz()
        file_path = filedialog.askopenfilename(initialdir="/", filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("SQLite databases", "*.db"), ("all files", "*.*")])
        if file_path:
            if file_path.endswith('.csv'):
                self.df = cargar_archivo_csv(file_path)
            elif file_path.endswith('.xlsx'):
                self.df = cargar_archivo_excel(file_path)
            elif file_path.endswith('.db'):
                self.df = cargar_archivo_db(file_path)

            self.actualizar_etiqueta_ruta(file_path)
            self.mostrar_tabla(self.df)  # Agrega esta línea para mostrar la tabla
            self.mostrar_variables(self.df.columns)

            print("Datos cargados exitosamente")

    def mostrar_variables(self, variables):
        """
        Muestra las variables disponibles en el DataFrame.

        Parámetros:
        - variables (list): Lista de nombres de las variables.

        Lanza:
        - ValueError: Si hay un problema al mostrar las variables.
        """
        """
        Muestra las variables disponibles en el DataFrame.

        Parámetros:
        - variables (list): Lista de nombres de las variables.

        Lanza:
        - ValueError: Si hay un problema al mostrar las variables.
        """
        self.variable_x = StringVar(value=" ")
        self.variable_y = StringVar(value=" ")
        for radiobutton in self.radiobuttons_x:
            radiobutton.destroy()
        for radiobutton in self.radiobuttons_y:
            radiobutton.destroy()
        self.radiobuttons_x = self.crear_radiobuttons(self.frame_variables, variables, self.variable_x, row=2, column=1)
        self.radiobuttons_y = self.crear_radiobuttons(self.frame_variables, variables, self.variable_y, row=3, column=1)
    
    def crear_radiobuttons(self, frame, options, variable, row, column):
        """
        Crea y muestra radiobuttons en un frame.

        Parámetros:
            - frame (tk.Frame): El frame en el que se colocarán los radiobuttons.
            - options (list): Lista de opciones para los radiobuttons.
            - variable (tk.StringVar): Variable que se asociará a los radiobuttons.
            - row (int): Número de fila en el que se ubicarán los radiobuttons.
            - column (int): Número de columna inicial en el que se ubicarán los radiobuttons.

        Devuelve:
            list: Lista de objetos tk.Radiobutton creados.
        """
        radiobuttons = []
        for i, option in enumerate(options):
            radiobutton = tk.Radiobutton(frame, text=option, variable=variable, value=option)
            radiobutton.grid(row=row, column=column + i, padx=5, pady=5, sticky=tk.W)
            radiobuttons.append(radiobutton)
        return radiobuttons    

    def actualizar_etiqueta_ruta(self, ruta):
        """
        Actualiza la etiqueta de la ruta en la interfaz gráfica.

        Parameters:
        - ruta (str): La nueva ruta que se mostrará en la etiqueta.
        """
        """
        Actualiza la etiqueta de la ruta en la interfaz gráfica.

        Parameters:
        - ruta (str): La nueva ruta que se mostrará en la etiqueta.
        """
        self.etiqueta_ruta.config(text=f"RUTA: {ruta}")

    def mostrar_tabla(self, df):
        """
        Muestra un DataFrame en un Treeview en la interfaz gráfica.

        Parameters:
        - df (pd.DataFrame): El DataFrame que se mostrará en la tabla.
        """
        """
        Muestra un DataFrame en un Treeview en la interfaz gráfica.

        Parameters:
        - df (pd.DataFrame): El DataFrame que se mostrará en la tabla.
        """
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

    def realizar_regresion(self):
        """
        Realiza una regresión lineal usando las variables x e y seleccionadas.
        Muestra el modelo ajustado en la interfaz gráfica.
        """
        """
        Realiza una regresión lineal usando las variables x e y seleccionadas.
        Muestra el modelo ajustado en la interfaz gráfica.
        """
        if self.variable_x.get() and self.variable_y.get():
            # Obtener las variables seleccionadas
            variable_x = self.variable_x.get()
            variable_y = self.variable_y.get()

            # Añadir la verificación de columnas numéricas solo para variable_x y variable_y
            columnas_a_verificar = [self.variable_x.get(), self.variable_y.get()]
            verificar_columnas_numericas(self.df, columnas_a_verificar)

            # Antes de realizar la regresión lineal, elimina las filas con NaN en la variable de respuesta
            self.df.dropna(subset=[variable_x, variable_y], inplace=True)

            # Seleccionar las columnas correspondientes
            X = self.df[[variable_x]]
            y = self.df[variable_y]

            # Inicializar el modelo de regresión lineal
            self.modelo = LinearRegression()

            # Ajustar el modelo a los datos
            self.modelo.fit(X, y)

            # Hacer predicciones
            y_pred = self.modelo.predict(X)

            # Calcular el error cuadrático medio
            self.mse = mean_squared_error(y, y_pred)

            # Calcular la bondad de ajuste (R^2)
            self.r2 = r2_score(y, y_pred)

            # Imprimir la ecuación de la recta
            self.ecuacion = f"{variable_y} = {self.modelo.intercept_:.4f} + {self.modelo.coef_[0]:.4f} * {variable_x}"
            print("Ecuación de la recta:", self.ecuacion)

            # Imprimir el error cuadrático medio y la bondad de ajuste
            print("Error Cuadrático Medio:", self.mse)
            print("Bondad de Ajuste (R^2):", self.r2)

            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            self.figure = Figure(figsize=(6, 4))
            ax = self.figure.add_subplot(111)
            ax.scatter(X, y, color='lightblue', label='Datos reales')
            ax.plot(X, y_pred, color='purple', linewidth=2, label='Ajuste del modelo')

            # Convertir los coeficientes y el intercepto a tipos de datos numéricos
            self.modelo.intercept_ = float(self.modelo.intercept_)
            self.modelo.coef_[0] = float(self.modelo.coef_[0])

            self.etiqueta_x = variable_x
            self.etiqueta_y = variable_y

            ax.set_xlabel(self.etiqueta_x)  # Utiliza la etiqueta de la variable X
            ax.set_ylabel(self.etiqueta_y)  # Utiliza la etiqueta de la variable Y
            ax.legend()
            ax.set_title('Modelo de Regresión Lineal')

            # Crear el área de dibujo (canvas)
            self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame_variables)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(row=4, rowspan=20, column=2, columnspan=5, padx=10, pady=5, sticky=tk.W)

            # Agregar etiquetas de texto a la derecha del gráfico
            self.etiqueta_ecuacion = Label(self.frame_variables, text=f"La ecuación de la recta es: {self.ecuacion}")
            self.etiqueta_ecuacion.grid(row=4, column=7, columnspan=4, padx=10, pady=5, sticky=tk.W)
            self.etiqueta_datos = Label(self.frame_variables, text=f"El error cuadrático medio es: {self.mse:.4f} y la bondad de ajuste es: {self.r2:.4f}")
            self.etiqueta_datos.grid(row=5, column=7, columnspan=4, padx=10, pady=5, sticky=tk.W)

            self.etiqueta_descripcion = Label(self.frame_variables, text='Introduzca la descripción del modelo:')
            self.etiqueta_descripcion.grid(row=6, column=7, columnspan=2, padx=10, pady=5, sticky=tk.W)
            self.texto_descripcion = tk.StringVar()
            self.entrada_descripcion = tk.Entry(self.frame_variables, width=50, textvariable=self.texto_descripcion)
            self.entrada_descripcion.grid(row=6, column=9, columnspan=2, padx=10, pady=5, sticky=tk.W)

            # Nueva línea: Crear botón para guardar el modelo
            self.boton_guardar_modelo = Button(self.frame_variables, text="Guardar modelo", command=self.guardar_modelo)
            self.boton_guardar_modelo.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
            
            self.info_modelo = ModeloInfo(self.variable_x.get(), self.variable_y.get(), self.modelo, self.modelo.intercept_, self.modelo.coef_, 
                                          self.ecuacion, self.mse, self.texto_descripcion.get())
            
            # Mostrar la ecuación en una etiqueta
            if self.etiqueta_nueva_ecuacion is not None:
                self.etiqueta_nueva_ecuacion.config(text='')
                self.etiqueta_nueva_ecuacion.grid_forget()
            self.elementos_prediccion()

        else:
            self.show_error("Seleccione las variables x e y antes de hacer la regresión")
            raise ValueError("Seleccione las variables x e y antes de hacer la regresión")


    def elementos_prediccion(self):
        """
        Configura los elementos de la interfaz gráfica para la predicción.
        """
        """
        Configura los elementos de la interfaz gráfica para la predicción.
        """
        self.frame_prediccion.grid(row=7, column=7, columnspan=4, padx=10, pady=5, sticky=tk.W)

        self.etiqueta_introducir_valor = Label(self.frame_prediccion, text=f"Introduzca un valor para {self.variable_x.get()}:")
        self.etiqueta_introducir_valor.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        self.texto_valor_x = tk.StringVar()
        self.entrada_valor_x = tk.Entry(self.frame_prediccion, width=10, textvariable=self.texto_valor_x)
        self.entrada_valor_x.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

        self.boton_realizar_prediccion = Button(self.frame_prediccion, text="Realizar predicción", command=self.realizar_prediccion)
        self.boton_realizar_prediccion.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)


    def realizar_prediccion(self):
        """
        Realiza una predicción utilizando el modelo de regresión lineal.
        Muestra la ecuación de la recta con el nuevo valor de x e y.
        """
        """
        Realiza una predicción utilizando el modelo de regresión lineal.
        Muestra la ecuación de la recta con el nuevo valor de x e y.
        """
        if hasattr(self, 'info_modelo') and self.info_modelo is not None:
            try:
                # Obtener el valor ingresado por el usuario
                valor_x_str = self.texto_valor_x.get()

                # Verificar si se ingresó un valor
                if valor_x_str == '':
                    self.show_error("Ingrese un valor para la predicción.")
                    raise ValueError("Ingrese un valor para la predicción.")

                # Convertir el valor ingresado a un número
                self.valor_x = float(valor_x_str)

                # Calcular el valor de y usando el modelo
                self.valor_y = self.modelo.predict([[self.valor_x]])[0]

                # Mostrar la ecuación con el nuevo valor de x e y
                self.nueva_ecuacion = f"{self.valor_y} = {self.info_modelo.intercepto} + {self.info_modelo.coeficiente} * {self.valor_x}"
                print(self.info_modelo.variable_y, '=', self.nueva_ecuacion)


                self.etiqueta_nueva_ecuacion = Label(self.frame_prediccion, text=(f"{self.info_modelo.variable_y} = {self.nueva_ecuacion}"))
                self.etiqueta_nueva_ecuacion.grid(row=8, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)
            
            except ValueError as e:
                self.show_error(f"Error al realizar la predicción: {str(e)}")
            except Exception as e:
                self.show_error(f"Error inesperado al realizar la predicción: {str(e)}")
    
    
    def guardar_modelo(self):
        """
        Guarda el modelo de regresión lineal en un archivo joblib.
        Muestra mensajes de error o éxito en la interfaz gráfica.
        """
        """
        Guarda el modelo de regresión lineal en un archivo joblib.
        Muestra mensajes de error o éxito en la interfaz gráfica.
        """
        if self.info_modelo is None:
            self.show_error("Realiza la regresión lineal antes de intentar guardar el modelo.")
            return None
        try:
            # Obtener la ruta y nombre de archivo seleccionados por el usuario
            file_path = filedialog.asksaveasfilename(defaultextension=".joblib", filetypes=[("Archivos joblib", "*.joblib")])
    
            if file_path:
                # Guardar la información del modelo en el archivo
                self.info_modelo.guardar_modelo(file_path)
    
                self.show_info(f"Modelo guardado en: {file_path}")
    
        except Exception as e:
            self.show_error(f"Error al guardar el modelo: {str(e)}")
    
    def cargar_modelo(self):
        """
        Carga un modelo de regresión lineal desde un archivo joblib.
        Actualiza la interfaz gráfica con la información del modelo cargado.
        """
        """
        Carga un modelo de regresión lineal desde un archivo joblib.
        Actualiza la interfaz gráfica con la información del modelo cargado.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Archivos joblib", "*.joblib")])
        if file_path:
            self.actualizar_etiqueta_ruta(file_path)
            self.modelo_cargado = joblib.load(file_path)
            print("Modelo cargado exitosamente")
            self.eliminar_tabla()
            self.ocultar_elementos_interfaz()
            self.mostrar_datos_modelo_cargado()

            # Agregar la siguiente línea para crear la etiqueta_nueva_ecuacion si no existe
            if not hasattr(self, 'etiqueta_nueva_ecuacion') or not self.etiqueta_nueva_ecuacion:
                self.etiqueta_nueva_ecuacion = Label(self.frame_prediccion, text="")
                self.etiqueta_nueva_ecuacion.grid(row=8, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)
            else:
                self.etiqueta_nueva_ecuacion.grid_forget()

            if (self.variable_x is None and hasattr(self.modelo_cargado, 'variable_x')) and (self.variable_y is None and hasattr(self.modelo_cargado, 'variable_y')):
                self.variable_x = StringVar(value=self.modelo_cargado.variable_x)
                self.variable_y = StringVar(value=self.modelo_cargado.variable_y)
                self.modelo = self.modelo_cargado.modelo
            
            # Luego, llamar a elementos_prediccion para crear los elementos de predicción
            self.elementos_prediccion()

    def show_error(self, message):
        """
        Muestra una ventana emergente de error con el mensaje proporcionado.

        Parameters:
        - message (str): Mensaje de error a mostrar.
        """
        """
        Muestra una ventana emergente de error con el mensaje proporcionado.

        Parameters:
        - message (str): Mensaje de error a mostrar.
        """
        top = tk.Toplevel()
        top.title("Error")
        text = tk.Text(top)
        text.insert(tk.INSERT, message)
        text.pack()# Función para obtener el valor ingresado en el cuadro de texto

    def show_info(self, message):
        """
        Muestra una ventana emergente de información con el mensaje proporcionado.

        Parameters:
        - message (str): Mensaje de información a mostrar.
        """
        """
        Muestra una ventana emergente de información con el mensaje proporcionado.

        Parameters:
        - message (str): Mensaje de información a mostrar.
        """
        top = tk.Toplevel()
        top.title("Información")
        text = tk.Text(top)
        text.insert(tk.INSERT, message)
        text.pack()# Función para obtener el valor ingresado en el cuadro de texto

    def eliminar_tabla(self):
         """
        Elimina la tabla (Treeview) de la interfaz gráfica.
        """
         if self.tabla_frame.winfo_ismapped():
                self.tabla_frame.grid_forget()
    
    def ocultar_elementos_interfaz(self):
        """
        Oculta los elementos de la interfaz, excepto el frame_contenedor_ruta.
        """
        for elemento in self.frame_variables.winfo_children():
            elemento.grid_forget()

    def mostrar_datos_modelo_cargado(self):
        """
        Muestra información específica del modelo cargado en la interfaz gráfica.
        """
        """
        Muestra información específica del modelo cargado en la interfaz gráfica.
        """
        if self.modelo_cargado is not None:
            # Obtener información específica del modelo cargado
            variable_x_cargada = self.modelo_cargado.variable_x
            variable_y_cargada = self.modelo_cargado.variable_y
            intercepto_cargado = self.modelo_cargado.intercepto
            coeficiente_cargado = self.modelo_cargado.coeficiente
            ecuacion_cargada = self.modelo_cargado.ecuacion_recta
            error_cargado = self.modelo_cargado.mse
            descripcion_cargada = self.modelo_cargado.descripcion

            # Puedes crear nuevos elementos en la interfaz para mostrar la información
            label_coeficientes = tk.Label(self.frame_variables, text=f"Ecuación del modelo: {ecuacion_cargada}")
            label_coeficientes.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
            label_intercepto = tk.Label(self.frame_variables, text=f"Error del modelo: {error_cargado}")
            label_intercepto.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
            
            # Mostrar la etiqueta solo si hay una descripción cargada
            if descripcion_cargada is not None and descripcion_cargada != "":
                label_descripcion = tk.Label(self.frame_variables, text=f"Descripción del modelo: {descripcion_cargada}")
                label_descripcion.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

            self.info_modelo = ModeloInfo(variable_x_cargada, variable_y_cargada, ecuacion_cargada, intercepto_cargado, coeficiente_cargado,
                                        error_cargado, descripcion_cargada)

        else:
            self.show_error("No hay un modelo cargado para mostrar.")
