import streamlit as st
import pandas as pd
import json
import os
import random
from itertools import combinations
from datetime import datetime

# --- CONFIGURACIÓN Y PERSISTENCIA ---
DB_FILE = "sirius_final_pro_db.json"

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
st.set_page_config(page_title="Sirius Community PRO", layout="wide")
db = cargar_datos()

# Mapeo de datos a session_state
if 'usuarios' not in st.session_state: st.session_state['usuarios'] = db["usuarios"]
if 'equipos_db' not in st.session_state: st.session_state['equipos_db'] = db["equipos"]
if 'partidos_db' not in st.session_state: st.session_state['partidos_db'] = db["partidos"]
if 'eliminatorias_db' not in st.session_state: st.session_state['eliminatorias_db'] = db["eliminatorias"]
if 'historial_campeones' not in st.session_state: st.session_state['historial_campeones'] = db["historial_campeones"]
if 'reportes_pendientes_db' not in st.session_state: st.session_state['reportes_pendientes_db'] = db["reportes_pendientes"]

if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    .stButton>button { background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; width: 100%; border-radius: 8px; }
    .card-match { background: #1a1c24; padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; margin-bottom: 10px; }
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

# --- LOGIN / REGISTRO / AYUDA ---
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ ACCESO SIRIUS")
    if st.session_state['view'] == 'login':
        u = st.text_input("Usuario (Correo)"); p = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u; st.rerun()
            else: st.error("Acceso denegado")
        c1, c2 = st.columns(2)
        if c1.button("Regístrate"): st.session_state['view'] = 'registro'; st.rerun()
        if c2.button("Olvidé mi clave"): st.session_state['view'] = 'ayuda'; st.rerun()
    elif st.session_state['view'] == 'ayuda':
        em = st.text_input("Correo registrado para recuperar")
        if st.button("Enviar"): st.success("Correo enviado."); st.session_state['view'] = 'login'; st.rerun()
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()
    elif st.session_state['view'] == 'registro':
        nu = st.text_input("Nuevo Correo"); np = st.text_input("Nueva Clave", type="password")
        if st.button("Crear Cuenta"):
            st.session_state['usuarios'][nu] = np; guardar_datos(); st.session_state['view'] = 'login'; st.rerun()
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()

# --- APP PRINCIPAL ---
else:
    menu = st.sidebar.radio("SIRIUS MENU", ["🏠 Inicio", "🏆 Liga Regular", "⚔️ Playoffs", "📝 Inscripción", "📋 Reporte DT", "⚙️ Admin"])
    if st.sidebar.button("Cerrar Sesión"): st.session_state['usuario_logueado'] = None; st.rerun()

    if menu == "🏠 Inicio":
        st.title("BIENVENIDO A SIRIUS COMMUNITY")
        st.write(f"Conectado como: **{st.session_state['usuario_logueado']}**")
        st.info("Revisa las pestañas para ver la tabla o reportar tus partidos.")

    elif menu == "🏆 Liga Regular":
        st.title("TABLA DE POSICIONES")
        t = calcular_tabla()
        if not t.empty: st.table(t)
        if st.session_state['partidos_db']:
            jor = st.selectbox("Ver Jornada", sorted(list(set(p['Jornada'] for p in st.session_state['partidos_db']))))
            for p in st.session_state['partidos_db']:
                if p['Jornada'] == jor:
                    st.markdown(f'<div class="card-match">{p["Local"]} {p["GL"]} - {p["GV"]} {p["Visitante"]} ({p["Estado"]})</div>', unsafe_allow_html=True)

    elif menu == "📝 Inscripción":
        st.title("REGISTRA TU CLUB")
        with st.form("form_ins"):
            nom_eq = st.text_input("Nombre del Club")
            whatsapp = st.text_input("WhatsApp de contacto")
            if st.form_submit_button("REGISTRAR EQUIPO"):
                if nom_eq:
                    st.session_state['equipos_db'].append({"Nombre": nom_eq, "WhatsApp": whatsapp})
                    guardar_datos(); st.success(f"¡{nom_eq} ha sido registrado!"); st.rerun()

    elif menu == "📋 Reporte DT":
        st.title("REPORTAR RESULTADO")
        with st.form("rep"):
            eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
            l = st.selectbox("Local", eqs); v = st.selectbox("Visitante", [x for x in eqs if x != l])
            foto = st.file_uploader("Sube foto del marcador", type=['jpg', 'png'])
            if st.form_submit_button("Enviar para Validación IA"):
                if foto:
                    # Simulación de IA leyendo marcador
                    g_l, g_v = random.randint(0,4), random.randint(0,4)
                    st.session_state['reportes_pendientes_db'].append({"Partido": f"{l} vs {v}", "GL": g_l, "GV": g_v, "DT": st.session_state['usuario_logueado']})
                    guardar_datos(); st.info(f"IA detectó {g_l}-{g_v}. Pendiente de aprobación.")

    elif menu == "⚙️ Admin":
        if st.session_state['usuario_logueado'] in ["admin@sirius.com", "walllesglint72@gmail.com"]:
            st.title("ADMINISTRACIÓN")
            t1, t2, t3 = st.tabs(["Ligas", "Playoffs", "Aprobar Reportes IA"])
            
            with t1:
                n_jor = st.slider("Jornadas", 1, 32, 1)
                if st.button("GENERAR LIGA"):
                    noms = [e["Nombre"] for e in st.session_state['equipos_db']]
                    st.session_state['partidos_db'] = []
                    for j in range(1, n_jor + 1):
                        for m in combinations(noms, 2):
                            st.session_state['partidos_db'].append({"Jornada": j, "Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                    guardar_datos(); st.rerun()
            
            with t3:
                for idx, r in enumerate(st.session_state['reportes_pendientes_db']):
                    st.write(f"Reporte de {r['DT']}: {r['Partido']} ({r['GL']}-{r['GV']})")
                    if st.button("Aprobar Marcador", key=f"btn{idx}"):
                        for p in st.session_state['partidos_db']:
                            if f"{p['Local']} vs {p['Visitante']}" == r['Partido']:
                                p.update({"GL": r['GL'], "GV": r['GV'], "Estado": "Finalizado"})
                        st.session_state['reportes_pendientes_db'].pop(idx); guardar_datos(); st.rerun()
        else:
            st.error("Acceso exclusivo para Admin.")
