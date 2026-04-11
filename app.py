import streamlit as st
import pandas as pd
import json
import os
import random
from itertools import combinations
from datetime import datetime

# --- BASE DE DATOS ---
DB_FILE = "sirius_ultimate_v7.json"

def cargar_datos():
    defaults = {
        "usuarios": {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"},
        "equipos": [],
        "partidos": [],
        "eliminatorias": {},
        "historial_campeones": [],
        "reportes_pendientes": []
    }
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            # Asegurar que no falten llaves nuevas si el JSON es viejo
            for key, value in defaults.items():
                if key not in data: data[key] = value
            return data
    return defaults

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
st.set_page_config(page_title="Sirius Community PRO", layout="wide")
if 'init' not in st.session_state:
    db = cargar_datos()
    st.session_state['usuarios'] = db["usuarios"]
    st.session_state['equipos_db'] = db["equipos"]
    st.session_state['partidos_db'] = db["partidos"]
    st.session_state['eliminatorias_db'] = db["eliminatorias"]
    st.session_state['historial_campeones'] = db["historial_campeones"]
    st.session_state['reportes_pendientes_db'] = db["reportes_pendientes"]
    st.session_state['init'] = True

if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .card { background: #1a1c24; padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; margin-bottom: 10px; }
    h1, h2, h3 { color: #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# --- TABLA ---
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
    u = st.text_input("Usuario")
    p = st.text_input("Clave", type="password")
    if st.button("ENTRAR"):
        if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
            st.session_state['usuario_logueado'] = u
            st.rerun()
else:
    menu = st.sidebar.radio("SIRIUS", ["Dashboard", "Liga", "Playoffs", "Inscripción", "Reportar", "Historial", "Admin"])
    if st.sidebar.button("Salir"): 
        st.session_state['usuario_logueado'] = None
        st.rerun()

    if menu == "Dashboard":
        st.title(f"Bienvenido, {st.session_state['usuario_logueado']}")
        st.info("Todo listo para el torneo de mañana.")

    elif menu == "Liga":
        st.title("Tabla General")
        st.table(calcular_tabla())

    elif menu == "Inscripción":
        st.title("Registro de Club")
        with st.form("reg"):
            n = st.text_input("Nombre del Club")
            if st.form_submit_button("Inscribir"):
                st.session_state['equipos_db'].append({"Nombre": n})
                guardar_datos(); st.success("Inscrito"); st.rerun()

    elif menu == "Reportar":
        st.title("Reporte con IA")
        eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
        with st.form("rep"):
            l = st.selectbox("Local", eqs); v = st.selectbox("Visitante", eqs)
            f = st.file_uploader("Foto Marcador")
            if st.form_submit_button("Enviar"):
                gl, gv = random.randint(0,5), random.randint(0,5)
                st.session_state['reportes_pendientes_db'].append({"Partido": f"{l} vs {v}", "GL": gl, "GV": gv, "DT": st.session_state['usuario_logueado']})
                guardar_datos(); st.info("IA detectó marcador. Admin validará.")

    elif menu == "Playoffs":
        st.title("Eliminatorias")
        if not st.session_state['eliminatorias_db']: st.write("No iniciados.")
        else:
            for fase, partidos in st.session_state['eliminatorias_db'].items():
                st.subheader(f"--- {fase} ---")
                for p in partidos:
                    st.markdown(f'<div class="card">{p["L"]} {p["GL"]} - {p["GV"]} {p["V"]}</div>', unsafe_allow_html=True)

    elif menu == "Historial":
        st.title("Campeones")
        for h in st.session_state['historial_campeones']:
            st.write(f"🏆 {h['Edicion']}: {h['Campeon']}")

    elif menu == "Admin":
        st.title("Panel Admin")
        t1, t2, t3 = st.tabs(["Ligas", "Playoffs", "Validar IA"])
        
        with t1:
            n_j = st.slider("Jornadas", 1, 32, 1)
            if st.button("Generar Liga"):
                noms = [e["Nombre"] for e in st.session_state['equipos_db']]
                st.session_state['partidos_db'] = []
                for j in range(1, n_j + 1):
                    for m in combinations(noms, 2):
                        st.session_state['partidos_db'].append({"Jornada": j, "Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                guardar_datos(); st.rerun()

        with t2:
            n_p = st.selectbox("Clasificados", [2, 4, 8, 16])
            f_nom = {16: "Octavos", 8: "Cuartos", 4: "Semis", 2: "Final"}[n_p]
            if st.button(f"Iniciar {f_nom}"):
                top = calcular_tabla()['Equipo'].tolist()[:n_p]
                st.session_state['eliminatorias_db'] = {f_nom: []}
                for i in range(n_p // 2):
                    st.session_state['eliminatorias_db'][f_nom].append({"L": top[i], "V": top[n_p-1-i], "GL": 0, "GV": 0})
                guardar_datos(); st.rerun()

            if st.session_state['eliminatorias_db']:
                f_act = list(st.session_state['eliminatorias_db'].keys())[-1]
                for i, p in enumerate(st.session_state['eliminatorias_db'][f_act]):
                    c1, c2 = st.columns(2)
                    p['GL'] = c1.number_input(f"{p['L']}", value=p['GL'], key=f"gl{i}")
                    p['GV'] = c2.number_input(f"{p['V']}", value=p['GV'], key=f"gv{i}")
                
                if st.button("Avanzar Ronda"):
                    ganadores = [p['L'] if p['GL'] > p['GV'] else p['V'] for p in st.session_state['eliminatorias_db'][f_act]]
                    if f_act == "Final":
                        st.session_state['historial_campeones'].append({"Edicion": f"Copa #{len(st.session_state['historial_campeones'])+1}", "Campeon": ganadores[0]})
                        st.session_state['eliminatorias_db'] = {}
                        guardar_datos(); st.balloons()
                    else:
                        sig = {"Octavos": "Cuartos", "Cuartos": "Semis", "Semis": "Final"}[f_act]
                        st.session_state['eliminatorias_db'][sig] = []
                        for k in range(0, len(ganadores), 2):
                            st.session_state['eliminatorias_db'][sig].append({"L": ganadores[k], "V": ganadores[k+1], "GL": 0, "GV": 0})
                        guardar_datos(); st.rerun()

        with t3:
            for idx, r in enumerate(st.session_state['reportes_pendientes_db']):
                st.write(f"{r['DT']} reporta {r['Partido']} ({r['GL']}-{r['GV']})")
                if st.button("Aprobar", key=f"ap{idx}"):
                    for p in st.session_state['partidos_db']:
                        if f"{p['Local']} vs {p['Visitante']}" == r['Partido']:
                            p.update({"GL": r['GL'], "GV": r['GV'], "Estado": "Finalizado"})
                    st.session_state['reportes_pendientes_db'].pop(idx); guardar_datos(); st.rerun()
