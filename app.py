import streamlit as st
import pandas as pd
import random

# 1. CONFIGURACIÓN Y MEMORIA
st.set_page_config(page_title="Sirius Community PRO", layout="wide", initial_sidebar_state="expanded")

if 'equipos_registrados' not in st.session_state:
    st.session_state['equipos_registrados'] = []
if 'ligas_creadas' not in st.session_state:
    st.session_state['ligas_creadas'] = ["Top Ligue", "Relámpago #6"]
if 'calendario' not in st.session_state:
    st.session_state['calendario'] = {}

# 2. ESTILO CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; }
    button[kind="headerNoPadding"] { background-color: #00ffcc !important; transform: scale(1.5); }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 2px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    st.title("🎮 PANEL SIRIUS")
    user_email = st.text_input("📩 Correo", placeholder="tu@correo.com")
    if user_email:
        rol = st.radio("Menú:", ["🏆 Clasificación y Cruces", "📝 Inscribir Equipo", "⚙️ Administración"])

# 4. FUNCIONES DE TORNEO
def generar_todos_contra_todos(equipos):
    if len(equipos) < 2: return []
    random.shuffle(equipos)
    jornadas = []
    # Genera 3 jornadas simples para el ejemplo
    for i in range(3):
        cruces = []
        temp_list = equipos.copy()
        while len(temp_list) > 1:
            e1 = temp_list.pop(0)
            e2 = temp_list.pop(0)
            cruces.append(f"{e1} vs {e2}")
        jornadas.append(cruces)
    return jornadas

# 5. CONTENIDO
if user_email:
    if rol == "🏆 Clasificación y Cruces":
        st.title("Estado del Torneo")
        
        tab1, tab2 = st.tabs(["📊 Tabla de Equipos", "📅 Calendario de Cruces"])
        
        with tab1:
            if st.session_state['equipos_registrados']:
                st.table(pd.DataFrame(st.session_state['equipos_registrados']))
            else:
                st.info("Esperando inscripciones...")
        
        with tab2:
            if st.session_state['calendario']:
                for liga, jornadas in st.session_state['calendario'].items():
                    st.header(f"Liga: {liga}")
                    for idx, j in enumerate(jornadas):
                        with st.expander(f"Jornada {idx + 1}"):
                            for partido in j:
                                st.write(f"⚽ {partido}")
            else:
                st.warning("El administrador aún no ha generado los cruces.")

    elif rol == "📝 Inscribir Equipo":
        st.title("Inscripción")
        with st.form("reg"):
            n = st.text_input("Nombre Equipo")
            l = st.selectbox("Liga", st.session_state['ligas_creadas'])
            if st.form_submit_button("Registrar"):
                st.session_state['equipos_registrados'].append({"Nombre": n, "Liga": l})
                st.success("¡Equipo anotado!")

    elif rol == "⚙️ Administración":
        st.title("Panel Maestro")
        clave = st.text_input("Código", type="password")
        if clave == "Sirius2026":
            st.subheader("⚡ Generador de Cruces Automáticos")
            liga_activa = st.selectbox("Seleccionar Liga para cerrar", st.session_state['ligas_creadas'])
            
            if st.button("🔒 Cerrar Inscripciones y Crear 3 Jornadas"):
                # Filtrar equipos de esta liga
                equipos_liga = [e["Nombre"] for e in st.session_state['equipos_registrados'] if e["Liga"] == liga_activa]
                
                if len(equipos_liga) >= 2:
                    st.session_state['calendario'][liga_activa] = generar_todos_contra_todos(equipos_liga)
                    st.balloons()
                    st.success(f"¡Cruces generados para {liga_activa}!")
                else:
                    st.error("Necesitas al menos 2 equipos en esta liga.")
            
            st.write("---")
            if st.button("🔥 Generar Fase de Eliminación (Playoffs)"):
                st.info("Lógica de Playoffs: Se activará al terminar las 3 jornadas.")
