# Importación de librerías
import sqlite3
import joblib
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from matplotlib.figure import Figure
from sklearn.impute import SimpleImputer
from leer_archivos import mostrar_archivos
from clase_modelo import ModeloInfo
from sklearn.metrics import mean_squared_error
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from regresion_lineal import crear_modelo_regresion_lineal, visualizar_modelo

valor_x_entry = None 
resultado_prediccion = None
etiqueta_valor_x = None 
button_prediccion = None
modelo_info = None
loaded_model_info = None

def browse_files():
    """
    Abre una ventana de explorador de archivos y permite al usuario seleccionar un archivo de datos.

    Parámetros:
    - Ninguno

    Devuelve:
    - str: Ruta del archivo seleccionado.
    """
    filename = get_selected_filename()

    # Definir las variables antes de la llamada a destroy_existing_radiobuttons
    radiobuttons_var1 = None
    radiobuttons_var2 = None
    if filename:
        update_file_explorer_label(filename)

        df = mostrar_archivos(filename)
        show_data_popup(df, text_data_display)

        radiobuttons_var1, radiobuttons_var2 = destroy_existing_radiobuttons(radiobuttons_var1, radiobuttons_var2)

        radiobuttons_var1 = create_and_display_radiobuttons(window, var1, filename, 0.355, Seleccionar)
        radiobuttons_var2 = create_and_display_radiobuttons(window, var2, filename, 0.38, Seleccionar)

        display_labels()

        create_regression_button(window, filename, var1, var2)

def get_selected_filename():
    """
    Devuelve la ruta del archivo seleccionado por el usuario en el explorador de archivos.

    Parámetros:
    - Ninguno

    Devuelve:
    - str: Ruta del archivo seleccionado.
    """
    return filedialog.askopenfilename(initialdir="/", title="Examinar", filetypes=(("Text files", "*.txt*"),
                                                                                   ("CSV files", "*.csv"),
                                                                                   ("Excel files", "*.xlsx"),
                                                                                   ("SQLite databases", "*.db"),
                                                                                   ("all files", "*.*")))

def update_file_explorer_label(filename): 
    """
    Actualiza la etiqueta que muestra la ruta del archivo seleccionado en la interfaz.

    Parámetros:
    - filename (str): Ruta del archivo seleccionado.

    Devuelve:
    - Ninguno
    """
    label_file_explorer.config(text=f"{filename}")

def create_and_display_radiobuttons(window, var, filename, rel_position, command):
    """
    Crea y muestra los botones de opción (Radiobuttons) para las variables X y Y en la interfaz.

    Parámetros:
    - window (tk.Tk): Ventana principal de la aplicación.
    - var (tk.StringVar): Variable de Tkinter asociada a los Radiobuttons.
    - filename (str): Ruta del archivo de datos seleccionado.
    - rel_position (float): Posición relativa en la interfaz.
    - command (function): Función de retorno de llamada para los Radiobuttons.

    Devuelve:
    - list: Lista de Radiobuttons creados y mostrados.
    """
    radiobuttons = create_radiobuttons(window, var, filename, rel_position, command)
    return radiobuttons

def destroy_existing_radiobuttons(radiobuttons_var1, radiobuttons_var2):
    """
    Destruye los botones de opción (Radiobuttons) existentes en la interfaz.

    Parámetros:
    - radiobuttons_var1 (list): Lista de Radiobuttons asociados a la variable X.
    - radiobuttons_var2 (list): Lista de Radiobuttons asociados a la variable Y.

    Devuelve:
    - tuple: Dos listas vacías (None, None).
    """
    destruir_radiobuttons(radiobuttons_var1)
    destruir_radiobuttons(radiobuttons_var2)
    return None, None

def display_labels():
    """
    Muestra etiquetas informativas en la interfaz.

    Parámetros:
    - Ninguno

    Devuelve:
    - Ninguno
    """
    etiqueta_seleccionar = tk.Label(window, text="Selecciona una variable x y una variable y:")
    etiqueta_seleccionar.place(relx=0.01, rely=0.328)

    etiqueta_variable_x = tk.Label(window, text="VARIABLE X:")
    etiqueta_variable_x.place(relx=0.01, rely=0.355)

    etiqueta_variable_y = tk.Label(window, text="VARIABLE Y:")
    etiqueta_variable_y.place(relx=0.01, rely=0.38)

