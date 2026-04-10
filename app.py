import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN E INTERFAZ
# 'expanded' hace que el menú lateral aparezca abierto por defecto
st.set_page_config(page_title="Sirius Community PRO", layout="wide", initial_sidebar_state="expanded")

# ESTILO VISUAL MEJORADO
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    p, span, label, .stMarkdown { color: #ffffff !important; font-weight: 500; }
    h1, h2, h3 { color: #00ffcc !important; text-shadow: 0 0 5px rgba(0, 255, 204, 0.3); }
    .stTextInput>div>div>input { background-color: #1a1c24 !important; color: white !important; border: 2px solid #3d3f4b !important; }
    .stButton>button { background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold !important; width: 100%; border-radius: 10px !important; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 1px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE LOGIN (CORREO)
st.sidebar.title("🔑 INICIO DE SESIÓN")
user_email = st.sidebar.text_input("Introduce tu Correo Electrónico", placeholder="ejemplo@correo.com")

if not user_email:
    st.title("⚽ Bienvenido a Sirius Community")
    st.warning("⚠️ Por favor, introduce tu correo en el menú de la izquierda para continuar.")
    st.stop() # Detiene la app hasta que pongan el correo

# 3. NAVEGACIÓN (Solo visible si hay correo)
st.sidebar.success(f"Sesión: {user_email}")
rol = st.sidebar.radio("Ir a:", ["Inicio / Clasificación", "Área de DT (Inscripción)", "Panel de Administrador"])

# 4. SECCIÓN: INICIO / CLASIFICACIÓN
if rol == "Inicio / Clasificación":
    st.title("🏆 Clasificación General")
    # Ejemplo de tabla de liga
    data = {"Equipo": ["Sirius A", "Sirius B", "Titanes FC"], "Puntos": [15, 12, 10], "PJ": [5, 5, 5]}
    df = pd.DataFrame(data)
    st.table(df)

# 5. SECCIÓN: ÁREA DE DT
elif rol == "Área de DT (Inscripción)":
    st.title("📝 Registro de Director Técnico")
    
    with st.form("registro_dt"):
        col1, col2 = st.columns(2)
        with col1:
            equipo = st.text_input("Nombre del Equipo")
            whatsapp = st.text_input("WhatsApp de contacto")
        with col2:
            liga_interes = st.selectbox("Selecciona la Liga", ["Top Ligue", "Relámpago #7", "Copa Sirius"])
            logo = st.file_uploader("Sube el Logo del Equipo", type=["png", "jpg"])
        
        if st.form_submit_button("Confirmar Inscripción"):
            st.success(f"¡Registro enviado! Gracias, DT del equipo {equipo}.")

# 6. SECCIÓN: ADMINISTRADOR
elif rol == "Panel de Administrador":
    st.title("🔐 Control Maestro")
    admin_code = st.text_input("Código de Administrador", type="password")
    
    if admin_code == "Sirius2026": # Tu clave actual
        st.write("### Gestión de Ligas")
        nueva_liga = st.text_input("Nombre de la nueva liga/torneo")
        if st.button("Crear Liga"):
            st.success(f"Liga '{nueva_liga}' creada exitosamente.")
            
        st.write("---")
        st.write("### Validar Resultados")
        st.info("Aquí aparecerán las fotos de evidencia enviadas por los DTs.")
    elif admin_code != "":
        st.error("Código incorrecto.")

st.sidebar.divider()
st.sidebar.caption("Sirius System v1.3 | Admin: Walllesglint72")
