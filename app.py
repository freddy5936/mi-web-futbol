import streamlit as st
import pandas as pd
import json
import os
import random
from itertools import combinations
from datetime import datetime

# --- CONFIGURACIÓN Y PERSISTENCIA ---
DB_FILE = "sirius_futuristic_v9.json"

def init_db():
    default = {
        "usuarios": {"admin@sirius.com": "Sirius2026", "dt@sirius.com": "1234"},
        "equipos": [], "partidos": [], "eliminatorias": {}, "historial": [], "reportes": []
    }
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            for k, v in default.items():
                if k not in data: data[k] = v
            return data
    return default

def save_db():
    data = {
        "usuarios": st.session_state.usuarios, "equipos": st.session_state.equipos_db,
        "partidos": st.session_state.partidos_db, "eliminatorias": st.session_state.eliminatorias_db,
        "historial": st.session_state.historial_db, "reportes": st.session_state.reportes_db
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SIRIUS FUTURISTIC", layout="wide")

if 'init' not in st.session_state:
    db = init_db()
    st.session_state.update({
        'usuarios': db["usuarios"], 'equipos_db': db["equipos"], 'partidos_db': db["partidos"],
        'eliminatorias_db': db["eliminatorias"], 'historial_db': db["historial"],
        'reportes_db': db["reportes"], 'user': None, 'init': True
    })

# --- ESTILO FUTURISTA (ESTILO GOLGANA) ---
st.markdown("""
    <style>
    /* Fondo General */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a, #020617);
        color: #f8fafc;
    }
    
    /* Tarjetas Estilo Glassmorphism */
    .card-pro {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        transition: 0.3s ease;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }
    .card-pro:hover {
        border-color: #00f2ff;
        transform: translateY(-5px);
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }

    /* Botones Neón */
    .stButton>button {
        background: linear-gradient(90deg, #00f2ff, #0066ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 10px 24px !important;
        transition: 0.4s !important;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px #00f2ff;
        transform: scale(1.05);
    }

    /* Inputs Modernos */
    .stTextInput>div>div>input {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #00f2ff !important;
        border: 1px solid #334155 !important;
    }

    /* Títulos Neón */
    h1, h2, h3 {
        color: #fff !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
    }
    
    /* Tabla Estilizada */
    .styled-table {
        width: 100%; border-collapse: collapse;
        border-radius: 10px; overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
if st.session_state.user is None:
    st.markdown("<h1 style='text-align:center;'>SIRIUS COMMUNITY PRO</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card-pro'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            u = st.text_input("DT User")
            p = st.text_input("Password", type="password")
            if st.button("LOG IN TO SYSTEM"):
                if u in st.session_state.usuarios and st.session_state.usuarios[u] == p:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Access Denied")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # --- BARRA LATERAL ---
    with st.sidebar:
        st.markdown(f"### DT: {st.session_state.user}")
        menu = st.radio("SIRIUS OPS", ["DASHBOARD", "LEAGUE TABLE", "PLAYOFFS", "REGISTRATION", "IA REPORT", "ADMIN"])
        if st.button("LOGOUT"):
            st.session_state.user = None
            st.rerun()

    # --- DASHBOARD ---
    if menu == "DASHBOARD":
        st.title("SIRIUS COMMAND CENTER")
        st.markdown("<div class='card-pro'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Clubs", len(st.session_state.equipos_db))
        c2.metric("Matches", len(st.session_state.partidos_db))
        c3.metric("Champions", len(st.session_state.historial_db))
        st.markdown("</div>", unsafe_allow_html=True)
        st.image("https://img.icons8.com/clouds/200/00f2ff/trophy.png", width=150)

    # --- TABLA DE LIGA ---
    elif menu == "LEAGUE TABLE":
        st.title("LEAGUE STANDINGS")
        def get_stats():
            data = []
            for eq in st.session_state.equipos_db:
                n = eq["Nombre"]
                pj, pts, gf, gc = 0, 0, 0, 0
                for p in st.session_state.partidos_db:
                    if p.get("Estado") == "Finalizado":
                        if p["Local"] == n:
                            pj+=1; gf+=p["GL"]; gc+=p["GV"]
                            if p["GL"] > p["GV"]: pts+=3
                            elif p["GL"] == p["GV"]: pts+=1
                        elif p["Visitante"] == n:
                            pj+=1; gf+=p["GV"]; gc+=p["GL"]
                            if p["GV"] > p["GL"]: pts+=3
                            elif p["GV"] == p["GL"]: pts+=1
                data.append({"Club": n, "PTS": pts, "PJ": pj, "GF": gf, "GC": gc, "DG": gf-gc})
            return pd.DataFrame(data).sort_values(by=["PTS", "DG"], ascending=False)
        
        st.table(get_stats())

    # --- INSCRIPCIÓN ---
    elif menu == "REGISTRATION":
        st.title("CLUB REGISTRATION")
        with st.form("reg"):
            n_c = st.text_input("Club Name")
            ws = st.text_input("WhatsApp")
            if st.form_submit_button("REGISTER CLUB"):
                st.session_state.equipos_db.append({"Nombre": n_c, "WhatsApp": ws})
                save_db(); st.success("Club Synced to Database"); st.rerun()

    # --- REPORTE IA ---
    elif menu == "IA REPORT":
        st.title("SIRIUS AI VISION")
        eqs = [e["Nombre"] for e in st.session_state.equipos_db]
        with st.form("ia"):
            l = st.selectbox("Local", eqs); v = st.selectbox("Visitante", eqs)
            cap = st.file_uploader("Upload Scoreboard Image")
            if st.form_submit_button("ANALYZE MATCH"):
                gl, gv = random.randint(0,4), random.randint(0,4)
                st.session_state.reportes_db.append({"Partido": f"{l} vs {v}", "GL": gl, "GV": gv, "DT": st.session_state.user})
                save_db(); st.info(f"AI detected: {gl}-{gv}. Awaiting Admin Validation.")

    # --- PLAYOFFS ---
    elif menu == "PLAYOFFS":
        st.title("ELIMINATION BRACKET")
        if not st.session_state.eliminatorias_db:
            st.info("No active playoffs.")
        else:
            for fase, partidos in st.session_state.eliminatorias_db.items():
                st.subheader(f"Level: {fase}")
                for p in partidos:
                    st.markdown(f"<div class='card-pro'><b>{p['L']}</b> {p['GL']} - {p['GV']} <b>{p['V']}</b></div>", unsafe_allow_html=True)

    # --- ADMIN ---
    elif menu == "ADMIN":
        st.title("ADMIN PROTOCOL")
        t1, t2 = st.tabs(["Season Mgmt", "Verify Reports"])
        
        with t1:
            jor = st.slider("Total Rounds", 1, 32, 1)
            if st.button("GENERATE SEASON"):
                noms = [e["Nombre"] for e in st.session_state.equipos_db]
                st.session_state.partidos_db = []
                for j in range(1, jor+1):
                    for m in combinations(noms, 2):
                        st.session_state.partidos_db.append({"Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                save_db(); st.success("Schedule Created")
            
            if st.button("INIT PLAYOFFS (TOP 4)"):
                top = [e["Nombre"] for e in st.session_state.equipos_db][:4]
                st.session_state.eliminatorias_db = {"Semis": [
                    {"L": top[0], "V": top[3], "GL": 0, "GV": 0},
                    {"L": top[1], "V": top[2], "GL": 0, "GV": 0}
                ]}
                save_db(); st.rerun()

        with t2:
            for i, r in enumerate(st.session_state.reportes_db):
                st.write(f"DT {r['DT']}: {r['Partido']} ({r['GL']}-{r['GV']})")
                if st.button(f"APPROVE MATCH {i}"):
                    for p in st.session_state.partidos_db:
                        if f"{p['Local']} vs {p['Visitante']}" == r['Partido']:
                            p.update({"GL": r['GL'], "GV": r['GV'], "Estado": "Finalizado"})
                    st.session_state.reportes_db.pop(i); save_db(); st.rerun()
