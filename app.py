import streamlit as st
import pandas as pd
from PIL import Image
import os

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

# ESTILO MEJORADO PARA VISIBILIDAD TOTAL
st.markdown("""
    <style>
    /* Fondo oscuro profundo */
    .stApp { 
        background-color: #0b0e14; 
    }
    
    /* Letras de todo el cuerpo en blanco para que se vean */
    p, span, label, .stMarkdown {
        color: #ffffff !important;
        font-weight: 500;
    }

    /* Títulos en Turquesa Neón */
    h1, h2, h3 {
        color: #00ffcc !important;
        text-shadow: 0 0 5px rgba(0, 255, 204, 0.3);
    }

    /* Campos de texto (Inputs) con bordes visibles */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #1a1c24 !important;
        color: white !important;
        border: 2px solid #3d3f4b !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #00ffcc !important;
    }

    /* Botones Pro */
    .stButton>button {
        background-color: #00ffcc !important;
        color: #0b0e14 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
    }

    /* Estilo de la barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #161922 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL
st.sidebar.title("🎮 PANEL SIRIUS")
rol = st.sidebar.radio("Selecciona tu rol:", ["Espectador", "Director Técnico (DT)", "Administrador"])

# 3. SECCIÓN: ESPECTADOR
if rol == "Espectador":
    st.title("⚽ SIRIUS COMMUNITY")
    if os.path.exists('logo.png'):
        st.image('logo.png', width=200)
    st.subheader("Clasificación en Vivo")
    st.info("Ve al menú de la izquierda para inscribir a tu equipo.")

# 4. SECCIÓN: DIRECTORES TÉCNICOS (INSCRIPCIONES Y RESULTADOS)
elif rol == "Director Técnico (DT)":
    st.title("📋 Área de Gestión para DTs")
    
    tab1, tab2 = st.tabs(["📝 Inscripción y Contacto", "⏱️ Reportar Resultado"])
    
    with tab1:
        with st.form("form_inscripcion"):
            st.write("### Datos del Equipo y Contacto")
            nombre_equipo = st.text_input("Nombre del Equipo")
            nombre_dt = st.text_input("Nombre del DT / EA ID")
            telefono = st.text_input("Número de WhatsApp (con código de país, ej: +593...)", placeholder="+593")
            logo_equipo = st.file_uploader("Sube el Logo del Equipo", type=["png", "jpg"])
            submit_inscripcion = st.form_submit_button("Enviar a Revisión")
            if submit_inscripcion:
                st.success(f"Inscripción de {nombre_equipo} enviada.")

    with tab2:
        with st.form("form_resultado"):
            st.write("### Reporte de Partido")
            col1, col2 = st.columns(2)
            with col1:
                local = st.text_input("Equipo Local")
                goles_l = st.number_input("Goles Local", min_value=0)
            with col2:
                visita = st.text_input("Equipo Visitante")
                goles_v = st.number_input("Goles Visitante", min_value=0)
            
            # --- NUEVO CAMPO: SUBIR EVIDENCIA (FOTO) ---
            st.write("---")
            st.write("### Evidencia del Resultado")
            evidencia_foto = st.file_uploader("Sube una captura de pantalla del final del partido (PNG/JPG)", type=["png", "jpg", "jpeg"])
            
            if st.form_submit_button("Subir Resultado"):
                if evidencia_foto is not None:
                    st.warning("Resultado y evidencia enviados. El Admin verificará la foto antes de actualizar la tabla.")
                else:
                    st.error("⚠️ Debes subir una foto como evidencia del resultado.")

# 5. SECCIÓN: ADMINISTRADOR
elif rol == "Administrador":
    st.title("🔐 Panel de Control Sirius")
    password = st.text_input("Clave de Acceso:", type="password")
    
    if password == "Sirius2026":
        st.success("Acceso concedido.")
        st.selectbox("Gestión:", ["Crear Torneo", "Ver solicitudes de DTs", "Validar Resultados (Ver Fotos)", "Editar Tabla"])
    elif password != "":
        st.error("Clave incorrecta.")

st.sidebar.divider()
st.sidebar.caption("Sirius System v1.2 - Walllesglint72")
