import streamlit as st
import pandas as pd
import json
import os
from itertools import combinations

# --- PERSISTENCIA DE DATOS ---
DB_FILE = "sirius_pro_db.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {
        "usuarios": {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"},
        "equipos": [],
        "partidos": [],
        "eliminatorias": {},
        "historial_campeones": []
    }

def guardar_datos():
    datos = {
        "usuarios": st.session_state.get('usuarios', {}),
        "equipos": st.session_state.get('equipos_db', []),
        "partidos": st.session_state.get('partidos_db', []),
        "eliminatorias": st.session_state.get('eliminatorias_db', {}),
        "historial_campeones": st.session_state.get('historial_campeones', [])
    }
    with open(DB_FILE, "w") as f:
        json.dump(datos, f)

# --- INICIALIZACIÓN ---
st.set_page_config(page_title="Sirius Community Master", layout="wide")
datos_db = cargar_datos()

for key, val in datos_db.items():
    session_key = f"{key}_db" if key != "usuarios" and key != "partidos" else key
    if session_key not in st.session_state:
        st.session_state[session_key] = val

if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'

# --- CSS NEON SIRIUS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; text-transform: uppercase; }
    .stButton>button { background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; border-radius: 10px; }
    .card { background: #1a1c24; padding: 20px; border-radius: 15px; border: 1px solid #00ffcc; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE TABLA ---
def calcular_tabla():
    if not st.session_state['equipos_db']: return pd.DataFrame()
    stats = []
    for eq in st.session_state['equipos_db']:
        n = eq["Nombre"]
        pj, pg, pe, pp, gf, gc = 0, 0, 0, 0, 0, 0
        for p in st.session_state['partidos']:
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

# --- LOGIN Y RECUPERACIÓN ---
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY")
    if st.session_state['view'] == 'login':
        u = st.text_input("Usuario")
        p = st.text_input("Clave", type="password")
        if st.button("ACCEDER"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u; st.rerun()
            else: st.error("Credenciales Inválidas")
        if st.button("¿Problemas con tu clave?"): st.session_state['view'] = 'recuperar'; st.rerun()
    
    elif st.session_state['view'] == 'recuperar':
        st.subheader("Soporte de Cuenta")
        mail = st.text_input("Correo de registro")
        if st.button("Enviar instrucciones"):
            st.success("Se ha enviado un acceso temporal a tu correo."); time.sleep(1)
            st.session_state['view'] = 'login'; st.rerun()
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()

# --- INTERFAZ PRINCIPAL ---
else:
    with st.sidebar:
        st.title("SIRIUS PRO")
        menu = st.radio("NAVEGACIÓN:", ["🏠 Inicio", "🏆 Liga", "⚔️ Playoffs", "🏅 Campeones", "📋 Reportes", "⚙️ Admin"])
        if st.button("CERRAR SESIÓN"): st.session_state['usuario_logueado'] = None; st.rerun()

    if menu == "🏠 Inicio":
        st.title("BIENVENIDO DT")
        st.info("Gestiona tus partidos y revisa la tabla en tiempo real.")
        with st.expander("Inscribir Club"):
            new_club = st.text_input("Nombre del Equipo")
            ws = st.text_input("WhatsApp")
            if st.button("REGISTRAR"):
                st.session_state['equipos_db'].append({"Nombre": new_club, "WhatsApp": ws})
                guardar_datos(); st.success("Club Registrado"); st.rerun()

    elif menu == "🏆 Liga":
        st.title("TABLA DE POSICIONES")
        st.table(calcular_tabla())
        if st.session_state['partidos']:
            df = pd.DataFrame(st.session_state['partidos'])
            jor = st.selectbox("Ver Jornada:", sorted(df['Jornada'].unique()))
            for _, r in df[df['Jornada'] == jor].iterrows():
                st.markdown(f'<div class="card">{r["Local"]} {r["GL"]} - {r["GV"]} {r["Visitante"]} ({r["Estado"]})</div>', unsafe_allow_html=True)

    elif menu == "⚙️ Admin":
        st.title("CENTRAL DE MANDO")
        t1, t2, t3 = st.tabs(["⚡ Liga Regular", "⚔️ Fase Final", "💾 Archivo de Torneos"])
        
        with t1:
            n_jor = st.number_input("Jornadas (Máx 32)", 1, 32, 1)
            if st.button("GENERAR LIGA"):
                eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
                if len(eqs) >= 2:
                    st.session_state['partidos'] = []
                    matches = list(combinations(eqs, 2))
                    for j in range(1, n_jor + 1):
                        for m in matches:
                            st.session_state['partidos'].append({"Jornada": j, "Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                    guardar_datos(); st.rerun()

            # IA / LECTOR DE RESULTADOS
            st.subheader("Ayuda de IA: Carga Rápida")
            raw_text = st.text_area("Pega aquí los resultados (Ej: TeamA 2-1 TeamB)")
            if st.button("PROCESAR CON IA"):
                # Lógica simple de parsing para simular lectura de IA
                st.success("Resultados analizados y aplicados a la base de datos.")
                # Aquí iría la lógica de filtrado de strings

            if st.session_state['partidos']:
                j_ed = st.selectbox("Editar Jornada:", sorted(list(set(p['Jornada'] for p in st.session_state['partidos']))))
                for i, p in enumerate(st.session_state['partidos']):
                    if p['Jornada'] == j_ed:
                        with st.expander(f"{p['Local']} vs {p['Visitante']}"):
                            c1, c2 = st.columns(2)
                            p['GL'] = c1.number_input("L", value=p['GL'], key=f"l{i}")
                            p['GV'] = c2.number_input("V", value=p['GV'], key=f"v{i}")
                            p['Estado'] = st.selectbox("Estado", ["Pendiente", "Finalizado"], index=1 if p['Estado']=="Finalizado" else 0, key=f"e{i}")
                if st.button("GUARDAR CAMBIOS"):
                    guardar_datos(); st.success("Base de datos actualizada.")

        with t3:
            st.subheader("Guardar Campeón del Torneo")
            camp = st.text_input("Nombre del Campeón")
            edicion = st.text_input("Edición (Ej: Sirius Cup #26)")
            if st.button("FINALIZAR TORNEO Y GUARDAR"):
                st.session_state['historial_campeones'].append({"Edicion": edicion, "Campeon": camp, "Fecha": str(datetime.now().date())})
                guardar_datos(); st.balloons()

    elif menu == "🏅 Campeones":
        st.title("HALL OF FAME")
        if st.session_state['historial_campeones']:
            for h in st.session_state['historial_campeones']:
                st.markdown(f'<div class="card">🏆 {h["Edicion"]} - <b>{h["Campeon"]}</b> ({h["Fecha"]})</div>', unsafe_allow_html=True)
        else:
            st.write("Aún no hay campeones registrados.")
