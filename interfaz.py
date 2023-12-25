# Importación de librerías
import os
import json
import sqlite3
import joblib
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
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
 
# Variables globales
button_explore = None
selected_variable_x = None
selected_variable_y = None
label_coeficientes = None
label_intercepto = None
label_mse = None
label_r2 = None
text_data_display = None
modelo_info = None
loaded_model_info = None
etiqueta_seleccionar = None
etiqueta_variable_x = None
etiqueta_variable_y = None
radiobuttons_var1 = None
radiobuttons_var2 = None
button_regresion = None
button_guardar_modelo = None
modelo_regresion = None
graph_canvas = None
label_ecuacion_recta = None
etiqueta_valor_x = None
valor_x_entry = None
button_prediccion = None
resultado_prediccion = None
descripcion_entry = None
etiqueta_descripcion = None

def browse_files():
    global radiobuttons_var1, radiobuttons_var2
    filename = get_selected_filename()

    if filename:
        update_file_explorer_label(filename)

        df = mostrar_archivos(filename)
        show_data_popup(df)

        limpiar_interfaz()

        radiobuttons_var1 = create_radiobuttons(window, var1, filename, 0.355, Seleccionar)
        radiobuttons_var2 = create_radiobuttons(window, var2, filename, 0.38, Seleccionar)

        display_labels()

        create_regression_button(window, filename, var1, var2)

def get_selected_filename():
    return filedialog.askopenfilename(initialdir="/", title="Examinar", filetypes=(("Text files", "*.txt*"),
                                                                                   ("CSV files", "*.csv"),
                                                                                   ("Excel files", "*.xlsx"),
                                                                                   ("SQLite databases", "*.db"),
                                                                                   ("all files", "*.*")))

def update_file_explorer_label(filename): 
    label_file_explorer.config(text=f"{filename}")

def display_labels():
    global etiqueta_seleccionar, etiqueta_variable_x, etiqueta_variable_y
    etiqueta_seleccionar = tk.Label(window, text="Selecciona una variable x y una variable y:")
    etiqueta_seleccionar.place(relx=0.01, rely=0.328)

    etiqueta_variable_x = tk.Label(window, text="VARIABLE X:")
    etiqueta_variable_x.place(relx=0.01, rely=0.355)

    etiqueta_variable_y = tk.Label(window, text="VARIABLE Y:")
    etiqueta_variable_y.place(relx=0.01, rely=0.38)

def create_regression_button(window, filename, var1, var2):
    global button_regresion
    button_regresion = tk.Button(window, text="Realizar Regresión Lineal", height=1, width=20,
                                 command=lambda: handle_regression_process(filename, var1.get(), var2.get()))
    button_regresion.place(relx=0.01, rely=0.42)

def handle_regression_process(filename, var1_value, var2_value):
    """
    Función intermedia que maneja el proceso de regresión y luego muestra descripcion_entry.
    """
    # Lógica para realizar la regresión lineal (aquí puedes agregar tu función realizar_regresion_lineal)
    realizar_regresion_lineal(filename, var1_value, var2_value, auto=True)

    # Una vez completada la regresión lineal, se llama a la función para mostrar descripcion_entry
    introducir_descripcion()
   
def cargar_modelo():
    global loaded_model_info, selected_variable_x, selected_variable_y, valor_x_entry, resultado_prediccion, etiqueta_valor_x, button_prediccion, descripcion_entry
    
    try:
        # Preguntar al usuario por el archivo del modelo
        file_path = filedialog.askopenfilename(defaultextension=".joblib", filetypes=[("Archivos joblib", "*.joblib")])
        
        # Si el usuario selecciona un archivo
        if file_path:
            # Limpiar la interfaz y las variables relacionadas con el modelo anterior
            limpiar_interfaz_y_variables()
            
            # Si existe un Entry anterior para descripción, destruirlo
            if descripcion_entry:
                descripciones_guardadas[file_path] = descripcion_entry.get()
                descripcion_entry.destroy()
                descripcion_entry = None
            
            # Crear una nueva instancia de ModeloInfo y cargar el modelo
            loaded_model_info = ModeloInfo(None, None, None, None, None, None, None)
            loaded_model_info.cargar_modelo(file_path)
            
            # Establecer la descripción en loaded_model_info usando el file_path para recuperar la descripción correcta
            loaded_model_info.descripcion = descripciones_guardadas.get(file_path, "")
            
            # Guardar las descripciones actualizadas en el archivo
            guardar_descripcion(file_path, loaded_model_info.descripcion )
            
            # Mostrar detalles del modelo en la interfaz
            mostrar_info_modelo(file_path, loaded_model_info)
            
            # Introducir el valor de x para la predicción
            introducir_valor_x()

    except Exception as e:
        show_error(f"Error al cargar el modelo: {str(e)}")

