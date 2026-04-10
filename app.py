import streamlit as st
import pandas as pd
import random

# 1. CONFIGURACIÓN Y SESIÓN
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"}
if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'
if 'equipos_db' not in st.session_state: st.session_state['equipos_db'] = []
if 'partidos_liga' not in st.session_state: st.session_state['partidos_liga'] = {}
if 'eliminatorias' not in st.session_state: st.session_state['eliminatorias'] = {"Cuartos": [], "Semifinal": [], "Final": []}

# 2. ESTILO NEÓN SIRIUS
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    h1, h2, h3 { color: #00ffcc !important; text-align: center; }
    .stButton>button { background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; border-radius: 10px; }
    .card { background: #1a1c24; padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE INICIO DE SESIÓN Y RECUPERACIÓN
def pantalla_login():
    st.title("⚽ ACCESO SIRIUS")
    
    if st.session_state['view'] == 'login':
        u = st.text_input("Correo")
        p = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u
                st.rerun()
            else: st.error("Datos incorrectos")
        
        c1, c2 = st.columns(2)
        if c1.button("Registrarse"): st.session_state['view'] = 'registro'; st.rerun()
        if c2.button("Olvidé mi contraseña"): st.session_state['view'] = 'recuperar'; st.rerun()

    elif st.session_state['view'] == 'recuperar':
        st.subheader("Recuperar Contraseña")
        email = st.text_input("Introduce tu correo registrado")
        if st.button("Enviar enlace de restablecimiento"):
            if email in st.session_state['usuarios']:
                st.success(f"Se ha enviado un enlace de recuperación a {email} (Simulado)")
                time.sleep(2)
                st.session_state['view'] = 'login'; st.rerun()
            else: st.error("Correo no encontrado")
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()

    elif st.session_state['view'] == 'registro':
        nu = st.text_input("Nuevo Correo")
        np = st.text_input("Nueva Clave", type="password")
        if st.button("Crear Cuenta"):
            st.session_state['usuarios'][nu] = np
            st.success("Cuenta creada"); st.session_state['view'] = 'login'; st.rerun()
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()

# 4. PANEL DE ADMINISTRACIÓN (Lógica del Video)
def panel_admin():
    st.title("⚙️ GESTIÓN DE TORNEO")
    t1, t2 = st.tabs(["📊 Fase 1: Todos contra Todos", "⚔️ Fase 2: Eliminatorias"])

    with t1:
        st.subheader("Configuración de Liga")
        num_fechas = st.number_input("Número de Fechas", 1, 10, 3)
        if st.button("Generar Calendario de Liga"):
            eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
            if len(eqs) >= 2:
                for f in range(1, num_fechas + 1):
                    random.shuffle(eqs)
                    st.session_state['partidos_liga'][f"Fecha {f}"] = [
                        {"L": eqs[i], "V": eqs[i+1], "GL": 0, "GV": 0} for i in range(0, len(eqs)-1, 2)
                    ]
                st.success("Calendario Generado")

    with t2:
        st.subheader("Configuración de Playoffs")
        equipos_pasan = st.selectbox("Equipos que clasifican", [4, 8])
        if st.button("Generar Cruces de Eliminatoria"):
            # Lógica para Cuartos o Semis según los equipos elegidos
            st.session_state['eliminatorias']["Cuartos"] = [{"P": f"Cruce {i+1}", "L": "TBD", "V": "TBD"} for i in range(equipos_pasan//2)]
            st.success("Cruces de Eliminatoria creados")

# 5. VISUALIZACIÓN PARA USUARIOS (Estilo App del video)
def vista_campeonato():
    st.title("🏆 Mini Relámpago")
    fase = st.selectbox("Seleccionar Fase", ["1º Fase: Todos contra Todos", "2º Fase: Eliminatorias"])
    
    if fase == "1º Fase: Todos contra Todos":
        if st.session_state['partidos_liga']:
            fecha_sel = st.selectbox("Seleccionar Fecha", list(st.session_state['partidos_liga'].keys()))
            for p in st.session_state['partidos_liga'][fecha_sel]:
                st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span>{p['L']}</span>
                        <b style="font-size: 20px;">{p['GL']} : {p['GV']}</b>
                        <span>{p['V']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        etapa = st.radio("Etapa", ["Cuartos de final", "Semifinal", "Final"], horizontal=True)
        st.info(f"Mostrando cruces de {etapa}...")

# CONTROL DE FLUJO
if st.session_state['usuario_logueado'] is None:
    pantalla_login()
else:
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/805/805404.png", width=100)
        menu = st.radio("Menú", ["Campeonato", "Mi Perfil", "Inscripción", "Admin"])
        if st.button("Cerrar Sesión"): st.session_state['usuario_logueado'] = None; st.rerun()
    
    if menu == "Campeonato": vista_campeonato()
    elif menu == "Admin": panel_admin()
    elif menu == "Inscripción":
        with st.form("ins"):
            n = st.text_input("Nombre del Equipo")
            if st.form_submit_button("Inscribir"):
                st.session_state['equipos_db'].append({"Nombre": n})
                st.success("Inscrito")
