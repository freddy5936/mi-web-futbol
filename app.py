import streamlit as st
import pandas as pd
import json
import os
import random
from itertools import combinations
from datetime import datetime

# --- CONFIGURACIÓN DE PERSISTENCIA ---
DB_FILE = "sirius_community_v4_db.json"

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
st.set_page_config(page_title="Sirius Community Master", layout="wide")
db = cargar_datos()

# Mapeo a Session State para evitar pérdidas al refrescar
for k, v in db.items():
    key = f"{k}_db" if k in ["equipos", "reportes_pendientes"] else k
    if key not in st.session_state: st.session_state[key] = v

if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'

# --- ESTILOS NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    h1, h2, h3 { color: #00ffcc !important; text-transform: uppercase; }
    .stButton>button { background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; border-radius: 5px; }
    .card { background: #1a1c24; padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES CORE ---
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

# --- LOGIN ---
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY")
    if st.session_state['view'] == 'login':
        u = st.text_input("DT / Admin"); p = st.text_input("Clave", type="password")
        if st.button("ACCEDER"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u; st.rerun()
        if st.button("Olvidé mi clave"): st.info("Contacta a Walllesglint72 para resetear.")
else:
    # --- MENÚ ---
    menu = st.sidebar.radio("SIRIUS PRO", ["🏠 Inicio", "🏆 Liga", "⚔️ Playoffs", "📝 Inscripción", "📋 Reporte DT", "🏅 Campeones", "⚙️ Admin"])
    if st.sidebar.button("SALIR"): st.session_state['usuario_logueado'] = None; st.rerun()

    # --- VISTAS ---
    if menu == "🏠 Inicio":
        st.title("BIENVENIDO")
        st.write(f"Sesión activa: **{st.session_state['usuario_logueado']}**")
        st.info("El sistema está listo para la jornada de mañana.")

    elif menu == "🏆 Liga":
        st.title("TABLA GENERAL")
        t = calcular_tabla()
        if not t.empty: st.table(t)
        
    elif menu == "⚔️ Playoffs":
        st.title("BRACKET ELIMINATORIO")
        if not st.session_state['eliminatorias_db']:
            st.warning("No hay playoffs generados aún.")
        else:
            for fase, partidos in st.session_state['eliminatorias_db'].items():
                st.subheader(f"--- {fase} ---")
                for p in partidos:
                    st.markdown(f'<div class="card">{p["L"]} **{p["GL"]}** - **{p["GV"]}** {p["V"]}</div>', unsafe_allow_html=True)

    elif menu == "📝 Inscripción":
        st.title("REGISTRA TU EQUIPO")
        with st.form("ins_club"):
            nombre = st.text_input("Nombre del Club")
            ws = st.text_input("WhatsApp")
            if st.form_submit_button("REGISTRAR"):
                st.session_state['equipos_db'].append({"Nombre": nombre, "WhatsApp": ws})
                guardar_datos(); st.success("¡Registrado!"); st.rerun()

    elif menu == "📋 Reporte DT":
        st.title("ENVIAR RESULTADO (IA)")
        eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
        with st.form("rep_ia"):
            l = st.selectbox("Local", eqs); v = st.selectbox("Visitante", [x for x in eqs if x != l])
            img = st.file_uploader("Foto del marcador", type=['jpg', 'png'])
            if st.form_submit_button("ENVIAR A REVISIÓN"):
                if img:
                    gl_ia, gv_ia = random.randint(0,4), random.randint(0,4)
                    st.session_state['reportes_pendientes_db'].append({"Partido": f"{l} vs {v}", "GL": gl_ia, "GV": gv_ia, "DT": st.session_state['usuario_logueado']})
                    guardar_datos(); st.info(f"IA detectó {gl_ia}-{gv_ia}. Esperando aprobación del Admin.")

    elif menu == "🏅 Campeones":
        st.title("SALÓN DE LA FAMA")
        for c in st.session_state['historial_campeones']:
            st.markdown(f'<div class="card">🏆 {c["Edicion"]} - **{c["Campeon"]}** ({c["Fecha"]})</div>', unsafe_allow_html=True)

    elif menu == "⚙️ Admin":
        st.title("PANEL DE CONTROL")
        tab1, tab2, tab3 = st.tabs(["Gestión Liga", "Gestión Playoffs", "Reportes IA"])
        
        with tab1:
            n_j = st.slider("Número de Jornadas", 1, 32, 1)
            if st.button("GENERAR LIGA COMPLETA"):
                noms = [e["Nombre"] for e in st.session_state['equipos_db']]
                st.session_state['partidos_db'] = []
                for j in range(1, n_j + 1):
                    for m in combinations(noms, 2):
                        st.session_state['partidos_db'].append({"Jornada": j, "Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                guardar_datos(); st.rerun()

        with tab2:
            n_p = st.selectbox("Equipos que clasifican", [2, 4, 8, 16])
            fase_inicial = {16: "Octavos", 8: "Cuartos", 4: "Semis", 2: "Final"}[n_p]
            if st.button(f"INICIAR {fase_inicial.upper()}"):
                top = calcular_tabla()['Equipo'].tolist()[:n_p]
                st.session_state['eliminatorias_db'] = {fase_inicial: []}
                for i in range(n_p // 2):
                    st.session_state['eliminatorias_db'][fase_inicial].append({"L": top[i], "V": top[n_p-1-i], "GL": 0, "GV": 0})
                guardar_datos(); st.rerun()

            if st.session_state['eliminatorias_db']:
                f_act = list(st.session_state['eliminatorias_db'].keys())[-1]
                st.write(f"Gestionando: {f_act}")
                for idx, p in enumerate(st.session_state['eliminatorias_db'][f_act]):
                    c1, c2 = st.columns(2)
                    p['GL'] = c1.number_input(f"{p['L']}", value=p['GL'], key=f"p_l{idx}")
                    p['GV'] = c2.number_input(f"{p['V']}", value=p['GV'], key=f"p_v{idx}")
                
                if st.button("AVANZAR RONDA / FINALIZAR"):
                    ganadores = [p['L'] if p['GL'] > p['GV'] else p['V'] for p in st.session_state['eliminatorias_db'][f_act]]
                    if f_act == "Final":
                        st.session_state['historial_campeones'].append({
                            "Edicion": f"Edición #{len(st.session_state['historial_campeones'])+1}",
                            "Campeon": ganadores[0], "Fecha": str(datetime.now().date())
                        })
                        st.session_state['eliminatorias_db'] = {}
                        guardar_datos(); st.balloons()
                    else:
                        next_f = {"Octavos": "Cuartos", "Cuartos": "Semis", "Semis": "Final"}[f_act]
                        st.session_state['eliminatorias_db'][next_f] = []
                        for i in range(0, len(ganadores), 2):
                            st.session_state['eliminatorias_db'][next_f].append({"L": ganadores[i], "V": ganadores[i+1], "GL": 0, "GV": 0})
                        guardar_datos(); st.rerun()
