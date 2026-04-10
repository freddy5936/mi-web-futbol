import streamlit as st
import pandas as pd
import random
import time

# 1. CONFIGURACIÓN Y DATOS
st.set_page_config(page_title="Sirius Community PRO", layout="centered")

if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {"admin@sirius.com": "Sirius2026"} 
if 'usuario_logueado' not in st.session_state:
    st.session_state['usuario_logueado'] = None
if 'view' not in st.session_state:
    st.session_state['view'] = 'login' # Controla qué formulario ver

# 2. ESTILO CSS MEJORADO
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    h1, h2 { color: #00ffcc !important; text-align: center; font-family: 'Arial Black'; }
    .stButton>button { background-color: #00ffcc !important; color: #0b0e14 !important; font-weight: bold; border-radius: 8px; }
    .link-button { background: none; border: none; color: #00ffcc; text-decoration: underline; cursor: pointer; font-size: 14px; }
    .css-10trblm { color: white; } /* Color de etiquetas */
    </style>
    """, unsafe_allow_html=True)

# 3. FUNCIONES DE LÓGICA
def cambiar_vista(nombre_vista):
    st.session_state['view'] = nombre_vista
    st.rerun()

# 4. INTERFAZ DE ACCESO
if st.session_state['usuario_logueado'] is None:
    st.title("⚽ SIRIUS COMMUNITY")

    # --- VISTA: LOGIN ---
    if st.session_state['view'] == 'login':
        st.subheader("Iniciar Sesión")
        u_login = st.text_input("Correo electrónico")
        p_login = st.text_input("Contraseña", type="password")
        
        if st.button("ENTRAR"):
            if u_login in st.session_state['usuarios'] and st.session_state['usuarios'][u_login] == p_login:
                st.session_state['usuario_logueado'] = u_login
                st.rerun()
            else:
                st.error("Correo o contraseña incorrectos.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("¿No tienes cuenta? Crea una aquí", key="btn_reg_link"):
                cambiar_vista('registro')
        with col2:
            if st.button("Olvidé mi contraseña", key="btn_olvido"):
                cambiar_vista('recuperar')

    # --- VISTA: REGISTRO ---
    elif st.session_state['view'] == 'registro':
        st.subheader("Crear Nueva Cuenta")
        u_reg = st.text_input("Nuevo Correo")
        p_reg = st.text_input("Contraseña")
        p_conf = st.text_input("Confirmar Contraseña", type="password")
        
        if st.button("REGISTRARME"):
            if u_reg in st.session_state['usuarios']:
                st.error("Este correo ya tiene cuenta.")
            elif p_reg != p_conf:
                st.error("Las contraseñas no coinciden.")
            elif u_reg and p_reg:
                st.session_state['usuarios'][u_reg] = p_reg
                st.success("¡Cuenta creada! Ya puedes iniciar sesión.")
                time.sleep(1)
                cambiar_vista('login')
        
        if st.button("Volver al Login"):
            cambiar_vista('login')

    # --- VISTA: RECUPERAR CONTRASEÑA ---
    elif st.session_state['view'] == 'recuperar':
        st.subheader("Recuperar Acceso")
        u_rec = st.text_input("Introduce tu correo para recibir el código")
        
        if "codigo_verificacion" not in st.session_state:
            if st.button("Enviar Código"):
                if u_rec in st.session_state['usuarios']:
                    # Simulamos envío de correo
                    st.session_state['codigo_verificacion'] = str(random.randint(1000, 9999))
                    st.info(f"CÓDIGO ENVIADO A {u_rec}: {st.session_state['codigo_verificacion']}") # Simulación
                else:
                    st.error("Ese correo no está registrado.")
        else:
            cod_ingresado = st.text_input("Introduce el código de 4 dígitos")
            nueva_pass = st.text_input("Nueva Contraseña", type="password")
            
            if st.button("Cambiar Contraseña"):
                if cod_ingresado == st.session_state['codigo_verificacion']:
                    st.session_state['usuarios'][u_rec] = nueva_pass
                    st.success("Contraseña actualizada con éxito.")
                    del st.session_state['codigo_verificacion']
                    time.sleep(1)
                    cambiar_vista('login')
                else:
                    st.error("Código incorrecto.")
        
        if st.button("Cancelar"):
            if "codigo_verificacion" in st.session_state: del st.session_state['codigo_verificacion']
            cambiar_vista('login')

# 5. PANEL DE CONTROL (CUANDO YA ENTRÓ)
else:
    st.sidebar.success(f"Sesión activa: {st.session_state['usuario_logueado']}")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state['usuario_logueado'] = None
        st.rerun()
    
    st.title(f"Bienvenido a Sirius, {st.session_state['usuario_logueado']}")
    st.write("Aquí va el resto de tu contenido (Noticias, Inscripciones, etc.)")