# Ruta al archivo donde se almacenará la descripción
DESCRIPCIONES_FILE = "descripciones.json"

# Cargar las descripciones guardadas desde el archivo (si existe)
descripciones_guardadas = {}
if os.path.exists(DESCRIPCIONES_FILE):
    with open(DESCRIPCIONES_FILE, "r") as f:
        descripciones_guardadas = json.load(f)

def guardar_descripcion(ruta_archivo, descripcion):
    """
    Guarda la descripción asociada con una ruta de archivo dada.
    """
    # Actualizar el diccionario con la nueva descripción
    descripciones_guardadas[ruta_archivo] = descripcion
    
    # Guardar el diccionario actualizado en el archivo
    guardar_diccionario_descripciones()

def guardar_diccionario_descripciones():
    """
    Guarda el diccionario de descripciones en un archivo o en la ubicación deseada.
    """
    with open(DESCRIPCIONES_FILE, "w") as archivo:
        json.dump(descripciones_guardadas, archivo)

def limpiar_interfaz_y_variables():
    global etiqueta_descripcion, loaded_model_info, selected_variable_x, selected_variable_y, valor_x_entry, resultado_prediccion, etiqueta_valor_x, button_prediccion, descripcion_entry, graph_canvas, etiqueta_seleccionar, etiqueta_variable_x, etiqueta_variable_y, button_guardar_modelo, button_regresion, label_ecuacion_recta, label_mse
    try:
        # Limpia los widgets y variables globales relacionados con el modelo anterior
        if loaded_model_info:
            # Aquí, puedes agregar cualquier método necesario en tu clase ModeloInfo para limpiar sus atributos o estados.
            loaded_model_info = None
        
        # Limpia otros widgets y variables globales
        if valor_x_entry:
            valor_x_entry.destroy()
        if resultado_prediccion:
            resultado_prediccion.destroy()
        if etiqueta_valor_x:
            etiqueta_valor_x.destroy()
        if button_prediccion:
            button_prediccion.destroy()
        if graph_canvas:
            graph_canvas.get_tk_widget().destroy()
        if etiqueta_seleccionar:
            etiqueta_seleccionar.destroy()
        if etiqueta_variable_x:
            etiqueta_variable_x.destroy()
        if etiqueta_variable_y:
            etiqueta_variable_y.destroy()
        if button_regresion:
            button_regresion.destroy()
        if button_guardar_modelo:
            button_guardar_modelo.destroy()
        if label_ecuacion_recta:
            label_ecuacion_recta.destroy()
        if label_mse:
            label_mse.destroy()
        if etiqueta_descripcion:
            etiqueta_descripcion.destroy()
            etiqueta_descripcion = None

        # Destruir los Radiobuttons
        destruir_radiobuttons(radiobuttons_var1)
        destruir_radiobuttons(radiobuttons_var2)

    except Exception as e:
        show_error(f"Error al limpiar la interfaz: {str(e)}")

