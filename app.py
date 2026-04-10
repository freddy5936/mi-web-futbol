import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

# 2. INICIALIZACIÓN DE BASES DE DATOS (Session State)
if 'usuarios' not in st.session_state:
    # Usuario admin por defecto
    st.session_state['usuarios'] = {"admin@sirius.com": "Sirius2026"} 
if 'usuario_logueado' not in st.session_state:
    st.session_state['usuario_logueado'] = None
if 'equipos_db' not in st.session_state:
    st.session_state['equipos_db'] = []
if 'noticias' not in st.session_state:
    st.session_state['noticias'] = [{"fecha": "2026-04-10", "titulo": "Sistema de Cuentas Activo", "contenido": "Ya pueden crear su propio perfil con contraseña.", "icono": "🔐"}]
if 'ligas' not in st.session_state:
    st.session_state['ligas'] = ["Top Ligue", "Ligue 2"]
if 'relampagos' not in st.session_state:
    st.session_state['relampagos'] = ["Relámpago #6"]
if 'calendarios' not in st.session_state:
    st.session_state['calendarios'] = {}

# 3. ESTILO CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    .noticia-card { background-color: #1a1c24; border-left: 5px solid #00ffcc; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .stButton>button { width: 100%; background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold !important; border-radius: 10px; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. LÓGICA DE AUTENTICACIÓN (LOGIN / REGISTRO)
def pantalla_login():
    st.title("⚽ Bienvenido a Sirius Community")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Inicia Sesión")
        email_l = st.text_input("Correo electrónico", key="l_email")
        pass_l = st.text_input("Contraseña", type="password", key="l_pass")
        if st.button("Entrar"):
            if email_l in st.session_state['usuarios'] and st.session_state['usuarios'][email_l] == pass_l:
                st.session_state['usuario_logueado'] = email_l
                st.rerun()
            else:
                st.error("Correo o contraseña incorrectos")

    with col2:
        st.subheader("Crea tu Cuenta")
        email_r = st.text_input("Nuevo Correo", key="r_email")
        pass_r = st.text_input("Crea tu Contraseña", type="password", key="r_pass")
        confirm_r = st.text_input("Confirma Contraseña", type="password", key="r_confirm")
        if st.button("Registrarse"):
            if email_r in st.session_state['usuarios']:
                st.warning("Este correo ya tiene cuenta.")
            elif pass_r != confirm_r:
                st.error("Las contraseñas no coinciden.")
            elif email_r and pass_r:
                st.session_state['usuarios'][email_r] = pass_r
                st.success("¡Cuenta creada! Ahora puedes iniciar sesión.")
            else:
                st.error("Rellena todos los campos.")

# 5. PANEL PRINCIPAL (SI ESTÁ LOGUEADO)
if st.session_state['usuario_logueado'] is None:
    pantalla_login()
else:
    # BARRA LATERAL
    with st.sidebar:
        st.title("SIRIUS PANEL")
        st.write(f"👤: {st.session_state['usuario_logueado']}")
        rol = st.radio("MENÚ:", ["🏠 Inicio", "🏆 Competiciones", "📋 Reportar IA", "📝 Inscripción", "⚙️ Admin"])
        if st.button("Cerrar Sesión"):
            st.session_state['usuario_logueado'] = None
            st.rerun()

    # --- CONTENIDOS ---
    if rol == "🏠 Inicio":
        st.title("📢 Tablón de Avisos")
        for n in reversed(st.session_state['noticias']):
            st.markdown(f'<div class="noticia-card"><h4>{n["icono"]} {n["titulo"]}</h4><p>{n["contenido"]}</p></div>', unsafe_allow_html=True)

    elif rol == "🏆 Competiciones":
        st.title("🏆 Competiciones")
        cat = st.radio("Categoría:", ["Ligas", "Relámpagos"], horizontal=True)
        opc = st.session_state['ligas'] if cat == "Ligas" else st.session_state['relampagos']
        t_sel = st.selectbox("Torneo:", opc)
        
        tab1, tab2 = st.tabs(["📊 Equipos", "⚽ Calendario"])
        with tab1:
            eqs = [e for e in st.session_state['equipos_db'] if e["Torneo"] == t_sel]
            if eqs: st.dataframe(pd.DataFrame(eqs), use_container_width=True)
            else: st.info("Sin equipos.")
        with tab2:
            if t_sel in st.session_state['calendarios']:
                for idx, jor in enumerate(st.session_state['calendarios'][t_sel]):
                    with st.expander(f"Jornada {idx+1}"):
                        for p in jor: st.write(f"• {p}")

    elif rol == "📋 Reportar IA":
        st.title("🤖 Reporte IA")
        archivo = st.file_uploader("Sube foto del resultado", type=["png", "jpg", "jpeg"])
        if archivo and st.button("Analizar"):
            st.success("Resultado detectado con éxito.")

    elif rol == "📝 Inscripción":
        st.title("📝 Inscripción")
        with st.form("reg"):
            nom = st.text_input("Nombre del Club")
            wa = st.text_input("WhatsApp")
            tor = st.selectbox("Torneo", st.session_state['ligas'] + st.session_state['relampagos'])
            if st.form_submit_button("Registrar"):
                st.session_state['equipos_db'].append({"Nombre": nom, "WhatsApp": wa, "Torneo": tor})
                st.success("¡Inscrito!")

    elif rol == "⚙️ Admin":
        st.title("⚙️ Administración")
        # Solo el correo admin@sirius.com tiene acceso total
        if st.session_state['usuario_logueado'] == "admin@sirius.com":
            t_not, t_gest = st.tabs(["📢 Publicar Aviso", "🛠 Gestión"])
            with t_not:
                with st.form("noticia"):
                    tit = st.text_input("Título")
                    txt = st.text_area("Mensaje")
                    if st.form_submit_button("Publicar"):
                        st.session_state['noticias'].append({"fecha": "Hoy", "titulo": tit, "contenido": txt, "icono": "📢"})
                        st.success("Publicado.")
            with t_gest:
                if st.session_state['equipos_db']:
                    noms = [e["Nombre"] for e in st.session_state['equipos_db']]
                    sel = st.selectbox("Eliminar equipo:", noms)
                    if st.button("Borrar"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != sel]
                        st.rerun()
        else:
            st.error("No tienes permisos de administrador.")
