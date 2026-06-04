import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURACIÓN DE PÁGINA ---
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


# --- CARGA DE DATOS SEGURA ---
@st.cache_data
def load_data():
    # Construcción de ruta absoluta para evitar FileNotFoundError
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, 'data', 'processed', 'egresos_hospitalarios_limpio.csv.gz')

    if not os.path.exists(file_path):
        st.error(f"Error: No se encontró el archivo en {file_path}")
        return pd.DataFrame()

    return pd.read_csv(file_path)


df = load_data()

# --- SIDEBAR: FILTROS ---
if not df.empty:
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
        # Métricas
        col1, col2 = st.columns(2)
        col1.metric("Total Egresos", len(df_f))
        col2.metric("Promedio días estancia", round(df_f['DIAS_ESTANCIA'].mean(), 1))

        # Gráfico
        st.subheader("Evolución de Egresos por Año")
        fig = px.histogram(df_f, x='AÑO', color='SECTOR', barmode='group')
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("No se pudieron cargar los datos. Revisa que el archivo exista en la ruta correcta.")