import tkinter as tk
from tkinter import filedialog, scrolledtext, StringVar, LEFT
from tkinter.ttk import Radiobutton, Button
from tkinter.ttk import Button as ttkButton
from tkinter import Label

import pandas as pd
import joblib
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from leer_archivos import mostrar_archivos
from regresion_lineal import crear_modelo_regresion_lineal, visualizar_modelo
from clase_modelo import ModeloInfo

class RegresionLinealApp:
    def __init__(self, root):
        self.root = root
        self.root.title('EXPLORADOR DE ARCHIVOS')
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.width_percentage = 100
        self.height_percentage = 100
        self.window_width = self.calculate_percentage(self.screen_width, self.width_percentage)
        self.window_height = self.calculate_percentage(self.screen_height, self.height_percentage)

        # Crear variables de control
        self.var1 = StringVar()
        self.var2 = StringVar()
        self.var1.set(' ')
        self.var2.set(' ')

        # Inicializar otros atributos
        self.filename = None
        self.modelo_info = None
        self.loaded_model_info = None
        self.graph_canvas = None
        self.etiqueta_seleccionar = None
        self.etiqueta_variable_x = None
        self.etiqueta_variable_y = None

        self.create_widgets()
    def clear_interface(self):
        # Lista de atributos que se deben destruir
        widgets_to_destroy = [
            self.etiqueta_seleccionar,
            self.etiqueta_variable_x,
            self.etiqueta_variable_y,
            self.button_regresion,  # Agrega otros atributos que desees destruir
            self.button_guardar_modelo,
            self.label_mse,
            self.label_ecuacion_recta,
            self.etiqueta_valor_x,
            self.valor_x_entry,
            self.button_prediccion,
            self.resultado_prediccion,
            # ... (otros atributos que necesites destruir)
        ]

        # Destruir cada widget en la lista si existe
        for widget in widgets_to_destroy:
            if widget:
                widget.destroy()

        # Destruir radiobuttons_var1 y radiobuttons_var2 si existen
        self.destruir_radiobuttons(self.radiobuttons_var1)
        self.destruir_radiobuttons(self.radiobuttons_var2)

        # Destruir el gráfico si existe
        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()

        # Restablecer atributos a None
        self.radiobuttons_var1 = None
        self.radiobuttons_var2 = None

    def create_widgets(self):
        self.label_file_explorer = self.create_label("", 0.065, 0.025, 8, 0.25)
        self.button_explore = self.create_button("Buscar Archivos", self.browse_files, 0.65, 0.03, 0.9, 0.18)
        self.button_cargar_modelo = self.create_button("Cargar Modelo", self.cargar_modelo, 0.72, 0.03, 0.9, 0.18)
        self.text_data_display = self.create_scrolled_text(0.035, 0.09, 10, 1.5)

        # Otras etiquetas y botones pueden agregarse aquí según sea necesario

    def browse_files(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Examinar",
                                                   filetypes=(("Text files", "*.txt*"),
                                                              ("CSV files", "*.csv"),
                                                              ("Excel files", "*.xlsx"),
                                                              ("SQLite databases", "*.db"),
                                                              ("all files", "*.*")))
        if self.filename:
            self.label_file_explorer.config(text=f"{self.filename}")
            df = mostrar_archivos(self.filename)
            self.show_data_popup(df)
            self.clear_interface()

            self.radiobuttons_var1 = self.create_radiobuttons(self.root, self.var1, 0.355, self.Seleccionar)
            self.radiobuttons_var2 = self.create_radiobuttons(self.root, self.var2, 0.38, self.Seleccionar)

    def show_data_popup(self, df):
        self.text_data_display.delete(1.0, tk.END)
        headers = df.columns
        max_column_widths = [max(len(str(header)), df[header].astype(str).apply(len).max()) for header in headers]
        
        header_text = " | ".join(f"{header:<{width}}" for header, width in zip(headers, max_column_widths)) + "\n"
        self.text_data_display.insert(tk.END, header_text)

        separator_line = "-" * sum(max_column_widths + [len(headers) - 1]) + "\n"
        self.text_data_display.insert(tk.END, separator_line)

        for _, row in df.iterrows():
            row_text = " | ".join(f"{str(value)[:width].center(width)}" for value, width in zip(row, max_column_widths)) + "\n"
            self.text_data_display.insert(tk.END, row_text)

    def cargar_modelo(self):
        try:
            file_path = filedialog.askopenfilename(defaultextension=".joblib", filetypes=[("Archivos joblib", "*.joblib")])

            if file_path:
                self.loaded_model_info = joblib.load(file_path)
                self.mostrar_info_modelo(file_path, self.loaded_model_info)

                self.clear_interface()
                self.introducir_valor_x()

        except Exception as e:
            self.show_error(f"Error al cargar el modelo: {str(e)}")

    def mostrar_info_modelo(self, file_path, loaded_model_info):
        if self.text_data_display is not None:
            self.text_data_display.delete(1.0, tk.END)
            self.text_data_display.insert(tk.END, f"Modelo cargado con éxito desde: {file_path}\n")

            if isinstance(loaded_model_info, ModeloInfo):
                self.text_data_display.insert(tk.END, f"Ecuación del modelo: {loaded_model_info.ecuacion_recta}\n")
                self.text_data_display.insert(tk.END, f"Error cuadrático medio (MSE): {loaded_model_info.mse}\n")
    def introducir_valor_x(self):
        if self.modelo_info is not None:
            variable_name = self.modelo_info.x
        elif self.loaded_model_info is not None:
            variable_name = self.loaded_model_info.x
        else:
            variable_name = "Variable X"

        etiqueta_valor_x = tk.Label(self.root, text=f"Seleccione el valor de {variable_name}:")
        etiqueta_valor_x.place(relx=0.55, rely=0.8)

        # Crear el cuadro de entrada para el valor de x
        valor_x_entry = tk.Entry(self.root, width=int(self.window_width * 0.01))
        valor_x_entry.place(relx=0.68, rely=0.8)
        valor_x_entry.bind("<Return>", self.obtener_valor_x)

        # Botón "Realizar Predicción"
        button_prediccion = tk.Button(self.root, text="Realizar Predicción", height=1, width=20, command=self.realizar_prediccion)
        button_prediccion.place(relx=0.55, rely=0.86)

        # Etiqueta para mostrar el resultado de la predicción
        resultado_prediccion = tk.Label(self.root, text="", width=int(self.window_width * 0.03),
                                        height=int(self.window_height * 0.002))
        resultado_prediccion.place(relx=0.68, rely=0.86)
    def obtener_valor_x(self, event=None):
        valor_x_entry = self.valor_x_entry.get()
        print(f"Valor de la variable x seleccionado: {valor_x_entry}")
        return valor_x_entry

    def realizar_prediccion(self):
        try:
            valor_x = self.obtener_valor_x(event=None)

            if self.loaded_model_info or self.modelo_info:
                model_info = self.loaded_model_info if self.loaded_model_info else self.modelo_info

                valor_y = model_info.intercept + model_info.slope * float(valor_x)
                self.resultado_prediccion.config(text=f"{valor_y} = {model_info.intercept} + {model_info.slope} * {valor_x}")
            else:
                self.show_error("Primero realiza una regresión lineal o carga un modelo antes de realizar predicciones.")

        except Exception as e:
            self.show_error(f"Error al realizar la predicción: {str(e)}")

    def clear_interface(self):
        widgets_to_destroy = [self.etiqueta_seleccionar, self.etiqueta_variable_x, self.etiqueta_variable_y,
                              self.button_regresion, self.button_guardar_modelo, self.label_mse,
                              self.label_ecuacion_recta, self.etiqueta_valor_x, self.valor_x_entry,
                              self.button_prediccion, self.resultado_prediccion]

        for widget in widgets_to_destroy:
            if widget:
                widget.destroy()

        self.destruir_radiobuttons(self.radiobuttons_var1)
        self.destruir_radiobuttons(self.radiobuttons_var2)
        
        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()

        self.radiobuttons_var1 = None
        self.radiobuttons_var2 = None

    def destruir_radiobuttons(self, radiobutton_list):
        if radiobutton_list:
            for rad in radiobutton_list:
                rad.destroy()

    def Seleccionar(self):
        self.selected_variable_x = self.var1.get()
        self.selected_variable_y = self.var2.get()

    # Otras funciones auxiliares pueden agregarse aquí

    def calculate_percentage(self, value, percentage):
        return int((value * percentage) / 100)

    def create_label(self, text, relx, rely, width_percentage, height_percentage):
        label = Label(self.root, text=text, width=self.calculate_percentage(self.window_width, width_percentage),
                      height=self.calculate_percentage(self.window_height, height_percentage))
        label.place(relx=relx, rely=rely)
        return label

    def create_button(self, text, command, relx, rely, width_percentage, height_percentage):
        button = tk.Button(self.root, text=text, command=command,
                           height=self.calculate_percentage(self.window_height, height_percentage),
                           width=self.calculate_percentage(self.window_width, width_percentage))
        button.place(relx=relx, rely=rely)
        return button

    def create_scrolled_text(self, relx, rely, width_percentage, height_percentage):
        text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.NONE,
                                                height=self.calculate_percentage(self.window_height, height_percentage),
                                                width=self.calculate_percentage(self.window_width, width_percentage),
                                                undo=True)
        text_widget.place(relx=relx, rely=rely)
        return text_widget

    def create_radiobuttons(self, window, variable, y_position, command_callback):
        radiobuttons = []
        primera_fila = self.get_first_row(self.filename)
        texto = ["longitude", 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'median_house_value', 'ocean_proximity']
        if primera_fila is not None:
            for i, (columna, value) in enumerate(primera_fila.items()):
                if i < len(texto):
                    rad = Radiobutton(window, variable=variable, value=columna, text=texto[i], command=command_callback, font=("Helvetica", 8))
                    rad.pack(side=tk.LEFT)
                    rad.place(relx=0.06+0.091*i, rely=y_position)
                    radiobuttons.append(rad)
        else:
            print("Error al obtener la primera fila del archivo.")
        return radiobuttons

    def get_first_row(self, filename):
        df = mostrar_archivos(filename)
        if df is not None:
            primera_fila = df.iloc[0]
            return primera_fila
        else:
            return None



# Crear la ventana raíz
root = tk.Tk()
app = RegresionLinealApp(root)
root.mainloop()

    

