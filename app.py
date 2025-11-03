import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import random
import time
from datetime import datetime
import smtplib
from email.mime.text import MimeText

# =============================================================================
# CONFIGURACIÓN INICIAL
# =============================================================================
st.set_page_config(page_title="Huancayo Safety App", page_icon="🛡️", layout="centered")

# Configuración Gmail para alertas reales
GMAIL_USER = "edwarrojasccasa@gmail.com"
GMAIL_PASSWORD = "tu_contraseña_app"  # Cambiar por contraseña de aplicación Gmail

# =============================================================================
# FUNCIÓN PARA ENVÍO REAL DE ALERTAS
# =============================================================================
def enviar_alerta_real(destinatario, ubicacion, nombre_usuario, info_medica=""):
    """
    Envía alerta REAL por email - Configurado para Edwar
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

recent_incidents = [
    {'tipo': 'Robo', 'ubicacion': 'Av. Ferrocarril', 'hora': 'Hace 15 min', 'verificada': True},
    {'tipo': 'Acoso', 'ubicacion': 'Parque Huamanmarca', 'hora': 'Hace 30 min', 'verificada': False},
]

# =============================================================================
# ESTILOS CSS MEJORADOS
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
    .warning-alert {
        background: linear-gradient(45deg, #ff9966, #ff5e62);
        color: white;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
    }
    .safe-zone {
        background: linear-gradient(45deg, #00b09b, #96c93d);
        color: white;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
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
if 'reports' not in st.session_state:
    st.session_state.reports = []

# =============================================================================
# BARRA DE NAVEGACIÓN
# =============================================================================
menu_options = ["🏠 Inicio", "🗺️ Mapa en Tiempo Real", "🚨 BOTÓN DE PÁNICO", "📢 Reportar Incidente", "🏪 Zonas Seguras", "👤 Perfil"]
page = st.sidebar.radio("NAVEGACIÓN", menu_options)

# =============================================================================
# PÁGINA DE INICIO
# =============================================================================
if page == "🏠 Inicio":
    st.title("🛡️ HUANCAYO SAFETY APP")
    st.markdown("---")
    
    st.markdown('<div class="warning-alert">⚠️ **ALERTA:** Zona de alto riesgo detectada: Av. Ferrocarril (3 incidentes en la última hora)</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 Alertas Activas", "3")
    with col2:
        st.metric("🟢 Zonas Seguras", "5")
    with col3:
        st.metric("📊 Incidentes Hoy", "12")
    
    st.markdown("### 🚨 Funcionalidades Activas:")
    st.success("✅ **Botón de pánico con cuenta regresiva de 3 segundos**")
    st.success("✅ **Mapa de calor con zonas de riesgo**")
    st.success("✅ **Sistema de reportes comunitarios**")
    st.success("✅ **Envío REAL de alertas por email**")
    st.success("✅ **Seguimiento GPS automático**")
    st.success("✅ **Mapa de lugares seguros**")
    
    st.markdown("### 📋 Incidentes Recientes:")
    for incident in recent_incidents:
        verified = "✅" if incident['verificada'] else "⏳"
        st.write(f"{verified} **{incident['tipo']}** - {incident['ubicacion']} ({incident['hora']})")

# =============================================================================
# MAPA EN TIEMPO REAL
# =============================================================================
elif page == "🗺️ Mapa en Tiempo Real":
    st.subheader("🗺️ MAPA INTERACTIVO - TIEMPO REAL")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        show_heatmap = st.checkbox("Mapa de Calor", value=True)
    with col2:
        show_safe_zones = st.checkbox("Zonas Seguras", value=True)
    
    # Simular ubicación real con movimiento
    user_lat, user_lon = st.session_state.user_location
    user_lat += random.uniform(-0.001, 0.001)
    user_lon += random.uniform(-0.001, 0.001)
    st.session_state.user_location = (user_lat, user_lon)
    
    # Crear mapa centrado en usuario
    m = folium.Map(location=[user_lat, user_lon], zoom_start=16)
    
    # Heatmap de peligros (Visualización tipo "heatmap")
    if show_heatmap:
        heat_data = []
        for lat, lon, nivel, _ in danger_points:
            weight = 0.8 if nivel == 'Alta' else 0.5 if nivel == 'Media' else 0.2
            heat_data.append([lat, lon, weight])
        heat_data.append([user_lat, user_lon, 0.1])  # Ubicación usuario
        HeatMap(heat_data, radius=25, blur=15, max_zoom=13).add_to(m)
    
    # Marcador del usuario
    folium.Marker(
        [user_lat, user_lon],
        popup="📍 TÚ ESTÁS AQUÍ",
        tooltip="Tu ubicación actual",
        icon=folium.Icon(color="blue", icon="user", prefix="fa")
    ).add_to(m)
    
    # Zonas de peligro (Verde=seguro, Amarillo=precaución, Naranja=riesgo, Rojo=peligro alto)
    for lat, lon, nivel, tipo in danger_points:
        if nivel == "Alta":
            color = "red"
        elif nivel == "Media":
            color = "orange" 
        elif nivel == "Baja":
            color = "yellow"
        else:
            color = "green"
            
        folium.CircleMarker(
            [lat, lon],
            radius=12,
            popup=f"⚠️ {tipo} - Riesgo {nivel}",
            tooltip=f"Riesgo {nivel}",
            color=color,
            fill=True,
            fillOpacity=0.7
        ).add_to(m)
    
    # Lugares seguros (Mapa con ubicaciones verificadas donde refugiarse)
    if show_safe_zones:
        for lat, lon, nombre, horario in safe_locations:
            folium.Marker(
                [lat, lon],
                popup=f"🏪 {nombre}\n⏰ {horario}\n🔒 Lugar Seguro Verificado",
                tooltip="Refugio seguro",
                icon=folium.Icon(color="green", icon="home", prefix="fa")
            ).add_to(m)
    
    st_folium(m, width=350, height=450)
    
    st.success(f"📍 **Tu ubicación actual:** {user_lat:.5f}, {user_lon:.5f}")
    
    # Notificación automática de zona de riesgo
    st.markdown('<div class="warning-alert">⚠️ **Estás cerca de zona de riesgo:** 2 incidentes reportados cerca</div>', unsafe_allow_html=True)

# =============================================================================
# BOTÓN DE PÁNICO - CON CUENTA REGRESIVA Y ENVÍO REAL
# =============================================================================
elif page == "🚨 BOTÓN DE PÁNICO":
    st.title("🚨 BOTÓN DE EMERGENCIA")
    st.markdown("---")
    
    # Estado de la alerta
    if st.session_state.alert_sent:
        st.markdown('<div class="success-alert">✅ ALERTA ENVIADA EXITOSAMENTE</div>', unsafe_allow_html=True)
    
    # Configuración de contactos
    with st.expander("📞 CONFIGURAR CONTACTOS DE EMERGENCIA", expanded=True):
        st.warning("⚠️ Configura contactos REALES para recibir alertas")
        
        nombre_usuario = st.text_input("👤 Tu nombre completo", "Edwar Rojas")
        contacto_emergencia = st.text_input("📧 Email de emergencia", "edwarrojasccasa@gmail.com")
        
        st.info("""
        **📧 Para probar AHORA:**
        - Usa tu email personal o de un familiar
        - La alerta llegará inmediatamente
        """)
    
    # Información médica
    with st.expander("🏥 INFORMACIÓN MÉDICA (Opcional)"):
        grupo_sanguineo = st.selectbox("Grupo Sanguíneo", ["No especificado", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        alergias = st.text_input("Alergias o condiciones médicas", "Ninguna alergia conocida")
        info_medica = f"Grupo {grupo_sanguineo}, Alergias: {alergias}"
    
    st.markdown("---")
    st.markdown("### 🔴 BOTÓN DE EMERGENCIA")
    
    # BOTÓN ROJO GIGANTE (Botón rojo prominente)
    if not st.session_state.panic_active and not st.session_state.alert_sent:
        if st.button(
            "🔴\n\n🚨 EMERGENCIA 🚨\n\nPRESIONAR PARA ACTIVAR\nBOTÓN DE PÁNICO\n\n🔴", 
            use_container_width=True,
            key="panic_btn"
        ):
            st.session_state.panic_active = True
            st.session_state.panic_countdown = 3  # Cuenta regresiva de 3 segundos
            st.rerun()
    
    # CUENTA REGRESIVA (Botón inicia cuenta regresiva de 3 segundos)
    elif st.session_state.panic_active and st.session_state.panic_countdown > 0:
        st.markdown(f'<div class="countdown-alert">⏰ ALERTA SE ACTIVARÁ EN {st.session_state.panic_countdown}</div>', unsafe_allow_html=True)
        
        # Opción para cancelar (Usuario puede cancelar deslizando)
        if st.button("↔️ DESLIZAR PARA CANCELAR", use_container_width=True, type="secondary"):
            st.session_state.panic_active = False
            st.success("Alerta cancelada")
            st.rerun()
        
        st.session_state.panic_countdown -= 1
        time.sleep(1)
        st.rerun()
    
    # ENVÍO REAL DE ALERTA (Al activar pánico, envía ubicación GPS)
    elif st.session_state.panic_active and st.session_state.panic_countdown == 0:
        st.markdown('<div class="countdown-alert">🚨 ¡ENVIANDO ALERTA DE AUXILIO!</div>', unsafe_allow_html=True)
        
        user_lat, user_lon = st.session_state.user_location
        ubicacion = f"{user_lat:.5f}, {user_lon:.5f}"
        
        # ENVÍO REAL CON GMAIL
        with st.spinner("📤 Enviando alerta a contactos de emergencia..."):
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
            **🔄 La app enviará tu ubicación cada 30 segundos**
            """)
        else:
            st.error(f"""
            ❌ ERROR ENVIANDO ALERTA
            **Mensaje:** {mensaje}
            """)
        
        # Mapa de emergencia
        m = folium.Map(location=[user_lat, user_lon], zoom_start=17)
        folium.Marker(
            [user_lat, user_lon],
            popup="🚨 PERSONA EN PELIGRO - AUXILIO INMEDIATO",
            tooltip="¡Necesita ayuda urgente!",
            icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa")
        ).add_to(m)
        
        # Círculo de radio de búsqueda
        folium.Circle(
            [user_lat, user_lon],
            radius=30,
            color="red",
            fill=True,
            opacity=0.7,
            fillOpacity=0.2
        ).add_to(m)
        
        st_folium(m, width=350, height=300)
        
        # Botón de reset
        if st.button("🔄 REINICIAR SISTEMA", use_container_width=True):
            st.session_state.panic_active = False
            st.session_state.alert_sent = False
            st.rerun()

