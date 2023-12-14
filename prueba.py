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


def browse_files():
    filename = filedialog.askopenfilename(initialdir="/", title="Examinar", filetypes=(("Text files", "*.txt*"), 
                                                                                       ("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("SQLite databases", "*.db"), ("all files", "*.*")))
    if filename:
        label_file_explorer.config(text=f"{filename}")

        df = mostrar_archivos(filename)
        show_data_popup(df)

        limpiar_interfaz()

        radiobuttons_var1 = create_radiobuttons(window, var1, filename, 0.355, Seleccionar)
        radiobuttons_var2 = create_radiobuttons(window, var2, filename, 0.38, Seleccionar)

        etiqueta_seleccionar = tk.Label(window, text="Selecciona una variable x y una variable y:")
        etiqueta_seleccionar.place(relx=0.01, rely=0.328)

        etiqueta_variable_x = tk.Label(window, text="VARIABLE X:")
        etiqueta_variable_x.place(relx=0.01, rely=0.355)

        etiqueta_variable_y = tk.Label(window, text="VARIABLE Y:")
        etiqueta_variable_y.place(relx=0.01, rely=0.38)

        button_regresion = tk.Button(window, text="Realizar Regresión Lineal", height=1, width=20, command=lambda: realizar_regresion_lineal(filename, var1.get(), var2.get(), auto=True))
        button_regresion.place(relx=0.01, rely=0.42)

def cargar_modelo():
    try:
        file_path = filedialog.askopenfilename(defaultextension=".joblib", filetypes=[("Archivos joblib", "*.joblib")])

        if file_path:
            loaded_model_info = joblib.load(file_path)
            mostrar_info_modelo(file_path, loaded_model_info)
            limpiar_interfaz()
            introducir_valor_x()               

    except Exception as e:
        show_error(f"Error al cargar el modelo: {str(e)}")

def mostrar_info_modelo(file_path, loaded_model_info):
    if text_data_display is not None:
        text_data_display.delete(1.0, tk.END)

        text_data_display.insert(tk.END, f"Modelo cargado con éxito desde: {file_path}\n")

        if isinstance(loaded_model_info, ModeloInfo):
            text_data_display.insert(tk.END, f"Ecuación del modelo: {loaded_model_info.ecuacion_recta}\n")
            text_data_display.insert(tk.END, f"Error cuadrático medio (MSE): {loaded_model_info.mse}\n")

def introducir_valor_x():
    etiqueta_valor_x = tk.Label(window, text="")
    etiqueta_valor_x.place(relx=0.55, rely=0.8)

    if modelo_info is not None:
        etiqueta_valor_x.config(text=f"Seleccione el valor de {modelo_info.x}:")
    elif loaded_model_info is not None:
        etiqueta_valor_x.config(text=f"Seleccione el valor de {loaded_model_info.x}:")

    valor_x_entry = tk.Entry(window, width=int(window_width * 0.01))
    valor_x_entry.place(relx=0.68, rely=0.8)
    valor_x_entry.bind("<Return>", lambda event: obtener_valor_x(valor_x_entry))

    button_prediccion = tk.Button(window, text="Realizar Predicción", height=1, width=20, command=lambda: realizar_prediccion(modelo_info, loaded_model_info, valor_x_entry))
    button_prediccion.place(relx=0.55, rely=0.86)

    resultado_prediccion = tk.Label(window, text="", width=int(window_width * 0.03), height=int(window_height * 0.002))
    resultado_prediccion.place(relx=0.68, rely=0.86)

def limpiar_interfaz():
    widgets_to_destroy = [etiqueta_seleccionar, etiqueta_variable_x, etiqueta_variable_y,
                          button_regresion, button_guardar_modelo, label_mse,
                          label_ecuacion_recta, etiqueta_valor_x, valor_x_entry,
                          button_prediccion, resultado_prediccion]

    for widget in widgets_to_destroy:
        if widget:
            widget.destroy()

    destruir_radiobuttons(radiobuttons_var1)
    destruir_radiobuttons(radiobuttons_var2)

    if graph_canvas:
        graph_canvas.get_tk_widget().destroy()

    radiobuttons_var1 = None
    radiobuttons_var2 = None

def destruir_radiobuttons(radiobutton_list):
    if radiobutton_list:
        for rad in radiobutton_list:
            rad.destroy()
def show_data_popup(df):
    global text_data_display  # Para acceder al widget Text desde otras funciones

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
    primera_fila = df.iloc[0]
    row_text = "     ".join(f"{columna}" for columna, valor in primera_fila.items())

def show_error(message):
    top = tk.Toplevel()
    top.title("Error")
    text = tk.Text(top)
    text.insert(tk.INSERT, message)
    text.pack()# Función para obtener el valor ingresado en el cuadro de texto

def show_info(message):
    top = tk.Toplevel()
    top.title("Información")
    text = tk.Text(top)
    text.insert(tk.INSERT, message)
    text.pack()# Función para obtener el valor ingresado en el cuadro de texto

#Función para seleccionar las columnas de los datos que se usarán como entradas y salida del modelo
def Seleccionar():
    global selected_variable_x, selected_variable_y
    selected_variable_x = var1.get()
    selected_variable_y = var2.get()

    print(selected_variable_x)
    print(selected_variable_y)
    print()

def obtener_valor_x(event=None):
    global valor_x_entry
    valor_x = valor_x_entry.get()
    print(f"Valor de la variable x seleccionado: {valor_x}")
    return valor_x

def realizar_prediccion(modelo_info, loaded_model_info, valor_x_entry):
    try:
        valor_x = obtener_valor_x(valor_x_entry)

        if loaded_model_info or modelo_info:
            model_info = loaded_model_info if loaded_model_info else modelo_info
            valor_y = model_info.intercept + model_info.slope * float(valor_x)
            resultado_prediccion.config(text=f"{valor_y} = {model_info.intercept} + {model_info.slope} * {valor_x}")
        else:
            show_error("Primero realiza una regresión lineal o carga un modelo antes de realizar predicciones.")

    except Exception as e:
        show_error(f"Error al realizar la predicción: {str(e)}")

def realizar_regresion_lineal(filename, variable_x, variable_y, auto=True):
    try:
        if not auto:
            loaded_model_info = None

        modelo = crear_modelo_regresion_lineal(filename, [variable_x], [variable_y])
        datos = mostrar_archivos(filename)

        imputer = SimpleImputer(strategy='mean')
        datos[[variable_x, variable_y]] = imputer.fit_transform(datos[[variable_x, variable_y]])

        X = datos[[variable_x]]
        y = datos[[variable_y]]

        etiqueta_x = variable_x 
        etiqueta_y = variable_y 

        fig = visualizar_modelo(modelo, X, y, etiqueta_x, etiqueta_y)

        label_mse, label_ecuacion_recta = crear_etiquetas_resultados(modelo, X, y, variable_x, variable_y)

        graph_canvas = integrar_figura_en_canvas(fig)

        modelo_info = crear_modelo_info(modelo, variable_x, variable_y, X, y)

        button_guardar_modelo = crear_boton_guardar_modelo()

        introducir_valor_x()               

    except Exception as e:
        show_error(f"Error al realizar la regresión lineal: {str(e)}")

def crear_etiquetas_resultados(modelo, X, y, variable_x, variable_y):
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
    graph_canvas = FigureCanvasTkAgg(fig, master=window)
    graph_canvas_widget = graph_canvas.get_tk_widget()
    graph_canvas_widget.place(relx=0.12, rely=0.42)
    
    return graph_canvas

def crear_modelo_info(modelo, variable_x, variable_y, X, y):
    ecuacion_recta = f"y = {float(modelo.intercept_)} + {float(modelo.coef_[0][0])} * {variable_x}"
    mse = mean_squared_error(y, modelo.predict(X))
    return ModeloInfo(variable_x, variable_y, modelo.intercept_, modelo.coef_, ecuacion_recta, mse)

def crear_boton_guardar_modelo():
    button_guardar_modelo = tk.Button(window, text="Guardar Modelo", height=1, width=20, command=guardar_modelo)
    button_guardar_modelo.place(relx=0.01, rely=0.46)
    return button_guardar_modelo

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
    df = mostrar_archivos(filename)
    if df is not None:
        primera_fila = df.iloc[0]
        return primera_fila
    else:
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



     