import streamlit as st
import pandas as pd
import os
from PIL import Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Sirius Community PRO", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. ESTILO CSS (Visibilidad y Flecha Neón)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-shadow: 0 0 5px rgba(0, 255, 204, 0.3); }
    
    /* Hacer la flecha del menú gigante y neón */
    button[kind="headerNoPadding"] {
        background-color: #00ffcc !important;
        color: #0b0e14 !important;
        border-radius: 50% !important;
        transform: scale(1.5);
        margin: 10px;
    }

    .stTextInput>div>div>input {
        background-color: #1a1c24 !important;
        color: white !important;
        border: 2px solid #3d3f4b !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #161922 !important;
        border-right: 2px solid #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (INICIO DE SESIÓN)
with st.sidebar:
    st.title("🎮 PANEL SIRIUS")
    user_email = st.text_input("📩 Correo Electrónico", placeholder="tu@correo.com")
    
    if user_email:
        st.success(f"Sesión: {user_email}")
        st.write("---")
        rol = st.radio("Menú:", ["🏆 Clasificación", "📝 Inscribir Equipo", "⚙️ Administración"])
    else:
        st.warning("Introduce tu correo para ver las opciones.")

# 4. CONTENIDO PRINCIPAL
if not user_email:
    st.title("⚽ Sirius Community")
    st.info("Abre el menú a la izquierda e ingresa tu correo para registrar tu equipo.")
    if os.path.exists('logo.png'):
        st.image('logo.png', width=250)

else:
    if rol == "🏆 Clasificación":
        st.title("Tabla de Posiciones")
        # Tabla de ejemplo
        df = pd.DataFrame({
            "Equipo": ["Sirius Elite", "Titanes FC", "Dragones Negros"],
            "PJ": [10, 10, 10],
            "PTS": [28, 22, 19]
        })
        st.table(df)
        
    elif rol == "📝 Inscribir Equipo":
        st.title("Registro de Equipo")
        st.write("Completa los datos para participar en la liga.")
        
        with st.form("registro_simplificado"):
            # SOLO LOS 3 CAMPOS QUE PEDISTE
            nombre_eq = st.text_input("Nombre del Equipo")
            whatsapp_dt = st.text_input("Número de WhatsApp (ej: +593...)")
            logo_subido = st.file_uploader("Sube el Logo del Equipo (PNG/JPG)", type=["png", "jpg", "jpeg"])
            
            submit = st.form_submit_button("Enviar Inscripción")
            
            if submit:
                if nombre_eq and whatsapp_dt:
                    st.balloons()
                    st.success(f"¡El equipo {nombre_eq} ha sido enviado con éxito!")
                else:
                    st.error("Por favor, rellena el nombre y el WhatsApp.")

    elif rol == "⚙️ Administración":
        st.title("Panel de Control")
        clave = st.text_input("Código Maestro", type="password")
        if clave == "Sirius2026":
            st.write("### Gestión de Torneos")
            st.button("Crear Nueva Liga")
            st.button("Ver Inscripciones")

st.sidebar.divider()
st.sidebar.caption("v1.4 | Walllesglint72")
