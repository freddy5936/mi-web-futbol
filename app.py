import streamlit as st
import pandas as pd
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sirius Community PRO", layout="wide", initial_sidebar_state="expanded")

# MEMORIA DEL SISTEMA
if 'equipos_registrados' not in st.session_state:
    st.session_state['equipos_registrados'] = []
if 'ligas' not in st.session_state:
    st.session_state['ligas'] = ["Top Ligue"]
if 'relampagos' not in st.session_state:
    st.session_state['relampagos'] = ["Relámpago #6"]
if 'calendarios' not in st.session_state:
    st.session_state['calendarios'] = {}

# 2. ESTILO CSS (Flecha Neón y Colores)
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
    user_email = st.text_input("📩 Correo Electrónico", placeholder="tu@correo.com")
    if user_email:
        st.write("---")
        rol = st.radio("Menú:", ["🏆 Clasificación y Cruces", "📝 Inscribir Equipo", "⚙️ Administración"])

# 4. LÓGICA DE CRUCES
def generar_fixture(nombres_equipos):
    if len(nombres_equipos) < 2: return []
    random.shuffle(nombres_equipos)
    jornadas = []
    for i in range(3): # Genera 3 jornadas
        partidos = []
        copia = nombres_equipos.copy()
        while len(copia) > 1:
            partidos.append(f"{copia.pop(0)} vs {copia.pop(0)}")
        jornadas.append(partidos)
    return jornadas

# 5. CONTENIDO PRINCIPAL
if user_email:
    if rol == "🏆 Clasificación y Cruces":
        st.title("Estado de las Competiciones")
        cat = st.radio("Ver categoría:", ["Ligas Regulares", "Torneos Relámpago"], horizontal=True)
        
        # Filtrar equipos según la categoría seleccionada
        lista_nombres = st.session_state['ligas'] if cat == "Ligas Regulares" else st.session_state['relampagos']
        torneo_sel = st.selectbox(f"Selecciona {cat}:", lista_nombres)
        
        tab1, tab2 = st.tabs(["📊 Equipos", "📅 Calendario de Cruces"])
        
        with tab1:
            equipos_filtro = [e for e in st.session_state['equipos_registrados'] if e["Torneo"] == torneo_sel]
            if equipos_filtro:
                st.table(pd.DataFrame(equipos_filtro))
            else:
                st.info("No hay equipos inscritos aquí todavía.")
        
        with tab2:
            if torneo_sel in st.session_state['calendarios']:
                for i, jornada in enumerate(st.session_state['calendarios'][torneo_sel]):
                    with st.expander(f"Jornada {i+1}"):
                        for p in jornada: st.write(f"⚽ {p}")
            else:
                st.warning("Cruces no generados por el Admin.")

    elif rol == "📝 Inscribir Equipo":
        st.title("Inscripción de Equipo")
        with st.form("registro"):
            nombre = st.text_input("Nombre del Equipo")
            whatsapp = st.text_input("Número de WhatsApp") # RECUPERADO
            tipo = st.radio("Tipo de competencia:", ["Liga Regular", "Relámpago"], horizontal=True)
            
            # Selección dinámica según el tipo
            opciones = st.session_state['ligas'] if tipo == "Liga Regular" else st.session_state['relampagos']
            destino = st.selectbox("Selecciona el Torneo", opciones)
            
            if st.form_submit_button("Confirmar Registro"):
                if nombre and whatsapp:
                    st.session_state['equipos_registrados'].append({
                        "Nombre": nombre, "WhatsApp": whatsapp, "Torneo": destino, "Categoría": tipo
                    })
                    st.success(f"¡{nombre} inscrito en {destino}!")
                    st.balloons()

    elif rol == "⚙️ Administración":
        st.title("Panel de Control Maestro")
        if st.text_input("Clave", type="password") == "Sirius2026":
            
            st.write("### 🛠️ Gestión de Estructura")
            col1, col2 = st.columns(2)
            with col1:
                nueva_l = st.text_input("Nueva Liga Regular")
                if st.button("Crear Liga"): st.session_state['ligas'].append(nueva_l); st.rerun()
            with col2:
                nuevo_r = st.text_input("Nuevo Relámpago")
                if st.button("Crear Relámpago"): st.session_state['relampagos'].append(nuevo_r); st.rerun()

            st.write("---")
            st.write("### 🔒 Cerrar Inscripciones y Generar Cruces")
            todo = st.session_state['ligas'] + st.session_state['relampagos']
            sel = st.selectbox("Torneo a cerrar:", todo)
            
            if st.button("Generar 3 Jornadas"):
                nombres = [e["Nombre"] for e in st.session_state['equipos_registrados'] if e["Torneo"] == sel]
                if len(nombres) >= 2:
                    st.session_state['calendarios'][sel] = generar_fixture(nombres)
                    st.success(f"Cruces creados para {sel}")
                else:
                    st.error("Necesitas mínimo 2 equipos.")
