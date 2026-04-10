import streamlit as st
import pandas as pd
import random
from PIL import Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Sirius Community PRO", 
    layout="wide",
    initial_sidebar_state="expanded" # Esto asegura que el menú aparezca abierto al inicio
)

# 2. INICIALIZACIÓN DE DATOS (Estado de la sesión)
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

# 3. ESTILO CSS PARA TEXTOS BLANCOS Y VISIBLES
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    
    /* Forzar visibilidad de textos en blanco */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label {
        color: #ffffff !important;
    }
    
    /* Títulos Turquesa */
    h1, h2, h3 { color: #00ffcc !important; }
    
    /* Estilo de la Barra Lateral */
    section[data-testid="stSidebar"] {
        background-color: #161922 !important;
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

# 4. BARRA LATERAL (CON FLECHITA RESTAURADA)
with st.sidebar:
    st.title("🎮 PANEL SIRIUS")
    user_email = st.text_input("📩 Introduce tu Correo", placeholder="ejemplo@correo.com")
    
    if user_email:
        st.write("---")
        # El radio button de Streamlit crea el menú de navegación
        rol = st.radio(
            "Selecciona una opción:", 
            ["🏆 Competiciones", "📋 Reportar Resultado", "📝 Inscripción", "⚙️ Admin"]
        )
    else:
        st.warning("Ingresa tu correo para habilitar el menú.")

# 5. LÓGICA DE NAVEGACIÓN PRINCIPAL
if user_email:
    # --- SECCIÓN: CRUCES Y TABLAS ---
    if rol == "🏆 Competiciones":
        st.title("🏆 Estado del Torneo")
        cat = st.radio("Categoría:", ["Ligas", "Relámpagos"], horizontal=True)
        opciones = st.session_state['ligas'] if cat == "Ligas" else st.session_state['relampagos']
        t_sel = st.selectbox("Selecciona el torneo:", opciones)
        
        tab_tabla, tab_cruces = st.tabs(["📊 Tabla", "⚽ Cruces"])
        
        with tab_tabla:
            # Filtrar equipos de este torneo
            eq_torneo = [e for e in st.session_state['equipos_db'] if e["Torneo"] == t_sel]
            if eq_torneo:
                st.table(pd.DataFrame(eq_torneo)[["Nombre", "WhatsApp"]])
            else:
                st.info("No hay equipos inscritos en este torneo.")
                
        with tab_cruces:
            if t_sel in st.session_state['calendarios']:
                for i, jornada in enumerate(st.session_state['calendarios'][t_sel]):
                    with st.expander(f"Jornada {i+1}"):
                        for partido in jornada: st.write(f"• {partido}")
            else:
                st.info("Cruces no generados.")

    # --- SECCIÓN: REPORTE IA ---
    elif rol == "📋 Reportar Resultado":
        st.title("🤖 Área de DTs")
        st.write("Sube la foto del final del partido.")
        t_rep = st.selectbox("Torneo:", st.session_state['ligas'] + st.session_state['relampagos'])
        archivo = st.file_uploader("Captura de pantalla", type=["png", "jpg", "jpeg"])
        
        if archivo:
            st.image(archivo, width=350)
            if st.button("Enviar a IA"):
                # Simulación de detección
                st.success("Resultado detectado: 3 - 1. Enviado a revisión.")
                st.session_state['reportes_ia'].append({"DT": user_email, "Torneo": t_rep, "Dato": "3-1"})

    # --- SECCIÓN: INSCRIPCIÓN ---
    elif rol == "📝 Inscripción":
        st.title("📝 Formulario de Registro")
        with st.form("registro_club"):
            nombre = st.text_input("Nombre del Club")
            whatsapp = st.text_input("WhatsApp de Contacto")
            torneo = st.selectbox("Torneo a inscribirse", st.session_state['ligas'] + st.session_state['relampagos'])
            if st.form_submit_button("Confirmar Registro"):
                if nombre:
                    st.session_state['equipos_db'].append({"Nombre": nombre, "WhatsApp": whatsapp, "Torneo": torneo})
                    st.success(f"¡{nombre} se ha unido a la comunidad!")

    # --- SECCIÓN: ADMIN ---
    elif rol == "⚙️ Admin":
        st.title("⚙️ Control Maestro")
        clave = st.text_input("Código de Acceso", type="password")
        if clave == "Sirius2026":
            t1, t2 = st.tabs(["Gestión de Equipos", "Generar Cruces"])
            
            with t1:
                if st.session_state['equipos_db']:
                    nombres = [e["Nombre"] for e in st.session_state['equipos_db']]
                    sel = st.selectbox("Selecciona equipo para borrar:", nombres)
                    if st.button("🗑️ Eliminar"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != sel]
                        st.success("Equipo eliminado.")
                        st.rerun()
                else:
                    st.write("No hay equipos en la base de datos.")

            with t2:
                t_gen = st.selectbox("Torneo para cerrar cruces:", st.session_state['ligas'] + st.session_state['relampagos'])
                if st.button("⚡ Generar y Publicar Cruces"):
                    lista = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == t_gen]
                    if len(lista) >= 2:
                        random.shuffle(lista)
                        st.session_state['calendarios'][t_gen] = [[f"{lista[0]} vs {lista[1]}"]]
                        st.success("¡Calendario publicado!")
                    else:
                        st.error("Necesitas al menos 2 equipos.")
else:
    # Pantalla de bienvenida si no hay correo
    st.title("⚽ Bienvenido a Sirius Community")
    st.info("Por favor, introduce tu correo en el menú lateral para acceder a las herramientas.")