def create_regression_button(window, filename, var1, var2):
    """
    Crea y muestra el botón para realizar la regresión lineal en la interfaz.

    Parámetros:
    - window (tk.Tk): Ventana principal de la aplicación.
    - filename (str): Ruta del archivo de datos seleccionado.
    - var1 (tk.StringVar): Variable asociada a la variable X.
    - var2 (tk.StringVar): Variable asociada a la variable Y.

    Devuelve:
    - Ninguno
    """
    button_regresion = tk.Button(window, text="Realizar Regresión Lineal", height=1, width=20,
                                 command=lambda: realizar_regresion_lineal(filename, var1.get(), var2.get(), auto=True))
    button_regresion.place(relx=0.01, rely=0.42)
    
def cargar_modelo():
    """
    Abre una ventana para que el usuario seleccione un modelo guardado (.joblib) y carga la información del modelo.

    Parámetros:
    - Ninguno

    Devuelve:
    - Ninguno
    """
    # Define las variables que quieres limpiar
    etiqueta_seleccionar = None
    etiqueta_variable_x = None
    etiqueta_variable_y = None
    button_regresion = None
    button_guardar_modelo = None
    label_mse = None
    label_ecuacion_recta = None
    graph_canvas = None
    radiobuttons_var1 = None
    radiobuttons_var2 = None
    
    try:
        file_path = filedialog.askopenfilename(defaultextension=".joblib", filetypes=[("Archivos joblib", "*.joblib")])

        if file_path:
            # Cargar el modelo y la información asociada
            loaded_model_info = joblib.load(file_path)

            # Mostrar la información del modelo en el área de visualización
            mostrar_info_modelo(file_path, loaded_model_info, text_data_display)

            # Limpiar la interfaz antes de cargar el modelo
            limpiar_interfaz(etiqueta_seleccionar, etiqueta_variable_x, etiqueta_variable_y,
                              button_regresion, button_guardar_modelo, label_mse,
                              label_ecuacion_recta, etiqueta_valor_x, valor_x_entry,
                              button_prediccion, resultado_prediccion, graph_canvas,
                              radiobuttons_var1, radiobuttons_var2)

            # Introducir el valor de x después de cargar el modelo
            introducir_valor_x(graph_canvas, radiobuttons_var1, radiobuttons_var2)

    except Exception as e:
        show_error(f"Error al cargar el modelo: {str(e)}")

def mostrar_info_modelo(file_path, loaded_model_info,text_data_display):
    """
    Muestra la información del modelo cargado en el área de visualización.

    Parámetros:
    - file_path (str): Ruta del archivo del modelo cargado.
    - loaded_model_info (ModeloInfo): Información del modelo cargado.
    - text_data_display (tk.scrolledtext.ScrolledText): Área de visualización de texto.

    Devuelve:
    - Ninguno
    """

    if text_data_display is not None:
        text_data_display.delete(1.0, tk.END)  # Limpiar el contenido actual

        # Mostrar información del modelo
        text_data_display.insert(tk.END, f"Modelo cargado con éxito desde: {file_path}\n")

        # Añadir información específica según la estructura del modelo
        if isinstance(loaded_model_info, ModeloInfo):
            text_data_display.insert(tk.END, f"Ecuación del modelo: {loaded_model_info.ecuacion_recta}\n")
            text_data_display.insert(tk.END, f"Error cuadrático medio (MSE): {loaded_model_info.mse}\n")
def introducir_valor_x(graph_canvas=None, radiobuttons_var1=None, radiobuttons_var2=None):
    """
    Introduce el valor de x en la interfaz.

    Parámetros:
    - graph_canvas: El canvas del gráfico.
    - radiobuttons_var1: Radiobuttons para la variable 1.
    - radiobuttons_var2: Radiobuttons para la variable 2.

    Devuelve:
    - Ninguno
    """


    global valor_x_entry, resultado_prediccion, etiqueta_valor_x, button_prediccion
    try:
        #Crear la etiqueta para indicar la variable x
        etiqueta_valor_x = tk.Label(window, text="")
        etiqueta_valor_x.place(relx=0.55, rely=0.8)
    
        if modelo_info is not None:
            etiqueta_valor_x.config(text=f"Seleccione el valor de {modelo_info.x}:")
        elif loaded_model_info is not None:
            etiqueta_valor_x.config(text=f"Seleccione el valor de {loaded_model_info.x}:")

        # Crear el cuadro de entrada para el valor de x
        valor_x_entry = tk.Entry(window, width=int(window_width * 0.01))
        valor_x_entry.place(relx=0.68, rely=0.8)
        valor_x_entry.bind("<Return>", obtener_valor_x)

        # Botón "Realizar Predicción"
        button_prediccion = tk.Button(window, text="Realizar Predicción", height=1, width=20, command= realizar_prediccion)
        button_prediccion.place(relx=0.55, rely=0.86)

        # Etiqueta para mostrar el resultado de la predicción
        resultado_prediccion = tk.Label(window, text="", width=int(window_width * 0.03), height=int(window_height * 0.002))
        resultado_prediccion.place(relx=0.68, rely=0.86)

    except Exception as e:
        show_error(f"Error al introducir el valor de x: {str(e)}")

