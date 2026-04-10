import streamlit as st
import pandas as pd
import json
import os
from itertools import combinations
from datetime import datetime

# --- CONFIGURACIÓN Y PERSISTENCIA ---
DB_FILE = "sirius_final_db.json"

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
        "reportes_pendientes": st.session_state['reportes_pendientes']
    }
    with open(DB_FILE, "w") as f:
        json.dump(datos, f)

# --- INICIALIZACIÓN ---
st.set_page_config(page_title="Sirius Community PRO", layout="wide")
db = cargar_datos()

for k, v in db.items():
    key = f"{k}_db" if k in ["equipos", "reportes_pendientes"] else k
    if key not in st.session_state: st.session_state[key] = v

if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'

# --- CSS ESTILO PROFESIONAL ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    .card-match { background: #1a1c24; padding: 15px; border-radius: 10px; border-left: 4px solid #00ffcc; margin-bottom: 10px; }
    .stButton>button { background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE IA Y TABLA ---
def procesar_ia_marcador(img_file):
    # Aquí simulamos la lectura de la IA de visión. 
    # En un entorno real conectaríamos con la API de Vision de Google.
    return random.randint(0, 5), random.randint(0, 5)

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

# --- VISTAS LOGIN / AYUDA ---
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY")
    if st.session_state['view'] == 'login':
        u = st.text_input("Usuario"); p = st.text_input("Clave", type="password")
        if st.button("ENTRAR"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u; st.rerun()
        if st.button("Olvidé mi contraseña"): st.session_state['view'] = 'ayuda'; st.rerun()
    elif st.session_state['view'] == 'ayuda':
        st.subheader("Restablecer Cuenta")
        em = st.text_input("Correo registrado")
        if st.button("Enviar enlace"): st.success("Revisa tu correo."); st.session_state['view'] = 'login'; st.rerun()
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()

# --- APP PRINCIPAL ---
else:
    menu = st.sidebar.radio("SIRIUS PRO", ["🏆 Liga", "⚔️ Playoffs", "📋 Reporte DT", "🏅 Salón de la Fama", "⚙️ Admin"])
    if st.sidebar.button("Cerrar Sesión"): st.session_state['usuario_logueado'] = None; st.rerun()

    if menu == "🏆 Liga":
        st.title("TABLA Y JORNADAS")
        st.table(calcular_tabla())
        if st.session_state['partidos_db']:
            jor = st.selectbox("Jornada", sorted(list(set(p['Jornada'] for p in st.session_state['partidos_db']))))
            for p in st.session_state['partidos_db']:
                if p['Jornada'] == jor:
                    st.markdown(f'<div class="card-match">{p["Local"]} {p["GL"]} - {p["GV"]} {p["Visitante"]} ({p["Estado"]})</div>', unsafe_allow_html=True)

    elif menu == "📋 Reporte DT":
        st.title("REPORTAR PARTIDO")
        with st.form("reporte"):
            noms = [e["Nombre"] for e in st.session_state['equipos_db']]
            l = st.selectbox("Local", noms); v = st.selectbox("Visitante", [x for x in noms if x != l])
            foto = st.file_uploader("Sube foto del resultado", type=['png','jpg'])
            if st.form_submit_button("Enviar para validación IA"):
                if foto:
                    # IA lee marcador
                    gl_ia, gv_ia = procesar_ia_marcador(foto)
                    st.session_state['reportes_pendientes_db'].append({
                        "Partido": f"{l} vs {v}", "GL": gl_ia, "GV": gv_ia, "DT": st.session_state['usuario_logueado']
                    })
                    guardar_datos(); st.info(f"IA detectó marcador: {gl_ia}-{gv_ia}. Pendiente de aprobación Admin.")

    elif menu == "⚙️ Admin":
        st.title("CENTRO DE CONTROL")
        t1, t2, t3 = st.tabs(["Ligas", "Playoffs", "Aprobar IA"])
        
        with t1:
            n_j = st.slider("Jornadas", 1, 32, 1)
            if st.button("GENERAR NUEVA LIGA"):
                eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
                st.session_state['partidos_db'] = []
                for j in range(1, n_j + 1):
                    for m in combinations(eqs, 2):
                        st.session_state['partidos_db'].append({"Jornada": j, "Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                guardar_datos(); st.rerun()

        with t2:
            num_p = st.selectbox("Clasificados", [2, 4, 8, 16])
            if st.button("GENERAR BRACKET"):
                top = calcular_tabla()['Equipo'].tolist()[:num_p]
                st.session_state['eliminatorias_db'] = {"Ronda Actual": []}
                for i in range(num_p // 2):
                    st.session_state['eliminatorias_db']["Ronda Actual"].append({"L": top[i], "V": top[num_p-1-i], "GL": 0, "GV": 0})
                guardar_datos(); st.success("Bracket Creado")

        with t3:
            st.subheader("Validación de Resultados IA")
            for idx, r in enumerate(st.session_state['reportes_pendientes_db']):
                st.write(f"Reporte de {r['DT']}: {r['Partido']} -> {r['GL']}-{r['GV']}")
                if st.button("Aprobar y Actualizar Liga", key=f"app{idx}"):
                    # Buscar el partido en la DB y actualizarlo
                    for p in st.session_state['partidos_db']:
                        if f"{p['Local']} vs {p['Visitante']}" == r['Partido']:
                            p.update({"GL": r['GL'], "GV": r['GV'], "Estado": "Finalizado"})
                    st.session_state['reportes_pendientes_db'].pop(idx)
                    guardar_datos(); st.rerun()

    elif menu == "🏅 Salón de la Fama":
        st.title("HISTORIAL DE CAMPEONES")
        for h in st.session_state['historial_campeones']:
            st.write(f"🏆 {h['Edicion']}: {h['Campeon']}")
