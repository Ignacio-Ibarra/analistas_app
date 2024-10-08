import pandas as pd
from pandas import DataFrame
import chardet
import streamlit as st


# Función para cargar y cachear el archivo
@st.cache_data
def cargar(archivo:str)->DataFrame:
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
                    df = pd.read_csv(archivo, encoding=encoding, delimiter=';')
            elif archivo.name.endswith('.xlsx'):
                df = pd.read_excel(archivo)
            else:
                st.error("Tipo de archivo no soportado.")
                return None, None, None

            return df, encoding, archivo.name
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
            return None, None, None
    return None, None, None

