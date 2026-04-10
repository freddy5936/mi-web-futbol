import streamlit as st
import pandas as pd
from PIL import Image
import os

# 1. Configuración de la página (lo primero siempre)
st.set_page_config(
    page_title="Sirius Community",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed" # Barra lateral cerrada por defecto
)

# 2. Estilo CSS Personalizado (Estilo Dark Sport / eSports)
st.markdown("""
    <style>
    /* Fondo general y fuentes */
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    
    /* Centrar el logo y el título */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        padding: 20px;
    }

    /* Título principal en color neón */
    .neon-title {
        color: #00ffcc !important;
        font-family: 'Arial Black', sans-serif;
        text-transform: uppercase;
        font-size: 3em !important;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    /* Subtítulo italic */
    .italic-subtitle {
        color: white;
        font-family: 'Arial', sans-serif;
        font-style: italic;
        font-size: 1.2em;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Estilo para las tarjetas de métricas */
    div[data-testid="metric-container"] {
        background-color: #1f222d;
        border: 1px solid #3d3f4b;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stMetricLabel"] { color: white !important; }
    [data-testid="stMetricValue"] { color: #00ffcc !important; }

    /* Estilo de la tabla */
    .stTable {
        background-color: #1a1c24;
        border-radius: 10px;
        color: white;
    }
    .stTable th { color: #00ffcc !important; }

    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #1a1c24;
        border-right: 1px solid #3d3f4b;
    }
    
    /* Divisiones */
    hr { border-color: #3d3f4b !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. ENCABEZADO CENTRADO CON LOGO Y TÍTULO
st.markdown('<div class="logo-container">', unsafe_allow_html=True)

# Cargamos el logo PNG centrado
logo_path = 'logo.png'
if os.path.exists(logo_path):
    try:
        img = Image.open(logo_path)
        # Mostramos la imagen centrada (use_container_width=False para controlar el tamaño)
        st.image(img, width=250) 
    except Exception as e:
        st.error(f"Error cargando el logo: {e}")
else:
    # Si no hay logo, mostramos un marcador
    st.markdown('<h1 style="text-align:center; font-size:5em;">⭐</h1>', unsafe_allow_html=True)

# Título y subtítulo centrado con CSS personalizado
st.markdown('<h1 class="neon-title">SIRIUS COMMUNITY</h1>', unsafe_allow_html=True)
st.markdown('<p class="italic-subtitle">Liderando el Pro Clubs de EA Sports FC</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True) # Cierra logo-container

st.divider()

# 4. Panel de Estadísticas (Métricas rápidas)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ediciones", "25", "S25")
col2.metric("Equipos", "48", "+4")
col3.metric("Relámpagos", "#6", "✅")
col4.metric("Estado", "Activo", "🔥")

st.divider()

# 5. Tabla de Clasificación Principal con estilo
st.subheader("🏆 CLASIFICACIÓN - TOP LIGUE")

# Aquí puedes editar los nombres de los equipos y sus puntos
tabla_data = {
    "POS": [1, 2, 3, 4, 5],
    "EQUIPO": ["Sirius Elite", "Titanes FC", "Dragones Negros", "Fénix Pro", "Leones FC"],
    "PJ": [10, 10, 10, 10, 10],
    "G": [9, 7, 6, 4, 3],
    "E": [1, 1, 1, 2, 1],
    "P": [0, 2, 3, 4, 6],
    "PTS": [28, 22, 19, 14, 10]
}

df = pd.DataFrame(tabla_data)
# Mostramos la tabla formateada
st.table(df)

# 6. Sidebar (Oculto por defecto para mejor vista)
st.sidebar.title("Navegación")
st.sidebar.radio("Secciones:", ["🏠 Inicio", "📅 Calendario", "📝 Inscripciones", "📺 TikTok Live"])
st.sidebar.divider()
st.sidebar.info("📢 **Aviso:** Próximo Torneo Relámpago anunciado en TikTok.")

# Pie de página
st.markdown("---")
st.caption("© 2026 Sirius Community - Administrado por Walllesglint72")
