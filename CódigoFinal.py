#import streamlit as st
#import pandas as pd
#import gdown
#
#id = 1op-iq0XhBXBQOPlagCPE9TzFsFkkNVjQ
#@st.experimental_memo
#def download_data():
#  #https://drive.google.com/uc?id=
#  url = "https://drive.google.com/uc?id=1op-iq0XhBXBQOPlagCPE9TzFsFkkNVjQ"
#  output= "data.csv"
#  gdown.download(url,output,quiet = False)
#  
#download_data()
#data = pd.read_csv("data.csv", sep = ";", parse_dates = ["FECHA_CORTE","FECHA_RESULTADO"])
#Simplificado = data.drop(columns = ["DISTRITO","FECHA_CORTE","FECHA_RESULTADO","UBIGEO","id_persona"])

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import gdown
import os

#0. TITULO Y DESCRIPCION DEL PROYECTO
st.title('Análisis de casos positivos registrados en Perú')
st.subheader("Miembros del equipo")
st.markdown("""
- Isabel Muñoz
- Enzo Baltazar
- Joel Huillca
- Stephany Samanez
- Lucero de la Cruz
- Leonardo Plasencia
""")
st.markdown("""
---
### 1. Descripción del proyecto
El proyecto consiste en análisis exploratorio de un dataset que registra información
de los casos positivos detectados en Perú durante el mes de mayo del año 2022.

Fuente de datos: [https://ejemplo.com/](https://ejemplo.com/)

### 2. Origen de los datos
El conjunto de dato se obtuvo del portal de datos abiertos del MINSA.
| Variable        |	Descripción                                                                                         |
| --------------- | --------------------------------------------------------------------------------------------------- |
| FECHA_CORTE     |	Fecha de corte de información                                                                       |
| UUID            |	ID de la persona como caso positivo de covid-19 confirmada con cualquier tipo de prueba.            |
| UBIGEO          |	Código de Ubicación Geografica que denotan "DDppdd" (Departamento, provincia,distrito), fuente INEI |
| DEPARTAMENTO    |	Departamento donde reside la persona confirmada como caso positivo de covid-19                      |
| PROVINCIA       |	Provincia donde reside la persona confirmada como caso positivo de covid-19                         |
| DISTRITO        |	Distrito donde reside la persona confirmada como caso positivo de covid-19                          |
| METODODX        |	Metodo de laboratorio a la que es sometida una prueba de covid-19                                   |
| EDAD            |	Edad de la persona confirmada como caso positivo de covid-19                                        |
| SEXO            |	Sexo de la persona confirmada como caso positivo de covid-19                                        |
| FECHA_RESULTADO |	Fecha del resultado de la prueba de covid-19                                                        |

&nbsp;
### 3. Herramientas utilizadas
A continuación se listan los paqueyes de Python utilizaron durant el desarrollo del proyecto.
```
gdown==4.4.0
numpy==1.22.4
pandas==1.4.2
pyecharts==1.9.1
streamlit==1.10.0
streamlit_echarts==0.4.0
```

### 4. Miembros del equipo
- Isabel Muñoz
- Enzo Baltazar
- Joel Huillca
- Stephany Samanez
- Lucero de la Cruz
- Leonardo Plasencia

### 5. Dashboard
""")

#1. CARGA DE DATOS

# Lectura de datos desde CSV
#id = 1op-iq0XhBXBQOPlagCPE9TzFsFkkNVjQ
if not os.path.exists('downloads'):
  os.makedirs('downloads')

@st.experimental_memo
def download_data():
  #https://drive.google.com/uc?id=
  url = "https://drive.google.com/uc?id=1op-iq0XhBXBQOPlagCPE9TzFsFkkNVjQ"
  output = "downloads/data.csv"
  gdown.download(url,output,quiet = False)
  
download_data()
df = pd.read_csv("downloads/data.csv", sep = ";", parse_dates = ["FECHA_CORTE","FECHA_RESULTADO"])
#Simplificacion del dataset (retiro de columnas)
df = df.drop(columns = ["FECHA_CORTE","FECHA_RESULTADO","UBIGEO","id_persona"])

#2. FILTROS

#Construccion del set/list de departamentos (Valores unicos sin NA)
set_departamentos = np.sort(df['DEPARTAMENTO'].dropna().unique())
#Seleccion del departamento
opcion_departamento = st.selectbox('Selecciona un departamento', set_departamentos)
df_departamentos = df[df['DEPARTAMENTO'] == opcion_departamento]
num_filas = len(df_departamentos.axes[0]) 

#Construccion del set/list de provincias (Valores unicos sin NA)
set_provincias = np.sort(df_departamentos['PROVINCIA'].dropna().unique())
#Seleccion de la provincia
opcion_provincia = st.selectbox('Selecciona una provincia', set_provincias)
df_provincias = df_departamentos[df_departamentos['PROVINCIA'] == opcion_provincia]
num_filas = len(df_provincias.axes[0]) 

#Construccion del set/list de distritos (Valores unicos sin NA)
set_distritos = np.sort(df_departamentos['DISTRITO'].dropna().unique())
#Seleccion de la distrito
opcion_distrito = st.selectbox('Selecciona un distrito', set_distritos)
df_distritos = df_departamentos[df_departamentos['DISTRITO'] == opcion_distrito]
num_filas = len(df_distritos.axes[0]) 

st.write('Numero de registros:', num_filas)

#GRAFICOS

#Pie chart de METODODX
df_metododx = df_distritos.METODODX.value_counts()
df_metododx = pd.DataFrame(df_metododx)
df_metododx = df_metododx.reset_index()  
df_metododx.columns = ['METODODX', 'Total']

fig1, ax1 = plt.subplots()
ax1.pie(df_metododx['Total'], labels=df_metododx['METODODX'], autopct='%1.1f%%')
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.write('Distribución por METODODX:')
st.pyplot(fig1)

#Ploteo de las frecuencias SEXO
df_SEXO = df_distritos.SEXO.value_counts()
st.write('Distribución por SEXO:')
st.bar_chart(df_SEXO)

#Ploteo de las frecuencias EDAD
df_edad = df_distritos.EDAD.value_counts()
st.write('Distribución por EDAD:')
st.bar_chart(df_edad)
