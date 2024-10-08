import pandas as pd
from pandas import DataFrame
import streamlit as st

@st.cache_data
def get_fuentes(db_path:str = 'db_fuentes/db_fuentes.csv')->DataFrame: 
    return pd.read_csv(db_path, sep = ";")


# Función para agregar nuevas combinaciones de institución y fuente
def add_fuente_to_dataset(fuentes_df:DataFrame):
    # Obtener la lista de instituciones únicas
    instituciones = fuentes_df['institucion'].unique()

    # Crear un selectbox para seleccionar la institución
    institucion_seleccionada = st.selectbox(
        f"Selecciona una institución", 
        instituciones
    )

    # Filtrar las fuentes de acuerdo a la institución seleccionada
    fuentes_filtradas = fuentes_df[fuentes_df['institucion'] == institucion_seleccionada]
    fuentes = fuentes_filtradas['nombre'].tolist()

    # Crear un selectbox para seleccionar la fuente
    fuente_seleccionada = st.selectbox(
        f"Selecciona una fuente", 
        fuentes
    )

    # Botón para agregar esta fuente
    if st.button(f"Agregar esta fuente"):
        # Añadir la fuente seleccionada a la lista
        st.session_state.fuente_list.append({
            "institucion": institucion_seleccionada, 
            "fuente": fuente_seleccionada
        })
        