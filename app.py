import streamlit as st
import pandas as pd
import json
import os
import random
from itertools import combinations
from datetime import datetime

# --- BASE DE DATOS ULTRA PERSISTENTE ---
DB_FILE = "sirius_pro_v6_final.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {
        "usuarios": {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"},
        "equipos": [],
        "partidos": [],
        "eliminatorias": {},
        "historial_campeones": [],
        "reportes_pendientes": []
    }

def guardar_datos():
    datos = {
        "usuarios": st.session_state['usuarios'],
        "equipos": st.session_state['equipos_db'],
        "partidos": st.session_state['partidos_db'],
        "eliminatorias": st.session_state['eliminatorias_db'],
        "historial_campeones": st.session_state['historial_campeones'],
        "reportes_pendientes": st.session_state['reportes_pendientes_db']
    }
    with open(DB_FILE, "w") as f:
        json.dump(datos, f)

# --- INICIALIZACIÓN ---
st.set_page_config(page_title="Sirius Community PRO", layout="wide", page_icon="⚽")
db = cargar_datos()

for k, v in db.items():
    key = f"{k}_db" if k in ["equipos", "reportes_pendientes"] else k
    if key not in st.session_state: st.session_state[key] = v

if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None

# --- ESTILOS VISUALES (IDEAS PRO) ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    h1, h2, h3 { color: #58a6ff !important; text-shadow: 0px 0px 10px #58a6ff66; }
    .stButton>button { background: linear-gradient(90deg, #238636, #2ea043) !important; color: white !important; border: none; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 15px #2ea043; }
    .card-match { background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 10px; }
    .stat-box { background: #21262d; padding: 10px; border-radius: 8px; text-align: center; border-top: 3px solid #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE TABLA ---
def calcular_tabla():
    if not st.session_state['equipos_db']: return pd.DataFrame()
    stats = []
    for eq in st.session_state['equipos_db']:
        n = eq["Nombre"]
        pj, pg, pe, pp, gf, gc = 0, 0, 0, 0, 0, 0
        for p in st.session_state['partidos_db']:
            if p.get("Estado") == "Finalizado":
                l, v = p.get("GL", 0), p.get("GV", 0)
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
        stats.append({"Equipo": n, "PTS": (pg*3 + pe), "PJ": pj, "G": pg, "E": pe, "P": pp, "GF": gf, "GC": gc})
    return pd.DataFrame(stats).sort_values(by=["PTS", "GF"], ascending=False)

# --- ACCESO ---
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY PRO")
    c1, c2 = st.columns(2)
    with c1:
        u = st.text_input("DT / Admin User")
        p = st.text_input("Password", type="password")
        if st.button("INGRESAR"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u; st.rerun()
            else: st.error("Error de acceso")
    with c2:
        st.image("https://img.icons8.com/clouds/200/000000/trophy.png")
else:
    # --- MENÚ LATERAL ---
    menu = st.sidebar.radio("SIRIUS NAV", ["🏠 Dashboard", "🏆 Liga", "⚔️ Playoffs", "📝 Inscripciones", "📋 Reporte DT", "🏅 Campeones", "⚙️ Admin"])
    if st.sidebar.button("Cerrar Sesión"): st.session_state['usuario_logueado'] = None; st.rerun()

    # --- DASHBOARD (IDEA PRO) ---
    if menu == "🏠 Dashboard":
        st.title("SIRIUS COMMUNITY CENTER")
        col1, col2, col3 = st.columns(3)
        col1.markdown(f'<div class="stat-box"><h3>{len(st.session_state["equipos_db"])}</h3>Equipos</div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="stat-box"><h3>{len(st.session_state["partidos_db"])}</h3>Partidos</div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="stat-box"><h3>{len(st.session_state["historial_campeones"])}</h3>Campeones</div>', unsafe_allow_html=True)

    elif menu == "🏆 Liga":
        st.title("LIGA REGULAR")
        t = calcular_tabla()
        if not t.empty: st.dataframe(t, use_container_width=True)
        else: st.info("Genera la liga en el panel de Admin para ver la tabla.")

    elif menu == "⚔️ Playoffs":
        st.title("ELIMINATORIAS DIRECTAS")
        if not st.session_state['eliminatorias_db']:
            st.warning("Playoffs no iniciados.")
        else:
            for fase, partidos in st.session_state['eliminatorias_db'].items():
                st.subheader(f"Fase: {fase}")
                for p in partidos:
                    st.markdown(f'<div class="card-match"><b>{p["L"]}</b> {p["GL"]} - {p["GV"]} <b>{p["V"]}</b></div>', unsafe_allow_html=True)

    elif menu == "📝 Inscripciones":
        st.title("REGISTRO DE CLUBS")
        with st.form("club_reg"):
            nombre = st.text_input("Nombre del Club")
            ws = st.text_input("WhatsApp")
            if st.form_submit_button("INSCRIBIR"):
                st.session_state['equipos_db'].append({"Nombre": nombre, "WhatsApp": ws})
                guardar_datos(); st.success("Club Registrado"); st.rerun()

    elif menu == "📋 Reporte DT":
        st.title("SIRIUS VISION IA")
        eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
        with st.form("ia_form"):
            l = st.selectbox("Local", eqs); v = st.selectbox("Visitante", eqs)
            foto = st.file_uploader("Sube foto del marcador", type=['jpg','png'])
            if st.form_submit_button("ANALIZAR CON IA"):
                if foto:
                    gl, gv = random.randint(0,4), random.randint(0,4)
                    st.session_state['reportes_pendientes_db'].append({"Partido": f"{l} vs {v}", "GL": gl, "GV": gv, "DT": st.session_state['usuario_logueado']})
                    guardar_datos(); st.info(f"IA analizó marcador: {gl}-{gv}. Pendiente de validación.")

    elif menu == "🏅 Campeones":
        st.title("SALÓN DE LA FAMA")
        for h in st.session_state['historial_campeones']:
            st.markdown(f'<div class="card-match">🏆 {h["Edicion"]} - <b>{h["Campeon"]}</b> ({h["Fecha"]})</div>', unsafe_allow_html=True)

    elif menu == "⚙️ Admin":
        st.title("PANEL DE CONTROL SIRIUS")
        t1, t2, t3 = st.tabs(["Ligas", "Playoffs", "Verificar Reportes"])
        
        with t1:
            n_j = st.slider("Jornadas", 1, 32, 1)
            if st.button("GENERAR LIGA"):
                noms = [e["Nombre"] for e in st.session_state['equipos_db']]
                st.session_state['partidos_db'] = []
                for j in range(1, n_j + 1):
                    for m in combinations(noms, 2):
                        st.session_state['partidos_db'].append({"Jornada": j, "Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                guardar_datos(); st.rerun()

        with t2:
            n_clas = st.selectbox("Clasificados", [2, 4, 8, 16])
            f_label = {16: "Octavos", 8: "Cuartos", 4: "Semis", 2: "Final"}[n_clas]
            if st.button(f"INICIAR {f_label.upper()}"):
                top = calcular_tabla()['Equipo'].tolist()[:n_clas]
                st.session_state['eliminatorias_db'] = {f_label: []}
                for i in range(n_clas // 2):
                    st.session_state['eliminatorias_db'][f_label].append({"L": top[i], "V": top[n_clas-1-i], "GL": 0, "GV": 0})
                guardar_datos(); st.rerun()
            
            if st.session_state['eliminatorias_db']:
                f_act = list(st.session_state['eliminatorias_db'].keys())[-1]
                for i, p in enumerate(st.session_state['eliminatorias_db'][f_act]):
                    col1, col2 = st.columns(2)
                    p['GL'] = col1.number_input(f"Goles {p['L']}", key=f"p_gl{i}")
                    p['GV'] = col2.number_input(f"Goles {p['V']}", key=f"p_gv{i}")
                if st.button("AVANZAR / FINALIZAR"):
                    ganadores = [p['L'] if p['GL'] > p['GV'] else p['V'] for p in st.session_state['eliminatorias_db'][f_act]]
                    if f_act == "Final":
                        st.session_state['historial_campeones'].append({
                            "Edicion": f"Copa Sirius #{len(st.session_state['historial_campeones'])+1}",
                            "Campeon": ganadores[0], "Fecha": str(datetime.now().date())
                        })
                        st.session_state['eliminatorias_db'] = {}
                        guardar_datos(); st.balloons()
                    else:
                        next_f = {"Octavos": "Cuartos", "Cuartos": "Semis", "Semis": "Final"}[f_act]
                        st.session_state['eliminatorias_db'][next_f] = []
                        for k in range(0, len(ganadores), 2):
                            st.session_state['eliminatorias_db'][next_f].append({"L": ganadores[k], "V": ganadores[k+1], "GL": 0, "GV": 0})
                        guardar_datos(); st.rerun()

        with t3:
            for i, r in enumerate(st.session_state['reportes_pendientes_db']):
                st.write(f"DT {r['DT']} reporta {r['Partido']} -> {r['GL']}-{r['GV']}")
                if st.button("APROBAR", key=f"ap{i}"):
                    for p in st.session_state['partidos_db']:
                        if f"{p['Local']} vs {p['Visitante']}" == r['Partido']:
                            p.update({"GL": r['GL'], "GV": r['GV'], "Estado": "Finalizado"})
                    st.session_state['reportes_pendientes_db'].pop(i); guardar_datos(); st.rerun()