def limpiar_interfaz(*widgets):
    """
    Limpia la interfaz de los widgets especificados.

    Parámetros:
    - *widgets: Lista variable de widgets a limpiar.

    Devuelve:
    - Ninguno
    """
    try:
        for widget in widgets:
            if widget:
                widget.destroy()

    except Exception as e:
        show_error(f"Error al limpiar la interfaz: {str(e)}")

def destruir_radiobuttons(radiobutton_list):
    """
    Destruye los Radiobuttons en la lista especificada.

    Parámetros:
    - radiobutton_list (list): Lista de Radiobuttons a destruir.

    Devuelve:
    - Ninguno
    """
    if radiobutton_list:
        for rad in radiobutton_list:
            rad.destroy()

def show_data_popup(df,text_data_display):
    """
    Muestra los datos del DataFrame en el área de visualización de texto.

    Parámetros:
    - df (pd.DataFrame): DataFrame de datos.
    - text_data_display (tk.scrolledtext.ScrolledText): Área de visualización de texto.

    Devuelve:
    - Ninguno
    """
    # Limpiar el contenido actual
    text_data_display.delete(1.0, tk.END) 

    # Obtener información sobre los datos
    headers = df.columns
    max_column_widths = [max(len(str(header)), df[header].astype(str).apply(len).max()) for header in headers]
    
    # Agregar encabezados al Text
    header_text = " | ".join(f"{header:<{width}}" for header, width in zip(headers, max_column_widths)) + "\n"
    text_data_display.insert(tk.END, header_text)

    # Agregar separador de columnas
    separator_line = "-" * sum(max_column_widths + [len(headers) - 1]) + "\n"
    text_data_display.insert(tk.END, separator_line)

    # Agregar filas al Text
    for _, row in df.iterrows():
        row_text = " | ".join(f"{str(value)[:width].center(width)}" for value, width in zip(row, max_column_widths)) + "\n"
        text_data_display.insert(tk.END, row_text)

def show_first_row(df):
    """
    Muestra la primera fila del DataFrame.

    Parámetros:
    - df (pd.DataFrame): DataFrame de datos.

    Devuelve:
    - Ninguno
    """
    primera_fila = df.iloc[0]
    row_text = "     ".join(f"{columna}" for columna, valor in primera_fila.items())

def show_error(message):
    """
    Muestra un mensaje de error en una ventana emergente.

    Parámetros:
    - message (str): Mensaje de error.

    Devuelve:
    - Ninguno
    """
    top = tk.Toplevel()
    top.title("Error")
    text = tk.Text(top)
    text.insert(tk.INSERT, message)
    text.pack()# Función para obtener el valor ingresado en el cuadro de texto

def show_info(message):
    """
    Muestra un mensaje de información en una ventana emergente.

    Parámetros:
    - message (str): Mensaje de información.

    Devuelve:
    - Ninguno
    """
    top = tk.Toplevel()
    top.title("Información")
    text = tk.Text(top)
    text.insert(tk.INSERT, message)
    text.pack()# Función para obtener el valor ingresado en el cuadro de texto

def Seleccionar():
    """
    Obtiene las variables seleccionadas por el usuario.

    Parámetros:
    - Ninguno

    Devuelve:
    - Tuple: Tupla con las variables seleccionadas (selected_variable_x, selected_variable_y).
    """
    selected_variable_x = var1.get()
    selected_variable_y = var2.get()
    return selected_variable_x, selected_variable_y

