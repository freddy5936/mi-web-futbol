import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sirius Community PRO", layout="wide", initial_sidebar_state="auto")

# 2. SISTEMA DE DATOS (Persistencia)
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {
        "admin@sirius.com": "Sirius2026",
        "walllesglint72@gmail.com": "Sirius2026"
    }
if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'
if 'equipos_db' not in st.session_state: st.session_state['equipos_db'] = []
if 'noticias' not in st.session_state: 
    st.session_state['noticias'] = [{"fecha": "2026-04-10", "titulo": "¡Plataforma Actualizada!", "contenido": "Sistema de reportes IA y gestión de noticias activo.", "icono": "🔥"}]
if 'resultados_ia' not in st.session_state: st.session_state['resultados_ia'] = []

# 3. ESTILO CSS PERSONALIZADO (Dark & Neon)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Botones de Acción */
    .stButton>button { 
        width: 100%; 
        background-color: #00ffcc !important; 
        color: #0b0e14 !important; 
        font-weight: bold !important; 
        border-radius: 8px !important;
        border: none !important;
        padding: 10px !important;
    }
    
    /* Tarjetas de Noticias */
    .noticia-card {
        background-color: #1a1c24;
        border-left: 5px solid #00ffcc;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Inputs */
    .stTextInput>div>div>input { background-color: #1a1c24 !important; color: white !important; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 1px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# 4. FUNCIONES DE NAVEGACIÓN
def navegar_a(vista):
    st.session_state['view'] = vista
    st.rerun()

# 5. PANTALLA DE ACCESO (Login / Registro / Recuperación)
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY")
    
    if st.session_state['view'] == 'login':
        with st.container():
            st.subheader("ACCESO AL PANEL")
            u_l = st.text_input("Correo electrónico")
            p_l = st.text_input("Contraseña", type="password")
            if st.button("ENTRAR AL SISTEMA"):
                if u_l in st.session_state['usuarios'] and st.session_state['usuarios'][u_l] == p_l:
                    st.session_state['usuario_logueado'] = u_l
                    st.rerun()
                else: st.error("Datos incorrectos. Inténtalo de nuevo.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📝 Crear cuenta"): navegar_a('registro')
            with col_b:
                if st.button("🔑 Olvidé clave"): navegar_a('recuperar')

    elif st.session_state['view'] == 'registro':
        st.subheader("REGISTRO DE NUEVO DT")
        u_r = st.text_input("Tu Correo")
        p_r = st.text_input("Elige Contraseña", type="password")
        if st.button("CONFIRMAR REGISTRO"):
            if u_r and p_r:
                st.session_state['usuarios'][u_r] = p_r
                st.success("¡Cuenta creada! Ya puedes loguearte.")
                time.sleep(1.5)
                navegar_a('login')
        if st.button("Volver"): navegar_a('login')

    elif st.session_state['view'] == 'recuperar':
        st.subheader("RECUPERAR CONTRASEÑA")
        u_rec = st.text_input("Correo registrado")
        if st.button("SOLICITAR CÓDIGO"):
            if u_rec in st.session_state['usuarios']:
                st.info("CÓDIGO ENVIADO: 7272 (Simulación)")
                st.session_state['reset_code'] = "7272"
            else: st.error("Correo no encontrado.")
        
        if 'reset_code' in st.session_state:
            c_in = st.text_input("Ingresa código")
            n_p = st.text_input("Nueva contraseña", type="password")
            if st.button("ACTUALIZAR"):
                if c_in == "7272":
                    st.session_state['usuarios'][u_rec] = n_p
                    st.success("¡Listo!")
                    navegar_a('login')
        if st.button("Volver"): navegar_a('login')

# 6. PANEL PRINCIPAL (AUTENTICADO)
else:
    with st.sidebar:
        st.image("https://img.icons8.com/neon/96/trophy.png", width=80)
        st.title("SIRIUS PRO")
        st.write(f"DT: {st.session_state['usuario_logueado']}")
        # Menú principal
        opciones = ["🏠 Inicio", "🏆 Torneos", "📋 Reporte IA", "📝 Inscripción"]
        # Solo tú ves el Admin
        if st.session_state['usuario_logueado'] in ["admin@sirius.com", "walllesglint72@gmail.com"]:
            opciones.append("⚙️ Admin")
            
        menu = st.radio("NAVEGACIÓN:", opciones)
        
        if st.button("SALIR"):
            st.session_state['usuario_logueado'] = None
            st.rerun()

    # --- SECCIÓN: INICIO (TABLÓN) ---
    if menu == "🏠 Inicio":
        st.title("📢 NOVEDADES Y AVISOS")
        for n in reversed(st.session_state['noticias']):
            st.markdown(f"""
            <div class="noticia-card">
                <h3>{n['icono']} {n['titulo']}</h3>
                <p style='color:#888; font-size:12px;'>{n['fecha']}</p>
                <p>{n['contenido']}</p>
            </div>
            """, unsafe_allow_html=True)

    # --- SECCIÓN: TORNEOS ---
    elif menu == "🏆 Torneos":
        st.title("🏆 ESTADO DE COMPETICIONES")
        if st.session_state['equipos_db']:
            df = pd.DataFrame(st.session_state['equipos_db'])
            st.dataframe(df, use_container_width=True)
        else: st.info("Próximamente: Tablas de posiciones y cruces.")

    # --- SECCIÓN: REPORTE IA ---
    elif menu == "📋 Reporte IA":
        st.title("🤖 SISTEMA DE REPORTES IA")
        if not st.session_state['equipos_db']:
            st.warning("Debe haber equipos registrados para reportar resultados.")
        else:
            eq_lista = [e["Nombre"] for e in st.session_state['equipos_db']]
            c1, c2 = st.columns(2)
            with c1: loc = st.selectbox("Local:", eq_lista)
            with c2: vis = st.selectbox("Visitante:", [e for e in eq_lista if e != loc])
            
            img = st.file_uploader("Sube foto del marcador", type=["png", "jpg", "jpeg"])
            if img:
                st.image(img, width=450)
                if st.button("⚡ ESCANEAR CON IA"):
                    with st.spinner("IA procesando marcador..."):
                        time.sleep(2)
                        res = f"{loc} {random.randint(0,4)} - {random.randint(0,4)} {vis}"
                        st.session_state['resultados_ia'].append({"partido": res, "dt": st.session_state['usuario_logueado']})
                        st.success(f"DETECTADO: {res}")

    # --- SECCIÓN: INSCRIPCIÓN ---
    elif menu == "📝 Inscripción":
        st.title("📝 REGISTRO DE CLUBES")
        with st.form("form_reg"):
            nombre = st.text_input("Nombre del Club")
            whatsapp = st.text_input("WhatsApp de Contacto")
            torneo = st.selectbox("Torneo", ["Top Ligue", "Ligue 2", "Relámpago"])
            if st.form_submit_button("UNIRSE A LA COMUNIDAD"):
                if nombre and whatsapp:
                    st.session_state['equipos_db'].append({"Nombre": nombre, "WhatsApp": whatsapp, "Torneo": torneo})
                    st.success(f"¡{nombre} ha sido inscrito!")

    # --- SECCIÓN: ADMIN (SOLO WALLLESGLINT72) ---
    elif menu == "⚙️ Admin":
        st.title("⚙️ PANEL DE CONTROL MAESTRO")
        t1, t2, t3 = st.tabs(["📢 Publicar Aviso", "🛠 Gestión Equipos", "✅ Validar Resultados"])
        
        with t1:
            with st.form("add_news"):
                st.subheader("Nueva Noticia")
                t_n = st.text_input("Título")
                c_n = st.text_area("Mensaje")
                i_n = st.selectbox("Icono", ["🔥", "📢", "⚽", "⚠️", "🏆"])
                if st.form_submit_button("PUBLICAR AHORA"):
                    nueva = {"fecha": datetime.now().strftime("%d/%m/%Y"), "titulo": t_n, "contenido": c_n, "icono": i_n}
                    st.session_state['noticias'].append(nueva)
                    st.success("Noticia enviada al tablón.")
        
        with t2:
            st.subheader("Equipos Registrados")
            if st.session_state['equipos_db']:
                st.table(pd.DataFrame(st.session_state['equipos_db']))
                if st.button("🗑️ Borrar todos los equipos"):
                    st.session_state['equipos_db'] = []
                    st.rerun()
            else: st.write("No hay equipos registrados.")
            
        with t3:
            st.subheader("Reportes Recibidos por IA")
            if st.session_state['resultados_ia']:
                for r in st.session_state['resultados_ia']:
                    st.write(f"⚽ **{r['partido']}** (Reportado por: {r['dt']})")
            else: st.write("No hay reportes nuevos.")
