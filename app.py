import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sirius Community PRO", layout="wide", initial_sidebar_state="auto")

# 2. BASE DE DATOS INTERNA (Persistencia en la sesión)
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {"admin@sirius.com": "Sirius2026"} 
if 'usuario_logueado' not in st.session_state:
    st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state:
    st.session_state['view'] = 'login'
if 'equipos_db' not in st.session_state:
    st.session_state['equipos_db'] = []
if 'noticias' not in st.session_state:
    st.session_state['noticias'] = [{"fecha": "2026-04-10", "titulo": "¡Web Restaurada!", "contenido": "Todo el contenido está activo tras iniciar sesión.", "icono": "🚀"}]
if 'ligas' not in st.session_state:
    st.session_state['ligas'] = ["Top Ligue", "Ligue 2"]
if 'relampagos' not in st.session_state:
    st.session_state['relampagos'] = ["Relámpago #6"]
if 'calendarios' not in st.session_state:
    st.session_state['calendarios'] = {}

# 3. ESTILO CSS PROFESIONAL
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    .noticia-card { background-color: #1a1c24; border-left: 5px solid #00ffcc; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
    .stButton>button { width: 100%; background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold !important; border-radius: 10px; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 1px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# 4. LÓGICA DE ACCESO (Login / Registro / Recuperación)
def cambiar_vista(v):
    st.session_state['view'] = v
    st.rerun()

if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY ACCESS")
    
    # --- VISTA: LOGIN ---
    if st.session_state['view'] == 'login':
        with st.container():
            u_l = st.text_input("Correo electrónico")
            p_l = st.text_input("Contraseña", type="password")
            if st.button("INICIAR SESIÓN"):
                if u_l in st.session_state['usuarios'] and st.session_state['usuarios'][u_l] == p_l:
                    st.session_state['usuario_logueado'] = u_l
                    st.rerun()
                else:
                    st.error("Datos incorrectos.")
            
            st.write("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("¿No tienes cuenta? Regístrate"): cambiar_vista('registro')
            with col2:
                if st.button("Olvidé mi contraseña"): cambiar_vista('recuperar')

    # --- VISTA: REGISTRO ---
    elif st.session_state['view'] == 'registro':
        st.subheader("Crear Cuenta")
        u_r = st.text_input("Nuevo Correo")
        p_r = st.text_input("Contraseña")
        p_c = st.text_input("Confirmar Contraseña", type="password")
        if st.button("FINALIZAR REGISTRO"):
            if u_r and p_r == p_c:
                st.session_state['usuarios'][u_r] = p_r
                st.success("¡Cuenta creada!")
                time.sleep(1)
                cambiar_vista('login')
            else: st.error("Error en los datos.")
        if st.button("Volver"): cambiar_vista('login')

    # --- VISTA: RECUPERAR ---
    elif st.session_state['view'] == 'recuperar':
        st.subheader("Recuperar Contraseña")
        u_rec = st.text_input("Correo de la cuenta")
        if st.button("Enviar Código"):
            if u_rec in st.session_state['usuarios']:
                st.info(f"CÓDIGO ENVIADO (Simulación): 1234")
                st.session_state['reset_code'] = "1234"
                st.session_state['reset_user'] = u_rec
            else: st.error("Correo no encontrado.")
        
        if 'reset_code' in st.session_state:
            cod = st.text_input("Introduce el código")
            n_p = st.text_input("Nueva contraseña", type="password")
            if st.button("Cambiar"):
                if cod == st.session_state['reset_code']:
                    st.session_state['usuarios'][st.session_state['reset_user']] = n_p
                    st.success("¡Contraseña cambiada!")
                    cambiar_vista('login')
        if st.button("Cancelar"): cambiar_vista('login')

# 5. PANEL DE CONTROL (TODO LO QUE TENÍAMOS)
else:
    with st.sidebar:
        st.title("SIRIUS PANEL")
        st.write(f"Conectado: **{st.session_state['usuario_logueado']}**")
        menu = st.radio("MENÚ:", ["🏠 Inicio", "🏆 Torneos", "📋 Reporte IA", "📝 Inscripción", "⚙️ Admin"])
        if st.button("Cerrar Sesión"):
            st.session_state['usuario_logueado'] = None
            st.rerun()

    # --- CONTENIDO DE LAS SECCIONES ---
    if menu == "🏠 Inicio":
        st.title("📢 Noticias de la Comunidad")
        for n in reversed(st.session_state['noticias']):
            st.markdown(f'<div class="noticia-card"><h4>{n["icono"]} {n["titulo"]}</h4><p>{n["contenido"]}</p></div>', unsafe_allow_html=True)

    elif menu == "🏆 Torneos":
        st.title("🏆 Competiciones")
        cat = st.radio("Ver:", ["Ligas", "Relámpagos"], horizontal=True)
        opc = st.session_state['ligas'] if cat == "Ligas" else st.session_state['relampagos']
        t_sel = st.selectbox("Torneo:", opc)
        tab1, tab2 = st.tabs(["📊 Equipos", "📅 Calendario"])
        with tab1:
            eqs = [e for e in st.session_state['equipos_db'] if e["Torneo"] == t_sel]
            if eqs: st.dataframe(pd.DataFrame(eqs), use_container_width=True)
            else: st.info("Sin equipos inscritos.")
        with tab2:
            if t_sel in st.session_state['calendarios']:
                for idx, jor in enumerate(st.session_state['calendarios'][t_sel]):
                    with st.expander(f"Jornada {idx+1}"):
                        for p in jor: st.write(f"• {p}")

    elif menu == "📋 Reporte IA":
        st.title("🤖 Reportar Resultado")
        archivo = st.file_uploader("Sube la foto", type=["png", "jpg"])
        if archivo and st.button("Analizar"):
            st.success("¡Imagen recibida! IA procesando marcador...")

    elif menu == "📝 Inscripción":
        st.title("📝 Inscripción de Club")
        with st.form("f_ins"):
            n_c = st.text_input("Nombre del Club")
            w_c = st.text_input("WhatsApp")
            t_c = st.selectbox("Torneo", st.session_state['ligas'] + st.session_state['relampagos'])
            if st.form_submit_button("Inscribir"):
                st.session_state['equipos_db'].append({"Nombre": n_c, "WhatsApp": w_c, "Torneo": t_c})
                st.success("¡Registrado!")

    elif menu == "⚙️ Admin":
        st.title("⚙️ Administración")
        if st.session_state['usuario_logueado'] == "admin@sirius.com":
            t_avisos, t_datos, t_fix = st.tabs(["📢 Avisos", "🛠 Datos", "⚡ Cruces"])
            with t_avisos:
                with st.form("n_av"):
                    tit = st.text_input("Título")
                    msg = st.text_area("Contenido")
                    if st.form_submit_button("Publicar"):
                        st.session_state['noticias'].append({"fecha": "Hoy", "titulo": tit, "contenido": msg, "icono": "📢"})
                        st.rerun()
            with t_datos:
                if st.session_state['equipos_db']:
                    sel = st.selectbox("Borrar equipo:", [e["Nombre"] for e in st.session_state['equipos_db']])
                    if st.button("Eliminar"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != sel]
                        st.rerun()
            with t_fix:
                t_f = st.selectbox("Torneo:", st.session_state['ligas'] + st.session_state['relampagos'])
                if st.button("Generar Cruces"):
                    lista = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == t_f]
                    if len(lista) >= 2:
                        random.shuffle(lista)
                        st.session_state['calendarios'][t_f] = [[f"{lista[0]} vs {lista[1]}"]]
                        st.success("Cruces publicados.")
        else:
            st.error("Acceso solo para el administrador.")
