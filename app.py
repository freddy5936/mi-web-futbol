import streamlit as st
import pandas as pd
import random
from PIL import Image

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sirius Community PRO v2", layout="wide", initial_sidebar_state="expanded")

# Inicialización de estados
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
def generar_fixture(nombres, num_jornadas):
    if len(nombres) < 2: return []
    total_fixture = []
    for i in range(num_jornadas):
        partidos = []
        copia = nombres.copy()
        random.shuffle(copia)
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
            else: st.info("Sin equipos inscritos.")
        with t2:
            if sel in st.session_state['calendarios']:
                for i, jor in enumerate(st.session_state['calendarios'][sel]):
                    with st.expander(f"Jornada {i+1}"):
                        for p in jor: st.write(f"⚽ {p}")
            else: st.warning("Cruces no generados.")

    elif rol == "📋 Área de DT (Reportar)":
        st.title("Reporte de Resultados")
        # Selección de torneo para filtrar equipos
        torneo_sel = st.selectbox("Selecciona el Torneo", st.session_state['ligas'] + st.session_state['relampagos'])
        
        # Obtener nombres de equipos registrados en ese torneo
        equipos_en_torneo = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == torneo_sel]
        
        if not equipos_en_torneo:
            st.warning("No hay equipos registrados en este torneo para reportar resultados.")
        else:
            with st.form("reporte"):
                col1, col2 = st.columns(2)
                loc = col1.selectbox("Equipo Local", equipos_en_torneo)
                vis = col2.selectbox("Equipo Visitante", equipos_en_torneo)
                
                g_l = col1.number_input(f"Goles {loc}", min_value=0, step=1)
                g_v = col2.number_input(f"Goles {vis}", min_value=0, step=1)
                
                foto = st.file_uploader("Evidencia (Captura de pantalla)", type=["jpg", "png", "jpeg"])
                
                if st.form_submit_button("Enviar Reporte"):
                    if loc == vis:
                        st.error("El equipo local y visitante no pueden ser el mismo.")
                    elif foto:
                        st.session_state['reportes_resultados'].append({
                            "Torneo": torneo_sel, 
                            "Partido": f"{loc} {g_l}-{g_v} {vis}", 
                            "Foto": foto, 
                            "DT": user_email
                        })
                        st.success("Reporte enviado correctamente a revisión.")
                    else:
                        st.error("Debes subir la foto de evidencia.")

    elif rol == "📝 Inscripción":
        st.title("Inscripción de Equipo")
        # Radio para elegir tipo
        tipo_t = st.radio("Tipo de Torneo:", ["Liga Regular", "Relámpago"], horizontal=True)
        
        # Filtrado dinámico de la lista de torneos según el radio anterior
        opciones_torneo = st.session_state['ligas'] if tipo_t == "Liga Regular" else st.session_state['relampagos']
        
        with st.form("ins_form"):
            nom_club = st.text_input("Nombre del Club / Equipo")
            wa_num = st.text_input("WhatsApp de Contacto")
            logo_club = st.file_uploader("Subir Logo (Opcional)", type=["png", "jpg", "jpeg"])
            torneo_final = st.selectbox("Confirmar Torneo", opciones_torneo)
            
            if st.form_submit_button("Registrar"):
                if nom_club and wa_num:
                    st.session_state['equipos_db'].append({
                        "Nombre": nom_club, 
                        "WhatsApp": wa_num, 
                        "Torneo": torneo_final, 
                        "Logo": logo_club
                    })
                    st.success(f"¡{nom_club} registrado con éxito en {torneo_final}!")
                else:
                    st.error("Faltan datos obligatorios.")

    elif rol == "⚙️ Admin":
        st.title("Panel Admin")
        pass_in = st.text_input("Código Maestro", type="password")
        if pass_in == "Sirius2026":
            t_admin1, t_admin2, t_admin3 = st.tabs(["Gestión", "Generar Cruces", "Reportes"])
            
            with t_admin1:
                if st.session_state['equipos_db']:
                    st.write("Equipos Registrados:")
                    df_eq = pd.DataFrame(st.session_state['equipos_db'])
                    st.dataframe(df_eq[["Nombre", "WhatsApp", "Torneo"]])
                    
                    e_borrar = st.selectbox("Eliminar equipo:", [e["Nombre"] for e in st.session_state['equipos_db']])
                    if st.button("🗑️ Borrar"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != e_borrar]
                        st.rerun()

            with t_admin2:
                t_gen = st.selectbox("Torneo para Calendario:", st.session_state['ligas'] + st.session_state['relampagos'])
                n_jor = st.number_input("Número de Jornadas:", min_value=1, max_value=20, value=3)
                if st.button("⚡ Generar"):
                    nombres = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == t_gen]
                    if len(nombres) >= 2:
                        st.session_state['calendarios'][t_gen] = generar_fixture(nombres, int(n_jor))
                        st.success(f"Calendario de {n_jor} jornadas creado.")
                    else:
                        st.error("Faltan equipos en este torneo.")

            with t_admin3:
                for rep in st.session_state['reportes_resultados']:
                    with st.expander(f"Resultado: {rep['Partido']} ({rep['Torneo']})"):
                        st.write(f"Informado por: {rep['DT']}")
                        st.image(rep['Foto'])
