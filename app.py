import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Dashboard Egresos Hospitalarios", layout="wide")


# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    # Obtiene la ruta del archivo donde está app.py
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Busca el archivo en la carpeta 'data'
    file_path = os.path.join(base_path, 'data', 'egresos_hospitalarios_limpio.csv')

    # Verifica si el archivo existe
    if not os.path.exists(file_path):
        st.error(f"Error: No se encontró el archivo en {file_path}")
        return pd.DataFrame()

    return pd.read_csv(file_path)


# --- EJECUCIÓN ---
df = load_data()

# --- INTERFAZ ---
if not df.empty:
    st.title("📊 Dashboard de Egresos Hospitalarios")

    # Filtros
    st.sidebar.markdown("## ⚙️ Filtros")
    min_a, max_a = int(df['AÑO'].min()), int(df['AÑO'].max())
    rango_anios = st.sidebar.slider("Rango de Años", min_a, max_a, (min_a, max_a))

    regiones = st.sidebar.multiselect("Región", df['REGION'].unique(), default=df['REGION'].unique())
    sectores = st.sidebar.multiselect("Sector", df['SECTOR'].unique(), default=df['SECTOR'].unique())

    df_f = df[
        (df['AÑO'].between(rango_anios[0], rango_anios[1])) &
        (df['REGION'].isin(regiones)) &
        (df['SECTOR'].isin(sectores))
        ]

    if df_f.empty:
        st.warning("No hay datos para estos filtros.")
    else:
        st.metric("Total Egresos", len(df_f))
        fig = px.histogram(df_f, x='AÑO', color='SECTOR')
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("La aplicación no pudo cargar los datos. Revisa la ruta.")