def obtener_valor_x(valor_x_entry,event=None):
    """
    Obtiene el valor ingresado en el cuadro de texto.

    Parámetros:
    - valor_x_entry (tk.Entry): Cuadro de texto para el valor de x.
    - event (tk.Event, opcional): Evento asociado al cuadro de texto.

    Devuelve:
    - str: Valor ingresado en el cuadro de texto.
    """
    valor_x = valor_x_entry.get()
    print(f"Valor de la variable x seleccionado: {valor_x}")
    return valor_x

def realizar_prediccion():
    """
    Realiza una predicción utilizando el modelo cargado.

    Parámetros:
    - Ninguno

    Devuelve:
    - Ninguno
    """
    global loaded_model_info, modelo_info, valor_x_entry, resultado_prediccion
    try:
        valor_x = obtener_valor_x(valor_x_entry,event=None)

        if loaded_model_info or modelo_info:
            # Seleccionar la información del modelo adecuada
            model_info = loaded_model_info if loaded_model_info else modelo_info

            # Calcular el valor y predicho
            valor_y = model_info.intercept + model_info.slope * float(valor_x)

            # Configurar el texto de la predicción
            resultado_prediccion.config(text=f"{valor_y} = {model_info.intercept} + {model_info.slope} * {valor_x}")
        else:
            show_error("Primero realiza una regresión lineal o carga un modelo antes de realizar predicciones.")

    except Exception as e:
        show_error(f"Error al realizar la predicción: {str(e)}")

def realizar_regresion_lineal(filename, variable_x, variable_y, auto=True):
    """
    Realiza la regresión lineal utilizando el archivo de datos y las variables especificadas.

    Parámetros:
    - filename (str): Ruta del archivo de datos.
    - variable_x (str): Nombre de la variable independiente (X).
    - variable_y (str): Nombre de la variable dependiente (Y).
    - auto (bool, opcional): Indica si se está utilizando el modo automático. Predeterminado es True.

    Devuelve:
    - Ninguno
    """
    global modelo_info, loaded_model_info
    try:
        #Restablecer loaded_model_info a None si se está creando un nuevo modelo
        if not auto:
            loaded_model_info = None

        #Crear modelo de regresión lineal  
        modelo = crear_modelo_regresion_lineal(filename, [variable_x], [variable_y])

        #Cargar datos y manejar valores NaN
        datos = mostrar_archivos(filename)
        imputer = SimpleImputer(strategy='mean')
        datos[[variable_x, variable_y]] = imputer.fit_transform(datos[[variable_x, variable_y]])

        #Extraer variables independientes (X) y dependientes (Y)
        X = datos[[variable_x]]
        y = datos[[variable_y]]

        #Etiquetas para el gráfico
        etiqueta_x = variable_x 
        etiqueta_y = variable_y 

        #Visualizar el modelo y crear etiquetas
        fig = visualizar_modelo(modelo, X, y, etiqueta_x, etiqueta_y)
        label_mse, label_ecuacion_recta = crear_etiquetas_resultados(modelo, X, y, variable_x, variable_y)

        #Integrar la figura en un Canvas de Tkinter
        graph_canvas = integrar_figura_en_canvas(fig)

        #Crear una instancia de ModeloInfo
        modelo_info = crear_modelo_info(modelo, variable_x, variable_y, X, y)

        # Crear el botón "Guardar Modelo"
        button_guardar_modelo = crear_boton_guardar_modelo()

        #Introducir valor de x si es necesario
        if auto:
            introducir_valor_x()
    except Exception as e:
        show_error(f"Error al realizar la regresión lineal: {str(e)}")

def crear_etiquetas_resultados(modelo, X, y, variable_x, variable_y):
    """
    Crea y muestra las etiquetas de resultados, incluida la ecuación de la recta y el error cuadrático medio.

    Parámetros:
    - modelo: Modelo de regresión lineal entrenado.
    - X: Variables independientes.
    - y: Variable dependiente.
    - variable_x: Nombre de la variable X.
    - variable_y: Nombre de la variable Y.

    Devuelve:
    - tuple: Etiquetas creadas para el error cuadrático medio y la ecuación de la recta.
    """
    label_mse = tk.Label(window, text="")
    label_mse.place(relx=0.55, rely=0.42)

    label_ecuacion_recta = tk.Label(window, text="")
    label_ecuacion_recta.place(relx=0.55, rely=0.45)

    ecuacion_recta =f"Ecuación de la recta:   {variable_y} = {float(modelo.intercept_):.2f} + {float(modelo.coef_[0][0]):.2f} * {variable_x}"
    label_ecuacion_recta.config(text=ecuacion_recta)
    window.update()

    label_mse.config(text=f"El error cuadrático medio (MSE) es: {mean_squared_error(y, modelo.predict(X))} y la bondad de ajuste (R²) es: {r2_score(y, modelo.predict(X))}")
    window.update()

    return label_mse, label_ecuacion_recta

