import streamlit as st
import pandas as pd
import random
from PIL import Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sirius Community v3", layout="wide")

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

# 3. ESTILO CSS (CORREGIDO PARA VISIBILIDAD)
st.markdown("""
    <style>
    /* Fondo de la app */
    .stApp { background-color: #0b0e14; }
    
    /* Forzar color blanco en todos los textos, etiquetas y párrafos */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label {
        color: #ffffff !important;
    }
    
    /* Títulos en Turquesa */
    h1, h2, h3 { color: #00ffcc !important; }
    
    /* Estilo de la barra lateral */
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 2px solid #00ffcc; }
    
    /* Botones Pro */
    .stButton>button {
        background-color: #00ffcc !important;
        color: #0b0e14 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    
    /* Inputs y Selectbox con texto claro */
    .stTextInput input, .stSelectbox div {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. BARRA LATERAL
with st.sidebar:
    st.title("🎮 PANEL SIRIUS")
    user_email = st.text_input("📩 Correo Electrónico")
    if user_email:
        st.write("---")
        rol = st.radio("Menú:", ["🏆 Cruces", "📋 Reporte IA (DTs)", "📝 Inscripción", "⚙️ Admin"])

# 5. CONTENIDO PRINCIPAL
if user_email:
    if rol == "🏆 Cruces":
        st.title("🏆 Competiciones")
        cat = st.radio("Categoría:", ["Ligas", "Relámpagos"], horizontal=True)
        opc = st.session_state['ligas'] if cat == "Ligas" else st.session_state['relampagos']
        t_sel = st.selectbox("Selecciona torneo:", opc)
        
        if t_sel in st.session_state['calendarios']:
            for idx, jor in enumerate(st.session_state['calendarios'][t_sel]):
                with st.expander(f"⚽ Jornada {idx + 1}"):
                    for p in jor: st.write(f"- {p}")
        else:
            st.info("Aún no se han generado cruces.")

    elif rol == "📋 Reporte IA (DTs)":
        st.title("🤖 Reporte por Foto (IA)")
        st.write("Sube la captura de pantalla y la IA detectará el marcador.")
        t_rep = st.selectbox("¿En qué torneo jugaste?", st.session_state['ligas'] + st.session_state['relampagos'])
        foto = st.file_uploader("Sube evidencia", type=["png", "jpg", "jpeg"])
        
        if foto:
            st.image(foto, width=300)
            if st.button("Analizar Resultado"):
                res_simulado = "Equipo Local 1 - 1 Equipo Visita"
                st.session_state['reportes_ia'].append({"DT": user_email, "Torneo": t_rep, "Resultado": res_simulado, "Foto": foto})
                st.success(f"IA Detectó: {res_simulado}")

    elif rol == "📝 Inscripción":
        st.title("📝 Inscripción de Clubes")
        with st.form("registro"):
            n_eq = st.text_input("Nombre del Club")
            w_eq = st.text_input("WhatsApp")
            t_eq = st.selectbox("Torneo", st.session_state['ligas'] + st.session_state['relampagos'])
            if st.form_submit_button("Confirmar Registro"):
                if n_eq:
                    st.session_state['equipos_db'].append({"Nombre": n_eq, "WhatsApp": w_eq, "Torneo": t_eq})
                    st.success("¡Registrado!")

    elif rol == "⚙️ Admin":
        st.title("⚙️ Administración")
        if st.text_input("Clave", type="password") == "Sirius2026":
            t1, t2, t3 = st.tabs(["Equipos", "Cruces", "Validar IA"])
            
            with t1:
                st.subheader("Gestión de Equipos")
                if st.session_state['equipos_db']:
                    df = pd.DataFrame(st.session_state['equipos_db'])
                    st.dataframe(df)
                    
                    # ELIMINACIÓN CORREGIDA (INDIVIDUAL)
                    nombres_lista = [e["Nombre"] for e in st.session_state['equipos_db']]
                    sel_del = st.selectbox("Selecciona el equipo a borrar:", nombres_lista)
                    if st.button("🗑️ Eliminar Solo Este Equipo"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != sel_del]
                        st.success(f"{sel_del} eliminado.")
                        st.rerun()
                
            with t2:
                st.subheader("Generar Calendarios")
                t_gen = st.selectbox("Elegir Torneo:", st.session_state['ligas'] + st.session_state['relampagos'])
                n_jor = st.number_input("Jornadas:", min_value=1, value=3)
                if st.button("⚡ Publicar"):
                    lista = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == t_gen]
                    if len(lista) >= 2:
                        # Lógica simple de cruces
                        random.shuffle(lista)
                        st.session_state['calendarios'][t_gen] = [[f"{lista[0]} vs {lista[1]}"]]
                        st.success("Jornadas publicadas.")
                    else:
                        st.error("No hay suficientes equipos.")

            with t3:
                st.subheader("Reportes IA Pendientes")
                for r in st.session_state['reportes_ia']:
                    st.write(f"**{r['Torneo']}**: {r['Resultado']}")
                    if st.button("Aceptar"): st.success("Confirmado")
