<h1 align="center"> Trabajo IS </h1>

Este proyecto consiste en el desarrollo de una aplicación que facilita la creación y visualización de modelos de regresión lineal simple. La aplicación está diseñada 
para trabajar con datos almacenados en archivos CSV, Excel y bases de datos. Además, destaca por su capacidad de cargar modelos previos y llevar a cabo predicciones de 
manera eficaz. 

## Instrucciones de Instalación 
1. **Abrir el terminal:**
   - En Windows, puedes utilizar el cmd.

2. **Navegar al directorio del proyecto:**
   - Utiliza el comando `cd` para cambiar al directorio donde se encuentra el archivo a ejecutar.
     ```bash
     cd rutadelproyecto
     ```

3. **Ejecutar el script:**
   - Usa el comando `python` seguido del nombre del archivo para ejecutar, en este caso, `main.py`.
     ```bash
     python main.py
     ```

   - Si deseas comprobar que las pruebas unitarias funcionan correctamente, ejecuta el siguiente comando:
     ```bash
     python elnombredeltest.py
     ```

## Librerías Necesarias
Antes de ejecutar la aplicación, asegúrate de tener instaladas las siguientes librerías de Python. Puedes instalarlas ejecutando los siguientes comandos en tu terminal:

```bash
pip install pandas
pip install sqlite3  # (Generalmente viene con Python por defecto, no es necesario instalarlo por separado)
pip install scikit-learn
pip install joblib
pip install matplotlib
pip install tkinter  # (Verifica si ya está instalado con tu distribución de Python)
pip install unnitest
```


## Manual de Usuario

1. **Cargar Datos:**
   - Haz clic en el botón "Examinar".
   - Selecciona un archivo CSV, Excel o SQLite con tus datos.
   - Los datos se cargarán automáticamente y se mostrarán en una tabla.

2. **Seleccionar Variables y Realizar Regresión:**
   - Selecciona las variables X e Y utilizando los radiobuttons.
   - Haz clic en "Realizar regresión" para ajustar el modelo lineal.
   - La ecuación de la recta, el error cuadrático medio y la bondad de ajuste se mostrarán en la interfaz.

3. **Guardar el Modelo:**
   - Después de realizar la regresión, puedes guardar el modelo haciendo clic en "Guardar modelo".
   - Selecciona la ubicación y el nombre del archivo joblib para guardar el modelo.

4. **Cargar Modelo Existente:**
   - Haz clic en "Cargar Modelo".
   - Selecciona el archivo joblib del modelo previamente guardado.
   - La información del modelo cargado se mostrará en la interfaz.

5. **Realizar Predicciones:**
   - Después de cargar un modelo, puedes introducir un valor para la variable X.
   - Haz clic en "Realizar predicción" para obtener el valor predicho de la variable Y.
   - La ecuación actualizada con el nuevo valor se mostrará en la interfaz.

6. **Descripción del Modelo (Opcional):**
   - Puedes agregar una descripción del modelo durante o después de realizar la regresión.
   - La descripción se mostrará junto con la información del modelo.

7. **Notas Adicionales:**
   - La tabla se actualizará automáticamente al cargar nuevos datos.
   - Asegúrate de introducir un valor válido para las predicciones.











