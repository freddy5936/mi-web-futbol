import streamlit as st
import pandas as pd
import random
from PIL import Image

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Sirius Community PRO v2", layout="wide", initial_sidebar_state="expanded")

# Inicialización de bases de datos internas (Session State)
if 'equipos_db' not in st.session_state:
    # Agregamos algunos equipos de prueba para la demo
    st.session_state['equipos_db'] = [
        {"Nombre": "Freddy FC", "WhatsApp": "+1234", "Torneo": "Top Ligue"},
        {"Nombre": "Wallles Elite", "WhatsApp": "+5678", "Torneo": "Top Ligue"}
    ]
if 'ligas' not in st.session_state:
    st.session_state['ligas'] = ["Top Ligue", "Ligue 2"]
if 'relampagos' not in st.session_state:
    st.session_state['relampagos'] = ["Relámpago #6"]
if 'calendarios' not in st.session_state:
    st.session_state['calendarios'] = {}
if 'reportes_pendientes' not in st.session_state:
    st.session_state['reportes_pendientes'] = [] # Buzón para el Admin

# 2. ESTILO VISUAL PERSONALIZADO (Modo Oscuro Sirius)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-shadow: 0 0 5px rgba(0, 255, 204, 0.3); }
    button[kind="headerNoPadding"] { background-color: #00ffcc !important; transform: scale(1.2); color: #0b0e14 !important; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 2px solid #00ffcc; }
    
    /* Campos de texto claros */
    .stTextInput>div>div>input {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Botones Pro */
    .stButton>button {
        background-color: #00ffcc !important;
        color: #0b0e14 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (Sidebar)
with st.sidebar:
    st.title("🎮 PANEL SIRIUS")
    user_email = st.text_input("📩 Correo Electrónico", placeholder="tu@correo.com")
    
    if user_email:
        st.write("---")
        rol = st.radio("Secciones:", ["🏆 Competiciones", "📋 Área de DT (Reportar)", "📝 Inscripción", "⚙️ Admin"])

# --- FUNCIONES TÉCNICAS ---
def generar_fixture(equipos, num_jornadas=3):
    if len(equipos) < 2: return []
    fixture = []
    # Generador simple de jornadas aleatorias
    for i in range(num_jornadas):
        jornada = []
        random.shuffle(equipos)
        lista = equipos.copy()
        while len(lista) > 1:
            jornada.append(f"{lista.pop(0)} vs {lista.pop(0)}")
        fixture.append(jornada)
    return fixture

# 4. CONTENIDO PRINCIPAL
if user_email:
    # ---------------------------------------------------------
    # SECCIÓN 1: ESTADO DE LAS COMPETICIONES (VISTA PÚBLICA)
    # ---------------------------------------------------------
    if rol == "🏆 Competiciones":
        st.title("🏆 Estado de las Competiciones")
        cat = st.radio("Categoría:", ["Ligas", "Relámpagos"], horizontal=True)
        lista = st.session_state['ligas'] if cat == "Ligas" else st.session_state['relampagos']
        sel = st.selectbox("Selecciona:", lista)
        
        tab_list, tab_cross = st.tabs(["📊 Equipos", "📅 Cruces"])
        with tab_list:
            eqs = [e for e in st.session_state['equipos_db'] if e["Torneo"] == sel]
            if eqs:
                df_eq = pd.DataFrame(eqs)
                st.table(df_eq[["Nombre"]])
            else: st.info("Sin equipos.")
        with tab_cross:
            if sel in st.session_state['calendarios']:
                for idx, jornada in enumerate(st.session_state['calendarios'][sel]):
                    with st.expander(f"Jornada {idx + 1}"):
                        for partido in jornada: st.write(f"⚽ {partido}")
            else: st.warning("Cruces no generados por el Admin.")

    # ---------------------------------------------------------
    # SECCIÓN 2: ÁREA DE DT (REPORTAR RESULTADO CON FOTO)
    # ---------------------------------------------------------
    elif rol == "📋 Área de DT (Reportar)":
        st.title("📋 Reporte de Resultados (DTs)")
        st.write("Bienvenido DT. Selecciona el torneo, equipos y sube la foto de evidencia.")
        
        torneo_r = st.selectbox("Selecciona el Torneo", st.session_state['ligas'] + st.session_state['relampagos'])
        eq_torneo = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == torneo_r]
        
        with st.form("reporte_dt"):
            col1, col2 = st.columns(2)
            local = col1.selectbox("Equipo Local", eq_torneo)
            vis = col2.selectbox("Equipo Visitante", eq_torneo)
            
            g_l = col1.number_input(f"Goles {local}", min_value=0, value=0)
            g_v = col2.number_input(f"Goles {vis}", min_value=0, value=0)
            
            st.write("---")
            foto = st.file_uploader("Subir Evidencia (Foto del final)", type=["jpg", "png", "jpeg"])
            
            if st.form_submit_button("Enviar Reporte a Admin"):
                if local != vis and foto:
                    # Guardamos el reporte en el buzón del Admin
                    nuevo_reporte = {
                        "DT": user_email,
                        "Torneo": torneo_r,
                        "Partido": f"{local} vs {vis}",
                        "Marcador": f"{g_l} - {g_v}",
                        "Foto": foto
                    }
                    st.session_state['reportes_pendientes'].append(nuevo_reporte)
                    st.success("¡Reporte enviado con éxito al Administrador!")
                else:
                    st.error("Revisa que los equipos sean distintos y sube la foto.")

    # ---------------------------------------------------------
    # SECCIÓN 3: INSCRIPCIÓN
    # ---------------------------------------------------------
    elif rol == "📝 Inscripción":
        st.title("Inscripción de Equipo")
        with st.form("ins"):
            nom_ins = st.text_input("Nombre del Club / Equipo")
            wa_ins = st.text_input("WhatsApp (DT)")
            tipo_ins = st.radio("Tipo:", ["Liga Regular", "Relámpago"], horizontal=True)
            t_r = st.selectbox("Torneo", st.session_state['ligas'] if tipo_ins == "Liga Regular" else st.session_state['relampagos'])
            if st.form_submit_button("Confirmar Registro"):
                if nom_ins and wa_ins:
                    st.session_state['equipos_db'].append({"Nombre": nom_ins, "WhatsApp": wa_ins, "Torneo": t_r})
                    st.success("¡Inscrito!")

    # ---------------------------------------------------------
    # SECCIÓN 4: ADMIN (EL CEREBRO DEL TORNEO)
    # ---------------------------------------------------------
    elif rol == "⚙️ Admin":
        st.title("⚙️ Panel de Administración")
        
        # Usamos una contraseña simple para la demo
        if st.text_input("Código Maestro", type="password") == "Sirius2026":
            
            t1, t2, t3 = st.tabs(["⚡ Generar Jornadas", "📩 Buzón de Reportes (IA)", "🛠 Gestión Datos"])
            
            # --- TAB 1: GENERAR JORNADAS ---
            with t1:
                st.subheader("Publicar Calendario de Liga")
                t_gen = st.selectbox("Selecciona Torneo para generar cruces:", st.session_state['ligas'] + st.session_state['relampagos'])
                n_jor = st.number_input("Número de Jornadas:", min_value=1, value=3)
                
                if st.button("⚡ Generar y Publicar Cruces"):
                    nombres = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == t_gen]
                    if len(nombres) >= 2:
                        st.session_state['calendarios'][t_gen] = generar_fixture(nombres, n_jor)
                        st.success(f"¡Calendario de {n_jor} jornadas publicado para {t_gen}!")
                    else:
                        st.error("Necesitas al menos 2 equipos inscritos en este torneo.")
            
            # --- TAB 2: BUZÓN DE REPORTES (VALIDAR FOTO) ---
            with t2:
                st.subheader("Reportes Pendientes de Validación (DTs)")
                st.write("Revisa la foto de evidencia enviada por el DT para confirmar el resultado.")
                
                if not st.session_state['reportes_pendientes']:
                    st.info("No hay reportes nuevos.")
                else:
                    for idx, rep in enumerate(st.session_state['reportes_pendientes']):
                        with st.expander(f"Reporte de {rep['DT']} - {rep['Torneo']}"):
                            st.write(f"**Partido:** {rep['Partido']}")
                            st.write(f"**Marcador Propuesto:** {rep['Marcador']}")
                            
                            # Mostramos la foto gigante para el Admin
                            image = Image.open(rep['Foto'])
                            st.image(image, caption="Evidencia enviada por el DT", use_column_width=True)
                            
                            st.write("---")
                            # Botones de acción para el admin
                            c1, c2 = st.columns(2)
                            if c1.button(f"✅ Aprobar y Actualizar Tabla", key=f"app_{idx}"):
                                st.success("Resultado validado. (Aquí integrarías la lógica de puntos)").
                                st.session_state['reportes_pendientes'].pop(idx) # Borramos del buzón
                                st.rerun()
                            if c2.button(f"🗑️ Descartar Reporte", key=f"desc_{idx}"):
                                st.warning("Reporte descartado.")
                                st.session_state['reportes_pendientes'].pop(idx) # Borramos del buzón
                                st.rerun()
            
            # --- TAB 3: GESTIÓN DE DATOS ---
            with t3:
                st.subheader("Base de Datos de Equipos")
                if st.session_state['equipos_db']:
                    df = pd.DataFrame(st.session_state['equipos_db'])
                    st.dataframe(df[["Nombre", "WhatsApp", "Torneo"]])
                    if st.button("🗑️ Eliminar todos los equipos"):
                        st.session_state['equipos_db'] = []
                        st.rerun()
        else:
            st.error("Código Maestro Incorrecto.")