def integrar_figura_en_canvas(fig):
    """
    Integra una figura de Matplotlib en un widget Canvas de Tkinter.

    Parámetros:
    - fig: Figura de Matplotlib.

    Devuelve:
    - FigureCanvasTkAgg: Objeto Canvas que contiene la figura.
    """
    graph_canvas = FigureCanvasTkAgg(fig, master=window)
    graph_canvas_widget = graph_canvas.get_tk_widget()
    graph_canvas_widget.place(relx=0.12, rely=0.42)
    
    return graph_canvas

def crear_modelo_info(modelo, variable_x, variable_y, X, y):
    """
    Crea una instancia de la clase ModeloInfo que contiene información del modelo.

    Parámetros:
    - modelo: Modelo de regresión lineal entrenado.
    - variable_x: Nombre de la variable X.
    - variable_y: Nombre de la variable Y.
    - X: Variables independientes.
    - y: Variable dependiente.

    Devuelve:
    - ModeloInfo: Instancia de la clase ModeloInfo.
    """
    ecuacion_recta = f"y = {float(modelo.intercept_)} + {float(modelo.coef_[0][0])} * {variable_x}"
    mse = mean_squared_error(y, modelo.predict(X))
    return ModeloInfo(variable_x, variable_y, modelo.intercept_, modelo.coef_, ecuacion_recta, mse)

def crear_boton_guardar_modelo():
    """
    Crea un botón para guardar el modelo.

    Devuelve:
    - Button: Botón para guardar el modelo.
    """
    button_guardar_modelo = tk.Button(window, text="Guardar Modelo", height=1, width=20, command=guardar_modelo)
    button_guardar_modelo.place(relx=0.01, rely=0.46)
    return button_guardar_modelo

def guardar_modelo():
    """
    Guarda el modelo actual en un archivo .joblib.

    Devuelve:
    - None
    """
    global modelo_info
    if modelo_info is None:
        show_error("Realiza la regresión lineal antes de intentar guardar el modelo.")
        return

    try:
        # Obtener la ruta y nombre de archivo seleccionados por el usuario
        file_path = filedialog.asksaveasfilename(defaultextension=".joblib", filetypes=[("Archivos joblib", "*.joblib")])

        if file_path:
            # Guardar la información del modelo en el archivo
            modelo_info.guardar_modelo(file_path)

            show_info(f"Modelo guardado en: {file_path}")

    except Exception as e:
        show_error(f"Error al guardar el modelo: {str(e)}")

def create_radiobuttons(window, variable, filename, y_position, command_callback):
    """
    Crea y muestra los botones de opción (radiobuttons) para seleccionar variables.

    Parámetros:
    - window: Ventana de Tkinter.
    - variable: Variable de control para los radiobuttons.
    - filename: Ruta del archivo de datos.
    - y_position: Posición en el eje Y donde se colocarán los radiobuttons.
    - command_callback: Función de retorno de llamada al seleccionar un radiobutton.

    Devuelve:
    - list: Lista de objetos Radiobutton creados.
    """
    radiobuttons = []

    # Obtener la primera fila del DataFrame
    primera_fila = get_first_row(filename)
    texto = ["longitude", 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'median_house_value', 'ocean_proximity']
    if primera_fila is not None:
        for i, (columna, value) in enumerate(primera_fila.items()):
            if i < len(texto):  # Asegurarse de que hay elementos en la lista 'texto'
                rad = Radiobutton(window, variable=variable, value=columna, text=texto[i], command=command_callback, font=("Helvetica", 8))
                rad.pack(side=LEFT)
                rad.place(relx=0.06+0.091*i, rely=y_position)
                radiobuttons.append(rad)
    else:
        print("Error al obtener la primera fila del archivo.")
    return radiobuttons

