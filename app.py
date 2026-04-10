import streamlit as st
import pandas as pd
import json
import os
import random
from itertools import combinations
from datetime import datetime

# --- CONFIGURACIÓN DE PERSISTENCIA ---
DB_FILE = "sirius_community_ultra_db.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {
        "usuarios": {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"},
        "equipos": [],
        "partidos": [],
        "eliminatorias": {}, # Diccionario de fases: {"Octavos": [...], "Semis": [...]}
        "historial_campeones": []
    }

def guardar_datos():
    datos = {
        "usuarios": st.session_state['usuarios'],
        "equipos": st.session_state['equipos_db'],
        "partidos": st.session_state['partidos_db'],
        "eliminatorias": st.session_state['eliminatorias_db'],
        "historial_campeones": st.session_state['historial_campeones']
    }
    with open(DB_FILE, "w") as f:
        json.dump(datos, f)

# --- INICIALIZACIÓN ---
st.set_page_config(page_title="Sirius Community PRO", layout="wide")
db = cargar_datos()

# Asegurar que todo esté en session_state
for k, v in db.items():
    key = f"{k}_db" if k in ["equipos"] else k
    if key not in st.session_state: st.session_state[key] = v

if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'

# --- CSS NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    .stButton>button { background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; }
    .card-bracket { background: #1a1c24; padding: 10px; border: 1px solid #00ffcc; border-radius: 8px; margin: 5px; text-align: center; }
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

# --- LOGIN ---
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ ACCESO SIRIUS")
    u = st.text_input("Usuario"); p = st.text_input("Clave", type="password")
    if st.button("ENTRAR"):
        if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
            st.session_state['usuario_logueado'] = u; st.rerun()
    if st.button("Ayuda con mi cuenta"): st.info("Contacta al soporte para recuperar tu acceso.")

# --- PANEL PRINCIPAL ---
else:
    menu = st.sidebar.radio("SIRIUS MENU", ["🏆 Liga", "⚔️ Playoffs", "🏅 Historial", "📝 Inscripción", "⚙️ Admin"])
    if st.sidebar.button("Cerrar Sesión"): st.session_state['usuario_logueado'] = None; st.rerun()

    if menu == "🏆 Liga":
        st.title("TABLA Y JORNADAS")
        st.table(calcular_tabla())
        if st.session_state['partidos_db']:
            jor = st.selectbox("Jornada", sorted(list(set(p['Jornada'] for p in st.session_state['partidos_db']))))
            for p in st.session_state['partidos_db']:
                if p['Jornada'] == jor:
                    st.markdown(f'<div class="card-bracket">{p["Local"]} {p["GL"]} - {p["GV"]} {p["Visitante"]}</div>', unsafe_allow_html=True)

    elif menu == "⚔️ Playoffs":
        st.title("FASE DE ELIMINACIÓN")
        if not st.session_state['eliminatorias_db']:
            st.warning("No hay eliminatorias activas.")
        else:
            for fase, partidos in st.session_state['eliminatorias_db'].items():
                st.subheader(f"--- {fase} ---")
                for p in partidos:
                    st.markdown(f'<div class="card-bracket">{p["L"]} ({p["GL"]}) vs ({p["GV"]}) {p["V"]}</div>', unsafe_allow_html=True)

    elif menu == "🏅 Historial":
        st.title("🏅 CAMPEONES ANTERIORES")
        if st.session_state['historial_campeones']:
            for h in st.session_state['historial_campeones']:
                st.write(f"🏆 {h['Edicion']}: **{h['Campeon']}** ({h['Fecha']})")
        else: st.write("No hay registros todavía.")

    elif menu == "📝 Inscripción":
        st.title("REGISTRO DE EQUIPO")
        with st.form("ins"):
            nom = st.text_input("Nombre del Club")
            if st.form_submit_button("INSCRIBIR"):
                st.session_state['equipos_db'].append({"Nombre": nom})
                guardar_datos(); st.success("Equipo guardado."); st.rerun()

    elif menu == "⚙️ Admin":
        st.title("CONTROL TOTAL")
        t1, t2 = st.tabs(["Ligas (32 Jornadas)", "Playoffs Estructurados"])
        
        with t1:
            n_j = st.slider("Número de Jornadas", 1, 32, 1)
            if st.button("GENERAR NUEVA LIGA"):
                eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
                st.session_state['partidos_db'] = []
                for j in range(1, n_j + 1):
                    for m in combinations(eqs, 2):
                        st.session_state['partidos_db'].append({"Jornada": j, "Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                guardar_datos(); st.success("Liga creada."); st.rerun()

            # Edición de partidos de liga
            if st.session_state['partidos_db']:
                j_ed = st.selectbox("Editar Jornada", sorted(list(set(p['Jornada'] for p in st.session_state['partidos_db']))))
                for idx, p in enumerate(st.session_state['partidos_db']):
                    if p['Jornada'] == j_ed:
                        col1, col2 = st.columns(2)
                        p['GL'] = col1.number_input(f"Goles {p['Local']}", value=p['GL'], key=f"l{idx}")
                        p['GV'] = col2.number_input(f"Goles {p['Visitante']}", value=p['GV'], key=f"v{idx}")
                        p['Estado'] = st.checkbox("Finalizado", value=(p['Estado']=="Finalizado"), key=f"st{idx}")
                        p['Estado'] = "Finalizado" if p['Estado'] else "Pendiente"
                if st.button("GUARDAR RESULTADOS LIGA"):
                    guardar_datos(); st.success("Resultados guardados permanentemente.")

        with t2:
            st.subheader("Configurar Fase Final")
            n_pasan = st.selectbox("Equipos que pasan", [2, 4, 8, 16])
            nombre_fase = {16: "Octavos", 8: "Cuartos", 4: "Semis", 2: "Final"}[n_pasan]
            
            if st.button(f"GENERAR {nombre_fase.upper()}"):
                tabla = calcular_tabla()
                top = tabla['Equipo'].tolist()[:n_pasan]
                st.session_state['eliminatorias_db'] = {nombre_fase: []}
                for i in range(n_pasan // 2):
                    st.session_state['eliminatorias_db'][nombre_fase].append({"L": top[i], "V": top[n_pasan-1-i], "GL": 0, "GV": 0})
                guardar_datos(); st.rerun()

            if st.session_state['eliminatorias_db']:
                f_act = list(st.session_state['eliminatorias_db'].keys())[-1]
                st.write(f"Editando: {f_act}")
                for idx, p in enumerate(st.session_state['eliminatorias_db'][f_act]):
                    c1, c2 = st.columns(2)
                    p['GL'] = c1.number_input(f"{p['L']}", value=p['GL'], key=f"egl{idx}")
                    p['GV'] = c2.number_input(f"{p['V']}", value=p['GV'], key=f"egv{idx}")
                
                if st.button("AVANZAR RONDA / GUARDAR"):
                    ganadores = [p['L'] if p['GL'] > p['GV'] else p['V'] for p in st.session_state['eliminatorias_db'][f_act]]
                    
                    if f_act == "Final":
                        campeon = ganadores[0]
                        st.balloons()
                        st.session_state['historial_campeones'].append({
                            "Edicion": f"Torneo {datetime.now().strftime('%Y')}",
                            "Campeon": campeon,
                            "Fecha": str(datetime.now().date())
                        })
                        st.session_state['eliminatorias_db'] = {} # Limpiar playoffs
                        guardar_datos(); st.success(f"¡CAMPEÓN: {campeon}! Guardado en historial.")
                    else:
                        next_fase = {"Octavos": "Cuartos", "Cuartos": "Semis", "Semis": "Final"}[f_act]
                        st.session_state['eliminatorias_db'][next_fase] = []
                        for i in range(0, len(ganadores), 2):
                            st.session_state['eliminatorias_db'][next_fase].append({"L": ganadores[i], "V": ganadores[i+1], "GL": 0, "GV": 0})
                        guardar_datos(); st.rerun()
