import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
from PIL import Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

# 2. SISTEMA DE DATOS (Persistencia)
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"}
if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'
if 'equipos_db' not in st.session_state: st.session_state['equipos_db'] = []
if 'partidos_db' not in st.session_state: st.session_state['partidos_db'] = []
if 'reportes_pendientes' not in st.session_state: st.session_state['reportes_pendientes'] = []
if 'noticias' not in st.session_state: 
    st.session_state['noticias'] = [{"fecha": "10/04/2026", "titulo": "Sistema Estabilizado", "contenido": "Error de jornadas corregido. WhatsApp y fotos activos.", "icono": "🛠️"}]

# 3. ESTILO CSS (Neon Sirius)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; text-transform: uppercase; }
    .noticia-card { background-color: #1a1c24; border-left: 5px solid #00ffcc; padding: 20px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { width: 100%; background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; border-radius: 8px; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 1px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE TORNEO (Arreglo del Error KeyError) ---
def calcular_tabla_automatica():
    if not st.session_state['equipos_db']: return pd.DataFrame()
    stats = []
    for eq in st.session_state['equipos_db']:
        nombre = eq["Nombre"]
        pj, pg, pe, pp, gf, gc = 0, 0, 0, 0, 0, 0
        for p in st.session_state['partidos_db']:
            if p.get("Estado") == "Finalizado":
                # Usamos .get() para evitar el error KeyError
                goles_l = p.get("GL", 0)
                goles_v = p.get("GV", 0)
                if p["Local"] == nombre:
                    pj += 1; gf += goles_l; gc += goles_v
                    if goles_l > goles_v: pg += 1
                    elif goles_l == goles_v: pe += 1
                    else: pp += 1
                elif p["Visitante"] == nombre:
                    pj += 1; gf += goles_v; gc += goles_l
                    if goles_v > goles_l: pg += 1
                    elif goles_v == goles_l: pe += 1
                    else: pp += 1
        stats.append({"Equipo": nombre, "PJ": pj, "G": pg, "E": pe, "P": pp, "GF": gf, "GC": gc, "PTS": (pg*3 + pe)})
    return pd.DataFrame(stats).sort_values(by=["PTS", "GF"], ascending=False)

# 4. ACCESO
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY")
    u = st.text_input("Correo"); p = st.text_input("Contraseña", type="password")
    if st.button("ENTRAR"):
        if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
            st.session_state['usuario_logueado'] = u; st.rerun()
        else: st.error("Datos incorrectos.")

# 5. PANEL PRINCIPAL
else:
    with st.sidebar:
        st.title("SIRIUS PRO")
        opc = ["🏠 Inicio", "🏆 Torneos", "📋 Reporte DT", "📝 Inscripción"]
        if st.session_state['usuario_logueado'] in ["admin@sirius.com", "walllesglint72@gmail.com"]:
            opc.append("⚙️ Admin")
        menu = st.radio("MENÚ:", opc)
        if st.button("SALIR"): st.session_state['usuario_logueado'] = None; st.rerun()

    if menu == "🏠 Inicio":
        st.title("📢 NOVEDADES")
        for n in reversed(st.session_state['noticias']):
            st.markdown(f'<div class="noticia-card"><h3>{n["icono"]} {n["titulo"]}</h3><p>{n["contenido"]}</p></div>', unsafe_allow_html=True)

    elif menu == "🏆 Torneos":
        st.title("🏆 TABLAS Y JORNADAS")
        t = calcular_tabla_automatica()
        if not t.empty: st.table(t)
        st.subheader("📅 FIXTURE")
        for p in st.session_state['partidos_db']:
            st.write(f"{p['Local']} {p.get('GL', 0)} - {p.get('GV', 0)} {p['Visitante']} ({p.get('Estado', 'Pendiente')})")

    elif menu == "📋 Reporte DT":
        st.title("📋 ENVIAR REPORTE (DT)")
        nombres = [e["Nombre"] for e in st.session_state['equipos_db']]
        with st.form("rep_dt"):
            loc = st.selectbox("Local:", nombres); vis = st.selectbox("Visitante:", [n for n in nombres if n != loc])
            gl = st.number_input("Goles Local", min_value=0); gv = st.number_input("Goles Visitante", min_value=0)
            foto = st.file_uploader("Sube Evidencia", type=["jpg", "png"])
            if st.form_submit_button("Enviar a Admin"):
                if foto:
                    st.session_state['reportes_pendientes'].append({"DT": st.session_state['usuario_logueado'], "Partido": f"{loc} vs {vis}", "Goles": f"{gl}-{gv}", "Foto": foto})
                    st.success("Reporte enviado al Admin.")

    elif menu == "📝 Inscripción":
        st.title("📝 REGISTRO")
        with st.form("ins"):
            nom = st.text_input("Nombre Equipo"); ws = st.text_input("WhatsApp"); tor = st.selectbox("Torneo", ["Top Ligue", "Ligue 2"])
            if st.form_submit_button("Registrar"):
                st.session_state['equipos_db'].append({"Nombre": nom, "WhatsApp": ws, "Torneo": tor})
                st.success("¡Inscrito!")

    elif menu == "⚙️ Admin":
        st.title("⚙️ PANEL MAESTRO")
        t1, t2, t3 = st.tabs(["📩 Buzón de Fotos", "⚡ Jornadas", "📱 Contactos"])
        
        with t1:
            st.subheader("Reportes con Evidencia")
            for idx, r in enumerate(st.session_state['reportes_pendientes']):
                with st.expander(f"Reporte de {r['DT']}"):
                    st.write(f"**Resultado:** {r['Partido']} ({r['Goles']})")
                    st.image(r['Foto'], use_column_width=True)
                    if st.button("Validar", key=f"v{idx}"):
                        st.session_state['reportes_pendientes'].pop(idx); st.rerun()

        with t2:
            if st.button("GENERAR JORNADAS AUTOMÁTICAS"):
                eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
                if len(eqs) >= 2:
                    st.session_state['partidos_db'] = []
                    random.shuffle(eqs)
                    for i in range(0, len(eqs)-1, 2):
                        st.session_state['partidos_db'].append({"Local": eqs[i], "Visitante": eqs[i+1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                    st.rerun()
            
            for i, p in enumerate(st.session_state['partidos_db']):
                with st.expander(f"{p['Local']} vs {p['Visitante']}"):
                    c1, c2 = st.columns(2)
                    gl = c1.number_input("GL", value=p['GL'], key=f"gl{i}")
                    gv = c2.number_input("GV", value=p['GV'], key=f"gv{i}")
                    est = st.selectbox("Estado", ["Pendiente", "Finalizado"], index=0 if p['Estado']=="Pendiente" else 1, key=f"st{i}")
                    if st.button("Guardar", key=f"sv{i}"):
                        st.session_state['partidos_db'][i].update({"GL": gl, "GV": gv, "Estado": est}); st.rerun()

        with t3:
            st.subheader("Lista de WhatsApp")
            if st.session_state['equipos_db']:
                st.table(pd.DataFrame(st.session_state['equipos_db']))
