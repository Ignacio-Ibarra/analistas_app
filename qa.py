import pandas as pd
import streamlit as st

# Función para hacer QA
def hacer_qa(df, encoding, tipo_archivo):
    st.subheader("Resultados del QA")
    
    # Mostrar el encoding detectado
    st.write(f"**Encoding detectado**: {encoding}")
    
    # Delimitador solo aplica para archivos CSV
    if tipo_archivo.endswith(".csv"):
        delimitador = ',' if df.to_csv().count(',') > df.to_csv().count(';') else ';'
        st.write(f"**Delimitador detectado**: {delimitador}")
    
    # Calcular valores nulos por columna
    nulos = df.isnull().sum()
    st.write("**Valores nulos por columna**:")
    st.write(nulos)