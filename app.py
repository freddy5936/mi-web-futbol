import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Sirius Community", page_icon="⚽")

# Título principal
st.title("⚽ Bienvenido a Sirius Community")

# Texto de bienvenida
st.write("Esta es la web oficial de nuestra comunidad de eSports.")

# Crear una tabla de ejemplo (puedes cambiar los nombres después)
st.subheader("🏆 Tabla de Posiciones - Top Ligue")
df = pd.DataFrame({
    "Equipo": ["Sirius A", "Sirius B", "Titanes FC", "Dragones"],
    "Puntos": [15, 12, 10, 7],
    "PJ": [5, 5, 5, 5]
})
st.table(df)

# Sección de avisos
st.info("📢 Próximo Torneo: Relámpago #7 - ¡Inscripciones abiertas!")
