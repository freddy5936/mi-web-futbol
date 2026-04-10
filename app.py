import streamlit as st
import pandas as pd
from PIL import Image
import os

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

# Estilo oscuro y neón
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .stButton>button { background-color: #00ffcc; color: black; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { background-color: #1a1c24; color: white; border: 1px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL (MENÚ DE USUARIO)
st.sidebar.title("🎮 PANEL SIRIUS")
rol = st.sidebar.radio("Selecciona tu rol:", ["Espectador", "Director Técnico (DT)", "Administrador"])

# 3. SECCIÓN: ESPECTADOR (LO QUE TODOS VEN)
if rol == "Espectador":
    st.title("⚽ SIRIUS COMMUNITY")
    st.subheader("Resultados y Clasificación en Vivo")
    
    # Aquí iría tu tabla de posiciones actual
    st.info("Selecciona 'Director Técnico' en el menú para inscribir a tu equipo.")

# 4. SECCIÓN: DIRECTORES TÉCNICOS (INSCRIPCIONES Y RESULTADOS)
elif rol == "Director Técnico (DT)":
    st.title("📋 Área para DTs")
    
    tab1, tab2 = st.tabs(["📝 Inscripción de Equipo", "⏱️ Reportar Resultado"])
    
    with tab1:
        with st.form("form_inscripcion"):
            st.write("### Formulario de Inscripción")
            nombre_equipo = st.text_input("Nombre del Equipo")
            nombre_dt = st.text_input("ID de PSN / EA ID del DT")
            logo_equipo = st.file_uploader("Sube el Logo de tu Equipo (PNG/JPG)", type=["png", "jpg", "jpeg"])
            
            submit_inscripcion = st.form_submit_button("Enviar Inscripción")
            if submit_inscripcion:
                st.success(f"¡Equipo {nombre_equipo} enviado para revisión del Administrador!")

    with tab2:
        with st.form("form_resultado"):
            st.write("### Reporte de Partido")
            equipo_local = st.text_input("Equipo Local")
            goles_local = st.number_input("Goles Local", min_value=0, step=1)
            st.write("VS")
            equipo_visita = st.text_input("Equipo Visitante")
            goles_visita = st.number_input("Goles Visitante", min_value=0, step=1)
            
            submit_resultado = st.form_submit_button("Subir Resultado")
            if submit_resultado:
                st.warning("Resultado enviado. El administrador debe validarlo para actualizar la tabla.")

# 5. SECCIÓN: ADMINISTRADOR (CONTROL TOTAL)
elif rol == "Administrador":
    st.title("🔐 Panel de Control Sirius")
    password = st.text_input("Introduce la clave de Admin:", type="password")
    
    if password == "Sirius2026": # CAMBIA ESTA CLAVE
        st.success("Acceso concedido, Comandante.")
        
        accion = st.selectbox("¿Qué quieres hacer?", ["Crear Torneo", "Validar Resultados", "Gestionar Equipos"])
        
        if accion == "Crear Torneo":
            nombre_t = st.text_input("Nombre del Nuevo Torneo")
            cupos = st.slider("Número de Cupos", 8, 32, 16)
            if st.button("Lanzar Torneo"):
                st.balloons()
                st.write(f"Torneo '{nombre_t}' creado con {cupos} cupos.")
                
    elif password != "":
        st.error("Clave incorrecta. Solo personal autorizado.")

# Pie de página
st.sidebar.divider()
st.sidebar.caption("Walllesglint72 Admin System v1.0")
