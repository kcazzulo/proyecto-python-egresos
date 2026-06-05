import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Análisis de Egresos Hospitalarios", layout="wide")


# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    # Buscamos en la carpeta 'data' dentro de la ruta actual
    ruta_carpeta = os.path.join(os.getcwd(), 'data')
    archivo_objetivo = 'egresos_hospitalarios_limpio.csv'
    file_path = os.path.join(ruta_carpeta, archivo_objetivo)

    if not os.path.exists(file_path):
        # Esta parte nos dirá qué está pasando realmente
        contenido = os.listdir(os.getcwd()) if not os.path.exists(ruta_carpeta) else os.listdir(ruta_carpeta)
        st.error(f"Error: No encontré '{archivo_objetivo}' en {ruta_carpeta}")
        st.write(f"Archivos encontrados en la carpeta donde busqué: {contenido}")
        return pd.DataFrame()

    return pd.read_csv(file_path)
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
    df_f = df[(df['AÑO'].between(rango_anios[0], rango_anios[1])) &
              (df['REGION'].isin(regiones)) &
              (df['SECTOR'].isin(sectores))]

    # RESUMEN ESTADÍSTICO (REQUISITO ACADÉMICO)
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

    with col_der:
        st.write("#### EGRESOS POR GÉNERO")
        fig_sexo = px.pie(df_f, names='GENERO', hole=0.6, color='GENERO', color_discrete_map={'F': '#FF69B4', 'M': '#00A8E8'})
        st.plotly_chart(fig_sexo, use_container_width=True)

    # --- GRÁFICO DE DISPERSIÓN (REQUISITO ACADÉMICO) ---
    st.markdown("---")
    st.subheader("🔗 Gráfico de Dispersión: Relación Años vs Volumen")
    scatter_data = df_f.groupby('AÑO').size().reset_index(name='CANTIDAD')
    fig_scatter = px.scatter(scatter_data, x='AÑO', y='CANTIDAD', size='CANTIDAD',
                             color='CANTIDAD', title="Tendencia de Egresos por Año")
    st.plotly_chart(fig_scatter, use_container_width=True)

else:
    st.error("No se pudieron cargar los datos. Verifica que el archivo esté en la carpeta /data/")