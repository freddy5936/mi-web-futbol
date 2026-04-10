import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y MEMORIA
st.set_page_config(page_title="Sirius Community PRO", layout="wide", initial_sidebar_state="expanded")

# Inicializamos la lista de equipos y ligas si no existen
if 'equipos_registrados' not in st.session_state:
    st.session_state['equipos_registrados'] = [] # Lista de diccionarios con datos de equipos
if 'ligas_creadas' not in st.session_state:
    st.session_state['ligas_creadas'] = ["Top Ligue", "Relámpago #6"]

# 2. ESTILO CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; }
    button[kind="headerNoPadding"] { background-color: #00ffcc !important; transform: scale(1.5); }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 2px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    st.title("🎮 PANEL SIRIUS")
    user_email = st.text_input("📩 Correo Electrónico", placeholder="tu@correo.com")
    
    if user_email:
        st.write("---")
        rol = st.radio("Menú:", ["🏆 Clasificación / Equipos", "📝 Inscribir Equipo", "⚙️ Administración"])
    else:
        st.warning("Ingresa tu correo para continuar.")

# 4. CONTENIDO
if user_email:
    if rol == "🏆 Clasificación / Equipos":
        st.title("Equipos en la Comunidad")
        
        if st.session_state['equipos_registrados']:
            df_equipos = pd.DataFrame(st.session_state['equipos_registrados'])
            st.write("### Lista de Equipos Inscritos")
            st.table(df_equipos[["Nombre", "Liga", "WhatsApp"]])
        else:
            st.info("Aún no hay equipos inscritos. ¡Sé el primero!")
        
    elif rol == "📝 Inscribir Equipo":
        st.title("Inscripción de Equipo")
        with st.form("registro_dt"):
            nombre_eq = st.text_input("Nombre del Equipo")
            wa_dt = st.text_input("WhatsApp")
            liga_destino = st.selectbox("Liga", st.session_state['ligas_creadas'])
            logo = st.file_uploader("Logo del Equipo", type=["png", "jpg"])
            
            if st.form_submit_button("Confirmar Registro"):
                if nombre_eq and wa_dt:
                    # Guardamos el equipo en la memoria
                    nuevo_equipo = {"Nombre": nombre_eq, "WhatsApp": wa_dt, "Liga": liga_destino}
                    st.session_state['equipos_registrados'].append(nuevo_equipo)
                    st.balloons()
                    st.success(f"¡El equipo {nombre_eq} ha sido registrado exitosamente!")
                else:
                    st.error("Faltan datos obligatorios.")

    elif rol == "⚙️ Administración":
        st.title("Panel de Control Maestro")
        clave = st.text_input("Código Maestro", type="password")
        
        if clave == "Sirius2026":
            # --- SECCIÓN: ELIMINAR O AGREGAR EQUIPOS ---
            st.write("### 🛠️ Gestión de Equipos")
            
            if st.session_state['equipos_registrados']:
                # Seleccionar equipo para eliminar
                nombres_equipos = [e["Nombre"] for e in st.session_state['equipos_registrados']]
                equipo_a_borrar = st.selectbox("Selecciona un equipo para ELIMINAR:", nombres_equipos)
                
                if st.button("🗑️ Eliminar Equipo Seleccionado"):
                    st.session_state['equipos_registrados'] = [e for e in st.session_state['equipos_registrados'] if e["Nombre"] != equipo_a_borrar]
                    st.rerun() # Refresca la página para mostrar los cambios
            else:
                st.write("No hay equipos para gestionar.")

            st.write("---")
            st.write("### ➕ Agregar Equipo Manualmente")
            with st.expander("Abrir formulario de alta rápida"):
                n_manual = st.text_input("Nombre Equipo (Manual)")
                l_manual = st.selectbox("Asignar a Liga", st.session_state['ligas_creadas'], key="manual_liga")
                if st.button("Guardar Equipo Manualmente"):
                    st.session_state['equipos_registrados'].append({"Nombre": n_manual, "WhatsApp": "Admin", "Liga": l_manual})
                    st.success(f"Equipo {n_manual} agregado.")
                    st.rerun()

            st.write("---")
            st.write("### 🏆 Gestión de Ligas")
            nueva_l = st.text_input("Nombre de nueva Liga")
            if st.button("Crear Liga"):
                st.session_state['ligas_creadas'].append(nueva_l)
                st.rerun()
