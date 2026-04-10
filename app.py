import streamlit as st
import pandas as pd

# ESTA LÍNEA DEBE IR PRIMERO SIEMPRE
st.set_page_config(page_title="Sirius Community", layout="wide")

st.title("⚽ Sirius Community")
st.write("¡La web está oficialmente activa!")

# Prueba con una tabla simple para ver si carga
df = pd.DataFrame({"Torneo": ["Relámpago #6", "Top Ligue"], "Estado": ["Finalizado", "En curso"]})
st.table(df)