def mostrar_info_modelo(file_path, loaded_model_info):
    global text_data_display, button_guardar_modelo
    try:
        if text_data_display is not None:
            text_data_display.delete(1.0, tk.END)  # Limpiar el contenido actual
    
            # Mostrar información del modelo
            text_data_display.insert(tk.END, f"Modelo cargado con éxito desde: {file_path}\n")
    
            # Añadir información específica según la estructura del modelo
            if isinstance(loaded_model_info, ModeloInfo):
                text_data_display.insert(tk.END, f"Ecuación del modelo: {loaded_model_info.ecuacion_recta}\n")
                text_data_display.insert(tk.END, f"Error cuadrático medio (MSE): {loaded_model_info.mse}\n")
                text_data_display.insert(tk.END, f"Descripción: {loaded_model_info.descripcion}\n")

    except Exception as e:
        show_error(f"Error al mostrar la información del modelo: {str(e)}")

def introducir_valor_x():
    global valor_x_entry, resultado_prediccion, etiqueta_valor_x, button_prediccion
    try:
        etiqueta_valor_x = tk.Label(window, text="")
        etiqueta_valor_x.place(relx=0.55, rely=0.6)

        if modelo_info is not None:
            etiqueta_valor_x.config(text=f"Seleccione el valor de {modelo_info.x}:")
        elif loaded_model_info is not None:
            etiqueta_valor_x.config(text=f"Seleccione el valor de {loaded_model_info.x}:")

        # Crear el cuadro de entrada para el valor de x
        valor_x_entry = tk.Entry(window, width=int(window_width * 0.01))
        valor_x_entry.place(relx=0.72, rely=0.6)
        valor_x_entry.bind("<Return>", obtener_valor_x)

        # Botón "Realizar Predicción"
        button_prediccion = tk.Button(window, text="Realizar Predicción", height=1, width=20, command=realizar_prediccion)
        button_prediccion.place(relx=0.55, rely=0.55)

        # Etiqueta para mostrar el resultado de la predicción
        resultado_prediccion = tk.Label(window, text="", width=int(window_width * 0.04), height=int(window_height * 0.002))
        resultado_prediccion.place(relx=0.58, rely=0.49)

    except Exception as e:
       show_error(f"Error al introducir el valor de x: {str(e)}")

def introducir_descripcion():
    global descripcion_entry, etiqueta_descripcion

    etiqueta_descripcion = tk.Label(window, text="Introduce la descripción del modelo:")
    etiqueta_descripcion.place(relx=0.55, rely=0.7)

    # Crear el cuadro de entrada para la descripción
    descripcion_entry = tk.Entry(window, width=int(window_width * 0.03))
    descripcion_entry.place(relx=0.72, rely=0.7)
    descripcion_entry.bind("<Return>", obtener_descripcion)
 
def limpiar_interfaz():
    global radiobuttons_var1, radiobuttons_var2, etiqueta_seleccionar, etiqueta_variable_x, etiqueta_variable_y, button_regresion, button_guardar_modelo, label_mse, graph_canvas, selected_variable_x, selected_variable_y, etiqueta_valor_x, valor_x_entry, button_prediccion, resultado_prediccion, etiqueta_descripcion, descripcion_entry
    try:
        selected_variable_x = None
        selected_variable_y = None
    
        # Limpiar las variables de control de los Radiobuttons
        var1.set(' ')
        var2.set(' ')
    
        widgets_to_destroy = [etiqueta_seleccionar, etiqueta_variable_x, etiqueta_variable_y,
                            button_regresion, button_guardar_modelo, label_mse,
                            label_ecuacion_recta, etiqueta_valor_x, valor_x_entry,
                            button_prediccion, resultado_prediccion, etiqueta_descripcion, descripcion_entry]
    
        for widget in widgets_to_destroy:
            if widget is not None:
                widget.destroy()
        
        if graph_canvas:
            graph_canvas.get_tk_widget().destroy()

        # Destruir los Radiobuttons y el Graph_canvas
        destruir_radiobuttons(radiobuttons_var1)
        destruir_radiobuttons(radiobuttons_var2)
    
        # Limpiar las variables globales relacionadas con Radiobuttons
        radiobuttons_var1 = None
        radiobuttons_var2 = None
    
    except Exception as e:
        show_error(f"Error al limpiar la interfaz: {str(e)}")
 
