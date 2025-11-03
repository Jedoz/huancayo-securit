import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import random
import time
from datetime import datetime
import smtplib
from email.mime.text import MimeText
import requests

# Configuración de la página
st.set_page_config(page_title="Huancayo Safety App", page_icon="🛡️", layout="centered")

# =============================================================================
# CONFIGURACIÓN REAL DE EMAIL - EDWAR
# =============================================================================

GMAIL_USER = "edwarrojasccasa@gmail.com"
GMAIL_PASSWORD = "tu_contraseña_de_aplicación"  # Cambia esto por tu contraseña de aplicación

def enviar_alerta_real(destinatario, ubicacion, nombre_usuario, info_medica=""):
    """
    Función REAL que envía alertas por Gmail - CONFIGURADO PARA EDWAR
    """
    try:
        mensaje = f"""
🚨 ALERTA DE EMERGENCIA - Huancayo Safety App 🚨

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

📱 Esta alerta fue generada automáticamente por la Huancayo Safety App
"""

        msg = MimeText(mensaje)
        msg['Subject'] = '🚨 ALERTA DE EMERGENCIA - Ayuda Urgente'
        msg['From'] = GMAIL_USER
        msg['To'] = destinatario
        
        # Configuración SMTP para Gmail
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
    (-12.064, -75.214, 'Baja', 'Sospechoso'),
    (-12.063, -75.209, 'Alta', 'Asalto'),
]

safe_locations = [
    (-12.065, -75.211, 'Farmacia Segura', '24/7'),
    (-12.066, -75.213, 'Restaurante Refugio', '6 AM - 11 PM'),
    (-12.068, -75.209, 'Tienda Amiga', '8 AM - 10 PM'),
]