def get_first_row(filename):
    """
    Obtiene la primera fila del archivo de datos como un objeto de tipo pandas Series.

    Parámetros:
    - filename: Ruta del archivo de datos.

    Devuelve:
    - pandas.Series: Primera fila del archivo de datos.
    """
    df = mostrar_archivos(filename)
    if df is not None:
        primera_fila = df.iloc[0]
        return primera_fila
    else:
        return None

def calculate_percentage(value, percentage):
    """
    Calcula el porcentaje de un valor.

    Parámetros:
    - value: Valor al que se aplicará el porcentaje.
    - percentage: Porcentaje a aplicar.

    Devuelve:
    - int: Valor resultante después de aplicar el porcentaje.
    """
    return int((value * percentage) / 100)

def create_label(text, relx, rely, width_percentage, height_percentage):
    """
    Crea y muestra una etiqueta en la ventana.

    Parámetros:
    - text: Texto de la etiqueta.
    - relx: Posición relativa en el eje X.
    - rely: Posición relativa en el eje Y.
    - width_percentage: Ancho de la etiqueta como porcentaje de la ventana.
    - height_percentage: Altura de la etiqueta como porcentaje de la ventana.

    Devuelve:
    - Label: Objeto de etiqueta creado.
    """
    label = tk.Label(window, text=text, width=calculate_percentage(window_width, width_percentage),
                     height=calculate_percentage(window_height, height_percentage))
    label.place(relx=relx, rely=rely)
    return label

def create_button(text, command, relx, rely, width_percentage, height_percentage):
    """
    Crea y muestra un botón en la ventana.

    Parámetros:
    - text: Texto del botón.
    - command: Función de retorno de llamada al hacer clic en el botón.
    - relx: Posición relativa en el eje X.
    - rely: Posición relativa en el eje Y.
    - width_percentage: Ancho del botón como porcentaje de la ventana.
    - height_percentage: Altura del botón como porcentaje de la ventana.

    Devuelve:
    - Button: Objeto de botón creado.
    """
    button = tk.Button(window, text=text, command=command,
                       height=calculate_percentage(window_height, height_percentage),
                       width=calculate_percentage(window_width, width_percentage))
    button.place(relx=relx, rely=rely)
    return button

def create_scrolled_text(relx, rely, width_percentage, height_percentage):
    """
    Crea y muestra un widget de texto desplazable en la ventana.

    Parámetros:
    - relx: Posición relativa en el eje X.
    - rely: Posición relativa en el eje Y.
    - width_percentage: Ancho del widget como porcentaje de la ventana.
    - height_percentage: Altura del widget como porcentaje de la ventana.

    Devuelve:
    - ScrolledText: Objeto de widget de texto desplazable creado.
    """
    text_widget = scrolledtext.ScrolledText(window, wrap=tk.NONE,
                                            height=calculate_percentage(window_height, height_percentage),
                                            width=calculate_percentage(window_width, width_percentage),
                                            undo=True)
    text_widget.place(relx=relx, rely=rely)
    return text_widget

# Crear la ventana raíz
window = tk.Tk()
window.title('EXPLORADOR DE ARCHIVOS')

# Obtener el ancho y alto de la pantalla
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Establecer porcentajes para la geometría de la ventana
width_percentage = 100
height_percentage = 100

# Calcular el tamaño de la ventana en función de los porcentajes
window_width = calculate_percentage(screen_width, width_percentage)
window_height = calculate_percentage(screen_height, height_percentage)

# Crear la geometría de la ventana con porcentajes
window.geometry(f"{window_width}x{window_height}")

# Creación de los Radiobutton
var1 = StringVar()
var2 = StringVar()
# Establecer valores predeterminados
var1.set(' ')
var2.set(' ')

# Crear elementos de la interfaz gráfica con porcentajes
label_file_explorer = create_label("", 0.065, 0.025, 8, 0.25)
button_explore = create_button("Buscar Archivos", browse_files, 0.65, 0.03, 0.9, 0.18)
button_cargar_modelo = create_button("Cargar Modelo", cargar_modelo, 0.72, 0.03, 0.9, 0.18)
text_data_display = create_scrolled_text(0.035, 0.09, 10, 1.5)

#Etiquetas
etiqueta_ruta = create_label("RUTA", 0.03, 0.01, 0.5, 0.5)

# Iniciar la aplicación
window.mainloop()