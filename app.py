import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Dashboard Hospitalario", layout="wide")

@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, 'data', 'egresos_hospitalarios_limpio.csv')
    return pd.read_csv(file_path)

df = load_data()

# --- SIDEBAR: FILTROS ---
st.sidebar.markdown("## ⚙️ Filtros de Análisis")
min_a, max_a = int(df['AÑO'].min()), int(df['AÑO'].max())
rango_anios = st.sidebar.slider("Rango de Años", min_a, max_a, (min_a, max_a))
regiones = st.sidebar.multiselect("Región", df['REGION'].unique(), default=df['REGION'].unique())

# APLICACIÓN DE FILTROS
df_f = df[(df['AÑO'].between(rango_anios[0], rango_anios[1])) & (df['REGION'].isin(regiones))]

# --- RESUMEN DESCRIPTIVO (ESTADÍSTICAS) ---
st.header("📊 Análisis Descriptivo")
st.write("Estadísticas de la columna 'AÑO' basada en los filtros:")
st.table(df_f['AÑO'].describe())

# --- VISUALIZACIÓN DINÁMICA ---
st.header("📈 Visualizaciones")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de Egresos")
    fig_hist = px.histogram(df_f, x="AÑO", nbins=10, title="Distribución por Año")
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("Relación Años vs Egresos")
    # Gráfico de dispersión (scatter)
    fig_scatter = px.scatter(df_f.groupby('AÑO').size().reset_index(name='TOTAL'),
                             x='AÑO', y='TOTAL', size='TOTAL', title="Relación Años/Volumen")
    st.plotly_chart(fig_scatter, use_container_width=True)

st.success("Dashboard actualizado con filtros interactivos y estadísticas descriptivas.")