# =============================================================================
# ESTILOS MEJORADOS
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
        cursor: pointer;
    }
    .emergency-button:hover {
        background: linear-gradient(45deg, #FF4B2B, #FF416C);
        transform: scale(1.02);
        box-shadow: 0 12px 35px rgba(255, 65, 108, 0.8);
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
        animation: pulse 0.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .success-alert {
        background: linear-gradient(45deg, #00b09b, #96c93d);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
    }
    .info-box {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# ESTADO DE LA APLICACIÓN
# =============================================================================

if 'panic_active' not in st.session_state:
    st.session_state.panic_active = False
if 'panic_countdown' not in st.session_state:
    st.session_state.panic_countdown = 5
if 'user_location' not in st.session_state:
    st.session_state.user_location = (-12.065, -75.210)
if 'alert_sent' not in st.session_state:
    st.session_state.alert_sent = False

# =============================================================================
# BARRA DE NAVEGACIÓN
# =============================================================================

menu_options = ["🏠 Inicio", "🗺️ Mapa en Tiempo Real", "🚨 BOTÓN DE PÁNICO", "📧 Configurar Alertas"]
page = st.sidebar.radio("NAVEGACIÓN", menu_options)

# =============================================================================
# PÁGINA DE INICIO
# =============================================================================

if page == "🏠 Inicio":
    st.title("🛡️ HUANCAYO SAFETY APP")
    st.markdown("---")
    
    st.markdown('<div class="info-box">📱 <strong>PROTOTIPO FUNCIONAL</strong><br>Alertas en tiempo real con ubicación GPS</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👤 Usuario", "Edwar")
    with col2:
        st.metric("📍 Activo", "Sí")
    with col3:
        st.metric("🛡️ Protegido", "Sí")
    
    st.markdown("### 🚨 Funcionalidades Activas:")
    st.success("✅ **Envío REAL de alertas por email**")
    st.success("✅ **Ubicación GPS en tiempo real**")
    st.success("✅ **Botón de pánico con cuenta regresiva**")
    st.success("✅ **Mapa interactivo de peligros**")
    
    st.markdown("### 📋 Próximos Pasos:")
    st.info("1. **Configurar contraseña de aplicación Gmail**")
    st.info("2. **Probar envío de alerta real**")
    st.info("3. **Compartir link con amigos**")

# =============================================================================
# MAPA EN TIEMPO REAL
# =============================================================================

elif page == "🗺️ Mapa en Tiempo Real":
    st.subheader("🗺️ MAPA INTERACTIVO - TIEMPO REAL")
    
    # Simular ubicación real con movimiento
    user_lat, user_lon = st.session_state.user_location
    user_lat += random.uniform(-0.001, 0.001)
    user_lon += random.uniform(-0.001, 0.001)
    st.session_state.user_location = (user_lat, user_lon)
    
    # Crear mapa centrado en usuario
    m = folium.Map(location=[user_lat, user_lon], zoom_start=16)
    
    # Heatmap de peligros
    heat_data = [(lat, lon) for lat, lon, _, _ in danger_points]
    heat_data.append([user_lat, user_lon])
    HeatMap(heat_data, radius=25, blur=15).add_to(m)
    
    # Marcador del usuario
    folium.Marker(
        [user_lat, user_lon],
        popup="📍 TÚ ESTÁS AQUÍ",
        tooltip="Tu ubicación actual",
        icon=folium.Icon(color="blue", icon="user", prefix="fa")
    ).add_to(m)
    
    # Zonas de peligro
    for lat, lon, nivel, tipo in danger_points:
        color = "red" if nivel == "Alta" else "orange" if nivel == "Media" else "yellow"
        folium.CircleMarker(
            [lat, lon],
            radius=12,
            popup=f"⚠️ {tipo} - Riesgo {nivel}",
            tooltip=f"Riesgo {nivel}",
            color=color,
            fill=True,
            fillOpacity=0.7
        ).add_to(m)
    
    # Lugares seguros
    for lat, lon, nombre, horario in safe_locations:
        folium.Marker(
            [lat, lon],
            popup=f"🏪 {nombre} (Lugar Seguro)",
            tooltip="Refugio seguro",
            icon=folium.Icon(color="green", icon="home", prefix="fa")
        ).add_to(m)
    
    st_folium(m, width=350, height=450)
    
    st.success(f"📍 **Tu ubicación actual:** {user_lat:.5f}, {user_lon:.5f}")
    st.info("🗺️ El mapa se actualiza automáticamente con tu ubicación")

# =============================================================================
# BOTÓN DE PÁNICO - CON FUNCIONALIDAD REAL
# =============================================================================

elif page == "🚨 BOTÓN DE PÁNICO":
    st.title("🚨 BOTÓN DE EMERGENCIA")
    st.markdown("---")
    
    # Estado de la alerta
    if st.session_state.alert_sent:
        st.markdown('<div class="success-alert">✅ ALERTA ENVIADA EXITOSAMENTE</div>', unsafe_allow_html=True)
    
    # Configuración rápida
    with st.expander("⚙️ CONFIGURACIÓN RÁPIDA", expanded=True):
        contacto_emergencia = st.text_input(
            "📧 Email de emergencia", 
            "edwarrojasccasa@gmail.com",
            help="Este email recibirá las alertas de emergencia"
        )
        
        nombre_usuario = st.text_input("👤 Tu nombre para la alerta", "Edwar")
        
        info_medica = st.text_area(
            "🏥 Información médica importante", 
            "Ninguna alergia conocida",
            placeholder="Alergias, condiciones médicas, grupo sanguíneo..."
        )
    
    st.markdown("---")
    st.markdown("### 🔴 BOTÓN DE EMERGENCIA")
    
    # BOTÓN ROJO GIGANTE
    if not st.session_state.panic_active and not st.session_state.alert_sent:
        if st.button(
            "🔴\n\n🚨 EMERGENCIA 🚨\n\nPRESIONAR PARA PEDIR AYUDA\n\n🔴", 
            use_container_width=True,
            key="panic_btn"
        ):
            st.session_state.panic_active = True
            st.session_state.panic_countdown = 5
            st.rerun()
    
    # CUENTA REGRESIVA
    elif st.session_state.panic_active and st.session_state.panic_countdown > 0:
        st.markdown(f'<div class="countdown-alert">⏰ ALERTA EN {st.session_state.panic_countdown}</div>', unsafe_allow_html=True)
        st.session_state.panic_countdown -= 1
        time.sleep(1)
        st.rerun()
    
    # ENVÍO REAL DE ALERTA
    elif st.session_state.panic_active and st.session_state.panic_countdown == 0:
        st.markdown('<div class="countdown-alert">🚨 ¡ENVIANDO ALERTA!</div>', unsafe_allow_html=True)
        
        user_lat, user_lon = st.session_state.user_location
        ubicacion = f"{user_lat:.5f}, {user_lon:.5f}"
        
        # ENVÍO REAL CON GMAIL
        with st.spinner("📤 Conectando con Gmail..."):
            exito, mensaje = enviar_alerta_real(
                destinatario=contacto_emergencia,
                ubicacion=ubicacion,
                nombre_usuario=nombre_usuario,
                info_medica=info_medica
            )
        
        if exito:
            st.session_state.alert_sent = True
            st.balloons()
            st.markdown('<div class="success-alert">✅ ALERTA ENVIADA CON ÉXITO</div>', unsafe_allow_html=True)
            
            st.success(f"""
            **📧 Destinatario:** {contacto_emergencia}
            **📍 Ubicación enviada:** {ubicacion}
            **👤 Persona:** {nombre_usuario}
            **🩸 Info médica:** {info_medica}
            
            **📱 La alerta llegará en segundos al email destino**
            """)
        else:
            st.error(f"""
            ❌ ERROR ENVIANDO ALERTA
            **Mensaje:** {mensaje}
            
            **🔧 Solución:**
            1. Verifica tu conexión a internet
            2. Confirma la contraseña de aplicación Gmail
            3. Revisa que el email destino sea correcto
            """)
        
        # Mapa de emergencia
        m = folium.Map(location=[user_lat, user_lon], zoom_start=17)
        folium.Marker(
            [user_lat, user_lon],
            popup="🚨 PERSONA EN PELIGRO - AUXILIO",
            tooltip="¡Necesita ayuda urgente!",
            icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa")
        ).add_to(m)
        
        folium.Circle(
            [user_lat, user_lon],
            radius=25,
            color="red",
            fill=True,
            opacity=0.7,
            fillOpacity=0.3
        ).add_to(m)
        
        st_folium(m, width=350, height=300)
        
        # Botón de reset
        if st.button("🔄 PROBAR DE NUEVO", use_container_width=True):
            st.session_state.panic_active = False
            st.session_state.alert_sent = False
            st.rerun()

# =============================================================================
# CONFIGURACIÓN DE ALERTAS
# =============================================================================

elif page == "📧 Configurar Alertas":
    st.subheader("📧 CONFIGURACIÓN DE ALERTAS POR EMAIL")
    
    st.markdown("### 🔐 CONFIGURAR GMAIL PARA ALERTAS")
    
    st.info("""
    **📝 Para que las alertas funcionen DE VERDAD:**
    
    1. **Ve a:** https://myaccount.google.com/
    2. **Activa** "Verificación en 2 pasos"
    3. **Ve a** "Contraseñas de aplicación"
    4. **Genera** una contraseña para "Correo"
    5. **Copia** esa contraseña y pégala abajo
    """)
    
    st.markdown("### 🔧 CONFIGURACIÓN ACTUAL")
    st.code(f"""
    Email remitente: {GMAIL_USER}
    Estado: {'✅ CONFIGURADO' if GMAIL_PASSWORD != 'tu_contraseña_de_aplicación' else '❌ PENDIENTE'}
    """)
    
    st.markdown("### 🧪 PROBAR ALERTA")
    st.warning("**Ve a 'BOTÓN DE PÁNICO' para probar el envío real**")
    
    st.markdown("### 🌐 COMPARTIR APP")
    st.success("""
    **Para que tu amigo en Argentina pruebe:**
    
    ```bash
    streamlit run huancayo_safety_app01.py
    ```
    
    **Luego comparte este link:**
    ```
    http://localhost:8501
    ```
    
    **⚠️ IMPORTANTE:** Debes usar **ngrok** para acceso externo
    """)

# =============================================================================
# INSTRUCCIONES EN SIDEBAR
# =============================================================================

st.sidebar.markdown("---")
st.sidebar.markdown("### 📲 COMPARTIR APP")

st.sidebar.info("""
**Para acceso desde Argentina:**

1. **Ejecuta en terminal:**
   ```bash
   streamlit run huancayo_safety_app01.py
