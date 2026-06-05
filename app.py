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
st.title("📊 Análisis de Egresos Hospitalarios")

# SIDEBAR: FILTROS
st.sidebar.markdown("## ⚙️ Filtros de Análisis")
min_a, max_a = int(df['AÑO'].min()), int(df['AÑO'].max())
rango_anios = st.sidebar.slider("Rango de Años", min_a, max_a, (min_a, max_a))
regiones = st.sidebar.multiselect("Región", df['REGION'].unique(), default=df['REGION'].unique())
sectores = st.sidebar.multiselect("Sector", df['SECTOR'].unique(), default=df['SECTOR'].unique())

# APLICACIÓN DE FILTROS
df_f = df[(df['AÑO'].between(rango_anios[0], rango_anios[1])) &
          (df['REGION'].isin(regiones)) &
          (df['SECTOR'].isin(sectores))]

# --- RESUMEN ESTADÍSTICO ---
st.markdown("---")
st.subheader("📊 Análisis Descriptivo Estadístico")
stats = df_f.describe().T[['mean', 'std', 'min', 'max', '50%']]
stats.columns = ['Media', 'Desviación Estándar', 'Mínimo', 'Máximo', 'Mediana']
st.dataframe(stats, use_container_width=True)

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total de Egresos", f"{len(df_f):,}")
col2.metric("Promedio Egresos/Año", f"{df_f.groupby('AÑO').size().mean():,.0f}")

# --- VISUALIZACIÓN DINÁMICA ---
st.subheader("📈 Visualización Dinámica")
col_izq, col_der = st.columns(2)

with col_izq:
    st.write("#### TOP 10 DIAGNÓSTICOS")
    top_10 = df_f['DIAGNOSTICO'].value_counts().nlargest(10).reset_index()
    fig_hist = px.bar(top_10, x='count', y='DIAGNOSTICO', orientation='h', color='count', color_continuous_scale='Blues')
    st.plotly_chart(fig_hist, use_container_width=True)

    # NUEVO: EGRESOS POR SECTOR Y AÑO
    st.write("#### EGRESOS POR SECTOR Y AÑO")
    sector_anio = df_f.groupby(['AÑO', 'SECTOR']).size().reset_index(name='CANTIDAD')
    fig_sector_anio = px.bar(sector_anio, x='AÑO', y='CANTIDAD', color='SECTOR', barmode='stack',
                             title="Evolución de Egresos por Sector")
    st.plotly_chart(fig_sector_anio, use_container_width=True)

with col_der:
    st.write("#### EGRESOS POR GÉNERO")
    fig_sexo = px.pie(df_f, names='GENERO', hole=0.6, color='GENERO', color_discrete_map={'F': '#FF69B4', 'M': '#00A8E8'})
    st.plotly_chart(fig_sexo, use_container_width=True)

# --- GRÁFICO DE DISPERSIÓN ---
st.markdown("---")
st.subheader("🔗 Gráfico de Dispersión: Relación Años vs Volumen")
scatter_data = df_f.groupby('AÑO').size().reset_index(name='CANTIDAD')
fig_scatter = px.scatter(scatter_data, x='AÑO', y='CANTIDAD', size='CANTIDAD',
                         color='CANTIDAD', title="Tendencia de Egresos por Año")
st.plotly_chart(fig_scatter, use_container_width=True)