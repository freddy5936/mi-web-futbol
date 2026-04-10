import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Sirius Community", layout="wide")

# 2. Estilo visual (Dark Mode)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .sidebar .sidebar-content { background-color: #1a1c24; }
    </style>
    """, unsafe_allow_html=True)

# 3. Contenido de la web
st.sidebar.title("🎮 Sirius Menu")
opcion = st.sidebar.radio("Navegación", ["Inicio", "Torneos", "Ligas"])

st.title("⚽ Sirius Community")
st.write("Bienvenido a la plataforma oficial de la comunidad.")

col1, col2, col3 = st.columns(3)
col1.metric("Miembros", "1,200", "+15")
col2.metric("Torneos", "25", "Activo")
col3.metric("Plataforma", "FC Pro Clubs")

st.subheader("🏆 Tabla de Posiciones Reciente")
df = pd.DataFrame({
    "Equipo": ["Sirius A", "Sirius B", "Titanes FC"],
    "Puntos": [45, 42, 38],
    "PJ": [20, 20, 20]
})
st.table(df)