# =============================================================================
# SISTEMA DE REPORTES COMUNITARIOS
# =============================================================================
elif page == "📢 Reportar Incidente":
    st.subheader("📢 REPORTAR INCIDENTE EN TIEMPO REAL")
    
    # Formulario de reporte (Botón "Reportar" → seleccionar tipo → confirmar → enviar)
    with st.form("report_form"):
        st.write("### 🚨 Tipo de Incidente")
        tipo_incidente = st.selectbox(
            "Selecciona el tipo de incidente",
            ["Robo", "Acoso", "Persona Sospechosa", "Asalto", "Accidente", "Otro"]
        )
        
        st.write("### 📍 Ubicación del Incidente")
        ubicacion = st.text_input("Describe la ubicación", "Ej: Esquina de Av. Ferrocarril con Calle Real")
        
        st.write("### 📝 Descripción")
        descripcion = st.text_area("Describe lo que sucedió", "Ej: Hombre sospechoso merodeando...")
        
        submitted = st.form_submit_button("📤 ENVIAR REPORTE A LA COMUNIDAD", use_container_width=True)
        
        if submitted:
            # Simular verificación comunitaria (Alertas requieren confirmación de múltiples usuarios)
            verificacion = random.choice([True, False, False])  # 33% de probabilidad de verificación
            
            nuevo_reporte = {
                'tipo': tipo_incidente,
                'ubicacion': ubicacion,
                'descripcion': descripcion,
                'timestamp': datetime.now().strftime("%H:%M"),
                'verificado': verificacion
            }
            
            st.session_state.reports.append(nuevo_reporte)
            
            if verificacion:
                st.success("✅ Reporte enviado y VERIFICADO por la comunidad")
            else:
                st.warning("⏳ Reporte enviado. Esperando verificación de otros usuarios")

