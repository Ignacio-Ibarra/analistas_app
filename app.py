import streamlit as st
import pandas as pd
import plotly.express as px
import chardet

# Función para cargar y cachear el archivo
@st.cache_data
def cargar_datos(archivo):
    if archivo is not None:
        try:
            # Detectar encoding del archivo
            raw_data = archivo.read(1024)
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            
            # Volver a cargar el archivo desde el principio
            archivo.seek(0)

            # Cargar CSV con el encoding detectado
            if archivo.name.endswith('.csv'):
                try:
                    # Intentar con distintos delimitadores comunes
                    df = pd.read_csv(archivo, encoding=encoding)
                except pd.errors.ParserError:
                    archivo.seek(0)
                    df = pd.read_csv(archivo, encoding=encoding, delimiter=';')  # Probar delimitador ';'
            elif archivo.name.endswith('.xlsx'):
                df = pd.read_excel(archivo)
            else:
                st.error("Tipo de archivo no soportado.")
                return None, None, None

            return df, encoding, "CSV" if archivo.name.endswith('.csv') else "XLSX"
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
            return None, None, None
    return None, None, None


# Función para hacer QA
def hacer_qa(df, encoding, tipo_archivo):
    st.subheader("Resultados del QA")
    
    # Mostrar el encoding detectado
    st.write(f"**Encoding detectado**: {encoding}")
    
    # Delimitador solo aplica para archivos CSV
    if tipo_archivo == "CSV":
        delimitador = ',' if df.to_csv().count(',') > df.to_csv().count(';') else ';'
        st.write(f"**Delimitador detectado**: {delimitador}")
    
    # Calcular valores nulos por columna
    nulos = df.isnull().sum()
    st.write("**Valores nulos por columna**:")
    st.write(nulos)
    


# Función para graficar
def graficar(df, tipo_grafico, x_col, y_col=None):
    if tipo_grafico == "Gráfico de líneas":
        fig = px.line(df, x=x_col, y=y_col)
    elif tipo_grafico == "Gráfico de barras":
        fig = px.bar(df, x=x_col, y=y_col)
    elif tipo_grafico == "Gráfico de tortas":
        fig = px.pie(df, names=x_col, values=y_col)
    else:
        st.error("Tipo de gráfico no soportado.")
        return None
    st.plotly_chart(fig)

# Configuración de la página
st.set_page_config(
    page_title="Mi Aplicación de Streamlit",
    page_icon="🎈",
    layout="wide",  # Opción: 'centered'
    initial_sidebar_state="expanded"  # Opción: 'collapsed'
)

st.title("Bienvenido a mi aplicación")

# Cargar archivo
archivo = st.file_uploader("Sube un archivo CSV o XLSX", type=['csv', 'xlsx'])

# Cargar datos
df, encoding, tipo_archivo = cargar_datos(archivo)
mostrar_data = None
nulos = None

if df is not None:
    st.subheader("Vamos a ver qué onda...")

# Botón azul para hacer QA
if st.button("Hacer QA", key="hacer_qa", help="Hacer controles de calidad en el archivo"):
    hacer_qa(df, encoding, tipo_archivo)

    

mostrar_data = st.checkbox("Mostrar data")

if mostrar_data:
    st.write(df)

    # Selección de gráfico
    tipo_grafico = st.selectbox("Selecciona el tipo de gráfico", ["Gráfico de líneas", "Gráfico de barras", "Gráfico de tortas"])

    # Seleccionar columnas para graficar
    columnas = df.columns.tolist()
    x_col = st.selectbox("Selecciona la columna X", columnas)

    # Para gráficos de líneas y barras se necesita seleccionar la columna Y
    y_col = None
    if tipo_grafico != "Gráfico de tortas":
        y_col = st.selectbox("Selecciona la columna Y", columnas)

    # Agregar opción de filtro
    filtro_col = st.selectbox("Selecciona una columna para filtrar (opcional)", ['Ninguno'] + columnas)

    if filtro_col != 'Ninguno':
        filtro_valores = df[filtro_col].unique()
        filtro_valor = st.selectbox(f"Selecciona el valor para filtrar en {filtro_col}", filtro_valores)
        df_filtrado = df[df[filtro_col] == filtro_valor]
    else:
        df_filtrado = df

    # Botón para graficar
    if st.button("Generar gráfico"):
        graficar(df_filtrado, tipo_grafico, x_col, y_col)