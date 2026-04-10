import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

# 2. SISTEMA DE DATOS (Persistencia)
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"}
if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'
if 'equipos_db' not in st.session_state: st.session_state['equipos_db'] = []
if 'partidos_db' not in st.session_state: st.session_state['partidos_db'] = []
if 'noticias' not in st.session_state: 
    st.session_state['noticias'] = [{"fecha": "10/04/2026", "titulo": "Base de Datos Corregida", "contenido": "Ya es visible el WhatsApp en el panel de control.", "icono": "📱"}]

# 3. ESTILO CSS (Diseño Neon & Dark)
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

# --- LÓGICA DE TORNEO ---
def calcular_tabla_automatica():
    if not st.session_state['equipos_db']: return pd.DataFrame()
    stats = []
    for eq in st.session_state['equipos_db']:
        nombre = eq["Nombre"]
        pj, pg, pe, pp, gf, gc = 0, 0, 0, 0, 0, 0
        for p in st.session_state['partidos_db']:
            if p["Estado"] == "Finalizado":
                if p["Local"] == nombre:
                    pj += 1; gf += p["GL"]; gc += p["GV"]
                    if p["GL"] > p["GV"]: pg += 1
                    elif p["GL"] == p["GV"]: pe += 1
                    else: pp += 1
                elif p["Visitante"] == nombre:
                    pj += 1; gf += p["GV"]; gc += p["GL"]
                    if p["GV"] > p["GL"]: pg += 1
                    elif p["GV"] == p["GL"]: pe += 1
                    else: pp += 1
        stats.append({"Equipo": nombre, "PJ": pj, "G": pg, "E": pe, "P": pp, "GF": gf, "GC": gc, "PTS": (pg*3 + pe)})
    return pd.DataFrame(stats).sort_values(by=["PTS", "GF"], ascending=False)

# 4. ACCESO
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY")
    if st.session_state['view'] == 'login':
        u = st.text_input("Correo")
        p = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u
                st.rerun()
            else: st.error("Error de acceso.")
        if st.button("Crear cuenta"): st.session_state['view'] = 'registro'; st.rerun()
    elif st.session_state['view'] == 'registro':
        nu = st.text_input("Nuevo Correo")
        np = st.text_input("Nueva Contraseña", type="password")
        if st.button("REGISTRARME"):
            st.session_state['usuarios'][nu] = np
            st.session_state['view'] = 'login'; st.rerun()
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()

# 5. PANEL PRINCIPAL
else:
    with st.sidebar:
        st.title("SIRIUS PRO")
        opc = ["🏠 Inicio", "🏆 Torneos", "📋 Reporte IA", "📝 Inscripción"]
        if st.session_state['usuario_logueado'] in ["admin@sirius.com", "walllesglint72@gmail.com"]:
            opc.append("⚙️ Admin")
        menu = st.radio("MENÚ:", opc)
        if st.button("SALIR"): st.session_state['usuario_logueado'] = None; st.rerun()

    if menu == "🏠 Inicio":
        st.title("📢 NOVEDADES")
        for n in reversed(st.session_state['noticias']):
            st.markdown(f'<div class="noticia-card"><h3>{n["icono"]} {n["titulo"]}</h3><p>{n["contenido"]}</p></div>', unsafe_allow_html=True)

    elif menu == "🏆 Torneos":
        st.title("🏆 TABLA DE POSICIONES")
        t = calcular_tabla_automatica()
        if not t.empty: st.table(t)
        st.subheader("📅 JORNADAS")
        for p in st.session_state['partidos_db']:
            st.write(f"{p['Local']} {p['GL']} - {p['GV']} {p['Visitante']} ({p['Estado']})")

    elif menu == "📋 Reporte IA":
        st.title("🤖 REPORTE INTELIGENTE")
        if not st.session_state['equipos_db']: st.warning("No hay equipos.")
        else:
            nombres = [e["Nombre"] for e in st.session_state['equipos_db']]
            c1, c2 = st.columns(2)
            loc = c1.selectbox("Local:", nombres)
            vis = c2.selectbox("Visitante:", [n for n in nombres if n != loc])
            f = st.file_uploader("Captura de pantalla", type=["jpg", "png"])
            if f and st.button("ESCANEAR"):
                with st.spinner("Leyendo..."):
                    time.sleep(2)
                    st.success("Reporte enviado. Esperando validación del Admin.")

    elif menu == "📝 Inscripción":
        st.title("📝 REGISTRO DE CLUB")
        with st.form("f_ins"):
            nom = st.text_input("Nombre del Equipo")
            ws = st.text_input("Número de WhatsApp (Con código de país)")
            tor = st.selectbox("Categoría", ["Top Ligue", "Ligue 2"])
            if st.form_submit_button("REGISTRAR"):
                if nom and ws:
                    st.session_state['equipos_db'].append({"Nombre": nom, "WhatsApp": ws, "Torneo": tor})
                    st.success("¡Inscrito correctamente!")

    elif menu == "⚙️ Admin":
        st.title("⚙️ PANEL MAESTRO")
        t1, t2, t3 = st.tabs(["⚡ Torneo", "📱 Registros", "📢 Noticias"])
        
        with t1:
            if st.button("GENERAR FIXTURE AUTOMÁTICO"):
                eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
                if len(eqs) >= 2:
                    st.session_state['partidos_db'] = []
                    random.shuffle(eqs)
                    for i in range(0, len(eqs)-1, 2):
                        st.session_state['partidos_db'].append({"Local": eqs[i], "Visitante": eqs[i+1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                    st.rerun()
            
            st.subheader("Editar Resultados")
            for i, p in enumerate(st.session_state['partidos_db']):
                with st.expander(f"{p['Local']} vs {p['Visitante']}"):
                    c1, c2 = st.columns(2)
                    gl = c1.number_input(f"Goles {p['Local']}", value=p['GL'], key=f"l{i}")
                    gv = c2.number_input(f"Goles {p['Visitante']}", value=p['GV'], key=f"v{i}")
                    est = st.selectbox("Estado", ["Pendiente", "Finalizado"], index=0 if p['Estado']=="Pendiente" else 1, key=f"s{i}")
                    if st.button("Actualizar", key=f"b{i}"):
                        st.session_state['partidos_db'][i].update({"GL": gl, "GV": gv, "Estado": est})
                        st.rerun()

        with t2:
            st.subheader("Equipos e Información de Contacto")
            if st.session_state['equipos_db']:
                st.table(pd.DataFrame(st.session_state['equipos_db']))
            else: st.write("No hay equipos registrados.")

        with t3:
            with st.form("not"):
                tit = st.text_input("Título"); msg = st.text_area("Contenido")
                if st.form_submit_button("Publicar Noticia"):
                    st.session_state['noticias'].append({"fecha": "Hoy", "titulo": tit, "contenido": msg, "icono": "📢"})
                    st.rerun()
