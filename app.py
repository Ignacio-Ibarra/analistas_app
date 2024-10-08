import pandas as pd
import json
import streamlit as st
from graficos import graficar
from dataset import cargar
from metadatos import get_metadatos, define_schema, guardar_metadatos
from qa import hacer_qa
from fuentes import get_fuentes, add_fuente_to_dataset

# Configuración de la página
st.set_page_config(
    page_title="Analistas App",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Bienvenidos la app de analistas")


# Inicializar lista para almacenar fuentes
st.session_state['fuente_list'] = []




# Cargar archivo
path_dataset = st.file_uploader("Sube un archivo CSV o XLSX", type=['csv', 'xlsx'])

# Cargar datos
df, encoding, dataset_archivo = cargar(path_dataset)


if df is not None:

    if st.button("Muestra de datos"):
        st.write(df.sample(len(df)).head(30))
    
    # Metadatos
    metadatos = get_metadatos(filename=dataset_archivo.replace(".csv",".json"))

    # Cargar fuentes
    fuentes_df = get_fuentes(db_path='db_fuentes/db_fuentes.csv')

    st.subheader(f"Metadatos: {dataset_archivo}")

    if metadatos: 
        st.write("Ya hay metadatos disponibles, si desea modificar haga clic en 'Generar metadatos'")
        st.json(metadatos)
    else: 

        # Modificación de metadatos
        if st.button('Generar metadatos'):

            # Solicitar al usuario la descripción global del dataset
            descripcion_dataset = st.text_area("Describa en qué consiste el dataset", help="Descripción acerca del contenido del dataset")

            # Agregar fuentes múltiples
            if fuentes_df is not None:
                st.write("Selecciona las fuentes utilizadas")
                add_fuente_to_dataset(fuentes_df)

                # Mostrar las fuentes seleccionadas
                if len(st.session_state.fuente_list) > 0:
                    st.write("Fuentes seleccionadas:")
                    for idx, fuente in enumerate(st.session_state.fuente_list, start=1):
                        st.write(f"{idx}. {fuente['institucion']} - {fuente['fuente']}")


            schema = define_schema(df=df)

            # Armar el diccionario de metadatos
            metadatos = {
                'dataset_archivo': dataset_archivo,
                'descripcion_dataset': descripcion_dataset,
                'fuentes':st.session_state.fuente_list,
                'schema': schema
            }

            # Guardar metadatos en un archivo JSON
            if st.button("Guardar Metadatos"):
                guardar_metadatos(metadatos, f"db_metadatos/metadatos_{dataset_archivo}.json")  

        # Botón azul para hacer QA
        if st.button("Hacer QA", key="hacer_qa", help="Hacer controles de calidad en el archivo", type="primary"):
            hacer_qa(df, encoding, dataset_archivo)
        
    
        # Botón para graficar
        if st.button("Generar gráfico"):
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
            graficar(df_filtrado, tipo_grafico, x_col, y_col)

