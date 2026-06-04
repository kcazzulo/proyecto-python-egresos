import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Análisis de Egresos Hospitalarios", layout="wide")


# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, 'data', 'egresos_hospitalarios_limpio.csv')

    if not os.path.exists(file_path):
        st.error(f"Error: No se encontró el archivo en {file_path}")
        return pd.DataFrame()

    return pd.read_csv(file_path)


# --- EJECUCIÓN ---
df = load_data()

# --- INTERFAZ ---
if not df.empty:
    st.title("📊 Análisis de Egresos Hospitalarios")

    # SIDEBAR: FILTROS
    st.sidebar.markdown("## ⚙️ Filtros de Análisis")
    min_a, max_a = int(df['AÑO'].min()), int(df['AÑO'].max())
    rango_anios = st.sidebar.slider("Rango de Años", min_a, max_a, (min_a, max_a))

    regiones = st.sidebar.multiselect("Región", df['REGION'].unique(), default=df['REGION'].unique())
    sectores = st.sidebar.multiselect("Sector", df['SECTOR'].unique(), default=df['SECTOR'].unique())

    # APLICACIÓN DE FILTROS
    df_f = df[
        (df['AÑO'].between(rango_anios[0], rango_anios[1])) &
        (df['REGION'].isin(regiones)) &
        (df['SECTOR'].isin(sectores))
        ]

    # KPIs
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    total_egresos = len(df_f)
    promedio_anual = df_f.groupby('AÑO').size().mean() if not df_f.empty else 0

    col1.metric("Total de Egresos", f"{total_egresos:,}")
    col2.metric("Promedio Egresos/Año", f"{promedio_anual:,.0f}")

    # RESUMEN TABULAR
    st.markdown("---")
    st.subheader("📋 Resumen de Egresos por Año")
    resumen_anual = df_f.groupby('AÑO').size().reset_index(name='CANTIDAD DE EGRESOS')
    st.dataframe(resumen_anual, use_container_width=True)

    # VISUALIZACIÓN DINÁMICA
    st.subheader("📈 Visualización Dinámica")
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.write("#### Top 10 Diagnósticos")
        top_10 = df_f['DIAGNOSTICO'].value_counts().nlargest(10).reset_index()
        top_10.columns = ['DIAGNOSTICO', 'Cantidad']
        fig_hist = px.bar(top_10, x='Cantidad', y='DIAGNOSTICO', orientation='h', color='Cantidad',
                          color_continuous_scale='Blues')
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_g2:
        st.write("#### Egresos por Sector")
        conteo_sector = df_f['SECTOR'].value_counts().reset_index()
        conteo_sector.columns = ['Sector', 'Cantidad']
        fig_pie = px.pie(conteo_sector, values='Cantidad', names='Sector', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.error("No se pudieron cargar los datos. Verifica la ruta en tu repositorio.")