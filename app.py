import streamlit as st
import pandas as pd
from PIL import Image
import os

# 1. Configuración de la Página
st.set_page_config(
    page_title="Sirius Community - Pro Clubs",
    page_icon="⚽",
    layout="wide"
)

# 2. Estilo CSS Avanzado (Efectos Neón y Modo Oscuro Profundo)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #e0e0e0;
    }
    
    /* Contenedor del Título y Logo */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem 0;
        background: linear-gradient(180deg, #1a1c24 0%, #0b0e14 100%);
        border-bottom: 2px solid #00ffcc;
        margin-bottom: 2rem;
    }

    .main-title {
        color: #00ffcc !important;
        font-family: 'Arial Black', sans-serif;
        font-size: 3.5rem !important;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
        margin: 10px 0;
    }

    /* Tarjetas de Estadísticas */
    [data-testid="stMetric"] {
        background-color: #1a1c24;
        border: 1px solid #3d3f4b;
        padding: 20px;
        border-radius: 15px;
        transition: transform 0.3s;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #00ffcc;
    }

    /* Estilo de Tablas */
    .stTable {
        background-color: #1a1c24;
        border-radius: 10px;
        border: 1px solid #3d3f4b;
    }
    
    /* Botones laterales */
    .stButton>button {
        width: 100%;
        background-color: #00ffcc;
        color: #0b0e14;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Encabezado Principal
st.markdown('<div class="header-container">', unsafe_allow_html=True)

# Carga de Logo
if os.path.exists('logo.png'):
    logo = Image.open('logo.png')
    st.image(logo, width=220)
else:
    st.markdown('<h1 style="font-size: 4rem;">⭐</h1>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">SIRIUS COMMUNITY</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-style: italic; font-size: 1.2rem;">Plataforma Oficial de Competiciones Pro Clubs</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 4. Panel de Control (Layout de Columnas)
col_stats, col_main = st.columns([1, 3])

with col_stats:
    st.subheader("📊 Resumen")
    st.metric("Torneos", "25", "S25")
    st.metric("Equipos", "48", "+4")
    st.metric("Jugadores", "+500", "🔥")
    
    st.divider()
    st.subheader("🔗 Accesos Rápidos")
    if st.button("Reglamento 2026"):
        st.write("Cargando documento...")
    if st.button("Inscribir Equipo"):
        st.write("Redirigiendo a Formulario...")

with col_main:
    # Pestañas para organizar la información como en la web de ejemplo
    tab1, tab2, tab3 = st.tabs(["🏆 Clasificación", "📅 Próximos Partidos", "📢 Noticias"])
    
    with tab1:
        st.subheader("Top Ligue - Clasificación General")
        data = {
            "Pos": [1, 2, 3, 4, 5],
            "Club": ["Sirius Elite", "Titanes FC", "Dragones Negros", "Fénix Pro", "Leones FC"],
            "PJ": [10, 10, 10, 10, 10],
            "G": [9, 7, 6, 4, 3],
            "E": [1, 1, 1, 2, 1],
            "P": [0, 2, 3, 4, 6],
            "GF": [25, 18, 15, 12, 8],
            "PTS": [28, 22, 19, 14, 10]
        }
        st.table(pd.DataFrame(data))

    with tab2:
        st.info("📅 Calendario de la Jornada 11")
        st.write("**Sirius Elite vs Titanes FC** - 22:00h")
        st.write("**Dragones Negros vs Fénix Pro** - 22:30h")

    with tab3:
        st.success("✨ ¡Nueva Edición #25 Iniciada!")
        st.write("No te pierdas las transmisiones en vivo por TikTok.")

# 5. Pie de Página
st.markdown("---")
st.caption("Administrado por Walllesglint72 | © 2026 Sirius Community")
