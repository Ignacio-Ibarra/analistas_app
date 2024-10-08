import json
from pathlib import Path
from pandas import DataFrame
import streamlit as st
from typing import Optional

def file_exists(path:str)->bool:
    return Path(path).is_file()
    


def get_metadatos(filename:str, db_path:str = 'db_metadatos/')-> Optional[dict]:
    
    path = db_path + filename
    if file_exists(path):
    
        # Open the JSON file
        with open( d, 'r') as file:
            data = file.read()
        # Parse JSON data into a dictionary
        return json.loads(data)
    else:
        return None


# Función para recoger metadatos
def define_schema(df:DataFrame)->list[dict]:
    
    # Crear diccionario para almacenar los metadatos
    schema = []
    
    # Permitir al usuario ingresar metadatos por columna
    for columna in df.columns:
        st.write(f"**Columna: {columna}**")
        es_primary_key = st.selectbox(f"¿Es primary key?", ["Ingresar", "True", "False"], key=f"{columna}_primary")
        es_nullable = st.selectbox(f"¿Es nullable?", ["Ingresar", "True", "False"],  key=f"{columna}_nullable")
        tipo_dato = st.selectbox(f"Selecciona el tipo de dato", ["Ingresar", "int", "float", "str", 'bool'], key=f"{columna}_tipo")
        descripcion = st.text_input(f"Descripción", key=f"{columna}_descripcion")

        # Agregar los metadatos de la columna al diccionario
        schema.append({
            'columna': columna,
            'es_primary_key': es_primary_key,
            'es_nullable': es_nullable,
            'tipo_dato': tipo_dato,
            'descripcion': descripcion
        })
    return schema



# Función para guardar metadatos
def guardar_metadatos(metadatos:dict, nombre_archivo:str)->None:
    with open(nombre_archivo, 'w') as f:
        json.dump(metadatos, f, indent=4)


