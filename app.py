import streamlit as st
import pandas as pd
import random
import io
from PIL import Image

# 1. CONFIGURACIÓN Y MEMORIA DEL SISTEMA
st.set_page_config(page_title="Sirius Community PRO v2", layout="wide", initial_sidebar_state="expanded")

# Inicialización de bases de datos temporales (session_state)
if 'equipos_db' not in st.session_state:
    st.session_state['equipos_db'] = [] # Lista de diccionarios de equipos
if 'ligas' not in st.session_state:
    st.session_state['ligas'] = ["Top Ligue", "Ligue 2"]
if 'relampagos' not in st.session_state:
    st.session_state['relampagos'] = ["Relámpago #6", "Copa Sirius"]
if 'calendarios' not in st.session_state:
    st.session_state['calendarios'] = {} # Fixtures generados
if 'reportes_resultados' not in st.session_state:
    st.session_state['reportes_resultados'] = [] # Evidencias subidas

# 2. ESTILO VISUAL (Modo Oscuro, Títulos Turquesa, Flecha Neón)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    p, span, label, .stMarkdown { color: #ffffff !important; font-weight: 500; }
    h1, h2, h3 { color: #00ffcc !important; text-shadow: 0 0 5px rgba(0, 255, 204, 0.3); }
    button[kind="headerNoPadding"] { background-color: #00ffcc !important; transform: scale(1.5); color: #0b0e14 !important; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 2px solid #00ffcc; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: #1a1c24 !important; color: white !important; border: 2px solid #3d3f4b !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (INICIO DE SESIÓN)
with st.sidebar:
    st.title("🎮 PANEL SIRIUS PRO")
    user_email = st.text_input("📩 Correo Electrónico", placeholder="tu@correo.com")
    
    if user_email:
        st.write("---")
        rol = st.radio("Secciones:", [
            "🏆 Competiciones y Cruces", 
            "📋 Área de Gestión para DTs", # Donde reportan resultados
            "Inscribir Nuevo Equipo", # Donde se registran
            "⚙️ Panel de Administrador" # Donde gestionas
        ])
    else:
        st.warning("⚠️ Ingresa tu correo para desbloquear la plataforma.")

# 4. FUNCIONES TÉCNICAS (LÓGICA DE CRUCES)
def generar_todos_contra_todos_simple(nombres_equipos):
    if len(nombres_equipos) < 2: return []
    random.shuffle(nombres_equipos)
    jornadas = []
    # Generamos 3 jornadas de ejemplo
    for i in range(3):
        partidos = []
        copia_lista = nombres_equipos.copy()
        while len(copia_lista) > 1:
            e1 = copia_lista.pop(0)
            e2 = copia_lista.pop(0)
            partidos.append(f"{e1} vs {e2}")
        jornadas.append(partidos)
    return jornadas

# 5. CONTENIDO PRINCIPAL (Visible solo si hay email)
if user_email:
    # ---------------------------------------------------------
    # SECCIÓN 1: ESTADO DE LAS COMPETICIONES (ESPECTADOR/GENERAL)
    # ---------------------------------------------------------
    if rol == "🏆 Competiciones y Cruces":
        st.title("🏆 Estado de las Competiciones")
        
        cat = st.radio("Ver Categoría:", ["Ligas Regulares", "Torneos Relámpago"], horizontal=True)
        opciones_torneo = st.session_state['ligas'] if cat == "Ligas Regulares" else st.session_state['relampagos']
        torneo_seleccionado = st.selectbox(f"Selecciona {cat}:", opciones_torneo)
        
        t1, t2 = st.tabs(["📊 Equipos Inscritos", "📅 Calendario de Cruces"])
        
        with t1:
            equipos_filtro = [e for e in st.session_state['equipos_db'] if e["Torneo"] == torneo_seleccionado]
            if equipos_filtro:
                df = pd.DataFrame(equipos_filtro)
                st.write(f"### Lista de Equipos en {torneo_seleccionado}")
                st.table(df[["Nombre", "WhatsApp", "EA ID"]])
            else:
                st.info("Aún no hay equipos inscritos en esta competición.")
                
        with t2:
            if torneo_seleccionado in st.session_state['calendarios']:
                fixture = st.session_state['calendarios'][torneo_seleccionado]
                st.write(f"### Fixture Generado (Primeras 3 Jornadas)")
                for idx, jornada in enumerate(fixture):
                    with st.expander(f"⚽ Jornada {idx + 1}"):
                        for partido in jornada:
                            st.write(f"- **{partido}**")
            else:
                st.warning("⚠️ El Administrador aún no ha generado los cruces para esta competición.")

    # ---------------------------------------------------------
    # SECCIÓN 2: ÁREA DE GESTIÓN PARA DTs (NUEVA INTERFAZ)
    # ---------------------------------------------------------
    elif rol == "📋 Área de Gestión para DTs":
        st.title("📋 Área de Gestión y Reporte para DTs")
        st.write("Bienvenido DT. Aquí puedes reportar tus resultados con la evidencia requerida.")
        
        with st.form("form_reporte_dt"):
            st.write("### Reporte de Partido")
            
            col_t, col_j = st.columns(2)
            with col_t:
                todos_los_torneos = st.session_state['ligas'] + st.session_state['relampagos']
                torneo_reporte = st.selectbox("Torneo/Liga del partido", todos_los_torneos)
            with col_j:
                n_jornada = st.number_input("Número de Jornada", min_value=1, step=1)
            
            st.write("---")
            c1, c2, c3 = st.columns([2, 1, 2])
            with c1:
                e_local = st.text_input("Nombre Equipo Local")
                g_local = st.number_input("Goles Local", min_value=0, step=1)
            with c2:
                st.markdown("<h1 style='text-align:center; padding-top:20px;'>VS</h1>", unsafe_allow_html=True)
            with c3:
                e_visita = st.text_input("Nombre Equipo Visitante")
                g_visita = st.number_input("Goles Visitante", min_value=0, step=1)
                
            st.write("---")
            st.write("### 📸 Evidencia del Resultado (Obligatorio)")
            foto_evidencia = st.file_uploader("Sube la captura de pantalla del final del partido (PNG/JPG)", type=["png", "jpg", "jpeg"])
            
            if st.form_submit_button("Subir Reporte a Validación"):
                if e_local and e_visita and foto_evidencia:
                    reporte = {
                        "DT": user_email,
                        "Torneo": torneo_reporte,
                        "Jornada": n_jornada,
                        "Partido": f"{e_local} {g_local} - {g_visita} {e_visita}",
                        "Evidencia": foto_evidencia
                    }
                    st.session_state['reportes_resultados'].append(reporte)
                    st.balloons()
                    st.success("¡Reporte enviado exitosamente! El Administrador lo validará pronto.")
                else:
                    st.error("⚠️ Faltan datos obligatorios (Equipos o Foto de Evidencia).")

    # ---------------------------------------------------------
    # SECCIÓN 3: INSCRIPCIÓN (INTERFAZ CLÁSICA)
    # ---------------------------------------------------------
    elif rol == "Inscribir Nuevo Equipo":
        st.title("📝 Inscripción de Nuevo Equipo")
        
        with st.form("registro_equipo"):
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                n_equipo = st.text_input("Nombre del Equipo")
                wa_dt = st.text_input("WhatsApp de contacto")
                id_ea = st.text_input("EA ID del DT")
            with col_d2:
                tipo_torneo = st.radio("Tipo de Competencia:", ["Liga Regular", "Relámpago"], horizontal=True)
                opciones = st.session_state['ligas'] if tipo_torneo == "Liga Regular" else st.session_state['relampagos']
                t_destino = st.selectbox("Torneo de destino", opciones)
                logo = st.file_uploader("Sube el Logo del Equipo (PNG/JPG)", type=["png", "jpg"])
                
            if st.form_submit_button("Enviar Inscripción"):
                if n_equipo and wa_dt:
                    # Guardamos el equipo en la base de datos
                    equipo = {
                        "Nombre": n_equipo, "WhatsApp": wa_dt, "EA ID": id_ea,
                        "Torneo": t_destino, "Categoría": tipo_torneo
                    }
                    st.session_state['equipos_db'].append(equipo)
                    st.balloons()
                    st.success(f"¡El equipo '{n_equipo}' se ha inscrito en {t_destino}!")
                else:
                    st.error("⚠️ El Nombre y WhatsApp son obligatorios.")

    # ---------------------------------------------------------
    # SECCIÓN 4: PANEL DE ADMINISTRADOR (CONTROL TOTAL)
    # ---------------------------------------------------------
    elif rol == "⚙️ Panel de Administrador":
        st.title("⚙️ Panel de Control Maestro (Admin)")
        
        if st.text_input("Introduce el Código Maestro:", type="password") == "Sirius2026":
            st.success("Acceso Autorizado.")
            
            tab_admin1, tab_admin2, tab_admin3 = st.tabs(["🛠️ Gestión Equipos", "⚡ Generar Cruces", "📸 Validar Resultados"])
            
            # --- TABS DE ADMIN 1: GESTIÓN EQUIPOS ---
            with tab_admin1:
                st.subheader("🛠️ Editar / Eliminar Equipos Inscritos")
                
                if st.session_state['equipos_db']:
                    df_gest = pd.DataFrame(st.session_state['equipos_db'])
                    st.dataframe(df_gest) # Ver todo
                    
                    st.write("---")
                    # Lógica para seleccionar y eliminar
                    nombres_eqs = [e["Nombre"] for e in st.session_state['equipos_db']]
                    eq_eliminar = st.selectbox("Selecciona un equipo para ELIMINAR:", nombres_eqs)
                    
                    if st.button("🗑️ Eliminar Equipo Seleccionado"):
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != eq_eliminar]
                        st.success(f"Equipo {eq_eliminar} eliminado.")
                        st.rerun()
                else:
                    st.info("No hay equipos para gestionar.")

            # --- TABS DE ADMIN 2: GENERAR CRUCES ---
            with tab_admin2:
                st.subheader("⚡ Publicar Cruces y Calendarios")
                st.write("### ➕ Crear Ligas/Relámpagos")
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    nueva_liga = st.text_input("Nueva Liga Regular")
                    if st.button("Crear Liga"):
                        if nueva_liga and nueva_liga not in st.session_state['ligas']:
                            st.session_state['ligas'].append(nueva_liga); st.rerun()
                with col_c2:
                    nuevo_rel = st.text_input("Nuevo Relámpago")
                    if st.button("Crear Relámpago"):
                        if nuevo_rel and nuevo_rel not in st.session_state['relampagos']:
                            st.session_state['relampagos'].append(nuevo_rel); st.rerun()
                
                st.write("---")
                st.write("### 🔒 Cerrar Inscripciones y Crear Fixture (3 Jornadas)")
                todos_torneos_admin = st.session_state['ligas'] + st.session_state['relampagos']
                torneo_cerrar = st.selectbox("Torneo a cerrar inscripciones:", todos_torneos_admin)
                
                if st.button("🔒 Generar Fixture"):
                    equipos_torneo_admin = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == torneo_cerrar]
                    
                    if len(equipos_torneo_admin) >= 2:
                        # Generamos los cruces
                        st.session_state['calendarios'][torneo_cerrar] = generar_todos_contra_todos_simple(equipos_torneo_admin)
                        st.balloons()
                        st.success(f"¡Calendario generado para {torneo_cerrar}! Ya es visible para los DTs.")
                    else:
                        st.error("⚠️ Necesitas al menos 2 equipos inscritos en este torneo.")

            # --- TABS DE ADMIN 3: VALIDAR RESULTADOS ---
            with tab_admin3:
                st.subheader("📸 Reportes de Resultados Enviados por DTs")
                
                if st.session_state['reportes_resultados']:
                    for idx, reporte in enumerate(st.session_state['reportes_resultados']):
                        with st.expander(f"Reporte {idx+1}: {reporte['Partido']} - {reporte['DT']} ({reporte['Torneo']})"):
                            col_f1, col_f2 = st.columns([2, 1])
                            with col_f1:
                                # Mostrar la imagen subida
                                try:
                                    image = Image.open(reporte['Evidencia'])
                                    st.image(image, caption="Evidencia del resultado", use_column_width=True)
                                except Exception as e:
                                    st.error(f"Error al cargar la imagen: {e}")
                            with col_f2:
                                st.write("**Detalles:**")
                                st.write(f"- Jornada: {reporte['Jornada']}")
                                st.write(f"- Reportado por: {reporte['DT']}")
                                if st.button(f"🗑️ Descartar Reporte #{idx+1}"):
                                    # Lógica para borrar el reporte de la lista
                                    st.session_state['reportes_resultados'].pop(idx)
                                    st.rerun()
                else:
                    st.info("No hay reportes de resultados pendientes por validar.")
        elif clave != "":
            st.error("Código incorrecto.")

# Pie de página
st.sidebar.divider()
st.sidebar.caption("Sirius System v2.0 | Walllesglint72")
