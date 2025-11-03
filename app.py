import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import random
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText  # CORREGIDO

# =============================================================================
# CONFIGURACIÓN INICIAL
# =============================================================================
st.set_page_config(page_title="Huancayo Safety App", page_icon="🛡️", layout="centered")

# Configuración Gmail para alertas reales
GMAIL_USER = "edwarrojasccasa@gmail.com"
GMAIL_PASSWORD = "tu_password_app"  # Cambiar por contraseña de aplicación Gmail

# =============================================================================
# FUNCIÓN PARA ENVÍO REAL DE ALERTAS - CORREGIDA
# =============================================================================
def enviar_alerta_real(destinatario, ubicacion, nombre_usuario, info_medica=""):
    """
    Envía alerta REAL por email - Configurado para Edwar
    """
    try:
        mensaje = f"""🚨 ALERTA DE EMERGENCIA - Huancayo Safety App 🚨

👤 {nombre_usuario} necesita ayuda URGENTE
📍 Ubicación: {ubicacion}
⏰ Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
🩸 Información médica: {info_medica}

🔗 Ver ubicación en Google Maps:
https://maps.google.com/?q={ubicacion}

🆘 POR FAVOR:
1. Contacta a {nombre_usuario} inmediatamente
2. Si no responde, alerta a las autoridades
3. Comparte esta ubicación con servicios de emergencia

📱 Esta alerta fue generada automáticamente por la Huancayo Safety App"""

        msg = MIMEText(mensaje)  # CORREGIDO
        msg['Subject'] = '🚨 ALERTA DE EMERGENCIA - Ayuda Urgente'
        msg['From'] = GMAIL_USER
        msg['To'] = destinatario
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, "✅ Alerta enviada exitosamente"
        
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# =============================================================================
# DATOS DE SIMULACIÓN
# =============================================================================
danger_points = [
    (-12.065, -75.210, 'Alta', 'Robo'),
    (-12.067, -75.212, 'Media', 'Acoso'),
]

safe_locations = [
    (-12.065, -75.211, 'Farmacia Segura', '24/7'),
    (-12.066, -75.213, 'Restaurante Refugio', '6 AM - 11 PM'),
]

