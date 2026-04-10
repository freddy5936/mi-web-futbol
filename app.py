import streamlit as st
import pandas as pd
import random
import time

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

# 2. BASE DE DATOS (Usuarios, Equipos y Resultados)
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {
        "admin@sirius.com": "Sirius2026",
        "walllesglint72@gmail.com": "Sirius2026" # <--- ESTA ES TU CUENTA
    }
if 'equipos_db' not in st.session_state:
    st.session_state['equipos_db'] = []
if 'resultados_ia' not in st.session_state:
    st.session_state['resultados_ia'] = []
if 'usuario_logueado' not in st.session_state:
    st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state:
    st.session_state['view'] = 'login'

# 3. ESTILO CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    .stButton>button { width: 100%; background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; border-radius: 10px; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 1px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# 4. LÓGICA DE ACCESO
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY")
    if st.session_state['view'] == 'login':
        with st.form("login_form"):
            st.subheader("🔑 Iniciar Sesión")
            u = st.text_input("Correo")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("ENTRAR"):
                if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                    st.session_state['usuario_logueado'] = u
                    st.rerun()
                else: st.error("Datos incorrectos. Usa Sirius2026")
        if st.button("¿No tienes cuenta? Crea una aquí"): 
            st.session_state['view'] = 'registro'
            st.rerun()

    elif st.session_state['view'] == 'registro':
        with st.form("reg_form"):
            st.subheader("📝 Nuevo Registro")
            nu = st.text_input("Correo")
            np = st.text_input("Contraseña", type="password")
            if st.form_submit_button("REGISTRARME"):
                st.session_state['usuarios'][nu] = np
                st.success("¡Cuenta creada! Vuelve al login.")
        if st.button("Volver al Inicio"):
            st.session_state['view'] = 'login'
            st.rerun()

# 5. PANEL PRINCIPAL
else:
    with st.sidebar:
        st.title("SIRIUS PANEL")
        st.write(f"DT: **{st.session_state['usuario_logueado']}**")
        menu = st.radio("MENÚ:", ["🏆 Torneos", "📋 Reporte IA", "📝 Inscripción", "⚙️ Admin"])
        if st.button("Cerrar Sesión"):
            st.session_state['usuario_logueado'] = None
            st.rerun()

    # --- REPORTE IA ---
    if menu == "📋 Reporte IA":
        st.title("🤖 Reportar Partido con IA")
        if not st.session_state['equipos_db']:
            st.warning("No hay equipos inscritos para reportar.")
        else:
            lista_equipos = [e["Nombre"] for e in st.session_state['equipos_db']]
            c1, c2 = st.columns(2)
            with c1: local = st.selectbox("Tu Equipo (Local):", lista_equipos)
            with c2: visitante = st.selectbox("Rival (Visitante):", [e for e in lista_equipos if e != local])
            
            foto = st.file_uploader("Sube la captura del marcador", type=["png", "jpg", "jpeg"])
            if foto:
                st.image(foto, width=400)
                if st.button("⚡ ESCANEAR MARCADOR"):
                    with st.spinner("IA analizando píxeles..."):
                        time.sleep(2)
                        gl, gv = random.randint(0,4), random.randint(0,4)
                        resultado = f"{local} {gl} - {gv} {visitante}"
                        st.session_state['resultados_ia'].append({"partido": resultado, "estado": "Pendiente"})
                        st.success(f"Detectado: {resultado}")
                        st.info("Resultado enviado al Admin para validación.")

    # --- ADMIN (ACCESO BLOQUEADO POR CORREO) ---
    elif menu == "⚙️ Admin":
        # SOLO TU CORREO PUEDE PASAR
        if st.session_state['usuario_logueado'] in ["admin@sirius.com", "walllesglint72@gmail.com"]:
            st.title("⚙️ Panel de Dueño")
            t1, t2 = st.tabs(["📊 Equipos Inscritos", "✅ Validar Resultados IA"])
            
            with t1:
                if st.session_state['equipos_db']:
                    df = pd.DataFrame(st.session_state['equipos_db'])
                    st.table(df)
                    if st.button("Eliminar todos los equipos"):
                        st.session_state['equipos_db'] = []
                        st.rerun()
                else: st.write("No hay equipos en la base de datos.")
            
            with t2:
                if st.session_state['resultados_ia']:
                    for res in st.session_state['resultados_ia']:
                        st.write(f"🔹 {res['partido']} | Estado: {res['estado']}")
                else: st.write("No hay reportes nuevos.")
        else:
            st.error("⛔ ACCESO DENEGADO. Solo Walllesglint72 puede entrar aquí.")

    # --- SECCIONES EXTRA ---
    elif menu == "🏆 Torneos":
        st.title("🏆 Competiciones")
        if st.session_state['equipos_db']:
            st.dataframe(pd.DataFrame(st.session_state['equipos_db']), use_container_width=True)
        else: st.info("Esperando equipos...")

    elif menu == "📝 Inscripción":
        st.title("📝 Registro de Club")
        with st.form("ins"):
            n = st.text_input("Nombre Club")
            t = st.selectbox("Torneo", ["Top Ligue", "Ligue 2", "Cup"])
            if st.form_submit_button("UNIRSE"):
                st.session_state['equipos_db'].append({"Nombre": n, "Torneo": t})
                st.success(f"{n} registrado.")
