import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
from itertools import combinations

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

# 2. SISTEMA DE DATOS (PERSISTENCIA)
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"}
if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'
if 'equipos_db' not in st.session_state: st.session_state['equipos_db'] = []
if 'partidos_db' not in st.session_state: st.session_state['partidos_db'] = []
if 'eliminatorias_db' not in st.session_state: st.session_state['eliminatorias_db'] = []
if 'reportes_pendientes' not in st.session_state: st.session_state['reportes_pendientes'] = []

# 3. ESTILO CSS NEON
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    .stButton>button { width: 100%; background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; border-radius: 8px; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 1px solid #00ffcc; }
    .noticia-card { background-color: #1a1c24; border-left: 5px solid #00ffcc; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE CÁLCULO ---
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
        stats.append({"Equipo": n, "PJ": pj, "G": pg, "E": pe, "P": pp, "GF": gf, "GC": gc, "PTS": (pg*3 + pe)})
    return pd.DataFrame(stats).sort_values(by=["PTS", "GF"], ascending=False)

# 4. LOGIN / REGISTRO
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY")
    if st.session_state['view'] == 'login':
        u = st.text_input("Correo"); p = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u; st.rerun()
            else: st.error("Acceso incorrecto.")
        if st.button("¿No tienes cuenta? Regístrate"): st.session_state['view'] = 'registro'; st.rerun()
    elif st.session_state['view'] == 'registro':
        nu = st.text_input("Nuevo Correo"); np = st.text_input("Nueva Clave", type="password")
        if st.button("CREAR MI CUENTA"):
            st.session_state['usuarios'][nu] = np
            st.session_state['view'] = 'login'; st.rerun()
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()

# 5. SISTEMA PRINCIPAL
else:
    with st.sidebar:
        st.title("SIRIUS PANEL")
        st.write(f"DT: {st.session_state['usuario_logueado']}")
        opciones = ["🏠 Inicio", "🏆 Tabla de Grupos", "⚔️ Eliminatorias", "📋 Reporte DT", "📝 Inscripción"]
        if st.session_state['usuario_logueado'] in ["admin@sirius.com", "walllesglint72@gmail.com"]:
            opciones.append("⚙️ Admin")
        menu = st.radio("IR A:", opciones)
        if st.button("Cerrar Sesión"): st.session_state['usuario_logueado'] = None; st.rerun()

    if menu == "🏠 Inicio":
        st.title("📢 NOVEDADES")
        st.markdown('<div class="noticia-card"><h3>🚀 Sistema Actualizado</h3><p>Gestión de grupos y eliminatorias ligadas activas.</p></div>', unsafe_allow_html=True)

    elif menu == "🏆 Tabla de Grupos":
        st.title("🏆 TABLA DE POSICIONES")
        t = calcular_tabla()
        if not t.empty: st.table(t)
        st.subheader("📅 JORNADAS")
        for p in st.session_state['partidos_db']:
            st.write(f"{p['Local']} {p.get('GL',0)} - {p.get('GV',0)} {p['Visitante']} ({p.get('Estado','Pendiente')})")

    elif menu == "⚔️ Eliminatorias":
        st.title("⚔️ FASE DE ELIMINACIÓN DIRECTA")
        if not st.session_state['eliminatorias_db']:
            st.info("Esperando que el Admin genere los cruces finales.")
        else:
            for p in st.session_state['eliminatorias_db']:
                st.write(f"🔥 {p['Fase']}: {p['Local']} vs {p['Visitante']} | Resultado: {p.get('GL',0)}-{p.get('GV',0)}")

    elif menu == "📋 Reporte DT":
        st.title("📋 ENVIAR RESULTADO (DT)")
        nombres = [e["Nombre"] for e in st.session_state['equipos_db']]
        with st.form("rep"):
            l = st.selectbox("Local", nombres); v = st.selectbox("Visitante", [x for x in nombres if x != l])
            gl = st.number_input("Goles Local", 0); gv = st.number_input("Goles Visitante", 0)
            f = st.file_uploader("Evidencia (Foto)", type=["jpg","png"])
            if st.form_submit_button("Enviar a Admin"):
                if f:
                    st.session_state['reportes_pendientes'].append({"DT":st.session_state['usuario_logueado'],"Partido":f"{l} vs {v}","Goles":f"{gl}-{gv}","Foto":f})
                    st.success("Reporte enviado.")

    elif menu == "📝 Inscripción":
        st.title("📝 REGISTRO DE CLUB")
        with st.form("ins"):
            nom = st.text_input("Nombre Club"); ws = st.text_input("WhatsApp"); tor = st.selectbox("Torneo",["Top Ligue","Ligue 2"])
            if st.form_submit_button("Inscribirme"):
                st.session_state['equipos_db'].append({"Nombre":nom, "WhatsApp":ws, "Torneo":tor})
                st.success("¡Registrado!")

    elif menu == "⚙️ Admin":
        st.title("⚙️ PANEL MAESTRO")
        t1, t2, t3, t4 = st.tabs(["⚡ Fase de Grupos", "⚔️ Fase Final", "📩 Reportes", "📱 Equipos"])
        
        with t1:
            st.subheader("Generar Todos contra Todos")
            jor_n = st.slider("¿Cuántas veces quieres que se enfrenten? (Jornadas)", 1, 3, 1)
            if st.button("GENERAR LIGA"):
                eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
                if len(eqs) >= 2:
                    st.session_state['partidos_db'] = []
                    matches = list(combinations(eqs, 2))
                    for _ in range(jor_n):
                        for m in matches:
                            st.session_state['partidos_db'].append({"Local":m[0],"Visitante":m[1],"GL":0,"GV":0,"Estado":"Pendiente"})
                    st.rerun()
            
            for i, p in enumerate(st.session_state['partidos_db']):
                with st.expander(f"{p['Local']} vs {p['Visitante']}"):
                    c1, c2 = st.columns(2)
                    gl = c1.number_input("GL", value=p['GL'], key=f"gl{i}")
                    gv = c2.number_input("GV", value=p['GV'], key=f"gv{i}")
                    est = st.selectbox("Estado", ["Pendiente","Finalizado"], index=0 if p['Estado']=="Pendiente" else 1, key=f"st{i}")
                    if st.button("Guardar", key=f"save{i}"):
                        st.session_state['partidos_db'][i].update({"GL":gl,"GV":gv,"Estado":est}); st.rerun()

        with t2:
            st.subheader("Pasar a Eliminatorias")
            num_pas = st.selectbox("¿Cuántos equipos pasan de la tabla?", [2, 4, 8])
            if st.button("CREAR CRUCES FINALES"):
                tabla = calcular_tabla()
                if len(tabla) >= num_pas:
                    top = tabla['Equipo'].tolist()[:num_pas]
                    st.session_state['eliminatorias_db'] = []
                    # Lógica simple 1ero vs último del top
                    for i in range(num_pas // 2):
                        st.session_state['eliminatorias_db'].append({"Fase":"Cruce Directo","Local":top[i],"Visitante":top[num_pas-1-i],"GL":0,"GV":0})
                    st.success(f"¡Cruces de Top {num_pas} creados!")
            
            for i, p in enumerate(st.session_state['eliminatorias_db']):
                with st.expander(f"{p['Local']} vs {p['Visitante']}"):
                    c1, c2 = st.columns(2)
                    p['GL'] = c1.number_input("Goles L", value=p['GL'], key=f"egl{i}")
                    p['GV'] = c2.number_input("Goles V", value=p['GV'], key=f"egv{i}")
                    if st.button("Actualizar Eliminatoria", key=f"eb{i}"): st.rerun()

        with t3:
            for idx, r in enumerate(st.session_state['reportes_pendientes']):
                with st.expander(f"Reporte de {r['DT']}"):
                    st.write(f"{r['Partido']} | {r['Goles']}")
                    st.image(r['Foto'])
                    if st.button("Aceptar", key=f"acc{idx}"): st.session_state['reportes_pendientes'].pop(idx); st.rerun()

        with t4:
            st.table(pd.DataFrame(st.session_state['equipos_db']))
