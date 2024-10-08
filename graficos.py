import plotly.express as px
from streamlit import plotly_chart as st_plotly_chart
from streamlit import error as st_error

# Función para graficar
def graficar(df, tipo_grafico, x_col, y_col=None):
    if tipo_grafico == "Gráfico de líneas":
        fig = px.line(df, x=x_col, y=y_col)
    elif tipo_grafico == "Gráfico de barras":
        fig = px.bar(df, x=x_col, y=y_col)
    elif tipo_grafico == "Gráfico de tortas":
        fig = px.pie(df, names=x_col, values=y_col)
    else:
        st_error("Tipo de gráfico no soportado.")
        return None
    st_plotly_chart(fig)