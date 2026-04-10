import streamlit as st
import pandas as pd
import random
from PIL import Image
import os
import io

# --- CONFIGURACIÓN DE LA PÁGINA (PROFESIONAL, MODO OSCURO) ---
st.set_page_config(
    page_title="Sirius Community PRO v3 - IA Fútbol",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INICIALIZACIÓN DE BASES DE DATOS (session_state) ---
# Usamos session_state para que los datos no se borren al recargar la página
if 'equipos_db' not in st.session_state:
    # Agregamos algunos equipos de prueba para la demo
    st.session_state['equipos_db'] = [
        {"Nombre": "Freddy FC", "WhatsApp": "+1234", "Torneo": "Relámpago #6", "Categoría": "Relámpago"},
        {"Nombre": "Wallles Elite", "WhatsApp": "+5678", "Torneo": "Relámpago #6", "Categoría": "Relámpago"},
        {"Nombre": "Estrellas F.C.", "WhatsApp": "+9012", "Torneo": "Top Ligue", "Categoría": "Liga Regular"}
    ]
if 'ligas' not in st.session_state:
    st.session_state['ligas'] = ["Top Ligue", "Ligue 2"]
if 'relampagos' not in st.session_state:
    st.session_state['relampagos'] = ["Relámpago #6", "Copa Sirius"]
if 'calendarios' not in st.session_state:
    st.session_state['calendarios'] = {}
if 'reportes_ia' not in st.session_state:
    st.session_state['reportes_ia'] = [] # Evidencias subidas por IA

# --- ESTILO CSS PERSONALIZADO (TURQUESA Y OSCURO) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    p, span, label, .stMarkdown { color: #ffffff !important; font-weight: 500; }
    h1, h2, h3 { color: #00ffcc !important; text-shadow: 0 0 5px rgba(0, 255, 204, 0.3); }
    button[kind="headerNoPadding"] { background-color: #00ffcc !important; transform: scale(1.5); color: #0b0e14 !important; }
    section[data-testid="stSidebar"] { background-color: #161922 !important; border-right: 2px solid #00ffcc; }
    
    /* Campos de texto y número claros */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #1a1c24 !important;
        color: white !important;
        border: 2px solid #3d3f4b !important;
    }
    
    /* Botones Pro */
    .stButton>button {
        background-color: #00ffcc !important;
        color: #0b0e14 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (INICIO DE SESIÓN) ---
with st.sidebar:
    st.title("🎮 PANEL SIRIUS v3")
    user_email = st.text_input("📩 Correo Electrónico", placeholder="tu@correo.com")
    
    if user_email:
        st.write("---")
        rol = st.radio("Secciones:", [
            "🏆 Competiciones y Cruces", 
            "📋 Reporte IA (DTs)", 
            " Inscribir Equipo", 
            "⚙️ Administración"
        ])
        st.write("---")
        st.caption(f"Sesión: {user_email}")
    else:
        st.warning("⚠️ Ingresa tu correo para desbloquear el menú.")

# --- FUNCIONES TÉCNICAS (GENERADOR DE CRUCES) ---
def generar_fixture_simple(nombres_equipos, n_jornadas):
    if len(nombres_equipos) < 2: return []
    fixture = []
    # Genera n jornadas simples (mezclando equipos)
    for i in range(n_jornadas):
        random.shuffle(nombres_equipos)
        partidos = []
        copia_lista = nombres_equipos.copy()
        while len(copia_lista) > 1:
            partidos.append(f"{copia_lista.pop(0)} vs {copia_lista.pop(0)}")
        fixture.append(partidos)
    return fixture

# --- CONTENIDO PRINCIPAL (Visible solo si hay email) ---
if user_email:
    # ---------------------------------------------------------
    # SECCIÓN 1: ESTADO DE LAS COMPETICIONES
    # ---------------------------------------------------------
    if rol == "🏆 Competiciones y Cruces":
        st.title("🏆 Competiciones y Cruces")
        
        cat = st.radio("Ver Categoría:", ["Ligas Regulares", "Torneos Relámpago"], horizontal=True)
        opciones_torneo = st.session_state['ligas'] if cat == "Ligas Regulares" else st.session_state['relampagos']
        torneo_seleccionado = st.selectbox(f"Selecciona {cat}:", opciones_torneo)
        
        tab_list, tab_cross = st.tabs(["📊 Equipos", "📅 Cruces (Calendario)"])
        
        with tab_list:
            equipos_filtro = [e for e in st.session_state['equipos_db'] if e["Torneo"] == torneo_seleccionado]
            if equipos_filtro:
                df = pd.DataFrame(equipos_filtro)
                st.write(f"### Equipos en {torneo_seleccionado}")
                st.table(df[["Nombre", "WhatsApp"]])
            else:
                st.info("Aún no hay equipos inscritos aquí.")
                
        with tab_cross:
            if torneo_seleccionado in st.session_state['calendarios']:
                fixture_gen = st.session_state['calendarios'][torneo_seleccionado]
                for idx, jornada in enumerate(fixture_gen):
                    with st.expander(f"⚽ Jornada {idx + 1}"):
                        for partido in jornada: st.write(f"- {partido}")
            else:
                st.warning("El Admin aún no ha generado los cruces para este torneo.")

    # ---------------------------------------------------------
    # SECCIÓN 2: REPORTE POR IA (SOLO FOTO) - ¡NUEVA MEJORA!
    # ---------------------------------------------------------
    elif rol == "📋 Reporte IA (DTs)":
        st.title("📋 Reporte IA (Solamente Foto)")
        st.write("Bienvenido DT. Para reportar, solamente sube la foto final del partido. Nuestra IA leerá los resultados automáticamente.")
        
        # Obtenemos los torneos disponibles
        todos_los_torneos = st.session_state['ligas'] + st.session_state['relampagos']
        torneo_reporte = st.selectbox("1. Selecciona el Torneo", todos_los_torneos)
        
        st.write("---")
        st.write("### 2. Sube la Evidencia (Foto)")
        foto_subida = st.file_uploader("Sube la captura de pantalla del final (PNG/JPG)", type=["png", "jpg", "jpeg"])
        
        # Botón de envío FUERA del file_uploader para corregir el error de la imagen
        if foto_subida:
            # Mostramos la imagen que subió
            image = Image.open(foto_subida)
            st.image(image, caption="Imagen Subida", use_column_width=True)
            
            # --- FUNCIÓN DE IA (Simulación) ---
            if st.button("Enviar y Analizar con IA"):
                st.balloons()
                st.success("¡Imagen subida y analizada!")
                
                # --- AQUÍ CONECTARÍAS LA API DE OPENAI (VISION) ---
                # Como es una demo sin API Key de pago, simulamos el resultado.
                # En un entorno real, la IA leería el texto de la foto.
                resultado_leido_ia = "Freddy FC 3 - 1 Wallles Elite" # Simulación
                
                # Guardamos el reporte en la memoria
                st.session_state['reportes_ia'].append({
                    "DT": user_email,
                    "Torneo": torneo_reporte,
                    "Partido": resultado_leido_ia,
                    "Evidencia": foto_subida
                })
                
                # Mostramos lo que "leyó" la IA
                st.divider()
                st.subheader("🤖 Lo que leyó la IA:")
                st.write(f"Resultado Detectado: **{resultado_leido_ia}**")
                st.warning("El Administrador debe validar este reporte para confirmar el resultado.")

    # ---------------------------------------------------------
    # SECCIÓN 3: INSCRIPCIÓN (INTERFAZ LIMPIA)
    # ---------------------------------------------------------
    elif rol == " Inscribir Equipo":
        st.title("Inscribir Equipo")
        
        tipo_t = st.radio("Tipo de Competencia:", ["Liga Regular", "Relámpago"], horizontal=True)
        opciones_t = st.session_state['ligas'] if tipo_t == "Liga Regular" else st.session_state['relampagos']
        
        # Formulario de inscripción (Corregido: Submit Button)
        with st.form("registro_eq_v3"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                nom_club = st.text_input("Nombre del Club / Equipo")
                wa_num = st.text_input("WhatsApp")
            with col_f2:
                id_ea = st.text_input("EA ID del DT (Opcional)")
                logo_club = st.file_uploader("Subir Logo (Opcional)", type=["png", "jpg"])
            
            # Torneo de destino
            torneo_final = st.selectbox("Confirmar Torneo Específico", opciones_t)
            
            submit_reg = st.form_submit_button("Confirmar Inscripción")
            
            if submit_reg:
                if nom_club and wa_num:
                    st.session_state['equipos_db'].append({
                        "Nombre": nom_club, 
                        "WhatsApp": wa_num, 
                        "EA ID": id_ea,
                        "Torneo": torneo_final, 
                        "Categoría": tipo_t
                    })
                    st.balloons()
                    st.success(f"¡El club '{nom_club}' ha sido registrado en {torneo_final}!")
                else:
                    st.error("⚠️ El Nombre del Equipo y WhatsApp son obligatorios.")

    # ---------------------------------------------------------
    # SECCIÓN 4: PANEL DE ADMINISTRADOR (CONTROL TOTAL)
    # ---------------------------------------------------------
    elif rol == "⚙️ Administración":
        st.title("⚙️ Administración")
        
        if st.text_input("Introduce el Código Maestro:", type="password") == "Sirius2026":
            st.success("Acceso Autorizado.")
            
            t_admin1, t_admin2, t_admin3 = st.tabs(["Gestión de Equipos", "⚡ Generar Cruces", "🤖 Validar IA"])
            
            # --- TABS DE ADMIN 1: GESTIÓN EQUIPOS (CORREGIDO) ---
            with t_admin1:
                st.subheader("🛠️ Editar / Eliminar Equipos Inscritos")
                
                if st.session_state['equipos_db']:
                    df_gest = pd.DataFrame(st.session_state['equipos_db'])
                    st.write("### Equipos Registrados (Total)")
                    st.dataframe(df_gest[["Nombre", "Torneo", "WhatsApp"]]) # Ver todo
                    
                    st.write("---")
                    # Lógica para seleccionar y eliminar (CORREGIDO: ELIMINACIÓN ÚNICA)
                    nombres_eqs_admin = [e["Nombre"] for e in st.session_state['equipos_db']]
                    eq_eliminar_admin = st.selectbox("Selecciona equipo para ELIMINAR:", nombres_eqs_admin)
                    
                    if st.button("🗑️ Eliminar ÚNicamente Equipo Seleccionado"):
                        # Corrección aquí: Filtramos para dejar FUERA solo el que seleccionaste
                        st.session_state['equipos_db'] = [e for e in st.session_state['equipos_db'] if e["Nombre"] != eq_eliminar_admin]
                        st.success(f"El equipo '{eq_eliminar_admin}' ha sido eliminado.")
                        st.rerun() # Refresca para mostrar la tabla actualizada
                else:
                    st.info("No hay equipos para gestionar.")

            # --- TABS DE ADMIN 2: GENERAR CRUCES ---
            with t_admin2:
                st.subheader("⚡ Publicar Calendarios de Torneo")
                
                st.write("### ➕ Crear Ligas/Relámpagos")
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    nueva_liga = st.text_input("Nueva Liga")
                    if st.button("Crear Liga"):
                        if nueva_liga: st.session_state['ligas'].append(nueva_liga); st.rerun()
                with col_c2:
                    nuevo_rel = st.text_input("Nuevo Relámpago")
                    if st.button("Crear Relámpago"):
                        if nuevo_rel: st.session_state['relampagos'].append(nuevo_rel); st.rerun()
                
                st.write("---")
                st.write("### 🔒 Cerrar Inscripciones y Publicar Jornadas")
                # Lógica para personalizar jornadas por torneo
                todos_los_torneos_admin = st.session_state['ligas'] + st.session_state['relampagos']
                torneo_a_cerrar = st.selectbox("Torneo/Liga para generar fixture:", todos_los_torneos_admin)
                
                # MEJORA: Número de jornadas personalizable por el Admin
                n_jor = st.number_input("¿Cuántas jornadas quieres generar para este torneo?", min_value=1, max_value=30, value=3)
                
                if st.button("⚡ Publicar Fixture"):
                    # Filtramos equipos registrados en este torneo
                    equipos_t_admin = [e["Nombre"] for e in st.session_state['equipos_db'] if e["Torneo"] == torneo_a_cerrar]
                    
                    if len(equipos_t_admin) >= 2:
                        # Generamos los cruces
                        st.session_state['calendarios'][torneo_a_cerrar] = generar_fixture_simple(equipos_t_admin, int(n_jor))
                        st.balloons()
                        st.success(f"¡Cruces generados para {torneo_a_cerrar}! ({n_jor} jornadas publicadas).")
                    else:
                        st.error("⚠️ Necesitas al menos 2 equipos inscritos en este torneo.")

            # --- TABS DE ADMIN 3: VALIDAR IA ---
            with t_admin3:
                st.subheader("🤖 Validar Reportes de IA")
                st.write("Aquí aparecen los reportes que la IA leyó automáticamente. Revisa la foto para confirmar.")
                
                if st.session_state['reportes_ia']:
                    for idx, reporte in enumerate(st.session_state['reportes_ia']):
                        with st.expander(f"Reporte #{idx+1}: {reporte['Partido']} - {reporte['DT']} ({reporte['Torneo']})"):
                            
                            col_ev1, col_ev2 = st.columns([2, 1])
                            with col_ev1:
                                image_ev = Image.open(reporte['Evidencia'])
                                st.image(image_ev, caption="Evidencia del partido", use_column_width=True)
                            with col_ev2:
                                st.write("**Detalles:**")
                                st.write(f"- Torneo: {reporte['Torneo']}")
                                st.write(f"- Reportado por: {reporte['DT']}")
                                
                                # Botones de acción para el admin
                                c_bot1, c_bot2 = st.columns(2)
                                if c_bot1.button(f"✅ Aceptar Resultado", key=f"acc_{idx}"):
                                    st.success("Resultado Aceptado. (Aquí integrarías la actualización de tabla)").
                                    st.session_state['reportes_ia'].pop(idx) # Borramos el reporte
                                    st.rerun()
                                if c_bot2.button(f"🗑️ Descartar", key=f"desc_{idx}"):
                                    st.session_state['reportes_ia'].pop(idx) # Borramos el reporte
                                    st.rerun()
                else:
                    st.info("No hay reportes de IA pendientes.")
        elif pass_input != "":
            st.error("Código incorrecto.")

# Pie de página
st.sidebar.divider()
st.sidebar.caption("v3.0 - Walllesglint72 System")
