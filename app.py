import streamlit as st
import pandas as pd
import random

# 1. CONFIGURACIÓN Y ESTILO FUTURISTA
st.set_page_config(page_title="SIRIUS PRO - Control Panel", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ffcc; }
    .stButton>button { 
        background-color: #00ffcc; color: black; border-radius: 10px;
        font-weight: bold; border: none; width: 100%;
    }
    .stTextInput>div>div>input { background-color: #1a1c23; color: white; border: 1px solid #00ffcc; }
    h1, h2, h3 { color: #00ffcc; text-shadow: 0px 0px 10px #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZACIÓN (Esto arregla los errores de tus imágenes)
if 'partidos_db' not in st.session_state:
    st.session_state['partidos_db'] = []
if 'eliminatorias_db' not in st.session_state:
    st.session_state['eliminatorias_db'] = []
if 'equipos_inscritos' not in st.session_state:
    st.session_state['equipos_inscritos'] = []
if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# 3. BARRA LATERAL (Navegación)
menu = st.sidebar.radio("Navegación", ["Registro de DTs", "Panel Admin (Cruces)", "Tabla y Jornadas", "Historial"])

# --- MÓDULO 1: REGISTRO DE EQUIPOS ---
if menu == "Registro de DTs":
    st.title("⚡ REGISTRO DE EQUIPO")
    with st.form("form_registro"):
        nombre_dt = st.text_input("Nombre del DT")
        nombre_equipo = st.text_input("Nombre del Club")
        if st.form_submit_button("Inscribirse al Torneo"):
            if nombre_dt and nombre_equipo:
                st.session_state['equipos_inscritos'].append({"DT": nombre_dt, "Equipo": nombre_equipo})
                st.success(f"¡{nombre_equipo} ha sido registrado!")
            else:
                st.error("Completa todos los campos.")

# --- MÓDULO 2: PANEL ADMIN (CREADOR DE CRUCES) ---
elif menu == "Panel Admin (Cruces)":
    st.title("⚙️ CONTROL TOTAL - CRUCES")
    
    if len(st.session_state['equipos_inscritos']) < 2:
        st.warning("Se necesitan al menos 2 equipos para generar cruces.")
    else:
        if st.button("GENERAR CRUCES AUTOMÁTICOS (Fase Eliminación)"):
            equipos = [e['Equipo'] for e in st.session_state['equipos_inscritos']]
            random.shuffle(equipos)
            
            # Crear cruces de a pares
            cruces = []
            for i in range(0, len(equipos), 2):
                if i+1 < len(equipos):
                    cruces.append({"Local": equipos[i], "Visitante": equipos[i+1], "Resultado": "VS"})
            
            st.session_state['eliminatorias_db'] = cruces
            st.success("Cruces generados con éxito.")

    if st.session_state['eliminatorias_db']:
        st.subheader("Fase de Eliminación Actual")
        st.table(st.session_state['eliminatorias_db'])

# --- MÓDULO 3: TABLA Y JORNADAS ---
elif menu == "Tabla y Jornadas":
    st.title("📊 TABLA Y JORNADAS")
    if not st.session_state['eliminatorias_db']:
        st.info("No hay jornadas activas en este momento.")
    else:
        df_jornadas = pd.DataFrame(st.session_state['eliminatorias_db'])
        st.dataframe(df_jornadas, use_container_width=True)

# --- MÓDULO 4: HISTORIAL ---
elif menu == "Historial":
    st.title("📁 HISTORIAL DE CAMPEONES")
    if not st.session_state['historial']:
        st.write("El historial está vacío. ¡Que comience la primera edición!")
    else:
        st.table(st.session_state['historial'])