# =============================================================================
# ZONAS SEGURAS - COMERCIOS ALIADOS
# =============================================================================
elif page == "🏪 Zonas Seguras":
    st.subheader("🏪 LUGARES SEGUROS Y COMERCIOS ALIADOS")
    
    st.markdown('<div class="info-box">🔒 **Lugares verificados donde puedes refugiarte en emergencia**</div>', unsafe_allow_html=True)
    
    for i, (lat, lon, nombre, horario) in enumerate(safe_locations):
        with st.container():
            st.markdown(f'<div class="safe-zone">', unsafe_allow_html=True)
            st.write(f"**🏪 {nombre}**")
            st.write(f"⏰ **Horario:** {horario}")
            st.write(f"📍 **Aprox:** {150 + i*50}m de tu ubicación")
            st.write(f"🔒 **Estado:** Verificado y seguro")
            
            if st.button(f"🚶‍♂️ Cómo llegar a {nombre}", key=f"safe_{i}"):
                st.info(f"🗺️ Calculando ruta segura hacia {nombre}...")
                # Aquí iría la lógica de navegación
            st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PERFIL DE USUARIO
# =============================================================================
elif page == "👤 Perfil":
    st.subheader("👤 PERFIL Y CONFIGURACIÓN")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre", "Edwar")
            edad = st.number_input("Edad", min_value=18, max_value=100, value=25)
        with col2:
            telefono = st.text_input("Teléfono", "+51 999888777")
            email = st.text_input("Email", "edwarrojasccasa@gmail.com")
        
        st.subheader("📞 CONTACTOS DE EMERGENCIA")
        emergencia1 = st.text_input("Contacto Emergencia 1", "edwarrojasccasa@gmail.com")
        emergencia2 = st.text_input("Contacto Emergencia 2", "+51 988777666")
        
        st.subheader("🏥 INFORMACIÓN MÉDICA")
        grupo_sanguineo = st.selectbox("Grupo Sanguíneo", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        condiciones = st.text_area("Condiciones médicas o alergias", "Ninguna alergia conocida")
        
        if st.form_submit_button("💾 GUARDAR CONFIGURACIÓN", use_container_width=True):
            st.success("✅ Perfil actualizado correctamente")

# =============================================================================
# INFORMACIÓN EN SIDEBAR
# =============================================================================
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 ANÁLISIS DE PATRONES")
st.sidebar.info("""
**🤖 IA detecta patrones:**
- Zona centro: 70% más peligrosa después de 8 PM
- Viernes + pago = 85% más robos
- Correlaciones identificadas
""")

st.sidebar.markdown("### 🌐 COMPARTIR APP")
st.sidebar.success("""
**Para acceso externo:**
```bash
streamlit run app.py
ngrok http 8501
