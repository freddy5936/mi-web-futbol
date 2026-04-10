import streamlit as st
import pandas as pd
import random
from PIL import Image

# 1. CONFIGURACIÓN
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

# Lógica de Cruces Dinámica
def generar_fixture(nombres, num_jornadas):
    if len(nombres) < 2: return []
    random.shuffle(nombres)
    total_fixture = []
    for i in range(num_jornadas):
        partidos = []
        copia = nombres.copy()
        random.shuffle(copia) # Mezclar en cada jornada para variedad
        while len(copia) > 1:
            partidos.append(f"{copia.pop(0)} vs {copia.pop(0)}")
        total_fixture.append(partidos)
    return total_fixture

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
            if eqs: st.table(pd.DataFrame(eqs)[["Nombre", "WhatsApp"]])
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
        st.title("Inscripción de Equipo")
        with st.form("ins"):
            nom = st.text_input("Nombre del Club / Equipo")
            wa = st.text_input("WhatsApp de Contacto")
            logo = st.file_uploader("Subir Logo del Club (Opcional)", type=["png", "jpg", "jpeg"])
            tipo = st.radio("Tipo de Torneo:", ["Liga Regular", "Relámpago"], horizontal=True)
            dest = st.selectbox("Seleccionar Torneo Específico", st.session_state['ligas'] if tipo == "Liga Regular" else st.session_state['relampagos'])
            if st.form_submit_button("Confirmar Registro"):
                if nom and wa:
                    st.session_state['equipos_db'].append({"Nombre": nom, "WhatsApp": wa, "Torneo": dest, "Logo": logo})
                    st.success(f"¡{nom} ha sido registrado en {dest}!")
                else:
                    st.error("Nombre y WhatsApp son obligatorios.")

    elif rol == "⚙️ Admin":
        st.title("Panel de Administración")
        pass_input = st.text_input("Código Maestro", type="password")
        if pass_input == "Sirius2026":
            tab1, tab2, tab3 = st.tabs(["Equipos", "Cruces", "Validar"])
            
            with tab1: # GESTIÓN
                if st.session_state['equipos_db']:
                    df = pd.DataFrame(st.session_state['equipos_db'])
                    st.dataframe(df[["Nombre", "WhatsApp", "Torneo"]])
                    eq_del = st.selectbox("Selecciona equipo para eliminar:", [e["Nombre"] for e in st.session_state['equipos_db']])
                    if st.button("🗑️ Eliminar Equipo"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != eq_del]
                        st.rerun()
            
            with tab2: # GENERADOR DE JORNADAS
                st.subheader("Generador de Calendario Personalizado")
                t_sel = st.selectbox("Selecciona Competición:", st.session_state['ligas'] + st.session_state['relampagos'])
                n_jor = st.number_input("¿Cuántas jornadas quieres generar?", min_value=1, max_value=20, value=3)
                
                if st.button("⚡ Generar Cruces"):
                    noms = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == t_sel]
                    if len(noms) >= 2:
                        st.session_state['calendarios'][t_sel] = generar_fixture(noms, int(n_jor))
                        st.success(f"Se han generado {n_jor} jornadas para {t_sel}.")
                    else:
                        st.error("Necesitas al menos 2 equipos inscritos en este torneo.")

            with tab3: # VALIDACIÓN
                for r in st.session_state['reportes_resultados']:
                    with st.expander(f"Partido: {r['Partido']}"):
                        st.write(f"Enviado por: {r['DT']}")
                        st.image(r['Foto'])
