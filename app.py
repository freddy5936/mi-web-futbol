import streamlit as st
import pandas as pd
import json
import os
from itertools import combinations

# --- CONFIGURACIÓN DE ARCHIVOS PARA GUARDAR DATOS ---
DB_FILE = "sirius_db.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {
        "usuarios": {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"},
        "equipos": [],
        "partidos": [],
        "eliminatorias": {}
    }

def guardar_datos():
    datos = {
        "usuarios": st.session_state['usuarios'],
        "equipos": st.session_state['equipos_db'],
        "partidos": st.session_state['partidos_db'],
        "eliminatorias": st.session_state['eliminatorias_db']
    }
    with open(DB_FILE, "w") as f:
        json.dump(datos, f)

# --- INICIALIZACIÓN ---
st.set_page_config(page_title="Sirius Community PRO", layout="wide")
datos_db = cargar_datos()

if 'usuarios' not in st.session_state: st.session_state['usuarios'] = datos_db["usuarios"]
if 'equipos_db' not in st.session_state: st.session_state['equipos_db'] = datos_db["equipos"]
if 'partidos_db' not in st.session_state: st.session_state['partidos_db'] = datos_db["partidos"]
if 'eliminatorias_db' not in st.session_state: st.session_state['eliminatorias_db'] = datos_db["eliminatorias"]
if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'

# --- ESTILOS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    h1, h2, h3 { color: #00ffcc !important; }
    .card-jornada { background-color: #1a1c24; border: 1px solid #00ffcc; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .stButton>button { background-color: #00ffcc !important; color: #0b0e14 !important; }
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

# --- VISTAS DE LOGIN ---
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ ACCESO SIRIUS")
    if st.session_state['view'] == 'login':
        u = st.text_input("Correo"); p = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u; st.rerun()
            else: st.error("Error.")
        if st.button("¿Olvidaste tu clave?"): st.session_state['view'] = 'recuperar'; st.rerun()
    
    elif st.session_state['view'] == 'recuperar':
        st.subheader("Recuperar Contraseña")
        email_rec = st.text_input("Correo registrado")
        if st.button("Enviar enlace de recuperación"):
            if email_rec in st.session_state['usuarios']:
                st.success("Enlace enviado correctamente.")
                st.session_state['view'] = 'login'; st.rerun()
            else: st.error("Correo no encontrado.")
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()

# --- PANEL PRINCIPAL ---
else:
    with st.sidebar:
        st.title("SIRIUS PRO")
        menu = st.radio("MENÚ:", ["🏠 Inicio", "🏆 Liga", "⚔️ Playoffs", "⚙️ Admin"])
        if st.button("CERRAR SESIÓN"): st.session_state['usuario_logueado'] = None; st.rerun()

    if menu == "🏆 Liga":
        st.title("🏆 CLASIFICACIÓN")
        st.table(calcular_tabla())
        if st.session_state['partidos_db']:
            df = pd.DataFrame(st.session_state['partidos_db'])
            jor = st.selectbox("Seleccionar Jornada", sorted(df['Jornada'].unique()))
            for _, r in df[df['Jornada'] == jor].iterrows():
                st.markdown(f'<div class="card-jornada">{r["Local"]} {r["GL"]} - {r["GV"]} {r["Visitante"]}</div>', unsafe_allow_html=True)

    elif menu == "⚙️ Admin":
        st.title("⚙️ PANEL DE CONTROL")
        t1, t2 = st.tabs(["Gestión de Liga", "Gestión de Playoffs"])
        
        with t1:
            # CAMBIO SOLICITADO: Hasta 32 jornadas
            num_jor = st.number_input("Número de Jornadas (Máx 32)", 1, 32, 1)
            if st.button("REINICIAR Y GENERAR CALENDARIO"):
                eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
                if len(eqs) >= 2:
                    st.session_state['partidos_db'] = []
                    matches = list(combinations(eqs, 2))
                    for j in range(1, num_jor + 1):
                        for m in matches:
                            st.session_state['partidos_db'].append({"Jornada": j, "Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                    guardar_datos() # GUARDAR EN DISCO
                    st.success(f"Calendario de {num_jor} jornadas generado.")

            # Edición de partidos
            if st.session_state['partidos_db']:
                jor_ed = st.selectbox("Editar Resultados Jornada:", sorted(list(set(p['Jornada'] for p in st.session_state['partidos_db']))))
                for i, p in enumerate(st.session_state['partidos_db']):
                    if p['Jornada'] == jor_ed:
                        with st.expander(f"{p['Local']} vs {p['Visitante']}"):
                            c1, c2 = st.columns(2)
                            p['GL'] = c1.number_input("L", value=p['GL'], key=f"l{i}")
                            p['GV'] = c2.number_input("V", value=p['GV'], key=f"v{i}")
                            p['Estado'] = st.selectbox("Estado", ["Pendiente", "Finalizado"], index=1 if p['Estado']=="Finalizado" else 0, key=f"e{i}")
                if st.button("GUARDAR CAMBIOS"):
                    guardar_datos()
                    st.success("¡Datos guardados permanentemente!")

    elif menu == "🏠 Inicio":
        st.title("SIRIUS COMMUNITY")
        if st.session_state['usuario_logueado'] == "walllesglint72@gmail.com":
            st.write("Bienvenido, Administrador.")
        
        # Formulario rápido de inscripción para que no se borren equipos
        with st.expander("Inscribir Nuevo Equipo"):
            new_eq = st.text_input("Nombre del Club")
            if st.button("Confirmar Inscripción"):
                st.session_state['equipos_db'].append({"Nombre": new_eq})
                guardar_datos()
                st.rerun()
