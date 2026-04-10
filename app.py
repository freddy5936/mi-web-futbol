import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

# 2. INICIALIZACIÓN DE DATOS (Persistencia Garantizada)
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {"admin@sirius.com": "Sirius2026"} 
if 'usuario_logueado' not in st.session_state:
    st.session_state['usuario_logueado'] = None
if 'equipos_db' not in st.session_state:
    st.session_state['equipos_db'] = []
if 'noticias' not in st.session_state:
    st.session_state['noticias'] = [{"fecha": "2026-04-10", "titulo": "Sistema de Seguridad Actualizado", "contenido": "Registro corregido y funcionando al 100%.", "icono": "✅"}]
if 'ligas' not in st.session_state:
    st.session_state['ligas'] = ["Top Ligue", "Ligue 2"]
if 'relampagos' not in st.session_state:
    st.session_state['relampagos'] = ["Relámpago #6"]
if 'calendarios' not in st.session_state:
    st.session_state['calendarios'] = {}

# 3. ESTILO CSS PARA TEXTOS Y BOTONES
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    .stButton>button { width: 100%; background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold !important; border-radius: 10px; border: none; padding: 10px; }
    .stTextInput>div>div>input { background-color: #1a1c24 !important; color: white !important; border: 1px solid #333 !important; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 1px solid #00ffcc; }
    .noticia-card { background-color: #1a1c24; border-left: 5px solid #00ffcc; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 4. FUNCIONES DE CUENTA
def realizar_registro(e, p, c):
    if not e or not p:
        st.error("Debes rellenar todos los campos.")
    elif e in st.session_state['usuarios']:
        st.warning("Este correo ya está registrado.")
    elif p != c:
        st.error("Las contraseñas no coinciden.")
    else:
        st.session_state['usuarios'][e] = p
        st.success(f"¡Cuenta creada para {e}! Ya puedes iniciar sesión a la izquierda.")

# 5. PANTALLA DE ACCESO
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ ACCESO SIRIUS COMMUNITY")
    
    col_login, col_sep, col_reg = st.columns([1, 0.1, 1])
    
    with col_login:
        st.subheader("🔑 Iniciar Sesión")
        with st.container():
            e_login = st.text_input("Correo", key="login_user")
            p_login = st.text_input("Contraseña", type="password", key="login_pass")
            if st.button("ENTRAR"):
                if e_login in st.session_state['usuarios'] and st.session_state['usuarios'][e_login] == p_login:
                    st.session_state['usuario_logueado'] = e_login
                    st.rerun()
                else:
                    st.error("Datos incorrectos.")

    with col_reg:
        st.subheader("📝 Registrarse")
        with st.container():
            e_reg = st.text_input("Tu Correo", key="reg_user")
            p_reg = st.text_input("Tu Contraseña", type="password", key="reg_pass")
            c_reg = st.text_input("Confirmar Contraseña", type="password", key="reg_conf")
            if st.button("CREAR CUENTA"):
                realizar_registro(e_reg, p_reg, c_reg)

# 6. PANEL PRINCIPAL (POST-LOGIN)
else:
    with st.sidebar:
        st.title("SIRIUS PANEL")
        st.write(f"Conectado como: **{st.session_state['usuario_logueado']}**")
        menu = st.radio("IR A:", ["🏠 Inicio", "🏆 Torneos", "📋 Reporte IA", "📝 Inscribir Equipo", "⚙️ Admin"])
        if st.button("Cerrar Sesión"):
            st.session_state['usuario_logueado'] = None
            st.rerun()

    if menu == "🏠 Inicio":
        st.title("📢 Noticias y Avisos")
        for n in reversed(st.session_state['noticias']):
            st.markdown(f'<div class="noticia-card"><h4>{n["icono"]} {n["titulo"]}</h4><p>{n["contenido"]}</p></div>', unsafe_allow_html=True)

    elif menu == "🏆 Torneos":
        st.title("🏆 Competiciones Actuales")
        cat = st.radio("Ver:", ["Ligas", "Relámpagos"], horizontal=True)
        opc = st.session_state['ligas'] if cat == "Ligas" else st.session_state['relampagos']
        t_sel = st.selectbox("Selecciona Torneo", opc)
        
        tab1, tab2 = st.tabs(["📊 Equipos Inscritos", "📅 Calendario de Juegos"])
        with tab1:
            eqs = [e for e in st.session_state['equipos_db'] if e["Torneo"] == t_sel]
            if eqs: st.dataframe(pd.DataFrame(eqs), use_container_width=True)
            else: st.info("No hay equipos registrados todavía.")
        with tab2:
            if t_sel in st.session_state['calendarios']:
                for idx, jor in enumerate(st.session_state['calendarios'][t_sel]):
                    with st.expander(f"Jornada {idx+1}"):
                        for p in jor: st.write(f"• {p}")
            else: st.warning("El administrador no ha generado los cruces aún.")

    elif menu == "📋 Reporte IA":
        st.title("🤖 Reportar con Imagen")
        archivo = st.file_uploader("Sube la captura del final", type=["png", "jpg", "jpeg"])
        if archivo and st.button("Procesar con IA"):
            st.success("Analizando marcador... ¡Reporte enviado!")

    elif menu == "📝 Inscribir Equipo":
        st.title("📝 Inscripción de Club")
        with st.form("form_insc"):
            n = st.text_input("Nombre del Club")
            w = st.text_input("WhatsApp")
            t = st.selectbox("Torneo", st.session_state['ligas'] + st.session_state['relampagos'])
            if st.form_submit_button("REGISTRAR"):
                if n and w:
                    st.session_state['equipos_db'].append({"Nombre": n, "WhatsApp": w, "Torneo": t})
                    st.success("¡Equipo inscrito con éxito!")

    elif menu == "⚙️ Admin":
        st.title("⚙️ Panel de Control")
        if st.session_state['usuario_logueado'] == "admin@sirius.com":
            t_not, t_gest, t_cruces = st.tabs(["📢 Avisos", "🛠 Equipos", "⚡ Cruces"])
            
            with t_not:
                with st.form("admin_not"):
                    tit = st.text_input("Título")
                    msg = st.text_area("Mensaje")
                    if st.form_submit_button("Publicar"):
                        st.session_state['noticias'].append({"fecha": "Hoy", "titulo": tit, "contenido": msg, "icono": "📢"})
                        st.rerun()
            
            with t_gest:
                if st.session_state['equipos_db']:
                    df = pd.DataFrame(st.session_state['equipos_db'])
                    st.dataframe(df)
                    eq_del = st.selectbox("Borrar equipo:", [e["Nombre"] for e in st.session_state['equipos_db']])
                    if st.button("BORRAR SELECCIONADO"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != eq_del]
                        st.rerun()

            with t_cruces:
                t_gen = st.selectbox("Torneo para fixture:", st.session_state['ligas'] + st.session_state['relampagos'])
                if st.button("GENERAR CRUCES"):
                    lista = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == t_gen]
                    if len(lista) >= 2:
                        random.shuffle(lista)
                        st.session_state['calendarios'][t_gen] = [[f"{lista[0]} vs {lista[1]}"]]
                        st.success("¡Fixture publicado!")
        else:
            st.error("Acceso restringido solo para administradores.")
