#Importación de librerías
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
label_mse = None
graph_canvas = None
label_ecuacion_recta = None
etiqueta_seleccion_valor_x = None
valor_x_entry = None
boton_confirmar_valor_x = None

def browse_files():
    global selected_variable_x, selected_variable_y, filename, button_regresion, radiobuttons_var1, radiobuttons_var2
    global etiqueta_seleccionar, etiqueta_variable_x, etiqueta_variable_y  # Agregando la declaración global

    filename = filedialog.askopenfilename(initialdir="/", title="Examinar", filetypes=(("Text files", "*.txt*"), 
                                                                                       ("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("SQLite databases", "*.db"), ("all files", "*.*")))

    if filename:  # Verificar si se seleccionó un archivo
        label_file_explorer.config(text=f"{filename}")
        label_file_explorer.config(text=f"{filename}")
        
        df = mostrar_archivos(filename)
        show_data_popup(df)

        # Limpiar Radiobuttons antes de crear nuevos
        limpiar_interfaz()

        radiobuttons_var1 = create_radiobuttons(window, var1, filename, 0.355, Seleccionar)
        radiobuttons_var2 = create_radiobuttons(window, var2, filename, 0.38, Seleccionar)

        # Restablecer las variables seleccionadas
        selected_variable_x = None
        selected_variable_y = None

    etiqueta_seleccionar = tk.Label(window, text="Selecciona una variable x y una variable y:")
    etiqueta_seleccionar.place(relx=0.01, rely=0.328)
    etiqueta_seleccionar.config(bg="#bcdbf3")

    etiqueta_variable_x = tk.Label(window, text="VARIABLE X:")
    etiqueta_variable_x.place(relx=0.01, rely=0.355)
    etiqueta_variable_x.config(bg="#bcdbf3")

    etiqueta_variable_y = tk.Label(window, text="VARIABLE Y:")
    etiqueta_variable_y.place(relx=0.01, rely=0.38)
    etiqueta_variable_y.config(bg="#bcdbf3")

    # Crear el botón "Realizar Regresión Lineal"
    button_regresion = tk.Button(window, text="Realizar Regresión Lineal", height=1, width=20)
    button_regresion["command"] = lambda: realizar_regresion_lineal(filename, selected_variable_x, selected_variable_y, auto=True)
    button_regresion.place(relx=0.4, rely=0.402)

def cargar_modelo():
    global loaded_model_info, text_data_display, button_guardar_modelo
    global selected_variable_x, selected_variable_y, valor_x_entry

    try:
        file_path = filedialog.askopenfilename(defaultextension=".joblib", filetypes=[("Archivos joblib", "*.joblib")])

        if file_path:
            loaded_model_info = joblib.load(file_path)

            # Mostrar información del modelo en el widget Text
            if text_data_display is not None:
                text_data_display.delete(1.0, tk.END)  # Limpiar el contenido actual

                # Mostrar información del modelo
                text_data_display.insert(tk.END, f"Modelo cargado con éxito desde: {file_path}\n")

                # Añadir información específica según la estructura del modelo
                if isinstance(loaded_model_info, ModeloInfo):
                    text_data_display.insert(tk.END, f"Ecuación del modelo: {loaded_model_info.ecuacion_recta}\n")
                    text_data_display.insert(tk.END, f"Error cuadrático medio (MSE): {loaded_model_info.mse}\n")

                # Limpiar la interfaz antes de cargar el modelo
                limpiar_interfaz()

                # Restablecer button_guardar_modelo a None
                button_guardar_modelo = None

                # Restablecer las variables seleccionadas
                selected_variable_x = None
                selected_variable_y = None

                # Crear la etiqueta "Seleccione el valor de x"
                etiqueta_seleccion_valor_x = tk.Label(window, text=f"Seleccione el valor de {loaded_model_info.x}:")
                etiqueta_seleccion_valor_x.place(relx=0.01, rely=0.42)
                etiqueta_seleccion_valor_x.config(bg="#bcdbf3")

                # Crear el cuadro de entrada para el valor de x
                valor_x_entry = tk.Entry(window, width=int(window_width * 0.01))
                valor_x_entry.place(relx=0.18, rely=0.42)
                valor_x_entry.bind("<Return>", obtener_valor_x)                

    except Exception as e:
        show_error(f"Error al cargar el modelo: {str(e)}")

def limpiar_interfaz():
    global radiobuttons_var1, radiobuttons_var2, etiqueta_seleccionar, etiqueta_variable_x, etiqueta_variable_y, button_regresion, button_guardar_modelo, label_mse, graph_canvas, selected_variable_x, selected_variable_y, etiqueta_seleccion_valor_x, valor_x_entry, boton_confirmar_valor_x

    selected_variable_x = None
    selected_variable_y = None

    if etiqueta_seleccionar:
        etiqueta_seleccionar.destroy()
    if etiqueta_variable_x:
        etiqueta_variable_x.destroy()
    if etiqueta_variable_y:
        etiqueta_variable_y.destroy()
    if radiobuttons_var1:
        for rad in radiobuttons_var1:
            rad.destroy()
    if radiobuttons_var2:
        for rad in radiobuttons_var2:
            rad.destroy()
    if button_regresion:
        button_regresion.destroy()
    if button_guardar_modelo:
        button_guardar_modelo.destroy()
    if label_mse:
        label_mse.destroy()
    if graph_canvas:
        graph_canvas.get_tk_widget().destroy()
    if label_ecuacion_recta:
        label_ecuacion_recta.destroy()
    if etiqueta_seleccion_valor_x:
        etiqueta_seleccion_valor_x.destroy()
    if valor_x_entry:
        valor_x_entry.destroy()
    if boton_confirmar_valor_x:
        boton_confirmar_valor_x.destroy()


    # Limpiar las variables globales relacionadas con Radiobuttons
    radiobuttons_var1 = None
    radiobuttons_var2 = None

def show_data_popup(df):
    global text_data_display  # Para acceder al widget Text desde otras funciones
    text_data_display.delete(1.0, tk.END)  # Limpiar el contenido actual
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



#Función para seleccionar las columnas de los datos que se usarán como entradas y salida del modelo
def Seleccionar():
    global selected_variable_x, selected_variable_y, valor_x_entry
    selected_variable_x = var1.get()
    selected_variable_y = var2.get()

    # Crear la etiqueta "Seleccione el valor de x"
    etiqueta_seleccion_valor_x = tk.Label(window, text=f"Seleccione el valor de {selected_variable_x}:")
    etiqueta_seleccion_valor_x.place(relx=0.01, rely=0.42)
    etiqueta_seleccion_valor_x.config(bg="#bcdbf3")

    # Crear el cuadro de entrada para el valor de x
    valor_x_entry = tk.Entry(window, width=int(window_width * 0.01))
    valor_x_entry.place(relx=0.18, rely=0.42)
    valor_x_entry.bind("<Return>", obtener_valor_x)

    print(selected_variable_x)
    print(selected_variable_y)
    print()

def obtener_valor_x(event=None):
    global valor_x_entry
    valor_x = valor_x_entry.get()
    print(f"Valor de la variable x seleccionado: {valor_x}")

def realizar_regresion_lineal(filename, variable_x, variable_y, auto=True):
    global label_mse, button_guardar_modelo, modelo_info, graph_canvas, label_ecuacion_recta 
    try:
        # Restablecer loaded_model_info a None si se está creando un nuevo modelo
        if not auto:
            loaded_model_info = None

        modelo = crear_modelo_regresion_lineal(filename, [variable_x], [variable_y])
        datos = mostrar_archivos(filename)

        # Imputar valores NaN
        imputer = SimpleImputer(strategy='mean')
        datos[[variable_x, variable_y]] = imputer.fit_transform(datos[[variable_x, variable_y]])

        X = datos[[variable_x]]
        y = datos[[variable_y]]
        fig = visualizar_modelo(modelo, X, y, [variable_x])

        # Crear o actualizar las etiquetas con los resultados
        if label_mse is None:
            label_mse = tk.Label(window, text="")
            label_mse.place(relx=0.315, rely=0.435)
        
        if label_ecuacion_recta is None:
            label_ecuacion_recta = tk.Label(window, text="")
            label_ecuacion_recta.place(relx=0.315, rely=0.46)

        ecuacion_recta =f"Ecuación de la recta: y = {float(modelo.intercept_):.2f} + {float(modelo.coef_[0][0]):.2f} * X"
        label_ecuacion_recta.config(text=ecuacion_recta)
        window.update()

        label_mse.config(text=f"El error cuadrático medio (MSE) es: {mean_squared_error(y, modelo.predict(X))} y la bondad de ajuste (R²) es: {r2_score(y, modelo.predict(X))}")
        window.update()

        # Integrar la figura en un Canvas de Tkinter
        graph_canvas = FigureCanvasTkAgg(fig, master=window)
        graph_canvas_widget = graph_canvas.get_tk_widget()
        graph_canvas_widget.place(relx=0.3, rely=0.48)

        # Crear una instancia de ModeloInfo
        ecuacion_recta = f"y = {float(modelo.intercept_)} + {float(modelo.coef_[0][0])} * {variable_x}"
        mse = mean_squared_error(y, modelo.predict(X))
        modelo_info = ModeloInfo(variable_x, variable_y, ecuacion_recta, mse)

        # Crear el botón "Realizar Regresión Lineal"
        button_guardar_modelo = tk.Button(window, text="Guardar Modelo", height=1, width=20, command=guardar_modelo)
        button_guardar_modelo.place(relx=0.51, rely=0.402)
    
    except Exception as e:
        show_error(f"Error al realizar la regresión lineal: {str(e)}")

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

            show_error(f"Modelo guardado en: {file_path}")

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
                rad.config(bg="#bcdbf3")
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
window_width = int((screen_width * width_percentage) / 100)
window_height = int((screen_height * height_percentage) / 100)

# Crear la geometría de la ventana con porcentajes
window.geometry(f"{window_width}x{window_height}")

window.config(bg="#bcdbf3")

# Creación de los Radiobutton
var1 = StringVar()
var2 = StringVar()
# Establecer valores predeterminados
var1.set(' ')
var2.set(' ')

# Crear elementos de la interfaz gráfica con porcentajes
label_file_explorer = tk.Label(window, text="", width=int(window_width * 0.08), height=int(window_height * 0.0025), fg="black", bg="#d9ffdf")
button_explore = tk.Button(window, text="Buscar Archivos", command=browse_files, height=int(window_height * 0.0018), width=int(window_width * 0.009))

# Organizar elementos en la ventana con porcentajes
label_file_explorer.place(relx=0.065, rely=0.025)
button_explore.place(relx=0.65, rely=0.03)

#Botón cargar modelo
button_cargar_modelo = tk.Button(window, text="Cargar Modelo", command=cargar_modelo, height=int(window_height * 0.0018), width=int(window_width * 0.009))
button_cargar_modelo.place(relx=0.72, rely=0.03)  

# Crear un widget Text para mostrar los datos
text_data_display = scrolledtext.ScrolledText(window, wrap=tk.NONE, height=int(window_height * 0.015), width=int(window_width * 0.1), undo=True)
#text_data_display.config(font=("Helvetica", 10))
text_data_display.place(relx=0.035, rely=0.09)

#Etiquetas
etiqueta_ruta = tk.Label(window, text="RUTA", width=int(window_width * 0.005), height=int(window_height * 0.005))
etiqueta_ruta.place(relx=0.03, rely=0.01)  # Posición en porcentaje
etiqueta_ruta.config(bg="#bcdbf3")


# Iniciar la aplicación
window.mainloop()     