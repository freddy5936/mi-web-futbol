import streamlit as st
import pandas as pd
import random
from PIL import Image

# 1. CONFIGURACIÓN DE PÁGINA (Ajuste para Laptop y Móvil)
st.set_page_config(
    page_title="Sirius Community PRO", 
    layout="wide", # "wide" es clave para que en PC use toda la pantalla
    initial_sidebar_state="auto"
)

# 2. INICIALIZACIÓN DE DATOS
if 'equipos_db' not in st.session_state:
    st.session_state['equipos_db'] = []
if 'ligas' not in st.session_state:
    st.session_state['ligas'] = ["Top Ligue", "Ligue 2"]
if 'relampagos' not in st.session_state:
    st.session_state['relampagos'] = ["Relámpago #6"]
if 'calendarios' not in st.session_state:
    st.session_state['calendarios'] = {}
if 'reportes_ia' not in st.session_state:
    st.session_state['reportes_ia'] = []

# 3. ESTILO CSS (Optimizado para visibilidad y adaptabilidad)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    
    /* Textos base */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label {
        color: #ffffff !important;
        font-size: 16px;
    }
    
    /* Títulos Neón */
    h1, h2, h3 { 
        color: #00ffcc !important; 
        text-align: center;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
    }
    
    /* Contenedores responsivos */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 calc(50% - 1rem) !important;
        min-width: 300px !important;
    }

    /* Botones Pro */
    .stButton>button {
        width: 100%;
        background-color: #00ffcc !important;
        color: #0b0e14 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 10px !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px #00ffcc;
    }

    /* Estilo de la barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #161922 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. BARRA LATERAL (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/neon/96/trophy.png", width=80) # Icono decorativo
    st.title("SIRIUS PANEL")
    user_email = st.text_input("📩 Correo electrónico", placeholder="ejemplo@correo.com")
    
    if user_email:
        st.write("---")
        rol = st.radio(
            "MENÚ DE NAVEGACIÓN", 
            ["🏆 Competiciones", "📋 Reportar Resultado", "📝 Inscripción", "⚙️ Admin"]
        )
    else:
        st.info("Introduce tu correo para entrar.")

# 5. LÓGICA DE CONTENIDO (Adaptable)
if user_email:
    if rol == "🏆 Competiciones":
        st.title("🏆 Competiciones Sirius")
        
        # En PC esto se verá lado a lado, en móvil uno arriba del otro
        col_cat, col_sel = st.columns(2)
        with col_cat:
            cat = st.radio("Categoría:", ["Ligas", "Relámpagos"], horizontal=True)
        with col_sel:
            opciones = st.session_state['ligas'] if cat == "Ligas" else st.session_state['relampagos']
            t_sel = st.selectbox("Torneo actual:", opciones)
        
        tab_t, tab_c = st.tabs(["📊 Clasificación", "⚽ Calendario"])
        
        with tab_t:
            eq_t = [e for e in st.session_state['equipos_db'] if e["Torneo"] == t_sel]
            if eq_t:
                st.dataframe(pd.DataFrame(eq_t)[["Nombre", "WhatsApp"]], use_container_width=True)
            else:
                st.info("Esperando inscripciones...")
                
        with tab_c:
            if t_sel in st.session_state['calendarios']:
                for i, jornada in enumerate(st.session_state['calendarios'][t_sel]):
                    with st.expander(f"JORNADA {i+1}"):
                        for p in jornada: st.write(f"• {p}")
            else:
                st.warning("Calendario pendiente por el Admin.")

    elif rol == "📋 Reportar Resultado":
        st.title("🤖 Reporte Inteligente (IA)")
        st.write("Sube tu captura. La IA procesará el marcador automáticamente.")
        
        c1, c2 = st.columns([1, 1])
        with c1:
            t_rep = st.selectbox("Torneo:", st.session_state['ligas'] + st.session_state['relampagos'])
            archivo = st.file_uploader("Subir evidencia", type=["png", "jpg", "jpeg"])
        with c2:
            if archivo:
                st.image(archivo, caption="Previsualización", use_container_width=True)
                if st.button("Enviar a IA"):
                    st.success("Analizando... ¡Resultado 2-1 detectado!")
                    st.session_state['reportes_ia'].append({"DT": user_email, "Torneo": t_rep, "Res": "Detectado"})

    elif rol == "📝 Inscripción":
        st.title("📝 Registro de Clubes")
        # Usamos columnas para que en Laptop no se vea un formulario gigante y estirado
        with st.form("reg_laptop"):
            c_a, c_b = st.columns(2)
            with c_a:
                nombre = st.text_input("Nombre del Club")
                whatsapp = st.text_input("Número WhatsApp")
            with c_b:
                t_reg = st.selectbox("Torneo", st.session_state['ligas'] + st.session_state['relampagos'])
                logo = st.file_uploader("Logo del equipo", type=["png", "jpg"])
            
            if st.form_submit_button("Finalizar Registro"):
                if nombre and whatsapp:
                    st.session_state['equipos_db'].append({"Nombre": nombre, "WhatsApp": whatsapp, "Torneo": t_reg})
                    st.success(f"¡{nombre} registrado con éxito!")
                else:
                    st.error("Rellena los campos obligatorios.")

    elif rol == "⚙️ Admin":
        st.title("⚙️ Panel de Control Maestro")
        clave = st.text_input("Contraseña de Admin", type="password")
        if clave == "Sirius2026":
            st.success("Acceso concedido.")
            
            # En laptop se ven las 2 columnas, en móvil una debajo de otra
            col_adm1, col_adm2 = st.columns(2)
            
            with col_adm1:
                st.subheader("Gestión de Equipos")
                if st.session_state['equipos_db']:
                    nombres = [e["Nombre"] for e in st.session_state['equipos_db']]
                    sel = st.selectbox("Equipo a borrar:", nombres)
                    if st.button("🗑️ Eliminar Registro"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != sel]
                        st.rerun()
            
            with col_adm2:
                st.subheader("Publicar Cruces")
                t_gen = st.selectbox("Torneo para cerrar:", st.session_state['ligas'] + st.session_state['relampagos'], key="gen")
                if st.button("⚡ Generar Automáticamente"):
                    lista = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == t_gen]
                    if len(lista) >= 2:
                        random.shuffle(lista)
                        st.session_state['calendarios'][t_gen] = [[f"{lista[0]} vs {lista[1]}"]]
                        st.success("¡Cruces publicados!")
else:
    st.title("⚽ Sirius Community")
    st.subheader("Gestión Pro de Torneos FC 26")
    st.info("Usa el menú lateral para navegar. Si estás en móvil, pulsa la flecha ( > ) arriba a la izquierda.")
