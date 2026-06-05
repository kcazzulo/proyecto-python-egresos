import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Análisis de Egresos Hospitalarios", layout="wide")


# --- VISUALIZACIÓN DINÁMICA ---
st.subheader("📈 VISUALIZACIÓN DINÁMICA")

# Definimos las dos columnas principales
col_izq, col_der = st.columns(2)

with col_izq:
    # 1. TOP 10 DIAGNÓSTICOS
    st.write("#### TOP 10 DIAGNÓSTICOS")
    top_10 = df_f['DIAGNOSTICO'].value_counts().nlargest(10).reset_index()
    top_10.columns = ['DIAGNOSTICO', 'CANTIDAD']
    fig_hist = px.bar(top_10, x='CANTIDAD', y='DIAGNOSTICO', orientation='h', color='CANTIDAD',
                      color_continuous_scale='BLUES')
    st.plotly_chart(fig_hist, use_container_width=True)

    # 2. TOP 10 CAUSAS EXTERNAS
    st.write("#### TOP 10 CAUSAS EXTERNAS")
    nombre_columna = 'CAUSA EXTERNA'
    if nombre_columna in df_f.columns:
        top_10_causas = df_f[nombre_columna].value_counts().nlargest(10).reset_index()
        top_10_causas.columns = ['CAUSA', 'CANTIDAD']
        fig_causas = px.bar(top_10_causas, x='CANTIDAD', y='CAUSA', orientation='h', color='CANTIDAD',
                            color_continuous_scale='Reds')
        fig_causas.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_causas, use_container_width=True)
    else:
        st.warning("Columna 'CAUSA EXTERNA' no encontrada.")

with col_der:
    # 3. EGRESOS POR GÉNERO
    st.write("#### EGRESOS POR GÉNERO")
    fig_sexo = px.pie(df_f, names='GENERO', hole=0.6, color='GENERO',
                      color_discrete_map={'F': '#FF69B4', 'M': '#00A8E8'})
    fig_sexo.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_sexo, use_container_width=True)

    # 4. DISTRIBUCIÓN POR SECTOR
    st.write("#### DISTRIBUCIÓN POR SECTOR")
    sexo_sector = df_f.groupby(['SECTOR', 'GENERO']).size().reset_index(name='CANTIDAD')
    fig_sexo_sector = px.bar(sexo_sector, x='SECTOR', y='CANTIDAD', color='GENERO', barmode='group',
                             color_discrete_map={'F': '#FF69B4', 'M': '#00A8E8'})
    st.plotly_chart(fig_sexo_sector, use_container_width=True)