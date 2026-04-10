import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
from PIL import Image

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sirius Copa Fácil IA", layout="wide")

# 2. BASE DE DATOS INTEGRADA
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {"walllesglint72@gmail.com": "Sirius2026"}
if 'equipos_db' not in st.session_state: st.session_state['equipos_db'] = []
if 'partidos_db' not in st.session_state: st.session_state['partidos_db'] = []
if 'buzon_ia' not in st.session_state: st.session_state['buzon_ia'] = []
if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None

# 3. ESTILO VISUAL NEÓN
st.markdown("""
    <style>
    .stApp { background-color: #0b1016; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; font-family: 'Oswald', sans-serif; }
    .stButton>button { background-color: #00ffcc !important; color: #0b1016 !important; font-weight: bold; border-radius: 10px; border: none; }
    .card { background-color: #1a1f26; padding: 15px; border-radius: 15px; border-left: 5px solid #00ffcc; margin-bottom: 10px; }
    section[data-testid="stSidebar"] { background-color: #11151c !important; border-right: 1px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE TABLA ---
def generar_tabla():
    if not st.session_state['equipos_db']: return pd.DataFrame()
    data = []
    for eq in st.session_state['equipos_db']:
        n = eq["Nombre"]
        pj, pg, pe, pp, gf, gc = 0, 0, 0, 0, 0, 0
        for p in st.session_state['partidos_db']:
            if p["Estado"] == "Finalizado":
                if p["Local"] == n:
                    pj += 1; gf += p["GL"]; gc += p["GV"]
                    if p["GL"] > p["GV"]: pg += 1
                    elif p["GL"] == p["GV"]: pe += 1
                    else: pp += 1
                elif p["Visitante"] == n:
                    pj += 1; gf += p["GV"]; gc += p["GL"]
                    if p["GV"] > p["GL"]: pg += 1
                    elif p["GV"] == p["GL"]: pe += 1
                    else: pp += 1
        data.append({"Equipo": n, "PJ": pj, "G": pg, "E": pe, "P": pp, "GF": gf, "GC": gc, "PTS": (pg*3 + pe)})
    return pd.DataFrame(data).sort_values(by="PTS", ascending=False)

# 4. LOGIN
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COPA FÁCIL")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("Correo")
        p = st.text_input("Contraseña", type="password")
        if st.button("INGRESAR"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u
                st.rerun()
            else: st.error("Acceso denegado")

# 5. PANEL DE CONTROL
else:
    with st.sidebar:
        st.header("SIRIUS PANEL")
        menu = st.radio("IR A:", ["🏠 Inicio", "🏆 Tabla y Jornadas", "📋 Reportar Resultado", "📝 Inscripción", "⚙️ Admin"])
        if st.button("Cerrar Sesión"):
            st.session_state['usuario_logueado'] = None
            st.rerun()

    # --- INICIO ---
    if menu == "🏠 Inicio":
        st.title("📢 BIENVENIDO A SIRIUS")
        st.markdown('<div class="card"><h3>🏆 Temporada FC 26</h3><p>Los DTs ya pueden enviar reportes vía IA para actualizar las tablas automáticamente.</p></div>', unsafe_allow_html=True)

    # --- TABLA Y JORNADAS ---
    elif menu == "🏆 Tabla y Jornadas":
        st.title("🏆 CLASIFICACIÓN Y FIXTURE")
        t1, t2 = st.tabs(["📊 Tabla de Posiciones", "📅 Jornadas Actuales"])
        with t1:
            tabla = generar_tabla()
            if not tabla.empty: st.table(tabla)
            else: st.info("Esperando resultados finales...")
        with t2:
            for i, p in enumerate(st.session_state['partidos_db']):
                status = "✅" if p["Estado"] == "Finalizado" else "⏳"
                st.markdown(f'<div class="card">{status} {p["Local"]} **{p["GL"]} - {p['GV']}** {p["Visitante"]}</div>', unsafe_allow_html=True)

    # --- REPORTE DT ---
    elif menu == "📋 Reportar Resultado":
        st.title("📋 REPORTAR PARTIDO")
        eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
        if not eqs: st.warning("No hay equipos.")
        else:
            with st.form("rep_dt"):
                c1, c2 = st.columns(2)
                loc = c1.selectbox("Local", eqs)
                vis = c2.selectbox("Visitante", [e for e in eqs if e != loc])
                f = st.file_uploader("Sube foto del marcador", type=["png", "jpg", "jpeg"])
                if st.form_submit_button("ENVIAR A IA"):
                    if f:
                        # Guardar en el buzón para el admin
                        st.session_state['buzon_ia'].append({
                            "dt": st.session_state['usuario_logueado'],
                            "partido": f"{loc} vs {vis}",
                            "foto": f,
                            "propuesta": f"{random.randint(0,5)} - {random.randint(0,5)}" # Simulación de IA
                        })
                        st.success("Reporte enviado al Admin correctamente.")

    # --- INSCRIPCIÓN ---
    elif menu == "📝 Inscripción":
        st.title("📝 REGISTRO")
        with st.form("ins"):
            n = st.text_input("Nombre Club")
            w = st.text_input("WhatsApp")
            if st.form_submit_button("REGISTRAR"):
                st.session_state['equipos_db'].append({"Nombre": n, "WhatsApp": w})
                st.success("¡Registrado!")

    # --- ADMIN (EL CORAZÓN) ---
    elif menu == "⚙️ Admin":
        if st.session_state['usuario_logueado'] == "walllesglint72@gmail.com":
            st.title("⚙️ PANEL DE ADMINISTRADOR")
            ad1, ad2, ad3 = st.tabs(["⚡ Generar Jornadas", "🤖 Buzón IA", "🛠 Gestión"])
            
            with ad1:
                st.subheader("Generador Tipo Copa Fácil")
                if st.button("CREAR JORNADAS AUTOMÁTICAS"):
                    nombres = [e["Nombre"] for e in st.session_state['equipos_db']]
                    if len(nombres) >= 2:
                        st.session_state['partidos_db'] = []
                        random.shuffle(nombres)
                        for i in range(0, len(nombres)-1, 2):
                            st.session_state['partidos_db'].append({"Local": nombres[i], "Visitante": nombres[i+1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                        st.success("¡Jornadas generadas!")
                    else: st.error("Faltan equipos para cruces.")

            with ad2:
                st.subheader("Reportes Enviados por DTs")
                if not st.session_state['buzon_ia']:
                    st.info("Sin reportes pendientes.")
                else:
                    for i, rep in enumerate(st.session_state['buzon_ia']):
                        with st.expander(f"Reporte de {rep['dt']} - {rep['partido']}"):
                            st.image(rep["foto"], width=400)
                            st.write(f"**IA Detectó:** {rep['propuesta']}")
                            c1, c2 = st.columns(2)
                            gl = c1.number_input("Goles Local", 0, 10, key=f"gl{i}")
                            gv = c2.number_input("Goles Visitante", 0, 10, key=f"gv{i}")
                            if st.button("VALIDAR Y SUBIR A TABLA", key=f"btn{i}"):
                                # Buscar el partido en el fixture y actualizarlo
                                for p in st.session_state['partidos_db']:
                                    if f"{p['Local']} vs {p['Visitante']}" == rep['partido']:
                                        p["GL"], p["GV"], p["Estado"] = gl, gv, "Finalizado"
                                st.session_state['buzon_ia'].pop(i)
                                st.rerun()

            with ad3:
                st.subheader("Control de Datos")
                if st.button("BORRAR TODO EL TORNEO"):
                    st.session_state['partidos_db'] = []
                    st.session_state['equipos_db'] = []
                    st.rerun()
