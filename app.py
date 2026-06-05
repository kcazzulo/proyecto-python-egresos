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

df = load_data()

# --- VALIDACIÓN CRÍTICA ---
if df is None:
    st.error("Error crítico: No se encontró el archivo en /data/egresos_hospitalarios_limpio.csv")
    st.stop()

# --- SIDEBAR: FILTROS ---
st.sidebar.markdown("## ⚙️ Filtros de Análisis")
min_a, max_a = int(df['AÑO'].min()), int(df['AÑO'].max())
rango_anios = st.sidebar.slider("Rango de Años", min_a, max_a, (min_a, max_a))
regiones = st.sidebar.multiselect("Región", df['REGION'].unique(), default=df['REGION'].unique())
sectores = st.sidebar.multiselect("Sector", df['SECTOR'].unique(), default=df['SECTOR'].unique())

# APLICACIÓN DE FILTROS
df_f = df[(df['AÑO'].between(rango_anios[0], rango_anios[1])) &
          (df['REGION'].isin(regiones)) &
          (df['SECTOR'].isin(sectores))]

# --- INTERFAZ ---
st.title("📊 Análisis Exploratorio de Egresos Hospitalarios")

# --- RESUMEN ESTADÍSTICO (Al final, para no romper el diseño) ---
with st.expander("Ver Resumen Descriptivo Estadístico"):
    stats = df_f.describe().T[['mean', 'std', '50%', '25%', '75%', 'min', 'max']]
    stats['range'] = stats['max'] - stats['min']
    stats.columns = ['Media', 'Desv. Estándar', 'Mediana', '25%', '75%', 'Mínimo', 'Máximo', 'Rango']
    st.dataframe(stats, use_container_width=True)

# --- KPIs (Formato imagen profesional) ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total de Egresos", f"{len(df_f):,}")
kpi2.metric("Promedio Egresos/Año", f"{df_f.groupby('AÑO').size().mean():,.0f}")

st.markdown("---")

# --- FILA 1 DE GRÁFICOS ---
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.subheader("Egresos por año")
    fig_sector_anio = px.bar(df_f.groupby(['AÑO', 'SECTOR']).size().reset_index(name='CANTIDAD'),
                             x='AÑO', y='CANTIDAD', color='SECTOR', barmode='stack')
    st.plotly_chart(fig_sector_anio, use_container_width=True)

with row1_col2:
    st.subheader("Egresos por Género")
    fig_sexo = px.pie(df_f, names='GENERO', hole=0.6, color='GENERO',
                      color_discrete_map={'F': '#FF69B4', 'M': '#00A8E8'})
    st.plotly_chart(fig_sexo, use_container_width=True)

# --- FILA 2 DE GRÁFICOS ---
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("TOP 10 DIAGNÓSTICOS")
    top_10 = df_f['DIAGNOSTICO'].value_counts().nlargest(10).reset_index()
    fig_hist = px.bar(top_10, x='count', y='DIAGNOSTICO', orientation='h',
                      color='count', color_continuous_scale='Blues')
    st.plotly_chart(fig_hist, use_container_width=True)

with row2_col2:
    st.subheader("Tendencia")
    scatter_data = df_f.groupby('AÑO').size().reset_index(name='CANTIDAD')
    fig_scatter = px.scatter(scatter_data, x='AÑO', y='CANTIDAD', size='CANTIDAD', color='CANTIDAD')
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- NUEVO GRÁFICO: ANÁLISIS DE CAUSAS EXTERNAS ---
st.markdown("---")
st.subheader("⚠️ Análisis de Causas Externas")

# Filtramos para ver solo registros con causa externa (ajusta el valor según tus datos)
# Si tu columna tiene valores como 'SI'/'NO' o tipos de causa, ajusta el filtro:
if 'CAUSA_EXTERNA' in df_f.columns:
    df_causas = df_f[df_f['CAUSA_EXTERNA'].notna()]

    col_c1, col_c2 = st.columns([1, 1])

    with col_c1:
        st.write("#### Distribución por tipo de Causa Externa")
        fig_causas = px.pie(df_causas, names='CAUSA_EXTERNA', hole=0.4,
                            color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_causas, use_container_width=True)

    with col_c2:
        st.write("#### Evolución temporal de Causas Externas")
        causas_tiempo = df_causas.groupby(['AÑO', 'CAUSA EXTERNA']).size().reset_index(name='TOTAL')
        fig_line_causas = px.line(causas_tiempo, x='AÑO', y='TOTAL', color='CAUSA EXTERNA', markers=True)
        st.plotly_chart(fig_line_causas, use_container_width=True)
else:
    st.warning("La columna 'CAUSA_EXTERNA' no fue encontrada en el dataset.")
