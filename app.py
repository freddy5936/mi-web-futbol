import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

# 2. INICIALIZACIÓN DE DATOS (Base de datos completa)
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"}
if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'

# Estructuras de Torneo
if 'equipos_db' not in st.session_state: st.session_state['equipos_db'] = []
if 'partidos_db' not in st.session_state: st.session_state['partidos_db'] = []
if 'noticias' not in st.session_state: st.session_state['noticias'] = []

# 3. ESTILO CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label { color: #ffffff !important; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    .stButton>button { background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; border-radius: 8px; }
    .noticia-card { background-color: #1a1c24; border-left: 5px solid #00ffcc; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 1px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE LÓGICA DE TORNEO ---
def generar_jornadas():
    equipos = [e["Nombre"] for e in st.session_state['equipos_db']]
    if len(equipos) < 2: return
    random.shuffle(equipos)
    nuevos_partidos = []
    # Generador simple de enfrentamientos
    for i in range(0, len(equipos)-1, 2):
        if i+1 < len(equipos):
            nuevos_partidos.append({
                "Local": equipos[i], "Goles L": 0,
                "Visitante": equipos[i+1], "Goles V": 0,
                "Estado": "Pendiente"
            })
    st.session_state['partidos_db'] = nuevos_partidos

def calcular_tabla():
    df_equipos = pd.DataFrame(st.session_state['equipos_db'])
    if df_equipos.empty: return pd.DataFrame()
    
    tabla = pd.DataFrame(columns=["Equipo", "PJ", "PG", "PE", "PP", "GF", "GC", "PTS"])
    for eq in df_equipos["Nombre"]:
        pj, pg, pe, pp, gf, gc, pts = 0, 0, 0, 0, 0, 0, 0
        for p in st.session_state['partidos_db']:
            if p["Estado"] == "Finalizado":
                if p["Local"] == eq or p["Visitante"] == eq:
                    pj += 1
                    g_propio = p["Goles L"] if p["Local"] == eq else p["Goles V"]
                    g_contra = p["Goles V"] if p["Local"] == eq else p["Goles L"]
                    gf += g_propio
                    gc += g_contra
                    if g_propio > g_contra: pg += 1; pts += 3
                    elif g_propio == g_contra: pe += 1; pts += 1
                    else: pp += 1
        # Añadir a la tabla
        nueva_fila = pd.DataFrame([{"Equipo": eq, "PJ": pj, "PG": pg, "PE": pe, "PP": pp, "GF": gf, "GC": gc, "PTS": pts}])
        tabla = pd.concat([tabla, nueva_fila], ignore_index=True)
    return tabla.sort_values(by="PTS", ascending=False)

# 4. ACCESO
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ ACCESO SIRIUS")
    u = st.text_input("Correo")
    p = st.text_input("Contraseña", type="password")
    if st.button("ENTRAR"):
        if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
            st.session_state['usuario_logueado'] = u
            st.rerun()
        else: st.error("Error de acceso.")
else:
    # 5. PANEL PRINCIPAL
    with st.sidebar:
        st.title("SIRIUS PANEL")
        menu = st.radio("MENÚ:", ["🏆 Tabla y Fixture", "📋 Reportar IA", "📝 Inscripción", "⚙️ Admin"])
        if st.button("Salir"):
            st.session_state['usuario_logueado'] = None
            st.rerun()

    # --- TABLA Y FIXTURE ---
    if menu == "🏆 Tabla y Fixture":
        st.title("🏆 Competición en Vivo")
        col_t, col_f = st.columns([2, 1])
        with col_t:
            st.subheader("Clasificación")
            tabla_res = calcular_tabla()
            if not tabla_res.empty: st.table(tabla_res)
            else: st.info("La tabla se actualizará cuando terminen los partidos.")
        with col_f:
            st.subheader("Próximos Partidos")
            for p in st.session_state['partidos_db']:
                st.write(f"◽ {p['Local']} vs {p['Visitante']} ({p['Estado']})")

    # --- REPORTE IA ---
    elif menu == "📋 Reporte IA":
        st.title("🤖 Reportar con IA")
        if not st.session_state['partidos_db']: st.warning("No hay partidos generados.")
        else:
            partido_sel = st.selectbox("Selecciona tu partido:", 
                                     [f"{p['Local']} vs {p['Visitante']}" for p in st.session_state['partidos_db'] if p['Estado'] == "Pendiente"])
            foto = st.file_uploader("Sube evidencia", type=["jpg", "png"])
            if foto and st.button("Analizar con IA"):
                st.success("¡Analizado! El admin debe validar el resultado para actualizar la tabla.")

    # --- INSCRIPCIÓN ---
    elif menu == "📝 Inscripción":
        st.title("📝 Inscripción")
        with st.form("ins"):
            nom = st.text_input("Nombre Club")
            if st.form_submit_button("Registrar"):
                st.session_state['equipos_db'].append({"Nombre": nom})
                st.success("¡Equipo guardado!")

    # --- ADMIN (EL CEREBRO) ---
    elif menu == "⚙️ Admin":
        if st.session_state['usuario_logueado'] in ["admin@sirius.com", "walllesglint72@gmail.com"]:
            st.title("⚙️ Gestión de Torneo")
            tab1, tab2 = st.tabs(["⚡ Generar Torneo", "✍️ Editar Resultados"])
            
            with tab1:
                st.subheader("Control de Jornadas")
                if st.button("Crear Jornada Automática (IA)"):
                    generar_jornadas()
                    st.success("¡Partidos generados con éxito!")
                if st.button("Resetear Todo"):
                    st.session_state['partidos_db'] = []
                    st.session_state['equipos_db'] = []
                    st.rerun()

            with tab2:
                st.subheader("Validar o Editar Marcadores")
                for i, p in enumerate(st.session_state['partidos_db']):
                    with st.expander(f"{p['Local']} vs {p['Visitante']}"):
                        c1, c2 = st.columns(2)
                        g_l = c1.number_input(f"Goles {p['Local']}", value=p['Goles L'], key=f"l_{i}")
                        g_v = c2.number_input(f"Goles {p['Visitante']}", value=p['Goles V'], key=f"v_{i}")
                        estado = st.selectbox("Estado", ["Pendiente", "Finalizado"], index=0 if p['Estado']=="Pendiente" else 1, key=f"e_{i}")
                        if st.button("Guardar Resultado", key=f"b_{i}"):
                            st.session_state['partidos_db'][i].update({"Goles L": g_l, "Goles V": g_v, "Estado": estado})
                            st.success("¡Resultado Actualizado y Tabla Sincronizada!")
                            st.rerun()
        else:
            st.error("Acceso denegado.")
