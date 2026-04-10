import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
from PIL import Image

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

# 3. ESTILO CSS NEON SIRIUS
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; text-transform: uppercase; }
    .stButton>button { width: 100%; background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; border-radius: 8px; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 1px solid #00ffcc; }
    .card-partido { background-color: #1a1c24; border-left: 5px solid #00ffcc; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
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

# 4. LOGIN / REGISTRO / RECUPERACIÓN
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY")
    
    if st.session_state['view'] == 'login':
        u = st.text_input("Correo")
        p = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u; st.rerun()
            else: st.error("Acceso incorrecto.")
        col1, col2 = st.columns(2)
        if col1.button("Regístrate"): st.session_state['view'] = 'registro'; st.rerun()
        if col2.button("¿Olvidaste tu clave?"): st.session_state['view'] = 'recuperar'; st.rerun()

    elif st.session_state['view'] == 'recuperar':
        st.subheader("Recuperar Cuenta")
        email_rec = st.text_input("Introduce tu correo para recibir el código")
        if st.button("Enviar Enlace de Recuperación"):
            if email_rec in st.session_state['usuarios']:
                st.success(f"Enlace enviado a {email_rec}. Revisa tu bandeja.")
                time.sleep(2); st.session_state['view'] = 'login'; st.rerun()
            else: st.error("Correo no encontrado.")
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()

    elif st.session_state['view'] == 'registro':
        nu = st.text_input("Nuevo Correo")
        np = st.text_input("Nueva Contraseña", type="password")
        if st.button("CREAR CUENTA"):
            st.session_state['usuarios'][nu] = np
            st.success("¡Cuenta creada!"); st.session_state['view'] = 'login'; st.rerun()
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()

# 5. PANEL PRINCIPAL
else:
    with st.sidebar:
        st.title("SIRIUS MENU")
        st.write(f"DT: {st.session_state['usuario_logueado']}")
        menu = st.radio("NAVEGACIÓN:", ["🏠 Inicio", "🏆 Torneo y Tabla", "⚔️ Eliminatorias", "📋 Reporte DT", "📝 Inscripción", "⚙️ Admin"])
        if st.button("SALIR"): st.session_state['usuario_logueado'] = None; st.rerun()

    # --- INICIO ---
    if menu == "🏠 Inicio":
        st.title("📢 NOVEDADES SIRIUS")
        st.markdown('<div class="card-partido"><h3>🔥 Gran Final Próximamente</h3><p>La fase de grupos está por terminar. ¡Prepárense!</p></div>', unsafe_allow_html=True)

    # --- TABLA Y LIGA ---
    elif menu == "🏆 Torneo y Tabla":
        st.title("🏆 LIGA REGULAR")
        t = calcular_tabla()
        if not t.empty: st.table(t)
        
        st.subheader("📅 JORNADAS ACTUALES")
        for p in st.session_state['partidos_db']:
            st.markdown(f"""
            <div class="card-partido">
                <b>{p['Local']}</b> {p.get('GL',0)} - {p.get('GV',0)} <b>{p['Visitante']}</b> <br>
                <small>Estado: {p.get('Estado','Pendiente')}</small>
            </div>
            """, unsafe_allow_html=True)

    # --- ELIMINATORIAS ---
    elif menu == "⚔️ Eliminatorias":
        st.title("⚔️ FASE FINAL")
        if not st.session_state['eliminatorias_db']:
            st.info("El administrador aún no ha generado los cruces finales.")
        else:
            for p in st.session_state['eliminatorias_db']:
                st.markdown(f'<div class="card-partido"><b>{p["Fase"]}</b>: {p["Local"]} vs {p["Visitante"]}</div>', unsafe_allow_html=True)

    # --- REPORTE DT ---
    elif menu == "📋 Reporte DT":
        st.title("📋 REPORTAR RESULTADO")
        nombres = [e["Nombre"] for e in st.session_state['equipos_db']]
        with st.form("rep"):
            loc = st.selectbox("Local:", nombres); vis = st.selectbox("Visitante:", [n for n in nombres if n != loc])
            gl = st.number_input("Goles Local", 0); gv = st.number_input("Goles Visitante", 0)
            foto = st.file_uploader("Sube Foto de Evidencia", type=["jpg", "png"])
            if st.form_submit_button("Enviar Reporte"):
                if foto:
                    st.session_state['reportes_pendientes'].append({"DT": st.session_state['usuario_logueado'], "Partido": f"{loc} vs {vis}", "Marcador": f"{gl}-{gv}", "Foto": foto})
                    st.success("Enviado al Admin.")

    # --- INSCRIPCIÓN ---
    elif menu == "📝 Inscripción":
        st.title("📝 REGISTRO DE CLUB")
        with st.form("ins"):
            nom = st.text_input("Nombre Club"); ws = st.text_input("WhatsApp"); tor = st.selectbox("Torneo", ["Top Ligue", "Ligue 2"])
            if st.form_submit_button("Inscribirme"):
                st.session_state['equipos_db'].append({"Nombre": nom, "WhatsApp": ws, "Torneo": tor})
                st.success("¡Registrado!")

    # --- ADMIN (EL CEREBRO) ---
    elif menu == "⚙️ Admin":
        if st.session_state['usuario_logueado'] in ["admin@sirius.com", "walllesglint72@gmail.com"]:
            st.title("⚙️ PANEL MAESTRO")
            t1, t2, t3, t4 = st.tabs(["⚡ Gestión Liga", "⚔️ Gestión Final", "📩 Reportes DT", "📱 Equipos"])
            
            with t1:
                jor_n = st.number_input("Número de Jornadas", 1, 5, 1)
                if st.button("GENERAR JORNADAS TODOS CONTRA TODOS"):
                    eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
                    if len(eqs) >= 2:
                        st.session_state['partidos_db'] = []
                        from itertools import combinations
                        matches = list(combinations(eqs, 2))
                        for _ in range(jor_n):
                            for m in matches:
                                st.session_state['partidos_db'].append({"Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                        st.success("Liga creada.")
                
                for i, p in enumerate(st.session_state['partidos_db']):
                    with st.expander(f"{p['Local']} vs {p['Visitante']}"):
                        c1, c2 = st.columns(2)
                        gl = c1.number_input("GL", value=p['GL'], key=f"l{i}")
                        gv = c2.number_input("GV", value=p['GV'], key=f"v{i}")
                        est = st.selectbox("Estado", ["Pendiente", "Finalizado"], index=0 if p['Estado']=="Pendiente" else 1, key=f"e{i}")
                        if st.button("Guardar", key=f"b{i}"):
                            st.session_state['partidos_db'][i].update({"GL": gl, "GV": gv, "Estado": est}); st.rerun()

            with t2:
                num_pasan = st.selectbox("Equipos que pasan:", [2, 4, 8])
                if st.button("GENERAR CRUCES FINALES"):
                    tabla = calcular_tabla()
                    if len(tabla) >= num_pasan:
                        top = tabla['Equipo'].tolist()[:num_pasan]
                        st.session_state['eliminatorias_db'] = []
                        for i in range(num_pasan // 2):
                            st.session_state['eliminatorias_db'].append({"Fase": "Eliminatoria", "Local": top[i], "Visitante": top[num_pasan-1-i], "GL": 0, "GV": 0})
                        st.success("Cruces creados.")

            with t3:
                for idx, r in enumerate(st.session_state['reportes_pendientes']):
                    with st.expander(f"Reporte de {r['DT']}"):
                        st.write(f"{r['Partido']} | Marcador: {r['Marcador']}")
                        st.image(r['Foto'])
                        if st.button("Aceptar Reporte", key=f"acc{idx}"):
                            st.session_state['reportes_pendientes'].pop(idx); st.rerun()

            with t4:
                st.table(pd.DataFrame(st.session_state['equipos_db']))
        else:
            st.error("Acceso denegado.")
