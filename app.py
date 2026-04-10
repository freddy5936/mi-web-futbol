import streamlit as st
import pandas as pd

# Configuración básica para evitar errores de carga
st.set_page_config(page_title="Sirius Community", layout="wide")

st.title("⚽ Sirius Community")
st.write("Bienvenido a la plataforma oficial.")

# Panel de control rápido
col1, col2 = st.columns(2)
with col1:
    st.info("🏆 Próximos Torneos: Disponibles pronto")
with col2:
    st.success("✅ Servidor: Activo")

st.subheader("📊 Clasificación")
datos = {"Equipo": ["Sirius A", "Sirius B"], "Puntos": [10, 8]}
st.table(pd.DataFrame(datos))
