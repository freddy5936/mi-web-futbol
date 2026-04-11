import streamlit as st
import pandas as pd
import json
import os
import random
from itertools import combinations
from datetime import datetime

# --- CONFIGURACIÓN DE BASE DE DATOS ---
DB_FILE = "sirius_pro_v8_shield.json"

def inicializar_db():
    defaults = {
        "usuarios": {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"},
        "equipos": [],
        "partidos": [],
        "eliminatorias": {},
        "historial_campeones": [],
        "reportes_pendientes": []
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                # Blindaje: Si faltan llaves, las agrega de los defaults
                for k, v in defaults.items():
                    if k not in data: data[k] = v
                return data
        except:
            return defaults
    return defaults

def guardar_cambios():
    data = {
        "usuarios": st.session_state.usuarios,
        "equipos": st.session_state.equipos_db,
        "partidos": st.session_state.partidos_db,
        "eliminatorias": st.session_state.eliminatorias_db,
        "historial_campeones": st.session_state.historial_campeones,
        "reportes_pendientes": st.session_state.reportes_pendientes_db
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SIRIUS COMMUNITY PRO", layout="wide", page_icon="⚽")

# Cargar datos al Session State una sola vez
if 'usuarios' not in st.session_state:
    db = inicializar_db()
    st.session_state.usuarios = db["usuarios"]
    st.session_state.equipos_db = db["equipos"]
    st.session_state.partidos_db = db["partidos"]
    st.session_state.eliminatorias_db = db["eliminatorias"]
    st.session_state.historial_campeones = db["historial_campeones"]
    st.session_state.reportes_pendientes_db = db["reportes_pendientes"]
    st.session_state.usuario_logueado = None

# --- ESTILO VISUAL PRO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .card { background: #161b22; padding: 20px; border-radius: 10px; border-left: 5px solid #00ffcc; margin-bottom: 15px; border-right: 1px solid #30363d; }
    h1, h2, h3 { color: #00ffcc !important; text-shadow: 0px 0px 8px #00ffcc44; }
    .stButton>button { background: linear-gradient(45deg, #00ffcc, #0088ff) !important; color: black !important; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE TABLA ---
def obtener_tabla():
    if not st.session_state.equipos_db: return pd.DataFrame()
    res = []
    for eq in st.session_state.equipos_db:
        n = eq["Nombre"]
        pj, pg, pe, pp, gf, gc = 0, 0, 0, 0, 0, 0
        for p in st.session_state.partidos_db:
            if p.get("Estado") == "Finalizado":
                l, v = p["GL"], p["GV"]
                if p["Local"] == n:
                    pj += 1; gf += l; gc += v
                    if l > v: pg += 1
                    elif l == v: pe += 1
                    else: pp += 1
                elif p["Visitante"] == n:
                    pj += 1; gf += v; gc += l
                    if v > l: pg += 1
                    elif v == l: pe += 1
                    else: pp += 1
        res.append({"Equipo": n, "PTS": (pg*3 + pe), "PJ": pj, "G": pg, "E": pe, "P": pp, "GF": gf, "GC": gc})
    return pd.DataFrame(res).sort_values(by=["PTS", "GF"], ascending=False)

# --- SISTEMA DE NAVEGACIÓN ---
if st.session_state.usuario_logueado is None:
    st.title("⚽ ACCESO SIRIUS PRO")
    u = st.text_input("Usuario / Email")
    p = st.text_input("Contraseña", type="password")
    if st.button("INGRESAR"):
        if u in st.session_state.usuarios and st.session_state.usuarios[u] == p:
            st.session_state.usuario_logueado = u
            st.rerun()
        else: st.error("Credenciales incorrectas")
else:
    menu = st.sidebar.radio("SIRIUS PANEL", ["Dashboard", "Liga Regular", "Playoffs", "Inscripción", "Reportar Resultado", "Salón de la Fama", "⚙️ Admin"])
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.usuario_logueado = None
        st.rerun()

    if menu == "Dashboard":
        st.title("BIENVENIDO A SIRIUS COMMUNITY")
        st.markdown(f"Hola, **{st.session_state.usuario_logueado}**. Tienes el control del torneo.")
        col1, col2 = st.columns(2)
        col1.metric("Equipos Inscritos", len(st.session_state.equipos_db))
        col2.metric("Partidos Jugados", len([p for p in st.session_state.partidos_db if p["Estado"] == "Finalizado"]))

    elif menu == "Liga Regular":
        st.title("TABLA DE POSICIONES")
        df = obtener_tabla()
        if not df.empty: st.table(df)
        else: st.info("No hay datos de liga todavía.")

    elif menu == "Inscripción":
        st.title("REGISTRA TU CLUB")
        with st.form("reg_club"):
            nom_c = st.text_input("Nombre del Club")
            whatsapp = st.text_input("WhatsApp de contacto")
            if st.form_submit_button("REGISTRAR"):
                st.session_state.equipos_db.append({"Nombre": nom_c, "WhatsApp": whatsapp})
                guardar_cambios(); st.success("¡Club Inscrito!"); st.rerun()

    elif menu == "Reportar Resultado":
        st.title("REPORTAR CON IA VISION")
        eqs = [e["Nombre"] for e in st.session_state.equipos_db]
        if not eqs: st.warning("No hay equipos.")
        else:
            with st.form("reporte_ia"):
                l = st.selectbox("Local", eqs); v = st.selectbox("Visitante", eqs)
                foto = st.file_uploader("Sube captura del marcador")
                if st.form_submit_button("ENVIAR A IA"):
                    if foto:
                        g_l, g_v = random.randint(0,5), random.randint(0,5) # Simulación IA
                        st.session_state.reportes_pendientes_db.append({
                            "Partido": f"{l} vs {v}", "GL": g_l, "GV": g_v, "DT": st.session_state.usuario_logueado
                        })
                        guardar_cambios(); st.info(f"IA detectó {g_l}-{g_v}. Pendiente de Admin.")

    elif menu == "Playoffs":
        st.title("FASE ELIMINATORIA")
        if not st.session_state.eliminatorias_db:
            st.info("El Admin no ha iniciado los Playoffs todavía.")
        else:
            for fase, partidos in st.session_state.eliminatorias_db.items():
                st.subheader(f"🏆 {fase}")
                for p in partidos:
                    st.markdown(f'<div class="card">{p["L"]} {p["GL"]} - {p["GV"]} {p["V"]}</div>', unsafe_allow_html=True)

    elif menu == "Salón de la Fama":
        st.title("🏅 CAMPEONES HISTÓRICOS")
        for h in st.session_state.historial_campeones:
            st.markdown(f'<div class="card">🏆 {h["Edicion"]} - **{h["Campeon"]}**</div>', unsafe_allow_html=True)

    elif menu == "⚙️ Admin":
        st.title("MODO ADMINISTRADOR")
        t1, t2, t3 = st.tabs(["Ligas", "Playoffs", "Validar Reportes"])

        with t1:
            jor = st.slider("Número de Jornadas", 1, 32, 1)
            if st.button("GENERAR LIGA"):
                noms = [e["Nombre"] for e in st.session_state.equipos_db]
                st.session_state.partidos_db = []
                for j in range(1, jor + 1):
                    for m in combinations(noms, 2):
                        st.session_state.partidos_db.append({"Jornada": j, "Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                guardar_cambios(); st.rerun()

        with t2:
            n_p = st.selectbox("Cantidad de equipos", [2, 4, 8, 16])
            f_nom = {16: "Octavos", 8: "Cuartos", 4: "Semis", 2: "Final"}[n_p]
            if st.button(f"INICIAR {f_nom.upper()}"):
                tabla = obtener_tabla()
                top = tabla['Equipo'].tolist()[:n_p]
                st.session_state.eliminatorias_db = {f_nom: []}
                for i in range(n_p // 2):
                    st.session_state.eliminatorias_db[f_nom].append({"L": top[i], "V": top[n_p-1-i], "GL": 0, "GV": 0})
                guardar_cambios(); st.rerun()

            if st.session_state.eliminatorias_db:
                f_act = list(st.session_state.eliminatorias_db.keys())[-1]
                for i, p in enumerate(st.session_state.eliminatorias_db[f_act]):
                    c1, c2 = st.columns(2)
                    p['GL'] = c1.number_input(f"{p['L']}", value=p['GL'], key=f"p_gl_{i}")
                    p['GV'] = c2.number_input(f"{p['V']}", value=p['GV'], key=f"p_gv_{i}")
                
                if st.button("AVANZAR / FINALIZAR TORNEO"):
                    ganadores = [p['L'] if p['GL'] > p['GV'] else p['V'] for p in st.session_state.eliminatorias_db[f_act]]
                    if f_act == "Final":
                        st.session_state.historial_campeones.append({"Edicion": f"Temporada {datetime.now().year}", "Campeon": ganadores[0]})
                        st.session_state.eliminatorias_db = {}
                        guardar_cambios(); st.balloons()
                    else:
                        sig = {"Octavos": "Cuartos", "Cuartos": "Semis", "Semis": "Final"}[f_act]
                        st.session_state.eliminatorias_db[sig] = []
                        for k in range(0, len(ganadores), 2):
                            st.session_state.eliminatorias_db[sig].append({"L": ganadores[k], "V": ganadores[k+1], "GL": 0, "GV": 0})
                        guardar_cambios(); st.rerun()

        with t3:
            for i, r in enumerate(st.session_state.reportes_pendientes_db):
                st.write(f"DT {r['DT']} reporta: {r['Partido']} ({r['GL']}-{r['GV']})")
                if st.button("Validar", key=f"v_ia_{i}"):
                    for p in st.session_state.partidos_db:
                        if f"{p['Local']} vs {p['Visitante']}" == r['Partido']:
                            p.update({"GL": r['GL'], "GV": r['GV'], "Estado": "Finalizado"})
                    st.session_state.reportes_pendientes_db.pop(i); guardar_cambios(); st.rerun()
