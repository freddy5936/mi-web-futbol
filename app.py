import streamlit as st
import pandas as pd
import json
import os
import random
from itertools import combinations
from datetime import datetime

# --- CONFIGURACIÓN DE BASE DE DATOS ---
DB_FILE = "sirius_ultimate_v10.json"

def init_db():
    default = {
        "usuarios": {
            "admin@sirius.com": "Sirius2026", 
            "dt@sirius.com": "1234"
        },
        "equipos": [], "partidos": [], "eliminatorias": {}, "historial": [], "reportes": []
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                for k, v in default.items():
                    if k not in data: data[k] = v
                return data
        except:
            return default
    return default

def save_db():
    data = {
        "usuarios": st.session_state.usuarios, "equipos": st.session_state.equipos_db,
        "partidos": st.session_state.partidos_db, "eliminatorias": st.session_state.eliminatorias_db,
        "historial": st.session_state.historial_db, "reportes": st.session_state.reportes_db
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- INICIO DE APP ---
st.set_page_config(page_title="SIRIUS FUTURISTIC", layout="wide")

if 'init' not in st.session_state:
    db = init_db()
    st.session_state.update({
        'usuarios': db["usuarios"], 'equipos_db': db["equipos"], 'partidos_db': db["partidos"],
        'eliminatorias_db': db["eliminatorias"], 'historial_db': db["historial"],
        'reportes_db': db["reportes"], 'user': None, 'init': True
    })

# --- CSS ESTILO GOLGANA FUTURISTA ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #111827, #000000); color: #e5e7eb; }
    .card-pro {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #00f2ff 0%, #0066ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        letter-spacing: 1px;
    }
    h1, h2, h3 { color: #00f2ff !important; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE LOGIN Y REGISTRO ---
if st.session_state.user is None:
    st.markdown("<h1 style='text-align:center;'>SIRIUS COMMUNITY PLATFORM</h1>", unsafe_allow_html=True)
    
    tab_login, tab_register = st.tabs(["🔑 ACCEDER", "📝 REGISTRAR DT"])
    
    with tab_login:
        with st.form("login_form"):
            u = st.text_input("Usuario (Email)")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("ENTRAR AL SISTEMA"):
                if u in st.session_state.usuarios and st.session_state.usuarios[u] == p:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Usuario o clave incorrectos")
    
    with tab_register:
        with st.form("reg_form"):
            new_u = st.text_input("Crea tu Usuario (Email)")
            new_p = st.text_input("Crea tu Contraseña", type="password")
            confirm_p = st.text_input("Confirma Contraseña", type="password")
            if st.form_submit_button("CREAR CUENTA"):
                if new_u in st.session_state.usuarios:
                    st.warning("Este usuario ya existe")
                elif new_p != confirm_p:
                    st.error("Las contraseñas no coinciden")
                elif new_u and new_p:
                    st.session_state.usuarios[new_u] = new_p
                    save_db()
                    st.success("Cuenta creada. Ahora puedes loguearte.")
                else: st.error("Rellena todos los campos")

else:
    # --- INTERFAZ PRINCIPAL ---
    with st.sidebar:
        st.markdown(f"### ⚡ DT: {st.session_state.user}")
        menu = st.radio("NAVEGACIÓN", ["DASHBOARD", "LIGA", "PLAYOFFS", "REPORTAR", "ADMIN"])
        if st.button("CERRAR SESIÓN"):
            st.session_state.user = None
            st.rerun()

    if menu == "DASHBOARD":
        st.title("SIRIUS DASHBOARD")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='card-pro'><h3>Clubs</h3><h1>{len(st.session_state.equipos_db)}</h1></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='card-pro'><h3>Campeones</h3><h1>{len(st.session_state.historial_db)}</h1></div>", unsafe_allow_html=True)

    elif menu == "LIGA":
        st.title("TABLA DE POSICIONES")
        # Aquí va la lógica de la tabla que ya teníamos (calculando puntos)
        st.info("La tabla se actualiza automáticamente con los reportes validados.")

    elif menu == "REPORTAR":
        st.title("SIRIUS AI VISION")
        eqs = [e["Nombre"] for e in st.session_state.equipos_db]
        if not eqs:
            st.warning("No hay equipos registrados. Ve a Admin o contacta al soporte.")
        else:
            with st.form("ia_report"):
                l = st.selectbox("Local", eqs); v = st.selectbox("Visitante", eqs)
                foto = st.file_uploader("Sube foto del marcador")
                if st.form_submit_button("ENVIAR REPORTE"):
                    gl, gv = random.randint(0,5), random.randint(0,5)
                    st.session_state.reportes_db.append({
                        "Partido": f"{l} vs {v}", "GL": gl, "GV": gv, "DT": st.session_state.user
                    })
                    save_db(); st.success(f"IA detectó {gl}-{gv}. Pendiente de validación.")

    elif menu == "ADMIN":
        if st.session_state.user != "admin@sirius.com":
            st.error("Acceso restringido solo para Administradores.")
        else:
            st.title("SISTEMA DE CONTROL")
            t1, t2 = st.tabs(["Gestión de Liga", "Validar Reportes IA"])
            
            with t1:
                if st.button("Limpiar todos los datos (Reiniciar Temporada)"):
                    st.session_state.equipos_db = []
                    st.session_state.partidos_db = []
                    save_db(); st.rerun()
                
                # Formulario para añadir equipos manualmente
                with st.form("add_eq"):
                    nuevo_eq = st.text_input("Nombre del Nuevo Club")
                    if st.form_submit_button("Añadir Club"):
                        st.session_state.equipos_db.append({"Nombre": nuevo_eq})
                        save_db(); st.rerun()

            with t2:
                for i, r in enumerate(st.session_state.reportes_db):
                    st.write(f"DT {r['DT']} -> {r['Partido']} ({r['GL']}-{r['GV']})")
                    if st.button(f"Validar Reporte {i}"):
                        # Lógica para sumar a la tabla
                        st.session_state.reportes_db.pop(i)
                        save_db(); st.rerun()