def destruir_radiobuttons(radiobutton_list):
    try:
        if radiobutton_list:
            for rad in radiobutton_list:
                rad.destroy()

    except Exception as e:
        show_error(f"Error al destruir los Radiobuttons: {str(e)}")
 
def show_data_popup(df):
    global text_data_display  # Para acceder al widget Text desde otras funciones
    try:
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
        
    except Exception as e:
        show_error(f"Error al mostrar los datos: {str(e)}")
 
def show_first_row(df):
    try:
        primera_fila = df.iloc[0]
        row_text = "     ".join(f"{columna}" for columna, valor in primera_fila.items())

    except Exception as e:
        show_error(f"Error al mostras la primera fila: {str(e)}")
 
def show_error(message):
    try:
        top = tk.Toplevel()
        top.title("Error")
        text = tk.Text(top)
        text.insert(tk.INSERT, message)
        text.pack()# Función para obtener el valor ingresado en el cuadro de texto

    except Exception as e:
        print(f"Error al mostrar el mensaje de error: {str(e)}")
 
def show_info(message):
    try:
        top = tk.Toplevel()
        top.title("Información")
        text = tk.Text(top)
        text.insert(tk.INSERT, message)
        text.pack()# Función para obtener el valor ingresado en el cuadro de texto

    except Exception as e:
        print(f"Error al mostrar el mensaje de información: {str(e)}")
 
def Seleccionar():
    global selected_variable_x, selected_variable_y
    selected_variable_x = var1.get()
    selected_variable_y = var2.get()
    return selected_variable_x, selected_variable_y
 
def obtener_valor_x(event=None):
    global valor_x_entry
    valor_x = valor_x_entry.get()
    try:
        print(f"Valor de la variable x seleccionado: {valor_x}")
        return valor_x
    
    except ValueError:
        show_error("Por favor, ingrese un valor numérico para x.")
        return None
    
def obtener_descripcion(event=None):
    global descripcion_entry
    
    if descripcion_entry is not None:
        descripcion = descripcion_entry.get()
        if not descripcion:
            descripcion = ''
        return descripcion
    else:
        # Manejar el caso en el que descripcion_entry es None
        return ''

 
def realizar_prediccion():
    global resultado_prediccion
 
    try:
        valor_x = obtener_valor_x(event=None)
 
        if loaded_model_info or modelo_info:
            # Seleccionar la información del modelo adecuada
            model_info = loaded_model_info if loaded_model_info else modelo_info
 
            # Calcular el valor y predicho
            valor_y = model_info.intercept + model_info.slope * float(valor_x)
 
            # Configurar el texto de la predicción
            resultado_prediccion.config(text=f"{model_info.y}={valor_y} = {model_info.intercept} + {model_info.slope} * {valor_x}")
        else:
            show_error("Primero realiza una regresión lineal o carga un modelo antes de realizar predicciones.")

    except ValueError:
        show_error(f"Por favor, ingrese un valor numérico para realizar la predicción.") 

    except Exception as e:
        show_error(f"Error al realizar la predicción: {str(e)}")
 
def realizar_regresion_lineal(filename, variable_x, variable_y, auto=True):
    global label_mse, button_guardar_modelo, modelo_info, graph_canvas, label_ecuacion_recta, loaded_model_info, descripcion_entry, etiqueta_descripcion
    try:
        # Restablecer loaded_model_info a None si se está creando un nuevo modelo
        if not auto:
            loaded_model_info = None
 
        modelo = crear_modelo_regresion_lineal(filename, [variable_x], [variable_y])

        #Cargar datos y manejar valores NaN
        datos = mostrar_archivos(filename)
        imputer = SimpleImputer(strategy='mean')
        datos[[variable_x, variable_y]] = imputer.fit_transform(datos[[variable_x, variable_y]])
 
        X = datos[[variable_x]]
        y = datos[[variable_y]]
 
        etiqueta_x = variable_x
        etiqueta_y = variable_y
 
        fig = visualizar_modelo(modelo, X, y, etiqueta_x, etiqueta_y)
 
        # Crear o actualizar las etiquetas con los resultados
        label_mse, label_ecuacion_recta = crear_etiquetas_resultados(modelo, X, y, variable_x, variable_y)
 
        # Integrar la figura en un Canvas de Tkinter
        graph_canvas = integrar_figura_en_canvas(fig)
 
        introducir_descripcion()
 
        # Crear una instancia de ModeloInfo
        modelo_info = crear_modelo_info(modelo, variable_x, variable_y, X, y)
 
        # Crear el botón "Realizar Regresión Lineal"
        button_guardar_modelo = crear_boton_guardar_modelo()
 
        introducir_valor_x()              
 
    except Exception as e:
        show_error(f"Error al realizar la regresión lineal: {str(e)}")
 
