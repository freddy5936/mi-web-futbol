import streamlit as st
import pandas as pd
import random
from PIL import Image

# 1. CONFIGURACIÓN Y MEMORIA
st.set_page_config(page_title="Sirius Community PRO v2", layout="wide", initial_sidebar_state="expanded")

if 'equipos_db' not in st.session_state:
    st.session_state['equipos_db'] = []
if 'ligas' not in st.session_state:
    st.session_state['ligas'] = ["Top Ligue", "Ligue 2"]
if 'relampagos' not in st.session_state:
    st.session_state['relampagos'] = ["Relámpago #6", "Copa Sirius"]
if 'calendarios' not in st.session_state:
    st.session_state['calendarios'] = {}
if 'reportes_resultados' not in st.session_state:
    st.session_state['reportes_resultados'] = []

# 2. ESTILO VISUAL
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-shadow: 0 0 5px rgba(0, 255, 204, 0.3); }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 2px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    st.title("🎮 PANEL SIRIUS")
    user_email = st.text_input("📩 Correo Electrónico", placeholder="tu@correo.com")
    if user_email:
        st.write("---")
        rol = st.radio("Menú:", ["🏆 Competiciones", "📋 Área de DT (Reportar)", "📝 Inscripción", "⚙️ Admin"])

# Lógica de Cruces
def generar_fixture(nombres):
    if len(nombres) < 2: return []
    random.shuffle(nombres)
    jornadas = []
    for i in range(3):
        partidos = []
        copia = nombres.copy()
        while len(copia) > 1:
            partidos.append(f"{copia.pop(0)} vs {copia.pop(0)}")
        jornadas.append(partidos)
    return jornadas

# 4. CONTENIDO
if user_email:
    if rol == "🏆 Competiciones":
        st.title("Estado de las Competiciones")
        cat = st.radio("Categoría:", ["Ligas", "Relámpagos"], horizontal=True)
        lista = st.session_state['ligas'] if cat == "Ligas" else st.session_state['relampagos']
        sel = st.selectbox("Selecciona:", lista)
        
        t1, t2 = st.tabs(["📊 Equipos", "📅 Cruces"])
        with t1:
            eqs = [e for e in st.session_state['equipos_db'] if e["Torneo"] == sel]
            if eqs: st.table(pd.DataFrame(eqs)[["Nombre", "WhatsApp", "EA ID"]])
            else: st.info("Sin equipos.")
        with t2:
            if sel in st.session_state['calendarios']:
                for i, jor in enumerate(st.session_state['calendarios'][sel]):
                    with st.expander(f"Jornada {i+1}"):
                        for p in jor: st.write(f"⚽ {p}")
            else: st.warning("Cruces no generados.")

    elif rol == "📋 Área de DT (Reportar)":
        st.title("Reporte de Resultados")
        with st.form("reporte"):
            torneo = st.selectbox("Torneo", st.session_state['ligas'] + st.session_state['relampagos'])
            col1, col2 = st.columns(2)
            loc = col1.text_input("Local"); vis = col2.text_input("Visitante")
            g_l = col1.number_input("Goles L", min_value=0); g_v = col2.number_input("Goles V", min_value=0)
            foto = st.file_uploader("Evidencia (Foto)", type=["jpg", "png"])
            if st.form_submit_button("Enviar Reporte"):
                if loc and vis and foto:
                    st.session_state['reportes_resultados'].append({
                        "Torneo": torneo, "Partido": f"{loc} {g_l}-{g_v} {vis}", "Foto": foto, "DT": user_email
                    })
                    st.success("Reporte enviado.")

    elif rol == "📝 Inscripción":
        st.title("Inscripción")
        with st.form("ins"):
            nom = st.text_input("Nombre Equipo")
            wa = st.text_input("WhatsApp")
            ea = st.text_input("EA ID")
            tipo = st.radio("Tipo:", ["Liga Regular", "Relámpago"], horizontal=True)
            dest = st.selectbox("Torneo", st.session_state['ligas'] if tipo == "Liga Regular" else st.session_state['relampagos'])
            if st.form_submit_button("Registrar"):
                st.session_state['equipos_db'].append({"Nombre": nom, "WhatsApp": wa, "EA ID": ea, "Torneo": dest})
                st.success("Inscrito correctamente.")

    elif rol == "⚙️ Admin":
        st.title("Panel Admin")
        # CORRECCIÓN DE LA CLAVE AQUÍ
        pass_input = st.text_input("Código Maestro", type="password")
        if pass_input == "Sirius2026":
            st.success("Acceso concedido")
            tab1, tab2, tab3 = st.tabs(["Equipos", "Cruces", "Validar"])
            
            with tab1: # EDITAR/BORRAR
                if st.session_state['equipos_db']:
                    df = pd.DataFrame(st.session_state['equipos_db'])
                    st.dataframe(df)
                    eq_del = st.selectbox("Borrar equipo:", [e["Nombre"] for e in st.session_state['equipos_db']])
                    if st.button("Eliminar"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != eq_del]
                        st.rerun()
            
            with tab2: # GENERAR CRUCES
                t_sel = st.selectbox("Generar para:", st.session_state['ligas'] + st.session_state['relampagos'])
                if st.button("Crear 3 Jornadas"):
                    noms = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == t_sel]
                    st.session_state['calendarios'][t_sel] = generar_fixture(noms)
                    st.success("Cruces creados.")

            with tab3: # FOTOS
                for r in st.session_state['reportes_resultados']:
                    st.write(f"**{r['Torneo']}**: {r['Partido']} (por {r['DT']})")
                    st.image(r['Foto'])
