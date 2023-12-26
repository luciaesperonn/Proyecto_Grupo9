# regresion_lineal.py

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import tkinter as tk
from matplotlib.figure import Figure
from tkinter import StringVar, Radiobutton
from clase_modelo import *
from gui_app import *
from tkinter import Tk, Label, Button, filedialog, Frame, ttk, Radiobutton, Scrollbar, StringVar

def crear_radiobuttons(frame, options, variable, row, column):
        radiobuttons = []
        for i, option in enumerate(options):
            radiobutton = Radiobutton(frame, text=option, variable=variable, value=option)
            radiobutton.grid(row=row, column=column + i, padx=5, pady=5, sticky=tk.W)
            radiobuttons.append(radiobutton)
        return radiobuttons

def realizar_regresion(self):
        if self.variable_x.get() and self.variable_y.get():
            # Obtener las variables seleccionadas
            variable_x = self.variable_x.get()
            variable_y = self.variable_y.get()

            # Añadir la verificación de columnas numéricas solo para variable_x y variable_y
            columnas_a_verificar = [self.variable_x.get(), self.variable_y.get()]
            self.verificar_columnas_numericas(self.df, columnas_a_verificar)

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
            
            self.info_modelo = ModeloInfo(self.variable_x.get(), self.variable_y.get(), self.modelo.intercept_, self.modelo.coef_, 
                                          self.ecuacion, self.mse, self.texto_descripcion.get())

            self.elementos_prediccion()

        else:
            raise ValueError("Seleccione las variables x e y antes de hacer la regresión")