# =============================================================================
# ESTILOS CSS
# =============================================================================
st.markdown("""
<style>
    .stApp {
        max-width: 380px; 
        margin: auto; 
        border: 16px solid #333; 
        border-radius: 40px; 
        padding: 10px;
        background: #f0f2f6;
    }
    .emergency-button {
        background: linear-gradient(45deg, #FF416C, #FF4B2B);
        color: white;
        border: none;
        padding: 40px 20px;
        border-radius: 25px;
        font-size: 28px;
        font-weight: bold;
        margin: 20px 0;
        width: 100%;
        height: 150px;
        box-shadow: 0 10px 30px rgba(255, 65, 108, 0.6);
    }
    .countdown-alert {
        background: linear-gradient(45deg, #ff9966, #ff5e62);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    .success-alert {
        background: linear-gradient(45deg, #00b09b, #96c93d);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# ESTADO DE LA APLICACIÓN
# =============================================================================
if 'panic_active' not in st.session_state:
    st.session_state.panic_active = False
if 'panic_countdown' not in st.session_state:
    st.session_state.panic_countdown = 3
if 'user_location' not in st.session_state:
    st.session_state.user_location = (-12.065, -75.210)
if 'alert_sent' not in st.session_state:
    st.session_state.alert_sent = False

# =============================================================================
# BARRA DE NAVEGACIÓN SIMPLIFICADA
# =============================================================================
menu_options = ["🏠 Inicio", "🗺️ Mapa", "🚨 BOTÓN DE PÁNICO"]
page = st.sidebar.radio("NAVEGACIÓN", menu_options)

# =============================================================================
# PÁGINA DE INICIO
# =============================================================================
if page == "🏠 Inicio":
    st.title("🛡️ HUANCAYO SAFETY APP")
    st.markdown("---")
    
    st.success("✅ **Botón de pánico con cuenta regresiva de 3 segundos**")
    st.success("✅ **Mapa de calor con zonas de riesgo**") 
    st.success("✅ **Envío REAL de alertas por email**")
    
    st.info("""
    **📱 Cómo usar:**
    1. Ve a **BOTÓN DE PÁNICO**
    2. Configura tu email de emergencia  
    3. Presiona el botón rojo en caso de peligro
    4. La alerta se enviará automáticamente
    """)

# =============================================================================
# MAPA EN TIEMPO REAL
# =============================================================================
elif page == "🗺️ Mapa":
    st.subheader("🗺️ MAPA DE SEGURIDAD")
    
    user_lat, user_lon = st.session_state.user_location
    
    m = folium.Map(location=[user_lat, user_lon], zoom_start=16)
    
    # Heatmap
    heat_data = [(lat, lon) for lat, lon, _, _ in danger_points]
    heat_data.append([user_lat, user_lon])
    HeatMap(heat_data, radius=25).add_to(m)
    
    # Marcador del usuario
    folium.Marker(
        [user_lat, user_lon],
        popup="📍 TÚ ESTÁS AQUÍ",
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)
    
    # Zonas de peligro
    for lat, lon, nivel, tipo in danger_points:
        color = "red" if nivel == "Alta" else "orange"
        folium.CircleMarker(
            [lat, lon],
            radius=10,
            popup=f"⚠️ {tipo}",
            color=color,
            fill=True
        ).add_to(m)
    
    st_folium(m, width=350, height=400)

# =============================================================================
# BOTÓN DE PÁNICO - FUNCIONAL
# =============================================================================
elif page == "🚨 BOTÓN DE PÁNICO":
    st.title("🚨 BOTÓN DE EMERGENCIA")
    st.markdown("---")
    
    # Configuración
    contacto_emergencia = st.text_input("📧 Email de emergencia", "edwarrojasccasa@gmail.com")
    nombre_usuario = st.text_input("👤 Tu nombre", "Edwar")
    
    st.markdown("### 🔴 BOTÓN ROJO - PRESIONAR EN CASO DE PELIGRO")
    
    # BOTÓN ROJO GIGANTE
    if not st.session_state.panic_active and not st.session_state.alert_sent:
        if st.button(
            "🔴\n\n🚨 EMERGENCIA 🚨\n\nPRESIONAR PARA ACTIVAR\n\n🔴", 
            use_container_width=True,
            key="panic_btn"
        ):
            st.session_state.panic_active = True
            st.session_state.panic_countdown = 3
            st.rerun()
    
    # CUENTA REGRESIVA
    elif st.session_state.panic_active and st.session_state.panic_countdown > 0:
        st.error(f"⏰ **ALERTA SE ACTIVARÁ EN {st.session_state.panic_countdown}**")
        
        if st.button("❌ CANCELAR", use_container_width=True):
            st.session_state.panic_active = False
            st.success("Alerta cancelada")
            st.rerun()
        
        st.session_state.panic_countdown -= 1
        time.sleep(1)
        st.rerun()
    
    # ENVÍO REAL DE ALERTA
    elif st.session_state.panic_active and st.session_state.panic_countdown == 0:
        st.error("🚨 ¡ENVIANDO ALERTA!")
        
        user_lat, user_lon = st.session_state.user_location
        ubicacion = f"{user_lat:.5f}, {user_lon:.5f}"
        
        # ENVÍO REAL
        with st.spinner("📤 Enviando alerta..."):
            exito, mensaje = enviar_alerta_real(
                destinatario=contacto_emergencia,
                ubicacion=ubicacion,
                nombre_usuario=nombre_usuario
            )
        
        if exito:
            st.session_state.alert_sent = True
            st.balloons()
            st.success(f"""
            ✅ **ALERTA ENVIADA**
            
            **📧 A:** {contacto_emergencia}
            **📍 Ubicación:** {ubicacion}
            **👤 Persona:** {nombre_usuario}
            
            **El email llegará en segundos**
            """)
        else:
            st.error(f"❌ Error: {mensaje}")
        
        if st.button("🔄 PROBAR DE NUEVO", use_container_width=True):
            st.session_state.panic_active = False
            st.session_state.alert_sent = False
            st.rerun()

# =============================================================================
# INFORMACIÓN EN SIDEBAR
# =============================================================================
st.sidebar.markdown("---")
st.sidebar.info("App Seguridad Huancayo - Prototipo Funcional")
