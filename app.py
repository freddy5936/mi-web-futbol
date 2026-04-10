import streamlit as st
import pandas as pd
import random
import time
from itertools import combinations

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sirius Community PRO", layout="wide")

# 2. PERSISTENCIA DE DATOS
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {"admin@sirius.com": "Sirius2026", "walllesglint72@gmail.com": "Sirius2026"}
if 'usuario_logueado' not in st.session_state: st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'
if 'equipos_db' not in st.session_state: st.session_state['equipos_db'] = []
if 'partidos_db' not in st.session_state: st.session_state['partidos_db'] = [] # Ahora guardará {"Jornada": X, ...}
if 'eliminatorias_db' not in st.session_state: st.session_state['eliminatorias_db'] = {} # Diccionario por fases
if 'reportes_pendientes' not in st.session_state: st.session_state['reportes_pendientes'] = []

# 3. ESTILO CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    h1, h2, h3 { color: #00ffcc !important; text-transform: uppercase; }
    .card-jornada { background-color: #1a1c24; border: 1px solid #00ffcc; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    .stButton>button { background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE LÓGICA ---
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

# 4. LOGIN / REGISTRO / RECUPERACIÓN (MANTENIDO)
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ ACCESO SIRIUS")
    if st.session_state['view'] == 'login':
        u = st.text_input("Correo"); p = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR"):
            if u in st.session_state['usuarios'] and st.session_state['usuarios'][u] == p:
                st.session_state['usuario_logueado'] = u; st.rerun()
            else: st.error("Error de acceso.")
        c1, c2 = st.columns(2)
        if c1.button("Registrarse"): st.session_state['view'] = 'registro'; st.rerun()
        if c2.button("¿Olvidaste tu clave?"): st.session_state['view'] = 'recuperar'; st.rerun()
    elif st.session_state['view'] == 'recuperar':
        em = st.text_input("Correo de recuperación")
        if st.button("Enviar Enlace"): st.success("Enviado."); time.sleep(1); st.session_state['view'] = 'login'; st.rerun()
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()
    elif st.session_state['view'] == 'registro':
        nu = st.text_input("Nuevo Correo"); np = st.text_input("Nueva Clave", type="password")
        if st.button("Crear"): st.session_state['usuarios'][nu] = np; st.session_state['view'] = 'login'; st.rerun()
        if st.button("Volver"): st.session_state['view'] = 'login'; st.rerun()

# 5. PANEL PRINCIPAL
else:
    with st.sidebar:
        st.title("SIRIUS PRO")
        menu = st.radio("MENÚ:", ["🏠 Inicio", "🏆 Liga (Grupos)", "⚔️ Fase Final", "📋 Reporte DT", "📝 Inscripción", "⚙️ Admin"])
        if st.button("SALIR"): st.session_state['usuario_logueado'] = None; st.rerun()

    # --- VISTA DE LIGA (GRUPOS) ---
    if menu == "🏆 Liga (Grupos)":
        st.title("🏆 CLASIFICACIÓN Y JORNADAS")
        tabla = calcular_tabla()
        if not tabla.empty: st.table(tabla)
        
        # Agrupar partidos por jornada para visualización clara
        if st.session_state['partidos_db']:
            df_p = pd.DataFrame(st.session_state['partidos_db'])
            for jor in sorted(df_p['Jornada'].unique()):
                st.subheader(f"📅 Jornada {jor}")
                p_jor = df_p[df_p['Jornada'] == jor]
                for _, row in p_jor.iterrows():
                    st.markdown(f'<div class="card-jornada">{row["Local"]} {row["GL"]} - {row["GV"]} {row["Visitante"]} ({row["Estado"]})</div>', unsafe_allow_html=True)

    # --- VISTA DE ELIMINATORIAS ---
    elif menu == "⚔️ Fase Final":
        st.title("⚔️ ELIMINATORIAS DIRECTAS")
        if not st.session_state['eliminatorias_db']:
            st.info("El torneo aún está en fase de grupos.")
        else:
            for fase, partidos in st.session_state['eliminatorias_db'].items():
                st.header(f"Bracket: {fase}")
                cols = st.columns(len(partidos) if len(partidos) > 0 else 1)
                for idx, p in enumerate(partidos):
                    with cols[idx % len(cols)]:
                        st.markdown(f"""
                        <div style="border: 1px solid #00ffcc; padding:10px; border-radius:5px; text-align:center;">
                            {p['L']} <b>{p['GL']}</b><br>vs<br>{p['V']} <b>{p['GV']}</b>
                        </div>
                        """, unsafe_allow_html=True)

    # --- ADMIN ---
    elif menu == "⚙️ Admin":
        if st.session_state['usuario_logueado'] in ["admin@sirius.com", "walllesglint72@gmail.com"]:
            st.title("⚙️ PANEL MAESTRO")
            t1, t2, t3 = st.tabs(["⚡ Gestión Liga", "⚔️ Gestión Playoffs", "📩 Reportes"])
            
            with t1:
                num_jor = st.number_input("¿Cuántas vueltas (jornadas)?", 1, 5, 1)
                if st.button("GENERAR CALENDARIO DE LIGA"):
                    eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
                    if len(eqs) >= 2:
                        st.session_state['partidos_db'] = []
                        matches = list(combinations(eqs, 2))
                        for j in range(1, num_jor + 1):
                            for m in matches:
                                st.session_state['partidos_db'].append({"Jornada": j, "Local": m[0], "Visitante": m[1], "GL": 0, "GV": 0, "Estado": "Pendiente"})
                        st.rerun()
                
                # Edición de resultados agrupados
                if st.session_state['partidos_db']:
                    jor_edit = st.selectbox("Editar Jornada:", sorted(list(set(p['Jornada'] for p in st.session_state['partidos_db']))))
                    for i, p in enumerate(st.session_state['partidos_db']):
                        if p['Jornada'] == jor_edit:
                            with st.expander(f"{p['Local']} vs {p['Visitante']}"):
                                c1, c2 = st.columns(2)
                                p['GL'] = c1.number_input("Goles L", value=p['GL'], key=f"l{i}")
                                p['GV'] = c2.number_input("Goles V", value=p['GV'], key=f"v{i}")
                                p['Estado'] = st.selectbox("Estado", ["Pendiente", "Finalizado"], index=0 if p['Estado']=="Pendiente" else 1, key=f"e{i}")
                                if st.button("Guardar Partido", key=f"b{i}"): st.rerun()

            with t2:
                st.subheader("Configurar Fase Final")
                n_pasan = st.selectbox("Equipos que clasifican:", [2, 4, 8, 16])
                fase_nombre = {16: "Octavos", 8: "Cuartos", 4: "Semis", 2: "Final"}[n_pasan]
                
                if st.button(f"GENERAR {fase_nombre.upper()}"):
                    tabla = calcular_tabla()
                    if len(tabla) >= n_pasan:
                        top = tabla['Equipo'].tolist()[:n_pasan]
                        st.session_state['eliminatorias_db'] = {fase_nombre: []}
                        for i in range(n_pasan // 2):
                            st.session_state['eliminatorias_db'][fase_nombre].append({"L": top[i], "V": top[n_pasan-1-i], "GL": 0, "GV": 0})
                        st.success(f"Fase de {fase_nombre} creada.")
                
                # Control manual de eliminatorias para avanzar de fase
                if st.session_state['eliminatorias_db']:
                    curr_fase = list(st.session_state['eliminatorias_db'].keys())[-1]
                    st.write(f"Gestionando: {curr_fase}")
                    for idx, p in enumerate(st.session_state['eliminatorias_db'][curr_fase]):
                        with st.expander(f"{p['L']} vs {p['V']}"):
                            c1, c2 = st.columns(2)
                            p['GL'] = c1.number_input("GL", value=p['GL'], key=f"egl{idx}")
                            p['GV'] = c2.number_input("GV", value=p['GV'], key=f"egv{idx}")
                    
                    if st.button("Avanzar a Siguiente Ronda (Ganadores)"):
                        ganadores = []
                        for p in st.session_state['eliminatorias_db'][curr_fase]:
                            ganadores.append(p['L'] if p['GL'] > p['GV'] else p['V'])
                        
                        next_fase = {"Octavos": "Cuartos", "Cuartos": "Semis", "Semis": "Final", "Final": "Campeón"}[curr_fase]
                        if next_fase == "Campeón":
                            st.balloons()
                            st.success(f"¡EL CAMPEÓN ES {ganadores[0]}!")
                        else:
                            st.session_state['eliminatorias_db'][next_fase] = []
                            for i in range(0, len(ganadores), 2):
                                st.session_state['eliminatorias_db'][next_fase].append({"L": ganadores[i], "V": ganadores[i+1], "GL": 0, "GV": 0})
                            st.rerun()

    # --- OTROS MENÚS (REPORTE E INSCRIPCIÓN) ---
    elif menu == "📋 Reporte DT":
        st.title("📋 REPORTAR")
        noms = [e["Nombre"] for e in st.session_state['equipos_db']]
        with st.form("r"):
            l = st.selectbox("Local", noms); v = st.selectbox("Visitante", [x for x in noms if x != l])
            gl = st.number_input("GL", 0); gv = st.number_input("GV", 0)
            f = st.file_uploader("Foto"); btn = st.form_submit_button("Enviar")
            if btn and f: st.success("Enviado al Admin.")
    
    elif menu == "📝 Inscripción":
        st.title("📝 INSCRIPCIÓN")
        with st.form("i"):
            n = st.text_input("Nombre Club"); w = st.text_input("WhatsApp")
            if st.form_submit_button("Inscribirme"):
                st.session_state['equipos_db'].append({"Nombre": n, "WhatsApp": w})
                st.success("Registrado.")