def crear_etiquetas_resultados(modelo, X, y, variable_x, variable_y):
    try:
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
    
    except Exception as e:
        show_error(f"Error al crear etiquetas de resultados: {str(e)}")
 
def integrar_figura_en_canvas(fig):
    try:
        graph_canvas = FigureCanvasTkAgg(fig, master=window)
        graph_canvas_widget = graph_canvas.get_tk_widget()
        graph_canvas_widget.place(relx=0.12, rely=0.42)
    
        return graph_canvas

    except Exception as e:
        show_error(f"Error al integrar la figura en el Canvas: {str(e)}")
 
def crear_modelo_info(modelo, variable_x, variable_y, X, y):
    try:
        ecuacion_recta = f"y = {float(modelo.intercept_)} + {float(modelo.coef_[0][0])} * {variable_x}"
        mse = mean_squared_error(y, modelo.predict(X))
        descripcion = obtener_descripcion()
        return ModeloInfo(variable_x, variable_y, modelo.intercept_, modelo.coef_, ecuacion_recta, mse, descripcion)

    except Exception as e:
        show_error(f"Error al crear modelo info: {str(e)}")
 
def crear_boton_guardar_modelo():
    try:
        button_guardar_modelo = tk.Button(window, text="Guardar Modelo", height=1, width=20, command=guardar_modelo)
        button_guardar_modelo.place(relx=0.01, rely=0.46)

        return button_guardar_modelo

    except Exception as e:
        show_error(f"Error al crear el botón para guardar el modelo: {str(e)}")
 
def guardar_modelo():
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
    radiobuttons = []

    #Definir los nombres de las columnas
    texto = ["longitude", 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'median_house_value', 'ocean_proximity']

    try:
        # Obtener la primera fila del DataFrame
        primera_fila = get_first_row(filename)

        if primera_fila is not None:
            for i, (columna, value) in enumerate(primera_fila.items()):
                if i < len(texto):  # Asegurarse de que hay elementos en la lista 'texto'
                    rad = Radiobutton(window, variable=variable, value=columna, text=texto[i], command=command_callback, font=("Helvetica", 8))
                    rad.pack(side=LEFT)
                    rad.place(relx=0.06+0.091*i, rely=y_position)
                    radiobuttons.append(rad)
        else:
            print("Error al obtener la primera fila del archivo.")
    
    except Exception as e:
        show_error(f"Error al crear radiobuttons: {str(e)}")
    
    return radiobuttons
 
def get_first_row(filename):
    try:
        df = mostrar_archivos(filename)
        return df.iloc[0] if df is not None else None
    
    except Exception as e:
        show_error(f"Error al obtener la primera fila del archivo: {str(e)}")
        return None
 
def calculate_percentage(value, percentage):
    return int((value * percentage) / 100)
 
def create_label(text, relx, rely, width_percentage, height_percentage):
    label = tk.Label(window, text=text, width=calculate_percentage(window_width, width_percentage),
                     height=calculate_percentage(window_height, height_percentage))
    label.place(relx=relx, rely=rely)
    return label
 
def create_button(text, command, relx, rely, width_percentage, height_percentage):
    button = tk.Button(window, text=text, command=command,
                       height=calculate_percentage(window_height, height_percentage),
                       width=calculate_percentage(window_width, width_percentage))
    button.place(relx=relx, rely=rely)
    return button
 
def create_scrolled_text(relx, rely, width_percentage, height_percentage):
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