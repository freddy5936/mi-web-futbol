import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA (Laptop + Móvil)
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

# 2. SISTEMA DE USUARIOS (Base de Datos en Sesión)
# Agregamos tu correo como admin por defecto
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {
        "admin@sirius.com": "Sirius2026",
        "walllesglint72@gmail.com": "Sirius2026" # Tu correo ya registrado
    } 

if 'usuario_logueado' not in st.session_state:
    st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state:
    st.session_state['view'] = 'login'

# --- DATOS DE LA WEB ---
if 'equipos_db' not in st.session_state: st.session_state['equipos_db'] = []
if 'noticias' not in st.session_state: st.session_state['noticias'] = []
if 'ligas' not in st.session_state: st.session_state['ligas'] = ["Top Ligue", "Ligue 2"]
if 'relampagos' not in st.session_state: st.session_state['relampagos'] = ["Relámpago #6"]
if 'calendarios' not in st.session_state: st.session_state['calendarios'] = {}

# 3. ESTILO VISUAL (Forzar visibilidad)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    .stButton>button { width: 100%; background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold !important; border-radius: 10px; padding: 10px; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 1px solid #00ffcc; }
    .noticia-card { background-color: #1a1c24; border-left: 5px solid #00ffcc; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 4. FUNCIONES DE NAVEGACIÓN
def ir_a(vista):
    st.session_state['view'] = vista
    st.rerun()

# 5. PANTALLA DE ACCESO (LOGIN / REGISTRO / RESET)
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY")
    
    if st.session_state['view'] == 'login':
        with st.form("login_form"):
            st.subheader("🔑 Iniciar Sesión")
            u = st.text_input("Correo electrónico")
            p = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("ENTRAR")
            
            if submit:
                if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                    st.session_state['usuario_logueado'] = u
                    st.success(f"Bienvenido {u}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Correo o contraseña no encontrados.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("¿No tienes cuenta? Regístrate"): ir_a('registro')
        with col2:
            if st.button("Olvidé mi contraseña"): ir_a('reset')

    elif st.session_state['view'] == 'registro':
        with st.form("reg_form"):
            st.subheader("📝 Crear Cuenta")
            new_u = st.text_input("Correo nuevo")
            new_p = st.text_input("Contraseña nueva", type="password")
            conf_p = st.text_input("Repetir contraseña", type="password")
            btn_reg = st.form_submit_button("REGISTRARME")
            
            if btn_reg:
                if new_u and new_p == conf_p:
                    st.session_state['usuarios'][new_u] = new_p
                    st.success("Cuenta creada con éxito.")
                    time.sleep(1)
                    ir_a('login')
                else:
                    st.error("Las contraseñas no coinciden o falta el correo.")
        
        if st.button("Volver al Login"): ir_a('login')

    elif st.session_state['view'] == 'reset':
        st.subheader("🔄 Recuperar Contraseña")
        email_reset = st.text_input("Correo de tu cuenta")
        if st.button("Enviar Código de Verificación"):
            if email_reset in st.session_state['usuarios']:
                st.info("CÓDIGO: 7272 (Simulación enviada a tu correo)")
                st.session_state['temp_code'] = "7272"
                st.session_state['temp_user'] = email_reset
            else:
                st.error("Ese correo no existe en Sirius.")
        
        if 'temp_code' in st.session_state:
            code_in = st.text_input("Introduce el código")
            new_pass = st.text_input("Nueva Contraseña", type="password")
            if st.button("Cambiar Contraseña"):
                if code_in == st.session_state['temp_code']:
                    st.session_state['usuarios'][st.session_state['temp_user']] = new_pass
                    st.success("¡Hecho! Inicia sesión ahora.")
                    time.sleep(1)
                    del st.session_state['temp_code']
                    ir_a('login')
        
        if st.button("Cancelar"): ir_a('login')

# 6. TODO EL CONTENIDO (Solo visible tras Login)
else:
    with st.sidebar:
        st.title("SIRIUS PANEL")
        st.write(f"Usuario: **{st.session_state['usuario_logueado']}**")
        menu = st.radio("MENÚ:", ["🏠 Inicio", "🏆 Torneos", "📋 Reporte IA", "📝 Inscripción", "⚙️ Admin"])
        if st.button("Cerrar Sesión"):
            st.session_state['usuario_logueado'] = None
            st.rerun()

    # --- INICIO ---
    if menu == "🏠 Inicio":
        st.title("📢 Noticias de la Comunidad")
        if not st.session_state['noticias']:
            st.info("No hay avisos recientes.")
        for n in reversed(st.session_state['noticias']):
            st.markdown(f'<div class="noticia-card"><h4>{n["icono"]} {n["titulo"]}</h4><p>{n["contenido"]}</p></div>', unsafe_allow_html=True)

    # --- TORNEOS ---
    elif menu == "🏆 Torneos":
        st.title("🏆 Competiciones")
        t_sel = st.selectbox("Torneo:", st.session_state['ligas'] + st.session_state['relampagos'])
        t1, t2 = st.tabs(["📊 Equipos", "⚽ Calendario"])
        with t1:
            eqs = [e for e in st.session_state['equipos_db'] if e["Torneo"] == t_sel]
            if eqs: st.table(pd.DataFrame(eqs))
            else: st.info("Sin equipos.")
        with t2:
            if t_sel in st.session_state['calendarios']:
                for idx, j in enumerate(st.session_state['calendarios'][t_sel]):
                    st.write(f"Jornada {idx+1}: {j}")

    # --- REPORTE IA ---
    elif menu == "📋 Reporte IA":
        st.title("🤖 Reportar con IA")
        f = st.file_uploader("Sube foto", type=["png", "jpg"])
        if f: st.success("Imagen cargada. Admin revisará el resultado.")

    # --- INSCRIPCIÓN ---
    elif menu == "📝 Inscripción":
        st.title("📝 Inscripción")
        with st.form("ins_form"):
            nom = st.text_input("Nombre Club")
            wa = st.text_input("WhatsApp")
            tor = st.selectbox("Torneo", st.session_state['ligas'] + st.session_state['relampagos'])
            if st.form_submit_button("REGISTRAR"):
                st.session_state['equipos_db'].append({"Nombre": nom, "WhatsApp": wa, "Torneo": tor})
                st.success("¡Inscrito!")

    # --- ADMIN ---
    elif menu == "⚙️ Admin":
        if st.session_state['usuario_logueado'] in ["admin@sirius.com", "walllesglint72@gmail.com"]:
            st.title("⚙️ Administración")
            t_not, t_gest = st.tabs(["📢 Publicar", "🛠 Gestionar"])
            with t_not:
                with st.form("admin_not"):
                    tit = st.text_input("Título")
                    msg = st.text_area("Mensaje")
                    if st.form_submit_button("Publicar Aviso"):
                        st.session_state['noticias'].append({"fecha": "Hoy", "titulo": tit, "contenido": msg, "icono": "📢"})
                        st.rerun()
            with t_gest:
                if st.session_state['equipos_db']:
                    sel = st.selectbox("Borrar:", [e["Nombre"] for e in st.session_state['equipos_db']])
                    if st.button("Eliminar"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != sel]
                        st.rerun()
        else:
            st.error("No tienes permisos de admin.")
