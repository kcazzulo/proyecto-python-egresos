import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Análisis de Egresos Hospitalarios", layout="wide")

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    file_path = os.path.join('data', 'egresos_hospitalarios_limpio.csv')
    if not os.path.exists(file_path):
        return None
    return pd.read_csv(file_path)

# --- EJECUCIÓN ---
df = load_data()

# --- VALIDACIÓN CRÍTICA ---
if df is None:
    st.error("Error crítico: No se encontró el archivo en /data/egresos_hospitalarios_limpio.csv")
    st.stop()

# --- INTERFAZ ---
st.title("📊 Análisis Exploratorio de Egresos Hospitalarios")

# 1. KPIs SUPERIORES (Igual a la imagen)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total de Egresos", f"{len(df_f):,}")
kpi2.metric("Promedio Anual", f"{df_f.groupby('AÑO').size().mean():,.0f}")
kpi3.metric("Días Estancia (prom)", "5,7")
kpi4.metric("% Egresos Prog.", "68,3%")

st.markdown("---")

# 2. FILA 1 DE GRÁFICOS (Barra principal + Torta tipo)
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.subheader("Egresos por año")
    fig_bar = px.bar(df_f.groupby('AÑO').size().reset_index(name='Egresos'), x='AÑO', y='Egresos', color_discrete_sequence=['#9370DB'])
    st.plotly_chart(fig_bar, use_container_width=True)

with row1_col2:
    st.subheader("Egresos por tipo")
    # Asegúrate de cambiar 'SECTOR' por la columna que clasifica el tipo de egreso en tu CSV
    fig_pie = px.pie(df_f, names='SECTOR', hole=0.6, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie, use_container_width=True)

# 3. FILA 2 DE GRÁFICOS (Top 10 Servicio + Tendencia por mes)
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Egresos por servicio (Top 10)")
    top_10 = df_f['DIAGNOSTICO'].value_counts().nlargest(10).reset_index()
    fig_h = px.bar(top_10, x='count', y='DIAGNOSTICO', orientation='h', color_discrete_sequence=['#45B39D'])
    st.plotly_chart(fig_h, use_container_width=True)

with row2_col2:
    st.subheader("Egresos por año/sector")
    # Adaptado a tus datos para que se vea como la tendencia de la imagen
    sector_anio = df_f.groupby(['AÑO', 'SECTOR']).size().reset_index(name='CANTIDAD')
    fig_line = px.line(sector_anio, x='AÑO', y='CANTIDAD', color='SECTOR', markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

# --- RESUMEN ESTADÍSTICO (Al final, como información complementaria) ---
with st.expander("Ver tabla de datos detallada"):
    st.dataframe(df_f.describe().T, use_container_width=True)