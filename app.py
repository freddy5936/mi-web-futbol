import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA (Menú abierto por defecto)
st.set_page_config(
    page_title="Sirius Community PRO", 
    layout="wide", 
    initial_sidebar_state="expanded" # Esto obliga a que el menú inicie abierto
)

# 2. ESTILO CSS PARA VISIBILIDAD Y BOTÓN DE MENÚ
st.markdown("""
    <style>
    /* Fondo y textos generales */
    .stApp { background-color: #0b0e14; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    
    /* Hacer que la flechita original de Streamlit sea NEÓN y más grande */
    button[kind="headerNoPadding"] {
        background-color: #00ffcc !important;
        color: #0b0e14 !important;
        border-radius: 50% !important;
        transform: scale(1.5);
        margin: 10px;
    }

    /* Estilo del menú lateral */
    section[data-testid="stSidebar"] {
        background-color: #161922 !important;
        border-right: 2px solid #00ffcc;
        min-width: 300px !important;
    }

    /* Botón Flotante de Registro para cuando no ven el menú */
    .menu-btn {
        background-color: #00ffcc;
        color: #0b0e14;
        padding: 10px 20px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (LOGIN)
with st.sidebar:
    st.title("🎮 PANEL DE ACCESO")
    st.write("---")
    user_email = st.text_input("📩 Introduce tu Correo para entrar", placeholder="tu@correo.com")
    
    if user_email:
        st.success(f"Sesión activa: {user_email}")
        st.write("---")
        rol = st.radio("Selecciona una opción:", 
                      ["🏆 Clasificación", "📝 Inscribir Equipo", "⚙️ Administración"])
    else:
        st.warning("Escribe tu correo para desbloquear el menú.")

# 4. CUERPO PRINCIPAL (LOGICA DE VISIBILIDAD)
if not user_email:
    st.title("⚽ Sirius Community")
    st.subheader("¡Bienvenido!")
    
    # Mensaje de ayuda con instrucciones visuales
    st.error("👉 MIRA A LA IZQUIERDA: Si no ves el cuadro de login, busca una pequeña flecha '>' en la esquina superior izquierda de tu pantalla.")
    
    st.info("""
    **¿Cómo registrarse?**
    1. Abre el menú lateral (usa la flecha arriba a la izquierda si está oculto).
    2. Pon tu correo electrónico.
    3. Elige 'Inscribir Equipo' en las opciones que aparecerán.
    """)
    
    # Imagen de referencia o Logo si lo tienes
    st.image("https://via.placeholder.com/800x200/0b0e14/00ffcc?text=SIRIUS+COMMUNITY+ESPORTS", use_column_width=True)

else:
    # SI YA PUSO EL CORREO, MOSTRAR EL CONTENIDO
    if rol == "🏆 Clasificación":
        st.title("Tabla de Posiciones")
        # Tu tabla de posiciones aquí...
        
    elif rol == "📝 Inscribir Equipo":
        st.title("Formulario de Inscripción")
        with st.form("registro_equipo"):
            st.text_input("Nombre del Equipo")
            st.text_input("EA ID del DT")
            st.text_input("WhatsApp")
            if st.form_submit_button("Enviar Registro"):
                st.balloons()
                st.success("¡Datos enviados al Administrador!")

    elif rol == "⚙️ Administración":
        st.title("Panel Maestro")
        passw = st.text_input("Clave de Admin", type="password")
        if passw == "Sirius2026":
            st.write("Bienvenido, Walllesglint72")
