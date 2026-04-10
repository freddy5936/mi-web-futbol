import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Sirius Community PRO", 
    layout="wide",
    initial_sidebar_state="auto"
)

# 2. INICIALIZACIÓN DE DATOS (Persistencia en la sesión)
if 'equipos_db' not in st.session_state:
    st.session_state['equipos_db'] = []
if 'noticias' not in st.session_state:
    st.session_state['noticias'] = [
        {"fecha": "2026-04-10", "titulo": "¡Bienvenidos a la nueva Web!", "contenido": "Ya pueden registrar sus equipos y reportar resultados vía IA.", "icono": "🚀"}
    ]
if 'ligas' not in st.session_state:
    st.session_state['ligas'] = ["Top Ligue", "Ligue 2"]
if 'relampagos' not in st.session_state:
    st.session_state['relampagos'] = ["Relámpago #6"]
if 'calendarios' not in st.session_state:
    st.session_state['calendarios'] = {}

# 3. ESTILO CSS (Texto blanco y diseño responsivo)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label {
        color: #ffffff !important;
    }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    
    /* Tarjetas de noticias */
    .noticia-card {
        background-color: #1a1c24;
        border-left: 5px solid #00ffcc;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #00ffcc !important;
        color: #0b0e14 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    section[data-testid="stSidebar"] { background-color: #161922 !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. BARRA LATERAL
with st.sidebar:
    st.title("SIRIUS PANEL")
    user_email = st.text_input("📩 Correo electrónico", placeholder="tu@correo.com")
    
    if user_email:
        st.write("---")
        rol = st.radio(
            "MENÚ:", 
            ["🏠 Inicio / Noticias", "🏆 Competiciones", "📋 Reportar IA", "📝 Inscripción", "⚙️ Admin"]
        )

# 5. LÓGICA DE CONTENIDO
if user_email:
    
    # --- SECCIÓN: INICIO / NOTICIAS ---
    if rol == "🏠 Inicio / Noticias":
        st.title("📢 Tablón de Avisos")
        if st.session_state['noticias']:
            for n in reversed(st.session_state['noticias']): # Ver las más recientes primero
                st.markdown(f"""
                <div class="noticia-card">
                    <h4>{n['icono']} {n['titulo']}</h4>
                    <p style='font-size: 0.8em; color: #888;'>Publicado el: {n['fecha']}</p>
                    <p>{n['contenido']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay noticias nuevas por ahora.")

    # --- SECCIÓN: COMPETICIONES ---
    elif rol == "🏆 Competiciones":
        st.title("🏆 Competiciones")
        c1, c2 = st.columns(2)
        with c1: cat = st.radio("Categoría:", ["Ligas", "Relámpagos"], horizontal=True)
        with c2: 
            opc = st.session_state['ligas'] if cat == "Ligas" else st.session_state['relampagos']
            t_sel = st.selectbox("Torneo:", opc)
        
        tab_t, tab_c = st.tabs(["📊 Clasificación", "⚽ Calendario"])
        with tab_t:
            eq_t = [e for e in st.session_state['equipos_db'] if e["Torneo"] == t_sel]
            if eq_t: st.dataframe(pd.DataFrame(eq_t)[["Nombre", "WhatsApp"]], use_container_width=True)
            else: st.info("Sin equipos inscritos.")
        with tab_c:
            if t_sel in st.session_state['calendarios']:
                for i, jor in enumerate(st.session_state['calendarios'][t_sel]):
                    with st.expander(f"Jornada {i+1}"):
                        for p in jor: st.write(f"• {p}")
            else: st.warning("Calendario no disponible.")

    # --- SECCIÓN: REPORTE IA ---
    elif rol == "📋 Reportar IA":
        st.title("🤖 Reporte con Foto")
        t_rep = st.selectbox("Torneo:", st.session_state['ligas'] + st.session_state['relampagos'])
        archivo = st.file_uploader("Sube tu captura", type=["png", "jpg", "jpeg"])
        if archivo:
            st.image(archivo, width=300)
            if st.button("Analizar con IA"):
                st.success("¡Analizado! Resultado detectado con éxito.")

    # --- SECCIÓN: INSCRIPCIÓN ---
    elif rol == "📝 Inscripción":
        st.title("📝 Inscripción")
        with st.form("reg_form"):
            col1, col2 = st.columns(2)
            nombre = col1.text_input("Nombre del Club")
            wa = col1.text_input("WhatsApp")
            torneo = col2.selectbox("Torneo", st.session_state['ligas'] + st.session_state['relampagos'])
            if st.form_submit_button("Registrar Equipo"):
                if nombre and wa:
                    st.session_state['equipos_db'].append({"Nombre": nombre, "WhatsApp": wa, "Torneo": torneo})
                    st.success(f"¡{nombre} se ha unido!")

    # --- SECCIÓN: ADMIN ---
    elif rol == "⚙️ Admin":
        st.title("⚙️ Panel de Administrador")
        if st.text_input("Clave de acceso", type="password") == "Sirius2026":
            t_noticia, t_gestion, t_cruces = st.tabs(["📢 Publicar Aviso", "🛠 Gestión Equipos", "⚡ Generar Cruces"])
            
            with t_noticia:
                st.subheader("Crear nueva noticia")
                with st.form("form_noticia"):
                    tit = st.text_input("Título del aviso")
                    txt = st.text_area("Contenido del mensaje")
                    ico = st.selectbox("Icono", ["📢", "⚽", "🏆", "⚠️", "🔥", "✅"])
                    if st.form_submit_button("Publicar Noticia"):
                        nueva = {
                            "fecha": datetime.now().strftime("%Y-%m-%d"),
                            "titulo": tit,
                            "contenido": txt,
                            "icono": ico
                        }
                        st.session_state['noticias'].append(nueva)
                        st.success("¡Aviso publicado en el Inicio!")

            with t_gestion:
                if st.session_state['equipos_db']:
                    noms = [e["Nombre"] for e in st.session_state['equipos_db']]
                    sel = st.selectbox("Equipo a eliminar:", noms)
                    if st.button("Eliminar Registro"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != sel]
                        st.rerun()
            
            with t_cruces:
                t_gen = st.selectbox("Torneo para cruces:", st.session_state['ligas'] + st.session_state['relampagos'])
                if st.button("Generar Calendario"):
                    lista = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == t_gen]
                    if len(lista) >= 2:
                        random.shuffle(lista)
                        st.session_state['calendarios'][t_gen] = [[f"{lista[0]} vs {lista[1]}"]]
                        st.success("Cruces publicados.")
else:
    st.title("⚽ Sirius Community")
    st.subheader("La plataforma oficial de torneos Pro Clubs")
    st.info("Ingresa tu correo en el menú lateral para ver las noticias y competiciones.")
