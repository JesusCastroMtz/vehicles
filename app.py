import pandas as pd
import plotly.express as px
import streamlit as st

#------------------------------------------------------------------------------#
#-Dataframe--------------------------------------------------------------------#
#------------------------------------------------------------------------------#
# Lee el dataframe original
df_raw = pd.read_csv('vehicles_us.csv') # leer los datos
# Tratamiento de ausentes
df_sin_na = df_raw
# Elimine los ausentes de las columnas
df_sin_na.dropna(subset=['model_year','cylinders','odometer'], inplace=True)
# Reempplazo los ausentes de las columnas
df_sin_na.fillna({'paint_color':'Unknown'}, inplace=True)
df_sin_na.fillna({'is_4wd':0}, inplace=True)
# Trasfomacion de columnas
df_transformado = df_sin_na
df_transformado['model_year'] = df_transformado['model_year'].astype('int')
df_transformado['cylinders'] = df_transformado['cylinders'].astype('int')
df_transformado['is_4wd'] = df_transformado['is_4wd'].astype('bool')
# Creo la columna de fabricante al extraer la primera palabra de modelo
df_transformado['manufacturer'] = df_transformado['model'].str.split().str[0]
# Asignación de los datos
df_car = df_transformado.reset_index()


#------------------------------------------------------------------------------#
#-TITULO DE LA APP-------------------------------------------------------------#
#------------------------------------------------------------------------------#
st.header('Análisis de datos {🚗...🚙}: ​') #titulo

#------------------------------------------------------------------------------#
#-TABLA INTERACTIVA DEL DATAFRAME----------------------------------------------#
#------------------------------------------------------------------------------#
st.subheader('Tabla interactiva:')# encabezado
st.dataframe(df_car) # tabla interactiva
    
#------------------------------------------------------------------------------#
#-HISTOGRAMA INTERACTIVO-------------------------------------------------------#
#------------------------------------------------------------------------------#
st.subheader('Histograma interactivo por año del modelo:') # encabezado

# Opciones
opcion_disponible = [
    ('price', 'Precio'),
    ('odometer', 'Kilometraje'),
]

# Caja de seleccion
opcion_y = st.selectbox(
    'Elige una opción:',
    opcion_disponible,
    format_func=lambda x: x[1],
    key='y_axis'
)

opcion_categorica = [
    ('condition', 'Condición'),
    ('fuel', 'Combustible'),
    ('transmission', 'Transmisión'),
    ('type', 'Tipo de vehículo'),
    ('paint_color', 'Color de la pintura'),
    ('manufacturer', 'Fabricante')
]

opcion_c = st.selectbox(
    'Elige una categoría:',
    opcion_categorica,
    format_func=lambda x: x[1],
)

# Checkbox para aplicar o no la categorización
usar_categoria = st.checkbox("Aplicar categoría seleccionada", value=False)  # Desactivado por defecto

# Obtener rango de años para el slider
min_year = int(df_car['model_year'].min())
max_year = int(df_car['model_year'].max())
selected_years = st.slider(
    "Selecciona el rango de años:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year))
    
# Filtrar datos según el rango seleccionado
df_filtered = df_car[(df_car['model_year'] >= selected_years[0]) & 
                   (df_car['model_year'] <= selected_years[1])]


# Crear el gráfico con o sin categorización
if usar_categoria and opcion_c:
    fig_hist = px.histogram(
        df_filtered,
        x='model_year',
        y=opcion_y[0],
        color=opcion_c[0],
        barmode='overlay',
        title=f"Distribución de {opcion_y[1]} vs Año del modelo (por {opcion_c[1]})",
        labels={'model_year': 'Año del modelo'}
    )
else:
    fig_hist = px.histogram(
        df_filtered,
        x='model_year',
        y=opcion_y[0],
        title=f"Distribución de {opcion_y[1]} vs Año del modelo",
        labels={'model_year': 'Año del modelo'}
    )

# Mostrar el gráfico
st.plotly_chart(fig_hist, use_container_width=True)

#------------------------------------------------------------------------------#
#-GRAFICO DE DISPERSION INTERACTIVO--------------------------------------------#
#------------------------------------------------------------------------------#
# Casilla de verificación
mostrar_grafico = st.checkbox('Mostrar gráfico de dispersión', value=False)

# Si la casilla está marcada, mostrar el gráfico
if mostrar_grafico:    
    # Crear el gráfico
    fig = px.scatter(
        df_filtered,
        x='model_year',
        y=opcion_y[0],    
        title=f"Relación {opcion_y[1]} vs. Año del modelo",
        labels={'model_year': 'Año del modelo'},
        hover_name="model"  # Opcional: muestra el modelo al pasar el cursor
    )
    
    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)
     