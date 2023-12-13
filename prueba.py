import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import StringVar

from regresion_lineal import crear_modelo_regresion_lineal, visualizar_modelo
from leer_archivos import mostrar_archivos
from clase_modelo import ModeloInfo
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score

class ModeloApp:
    def __init__(self, root):
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        self.button_explore = None
        self.selected_variable_x = None
        self.selected_variable_y = None
        self.label_file_explorer = None
        self.text_data_display = None

        self.button_explore = self.create_button("Buscar Archivos", self.browse_files, 0.65, 0.03, 0.9, 0.18)
        self.button_cargar_modelo = self.create_button("Cargar Modelo", self.cargar_modelo, 0.72, 0.03, 0.9, 0.18)

        self.var1 = StringVar()
        self.var2 = StringVar()
        self.var1.set(' ')
        self.var2.set(' ')

        # Crear la ventana raíz
        self.root.title('EXPLORADOR DE ARCHIVOS')

        # Obtener el ancho y alto de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Establecer porcentajes para la geometría de la ventana
        width_percentage = 100
        height_percentage = 100

        # Calcular el tamaño de la ventana en función de los porcentajes
        self.window_width = self.calculate_percentage(screen_width, width_percentage)
        self.window_height = self.calculate_percentage(screen_height, height_percentage)

        # Crear la geometría de la ventana con porcentajes
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        self.label_file_explorer = self.create_label("", 0.065, 0.025, 8, 0.25)
        self.text_data_display = self.create_scrolled_text(0.035, 0.09, 10, 1.5)

        self.etiqueta_seleccionar = tk.Label(self.root, text="Selecciona una variable x y una variable y:")
        self.etiqueta_seleccionar.place(relx=0.01, rely=0.328)

        self.etiqueta_variable_x = tk.Label(self.root, text="VARIABLE X:")
        self.etiqueta_variable_x.place(relx=0.01, rely=0.355)

        self.etiqueta_variable_y = tk.Label(self.root, text="VARIABLE Y:")
        self.etiqueta_variable_y.place(relx=0.01, rely=0.38)

        # Crear el botón "Realizar Regresión Lineal"
        self.button_regresion = tk.Button(self.root, text="Realizar Regresión Lineal", height=1, width=20, command=lambda: self.realizar_regresion_lineal(self.filename, self.var1.get(), self.var2.get(), auto=True))
        self.button_regresion.place(relx=0.01, rely=0.42)

        self.button_guardar_modelo = self.create_button("Guardar Modelo", self.guardar_modelo, 0.01, 0.46, 0.9, 0.18)

        self.introducir_valor_x()

        self.radiobuttons_var1 = self.create_radiobuttons(self.root, self.var1, self.filename, 0.355, self.Seleccionar)
        self.radiobuttons_var2 = self.create_radiobuttons(self.root, self.var2, self.filename, 0.38, self.Seleccionar)


    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Examinar", filetypes=(("Text files", "*.txt*"),
                                                                                           ("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("SQLite databases", "*.db"), ("all files", "*.*")))
        if filename:
            self.label_file_explorer.config(text=f"{filename}")

            df = mostrar_archivos(filename)
            self.show_data_popup(df)

            # Limpiar Radiobuttons antes de crear nuevos
            self.limpiar_interfaz()

            self.radiobuttons_var1 = self.create_radiobuttons(self.root, self.var1, filename, 0.355, self.Seleccionar)
            self.radiobuttons_var2 = self.create_radiobuttons(self.root, self.var2, filename, 0.38, self.Seleccionar)

        self.etiqueta_seleccionar = tk.Label(self.root, text="Selecciona una variable x y una variable y:")
        self.etiqueta_seleccionar.place(relx=0.01, rely=0.328)

        self.etiqueta_variable_x = tk.Label(self.root, text="VARIABLE X:")
        self.etiqueta_variable_x.place(relx=0.01, rely=0.355)

        self.etiqueta_variable_y = tk.Label(self.root, text="VARIABLE Y:")
        self.etiqueta_variable_y.place(relx=0.01, rely=0.38)

        # Crear el botón "Realizar Regresión Lineal"
        self.button_regresion = tk.Button(self.root, text="Realizar Regresión Lineal", height=1, width=20, command=lambda: self.realizar_regresion_lineal(filename, self.var1.get(), self.var2.get(), auto=True))
        self.button_regresion.place(relx=0.01, rely=0.42)

    def cargar_modelo(self):
        try:
            file_path = filedialog.askopenfilename(defaultextension=".joblib", filetypes=[("Archivos joblib", "*.joblib")])

            if file_path:
                # Usa 'self' para que 'loaded_model_info' sea una variable de instancia
                self.loaded_model_info = joblib.load(file_path)
                
                # Utiliza 'self' para referenciar las funciones de la clase
                self.mostrar_info_modelo(file_path, self.loaded_model_info)

                # Limpia la interfaz antes de cargar el modelo
                self.limpiar_interfaz()
                self.introducir_valor_x()

        except Exception as e:
            # Usa 'self' para referenciar las funciones de la clase
            self.show_error(f"Error al cargar el modelo: {str(e)}")

    def show_data_popup(self, df):
        # Limpiar el contenido actual
        self.text_data_display.delete(1.0, tk.END) 

        # Obtener información sobre los datos
        headers = df.columns
        max_column_widths = [max(len(str(header)), df[header].astype(str).apply(len).max()) for header in headers]
        
        # Agregar encabezados al Text
        header_text = " | ".join(f"{header:<{width}}" for header, width in zip(headers, max_column_widths)) + "\n"
        self.text_data_display.insert(tk.END, header_text)

        # Agregar separador de columnas
        separator_line = "-" * sum(max_column_widths + [len(headers) - 1]) + "\n"
        self.text_data_display.insert(tk.END, separator_line)

        # Agregar filas al Text
        for _, row in df.iterrows():
            row_text = " | ".join(f"{str(value)[:width].center(width)}" for value, width in zip(row, max_column_widths)) + "\n"
            self.text_data_display.insert(tk.END, row_text)
            

    def limpiar_interfaz(self):
        self.selected_variable_x = None
        self.selected_variable_y = None

        # Limpiar las variables de control de los Radiobuttons
        self.var1.set(' ')
        self.var2.set(' ')

        widgets_to_destroy = [self.etiqueta_seleccionar, self.etiqueta_variable_x, self.etiqueta_variable_y,
                            self.button_regresion, self.button_guardar_modelo, self.label_mse,
                            self.label_ecuacion_recta, self.etiqueta_valor_x, self.valor_x_entry,
                            self.button_prediccion, self.resultado_prediccion]
        
        for widget in widgets_to_destroy:
            if widget:
                widget.destroy()

        # Destruir los Radiobuttons y el Graph_canvas
        self.destruir_radiobuttons(self.radiobuttons_var1)
        self.destruir_radiobuttons(self.radiobuttons_var2)
            
        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()

        # Limpiar las variables globales relacionadas con Radiobuttons
        self.radiobuttons_var1 = None
        self.radiobuttons_var2 = None

# Método para destruir Radiobuttons
    def destruir_radiobuttons(self, radiobutton_list):
        if radiobutton_list:
            for rad in radiobutton_list:
                rad.destroy()

        

    def create_button(self, text, command, relx, rely, width_percentage, height_percentage):
        button = tk.Button(self.window, text=text, command=command,
                       height=self.calculate_percentage(self.window_height, height_percentage),
                       width=self.calculate_percentage(self.window_width, width_percentage))
        button.place(relx=relx, rely=rely)
        return button

    def create_label(self, text, relx, rely, width_percentage, height_percentage):
        label = tk.Label(self.window, text=text, width=self.calculate_percentage(self.window_width, width_percentage),
                     height=self.calculate_percentage(self.window_height, height_percentage))
        label.place(relx=relx, rely=rely)
        return label

    def create_scrolled_text(self, relx, rely, width_percentage, height_percentage):
        text_widget = scrolledtext.ScrolledText(self.window, wrap=tk.NONE,
                                            height=self.calculate_percentage(self.window_height, height_percentage),
                                            width=self.calculate_percentage(self.window_width, width_percentage),
                                            undo=True)
        text_widget.place(relx=relx, rely=rely)
        return text_widget

    def create_radiobuttons(self, window, variable, filename, y_position, command_callback):
        radiobuttons = []

    # Obtener la primera fila del DataFrame
        primera_fila = self.get_first_row(filename)
        texto = ["longitude", 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'median_house_value', 'ocean_proximity']
        if primera_fila is not None:
            for i, (columna, value) in enumerate(primera_fila.items()):
                if i < len(texto):  # Asegurarse de que hay elementos en la lista 'texto'
                    rad = self.Radiobutton(window, variable=variable, value=columna, text=texto[i], command=command_callback, font=("Helvetica", 8))
                    rad.pack(side=LEFT)
                    rad.place(relx=0.06+0.091*i, rely=y_position)
                    radiobuttons.append(rad)
        else:
            print("Error al obtener la primera fila del archivo.")
        return radiobuttons


    def Seleccionar(self):
        global selected_variable_x, selected_variable_y
        selected_variable_x = self.var1.get()
        selected_variable_y = self.var2.get()

        print(selected_variable_x)
        print(selected_variable_y)
        print()

    def calculate_percentage(self, value, percentage):
        return int((value * percentage) / 100)

    def realizar_regresion_lineal(self, filename, variable_x, variable_y, auto=True):
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

            etiqueta_x = variable_x 
            etiqueta_y = variable_y 

            fig = visualizar_modelo(modelo, X, y, etiqueta_x, etiqueta_y)

            # Crear o actualizar las etiquetas con los resultados
            label_mse, label_ecuacion_recta = self.crear_etiquetas_resultados(modelo, X, y, variable_x, variable_y)

            # Integrar la figura en un Canvas de Tkinter
            graph_canvas = self.integrar_figura_en_canvas(fig)

            # Crear una instancia de ModeloInfo
            modelo_info = self.crear_modelo_info(modelo, variable_x, variable_y, X, y)

            # Crear el botón "Realizar Regresión Lineal"
            button_guardar_modelo = self.crear_boton_guardar_modelo()

            self.introducir_valor_x()               

        except Exception as e:
            self.show_error(f"Error al realizar la regresión lineal: {str(e)}")

    def integrar_figura_en_canvas(self, fig):
        graph_canvas = self.FigureCanvasTkAgg(fig, master=self.window)
        graph_canvas_widget = graph_canvas.get_tk_widget()
        graph_canvas_widget.place(relx=0.12, rely=0.42)
    
        return graph_canvas

    def create_modelo_info(self, modelo, variable_x, variable_y, X, y):
        ecuacion_recta = f"y = {float(modelo.intercept_)} + {float(modelo.coef_[0][0])} * {variable_x}"
        mse = mean_squared_error(y, modelo.predict(X))
        return ModeloInfo(variable_x, variable_y, modelo.intercept_, modelo.coef_, ecuacion_recta, mse)


    def create_boton_guardar_modelo(self):
        button_guardar_modelo = tk.Button(self.window, text="Guardar Modelo", height=1, width=20, command=self.guardar_modelo)
        button_guardar_modelo.place(relx=0.01, rely=0.46)
        return button_guardar_modelo

    def guardar_modelo(self):
        if self.modelo_info is None:
            self.show_error("Realiza la regresión lineal antes de intentar guardar el modelo.")
            return

        try:
            # Obtener la ruta y nombre de archivo seleccionados por el usuario
            file_path = filedialog.asksaveasfilename(defaultextension=".joblib", filetypes=[("Archivos joblib", "*.joblib")])

            if file_path:
                # Guardar la información del modelo en el archivo
                self.modelo_info.guardar_modelo(file_path)

                self.show_info(f"Modelo guardado en: {file_path}")

        except Exception as e:
            self.show_error(f"Error al guardar el modelo: {str(e)}")
        


class ModeloInfo:
    


class RegresionLinealApp:
    

if __name__ == "__main__":
    root = tk.Tk()
    app = ModeloApp(root)
    root.mainloop()
