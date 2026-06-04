import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración inicial (debe ser lo primero)
st.set_page_config(page_title="Dashboard Egresos Hospitalarios", layout="wide")

# --- ESTILOS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fb; }
    div[data-testid="stMetricValue"] { color: #4B4679; font-size: 24px; }
    h1 { color: #2D3748; }
    h2, h3 { color: #4A5568; }
    </style>
    """, unsafe_allow_html=True)


# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    # APUNTAMOS A TU NUEVO ARCHIVO COMPRIMIDO
    return pd.read_csv('data/processed/egresos_hospitalarios_limpio.csv.gz')


df = load_data()

# --- SIDEBAR: FILTROS ---
st.sidebar.markdown("## ⚙️ Filtros de Análisis")
min_a, max_a = int(df['AÑO'].min()), int(df['AÑO'].max())
rango_anios = st.sidebar.slider("Rango de Años", min_a, max_a, (min_a, max_a))

regiones = st.sidebar.multiselect("Región", df['REGION'].unique(), default=df['REGION'].unique())
sectores = st.sidebar.multiselect("Sector", df['SECTOR'].unique(), default=df['SECTOR'].unique())

# --- APLICACIÓN DE FILTROS ---
df_f = df[
    (df['AÑO'].between(rango_anios[0], rango_anios[1])) &
    (df['REGION'].isin(regiones)) &
    (df['SECTOR'].isin(sectores))
    ]

# --- DASHBOARD ---
st.title("📊 Dashboard de Egresos Hospitalarios")

if df_f.empty:
    st.warning("No hay datos para los filtros seleccionados.")
else:
    # Ejemplo de métrica rápida
    col1, col2 = st.columns(2)
    col1.metric("Total Egresos", len(df_f))
    col2.metric("Promedio días estancia", round(df_f['DIAS_ESTANCIA'].mean(), 1))

    # Ejemplo de gráfico
    st.subheader("Evolución de Egresos por Año")
    fig = px.histogram(df_f, x='AÑO', color='SECTOR', barmode='group')
    st.plotly_chart(fig, use_container_width=True)
