import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sirius Community PRO", layout="wide", initial_sidebar_state="expanded")

# 2. INICIALIZAR MEMORIA (Para que las ligas no desaparezcan al navegar)
if 'ligas_creadas' not in st.session_state:
    st.session_state['ligas_creadas'] = ["Top Ligue", "Relámpago #6"] # Ligas por defecto

# 3. ESTILO CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; }
    button[kind="headerNoPadding"] { background-color: #00ffcc !important; transform: scale(1.5); }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 2px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# 4. BARRA LATERAL
with st.sidebar:
    st.title("🎮 PANEL SIRIUS")
    user_email = st.text_input("📩 Correo Electrónico", placeholder="tu@correo.com")
    
    if user_email:
        st.write("---")
        rol = st.radio("Menú:", ["🏆 Clasificación", "📝 Inscribir Equipo", "⚙️ Administración"])
    else:
        st.warning("Ingresa tu correo para activar el menú.")

# 5. CONTENIDO
if not user_email:
    st.title("⚽ Sirius Community")
    st.info("Por favor, inicia sesión en el menú lateral.")
else:
    if rol == "🏆 Clasificación":
        st.title("Clasificación de Ligas")
        liga_sel = st.selectbox("Selecciona la liga para ver puntos:", st.session_state['ligas_creadas'])
        st.write(f"Mostrando resultados de: **{liga_sel}**")
        st.table(pd.DataFrame({"Equipo": ["Pendiente"], "PTS": [0]}))
        
    elif rol == "📝 Inscribir Equipo":
        st.title("Inscripción de Equipos")
        with st.form("registro"):
            nombre = st.text_input("Nombre del Equipo")
            wa = st.text_input("WhatsApp")
            liga_destino = st.selectbox("¿En qué liga quieres inscribirte?", st.session_state['ligas_creadas'])
            logo = st.file_uploader("Logo", type=["png", "jpg"])
            if st.form_submit_button("Enviar"):
                st.success(f"¡Inscrito en {liga_destino}!")

    elif rol == "⚙️ Administración":
        st.title("Panel de Control Maestro")
        clave = st.text_input("Código Maestro", type="password")
        
        if clave == "Sirius2026":
            st.success("Acceso Autorizado")
            
            # --- SECCIÓN PARA CREAR LIGAS DE VERDAD ---
            st.write("### ➕ Crear Nueva Liga o Torneo")
            nombre_nueva_liga = st.text_input("Nombre de la Liga (ej: Copa Sirius 2026)")
            
            if st.button("🚀 Publicar Liga"):
                if nombre_nueva_liga:
                    if nombre_nueva_liga not in st.session_state['ligas_creadas']:
                        st.session_state['ligas_creadas'].append(nombre_nueva_liga)
                        st.balloons()
                        st.success(f"¡La liga '{nombre_nueva_liga}' ha sido creada y ya aparece en las opciones!")
                    else:
                        st.warning("Esa liga ya existe.")
                else:
                    st.error("Escribe un nombre para la liga.")
            
            st.write("---")
            st.write("### 📋 Ligas Activas")
            for l in st.session_state['ligas_creadas']:
                st.write(f"✅ {l}")
        elif clave != "":
            st.error("Código incorrecto.")
