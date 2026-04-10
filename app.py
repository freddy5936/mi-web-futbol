import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Sirius Community",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ESTILO CSS PERSONALIZADO (Estilo Gol Gana / Dark Sport) ---
st.markdown("""
    <style>
    /* Fondo general y fuentes */
    .main {
        background-color: #0e1117;
    }
    
    /* Personalización de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #1a1c24;
        border-right: 1px solid #3d3f4b;
    }

    /* Estilo para las tarjetas de métricas */
    div[data-testid="metric-container"] {
        background-color: #1f222d;
        border: 1px solid #3d3f4b;
        padding: 15px;
        border-radius: 10px;
        color: white;
    }

    /* Títulos con degradado */
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        background: -webkit-linear-gradient(#fff, #999);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 3rem;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #00d4ff;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* Ajuste de la tabla */
    .stDataFrame {
        border: 1px solid #3d3f4b;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4730/4730534.png", width=100) # Logo temporal
    st.title("SIRIUS")
    st.markdown("---")
    
    # Menú de Navegación
    menu = st.radio(
        "Navegación",
        ["🏠 Inicio", "🏆 Clasificación", "⚽ Plantilla", "📅 Calendario", "⚙️ Configuración"]
    )
    
    st.markdown("---")
    st.info("Conectado como: **Admin_Sirius**")

# --- CUERPO PRINCIPAL ---

# Encabezado estilo Premium
st.markdown('<p class="main-title">SIRIUS COMMUNITY</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Gestión de Clubes Pro | Temporada 2026</p>', unsafe_allow_html=True)

# Fila de métricas rápidas
col1, col2, col3, col4 = st.columns(4)
col1.metric("Partidos Jugados", "24", "+2")
col2.metric("Victorias", "18", "75%")
col3.metric("Goles Favor", "56", "+5")
col4.metric("Posición", "2º", "-1")

st.write("---")

# --- SECCIÓN DE TABLA DE EJEMPLO ---
st.subheader("📊 Tabla de Rendimiento - Plantilla Actual")

# Creación de datos de ejemplo
data = {
    "Jugador": ["Alex7", "GamerPro_99", "Sirius_Capitán", "TheWall_GK", "SpeedyGonz"],
    "Posición": ["DC", "MCO", "MC", "POR", "ED"],
    "Partidos":,
    "Goles":,
    "Asistencias":,
    "Valoración": [8.5, 7.9, 8.2, 9.0, 7.5]
}

df = pd.DataFrame(data)

# Mostrar la tabla con diseño limpio
st.dataframe(
    df.style.set_properties(**{
        'background-color': '#1a1c24',
        'color': 'white',
        'border-color': '#3d3f4b'
    }),
    use_container_width=True,
    hide_index=True
)

# Sección inferior informativa
st.write("---")
c1, c2 = st.columns(2)
with c1:
    st.markdown("### 📝 Próximo Encuentro")
    st.success("⚽ **Sirius CF vs Titan Squad** | Hoy 22:00 CET")
with c2:
    st.markdown("### 📢 Avisos")
    st.warning("Recuerden confirmar asistencia en el canal de Discord.")
