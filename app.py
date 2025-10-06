import streamlit as st
import time
import os
from unidecode import unidecode
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import io
import colorsys
import wave
import struct

# Frases motivacionales personalizadas
FRASES_MOTIVACIONALES = [
    "Tu bienestar mental es una prioridad, no un lujo",
    "Cada día es una nueva oportunidad para cuidar tu mente",
    "Eres más fuerte de lo que crees y más valioso de lo que imaginas",
    "La paz interior comienza con una respiración consciente",
    "Tu salud mental merece la misma atención que tu salud física",
    "Pequeños pasos diarios hacia el bienestar crean grandes transformaciones",
    "Está bien no estar bien todo el tiempo, es parte de ser humano",
    "Tu mente es como un jardín: cultiva pensamientos que te nutran"
]

# Avatar principal de Serenity - imagen profesional y amigable
AVATAR_SERENITY_IMAGEN = "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400&h=400&fit=crop&crop=face&q=80"

# Configuración inicial
st.set_page_config(
    page_title="🌱 Serenity App - Tu Bienestar Mental",
    page_icon="🌱",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E7D32;
        font-size: 2.5em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        text-align: center;
        color: #1B5E20;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .feature-card {
        background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #4CAF50;
    }
    .motivational-quote {
        background: linear-gradient(45deg, #81C784, #A5D6A7);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-style: italic;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .emotion-button {
        width: 100%;
        padding: 15px;
        margin: 5px 0;
        border: none;
        border-radius: 10px;
        font-size: 1.1em;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .avatar-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Constantes y configuración
AVATAR_SERENITY_IMAGEN = "https://raw.githubusercontent.com/johanavalencia788-boop/serenity-johana-app/main/johana_avatar.jpg"

# Frases motivacionales
FRASES_MOTIVACIONALES = [
    "🌟 Cada día es una nueva oportunidad para crecer",
    "💪 Eres más fuerte de lo que crees",
    "🌈 Después de la tormenta siempre sale el sol",
    "🦋 Los cambios te hacen crecer y transformarte",
    "❤️ Cuídate con la misma gentileza que cuidas a otros",
    "🌱 El crecimiento personal es un viaje, no un destino",
    "✨ Tu bienestar mental es tu mayor tesoro",
    "🎯 Enfócate en el progreso, no en la perfección"
]

def generar_avatar_ia(nombre, estilo="moderno", color_primario="azul"):
    """Genera un avatar personalizado usando PIL con IA básica"""
    
    # Configurar colores según preferencia
    colores = {
        "azul": [(30, 144, 255), (70, 130, 180), (135, 206, 235)],
        "verde": [(34, 139, 34), (50, 205, 50), (144, 238, 144)],
        "rosa": [(255, 20, 147), (255, 105, 180), (255, 182, 193)],
        "morado": [(138, 43, 226), (147, 112, 219), (221, 160, 221)],
        "naranja": [(255, 140, 0), (255, 165, 0), (255, 218, 185)]
    }
    
    color_principal, color_secundario, color_fondo = colores.get(color_primario, colores["azul"])
    
    # Crear imagen base
    size = (400, 400)
    img = Image.new('RGB', size, color_fondo)
    draw = ImageDraw.Draw(img)
    
    # Dibujar fondo con gradiente simulado
    for y in range(size[1]):
        ratio = y / size[1]
        r = int(color_fondo[0] * (1 - ratio) + color_secundario[0] * ratio)
        g = int(color_fondo[1] * (1 - ratio) + color_secundario[1] * ratio)
        b = int(color_fondo[2] * (1 - ratio) + color_secundario[2] * ratio)
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))
    
    # Dibujar cara (círculo principal)
    face_size = 180
    face_x = (size[0] - face_size) // 2
    face_y = (size[1] - face_size) // 2 - 20
    
    # Cara base
    draw.ellipse([face_x, face_y, face_x + face_size, face_y + face_size], 
                fill=(255, 220, 177), outline=color_principal, width=3)
    
    # Ojos
    eye_size = 15
    left_eye_x = face_x + 50
    right_eye_x = face_x + face_size - 50 - eye_size
    eye_y = face_y + 60
    
    draw.ellipse([left_eye_x, eye_y, left_eye_x + eye_size, eye_y + eye_size], 
                fill=(0, 0, 0))
    draw.ellipse([right_eye_x, eye_y, right_eye_x + eye_size, eye_y + eye_size], 
                fill=(0, 0, 0))
    
    # Pupilas brillantes
    pupil_size = 5
    draw.ellipse([left_eye_x + 5, eye_y + 5, left_eye_x + pupil_size + 5, eye_y + pupil_size + 5], 
                fill=(255, 255, 255))
    draw.ellipse([right_eye_x + 5, eye_y + 5, right_eye_x + pupil_size + 5, eye_y + pupil_size + 5], 
                fill=(255, 255, 255))
    
    # Nariz simple
    nose_x = face_x + face_size // 2
    nose_y = face_y + 90
    draw.ellipse([nose_x - 3, nose_y, nose_x + 3, nose_y + 6], fill=(255, 192, 163))
    
    # Sonrisa
    smile_width = 60
    smile_x = face_x + (face_size - smile_width) // 2
    smile_y = face_y + 110
    draw.arc([smile_x, smile_y, smile_x + smile_width, smile_y + 30], 
            start=0, end=180, fill=color_principal, width=4)
    
    # Cabello/sombrero según estilo
    if estilo == "profesional":
        draw.ellipse([face_x - 10, face_y - 30, face_x + face_size + 10, face_y + 80], 
                    fill=(101, 67, 33), outline=color_principal, width=2)
    elif estilo == "creativo":
        draw.ellipse([face_x - 15, face_y - 35, face_x + face_size + 15, face_y + 75], 
                    fill=color_principal, outline=color_secundario, width=3)
    else:  # moderno
        draw.ellipse([face_x - 5, face_y - 25, face_x + face_size + 5, face_y + 70], 
                    fill=(139, 69, 19), outline=color_principal, width=2)
    
    # Agregar nombre personalizado
    try:
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Nombre en la parte inferior
    nombre_limpio = unidecode(nombre).upper()
    text_bbox = draw.textbbox((0, 0), nombre_limpio, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (size[0] - text_width) // 2
    text_y = face_y + face_size + 30
    
    # Sombra del texto
    draw.text((text_x + 2, text_y + 2), nombre_limpio, fill=(0, 0, 0, 128), font=font)
    # Texto principal
    draw.text((text_x, text_y), nombre_limpio, fill=color_principal, font=font)
    
    # Elementos decorativos según estilo
    if estilo == "creativo":
        for _ in range(8):
            star_x = random.randint(20, size[0] - 20)
            star_y = random.randint(20, size[1] - 20)
            draw.text((star_x, star_y), "✨", fill=color_secundario)
    elif estilo == "profesional":
        draw.rectangle([10, 10, size[0] - 10, size[1] - 10], 
                      outline=color_principal, width=3)
    
    # Convertir a bytes para almacenamiento
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def crear_avatar_animado_ia(nombre, frames=4):
    """Crea una secuencia de frames para avatar animado"""
    estilos = ["moderno", "profesional", "creativo"]
    colores = ["azul", "verde", "rosa", "morado", "naranja"]
    
    frames_generados = []
    
    for i in range(frames):
        estilo = estilos[i % len(estilos)]
        color = colores[i % len(colores)]
        
        avatar_bytes = generar_avatar_ia(nombre, estilo, color)
        avatar_img = Image.open(io.BytesIO(avatar_bytes))
        frames_generados.append(avatar_img)
    
    return frames_generados

def generar_avatar_personalizado(iniciales, nombre_completo):
    """Genera un avatar personalizado con las iniciales de la persona"""
    size = (300, 300)
    
    # Crear imagen con fondo gradiente suave
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Fondo gradiente personalizado (colores suaves y elegantes)
    for y in range(size[1]):
        # Gradiente de rosa suave a lavanda
        r = int(255 - (y / size[1]) * 50)  # 255 -> 205
        g = int(240 - (y / size[1]) * 60)  # 240 -> 180  
        b = int(245 - (y / size[1]) * 30)  # 245 -> 215
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))
    
    # Círculo principal para el avatar
    circle_size = 200
    circle_x = (size[0] - circle_size) // 2
    circle_y = (size[1] - circle_size) // 2 - 20
    
    # Sombra del círculo
    shadow_offset = 8
    draw.ellipse([circle_x + shadow_offset, circle_y + shadow_offset, 
                  circle_x + circle_size + shadow_offset, circle_y + circle_size + shadow_offset], 
                fill=(200, 200, 200, 100))
    
    # Círculo principal con bordes elegantes
    draw.ellipse([circle_x, circle_y, circle_x + circle_size, circle_y + circle_size], 
                fill=(255, 255, 255), outline=(180, 120, 180), width=4)
    
    # Dibujar las iniciales grandes y elegantes
    try:
        # Intentar usar una fuente más grande
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Obtener tamaño del texto de iniciales
    iniciales_text = iniciales.upper()
    text_bbox = draw.textbbox((0, 0), iniciales_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Posicionar las iniciales en el centro del círculo
    text_x = circle_x + (circle_size - text_width) // 2
    text_y = circle_y + (circle_size - text_height) // 2 - 10
    
    # Sombra de las iniciales
    draw.text((text_x + 3, text_y + 3), iniciales_text, fill=(100, 100, 100), font=font)
    # Iniciales principales en color elegante
    draw.text((text_x, text_y), iniciales_text, fill=(120, 60, 120), font=font)
    
    # Nombre completo en la parte inferior
    nombre_bbox = draw.textbbox((0, 0), nombre_completo, font=font)
    nombre_width = nombre_bbox[2] - nombre_bbox[0]
    nombre_x = (size[0] - nombre_width) // 2
    nombre_y = circle_y + circle_size + 25
    
    # Sombra del nombre
    draw.text((nombre_x + 2, nombre_y + 2), nombre_completo, fill=(150, 150, 150), font=font)
    # Nombre principal
    draw.text((nombre_x, nombre_y), nombre_completo, fill=(100, 50, 100), font=font)
    
    # Elementos decorativos alrededor
    for i in range(6):
        angle = i * 60  # 6 estrellas alrededor
        star_radius = 120
        star_x = circle_x + circle_size//2 + int(star_radius * np.cos(np.radians(angle)))
        star_y = circle_y + circle_size//2 + int(star_radius * np.sin(np.radians(angle)))
        
        if 0 <= star_x < size[0] - 20 and 0 <= star_y < size[1] - 20:
            draw.text((star_x, star_y), "✨", fill=(200, 150, 200))
    
    # Convertir a bytes para uso en Streamlit
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def generar_musica_relajante(tipo="piano", duracion=30):
    """Genera música relajante usando numpy"""
    sample_rate = 44100
    duration = duracion  # segundos
    
    # Crear el array de tiempo
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    if tipo == "piano":
        # "Ballade pour Adeline" - Richard Clayderman
        # Melodía original completa de esta obra maestra
        
        # Frecuencias exactas de las notas (Hz)
        # Tema principal de Ballade pour Adeline
        notas_melodia = [
            # Introducción melancólica - Frase A
            349.23, 392.00, 440.00, 493.88, 523.25, 493.88, 440.00, 392.00,  # Fa-Sol-La-Si-Do-Si-La-Sol
            
            # Desarrollo emotivo - Frase B  
            329.63, 369.99, 415.30, 466.16, 523.25, 587.33, 523.25, 466.16,  # Mi-Fa#-Sol#-La#-Do-Re-Do-La#
            
            # Tema principal Adeline - Frase C (la parte más reconocible)
            392.00, 440.00, 493.88, 523.25, 587.33, 659.25, 698.46, 659.25,  # Sol-La-Si-Do-Re-Mi-Fa-Mi
            587.33, 523.25, 493.88, 440.00, 392.00, 349.23, 329.63, 293.66,  # Re-Do-Si-La-Sol-Fa-Mi-Re
            
            # Variación ornamental - Frase D
            523.25, 466.16, 415.30, 369.99, 329.63, 369.99, 415.30, 466.16,  # Do-La#-Sol#-Fa#-Mi-Fa#-Sol#-La#
            
            # Clímax romántico - Frase E (octava alta)
            659.25, 698.46, 783.99, 880.00, 987.77, 880.00, 783.99, 698.46,  # Mi-Fa-Sol-La-Si-La-Sol-Fa (alta)
            
            # Resolución final - Frase F (descenso suave)
            659.25, 587.33, 523.25, 466.16, 415.30, 369.99, 329.63, 293.66,  # Mi-Re-Do-La#-Sol#-Fa#-Mi-Re
            261.63, 293.66, 329.63, 349.23, 392.00, 349.23, 329.63, 261.63   # Do-Re-Mi-Fa-Sol-Fa-Mi-Do
        ]
        
        # Duraciones específicas para cada frase (ritmo de Ballade pour Adeline)
        duraciones_notas = [
            # Frase A - Introducción (notas largas y expresivas)
            0.8, 0.6, 0.8, 0.6, 1.2, 0.6, 0.8, 1.0,
            # Frase B - Desarrollo (ritmo moderado)
            0.6, 0.4, 0.6, 0.4, 0.8, 0.6, 0.8, 0.6,
            # Frase C - Tema principal (notas fluidas)
            0.5, 0.5, 0.5, 0.5, 0.7, 0.5, 0.5, 0.7,
            0.5, 0.5, 0.5, 0.5, 0.7, 0.5, 0.7, 0.8,
            # Frase D - Variación (notas rápidas y ligeras)
            0.4, 0.4, 0.4, 0.4, 0.6, 0.4, 0.4, 0.6,
            # Frase E - Clímax (notas sostenidas y dramáticas)
            1.0, 0.8, 1.0, 0.8, 1.2, 0.8, 1.0, 1.2,
            # Frase F - Resolución final (rallentando gradual)
            0.8, 0.6, 0.8, 0.6, 0.8, 0.6, 1.0, 1.5
        ]
        
        audio = np.zeros_like(t)
        tiempo_actual = 0
        
        for i, (freq, dur_nota) in enumerate(zip(notas_melodia, duraciones_notas)):
            # Ajustar duración proporcionalmente
            duracion_real = dur_nota * (duration / sum(duraciones_notas))
            
            # Calcular posición en el array
            inicio = int(tiempo_actual * sample_rate)
            fin = int((tiempo_actual + duracion_real) * sample_rate)
            if fin > len(t):
                fin = len(t)
            
            # Tiempo específico para esta nota
            t_nota = np.linspace(0, duracion_real, fin - inicio, False)
            tiempo_actual += duracion_real
            
            # Crear sonido de piano más realista
            # Fundamental + armónicos para timbre de piano
            nota = np.sin(2 * np.pi * freq * t_nota) * 0.5        # Fundamental
            nota += np.sin(2 * np.pi * freq * 2 * t_nota) * 0.25  # Octava
            nota += np.sin(2 * np.pi * freq * 3 * t_nota) * 0.12  # Quinta perfecta
            nota += np.sin(2 * np.pi * freq * 4 * t_nota) * 0.08  # Doble octava
            nota += np.sin(2 * np.pi * freq * 0.5 * t_nota) * 0.15 # Sub-armónico
            
            # Envolvente más natural (ataque rápido, decay suave)
            envolvente = np.exp(-t_nota * 1.2) * (1 - np.exp(-t_nota * 30))
            
            # Añadir acompañamiento armónico sutil
            if i % 4 == 0:  # Cada 4 notas, añadir acorde de acompañamiento
                acorde_freq = freq / 2  # Una octava abajo
                acompañamiento = np.sin(2 * np.pi * acorde_freq * t_nota) * 0.2 * envolvente
                acompañamiento += np.sin(2 * np.pi * acorde_freq * 1.25 * t_nota) * 0.15 * envolvente  # Tercera
                audio[inicio:fin] += acompañamiento
            
            # Aplicar envolvente y añadir al audio total
            nota *= envolvente
            audio[inicio:fin] += nota
        
        # Procesamiento final para sonido más suave y romántico
        audio = audio * 0.4  # Volumen moderado
        
    elif tipo == "naturaleza":
        # Simulación de sonidos de lluvia y viento
        # Ruido blanco filtrado para simular lluvia
        lluvia = np.random.normal(0, 0.1, len(t))
        
        # Filtro pasa bajos simple para suavizar
        for i in range(1, len(lluvia)):
            lluvia[i] = 0.9 * lluvia[i-1] + 0.1 * lluvia[i]
        
        # Agregar tonos bajos para viento
        viento = 0.05 * np.sin(40 * 2 * np.pi * t) + 0.03 * np.sin(60 * 2 * np.pi * t)
        
        audio = lluvia + viento
        audio = audio * 0.5
        
    elif tipo == "ambient":
        # Drones ambientales
        frecuencias_base = [110, 165, 220]  # A2, E3, A3
        audio = np.zeros_like(t)
        
        for freq in frecuencias_base:
            # Ondas senoidales con modulación lenta
            onda = np.sin(2 * np.pi * freq * t) * 0.3
            modulacion = 1 + 0.2 * np.sin(0.1 * 2 * np.pi * t)
            audio += onda * modulacion
        
        audio = audio * 0.3
        
    elif tipo == "meditacion":
        # Tonos de cuencos tibetanos
        frecuencias_cuencos = [256, 341.3, 426.7, 512]  # Do, Fa, La, Do octava
        audio = np.zeros_like(t)
        
        for i, freq in enumerate(frecuencias_cuencos):
            # Tono principal con decay
            tono = np.sin(2 * np.pi * freq * t) * np.exp(-t * 0.3)
            # Armónicos
            tono += 0.3 * np.sin(2 * np.pi * freq * 2 * t) * np.exp(-t * 0.5)
            # Reverb simulado
            tono += 0.1 * np.sin(2 * np.pi * freq * t + np.pi/4) * np.exp(-t * 0.2)
            
            audio += tono * 0.25
    
    # Normalizar audio
    audio = audio / np.max(np.abs(audio))
    
    # Convertir a formato WAV
    audio_int = (audio * 32767).astype(np.int16)
    
    # Crear archivo WAV en memoria
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int.tobytes())
    
    wav_buffer.seek(0)
    return wav_buffer.getvalue()

def crear_avatar_personalizado():
    """Función principal para crear avatars personalizados"""
    st.markdown("## 🎨 Creador de Avatar Personalizado")
    st.markdown("---")
    
    # Crear tabs para diferentes opciones
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🤖 IA Integrada", 
        "🌐 IA Externa", 
        "📹 Video Selfie", 
        "🎮 Avatar 3D", 
        "📱 Subir Archivo"
    ])
    
    with tab1:
        st.markdown("#### 🧠 Generador de Avatar con IA")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_avatar = st.text_input("¿Cuál es tu nombre?", 
                                        value="Usuario", 
                                        key="nombre_avatar")
            
            estilo_avatar = st.selectbox("Elige tu estilo:", 
                                       ["moderno", "profesional", "creativo"],
                                       key="estilo_avatar")
            
            color_avatar = st.selectbox("Color principal:", 
                                      ["azul", "verde", "rosa", "morado", "naranja"],
                                      key="color_avatar")
        
        with col2:
            if st.button("🎨 Generar Avatar", key="generar_avatar", use_container_width=True):
                with st.spinner("🎨 Creando tu avatar personalizado..."):
                    avatar_generado = generar_avatar_ia(nombre_avatar, estilo_avatar, color_avatar)
                    st.session_state.avatar_generado = avatar_generado
                    time.sleep(1)
                    st.success("✅ ¡Avatar generado!")
            
            if st.button("🎬 Crear Avatar Animado", key="avatar_animado", use_container_width=True):
                with st.spinner("🎬 Generando secuencia animada..."):
                    frames = crear_avatar_animado_ia(nombre_avatar, 4)
                    
                    st.markdown("#### 🎞️ Frames de Animación:")
                    cols = st.columns(4)
                    
                    for i, frame in enumerate(frames):
                        with cols[i]:
                            st.image(frame, caption=f"Frame {i+1}", width=150)
                    
                    st.success("✅ Avatar animado generado!")
        
        # Mostrar avatar generado si existe
        if st.session_state.get('avatar_generado'):
            st.markdown("---")
            st.markdown("#### 🎯 Tu Avatar Generado")
            
            avatar_img = Image.open(io.BytesIO(st.session_state.avatar_generado))
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(avatar_img, caption="Tu avatar personalizado", width=250)
            
            if st.button("💾 Usar como Mi Avatar"):
                st.session_state.avatar_personalizado = st.session_state.avatar_generado
                st.success("✅ Avatar configurado!")
                st.balloons()
        
        st.markdown("---")
        st.info("""
        🧠 **IA Integrada incluye:**
        - Generación automática de rostros
        - Personalización por nombre y estilo  
        - Colores adaptativos
        - Elementos decorativos dinámicos
        - Múltiples frames para animación
        """)
    
    with tab2:
        st.markdown("#### 🤖 Avatar con IA Externa")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **D-ID (Recomendado) - Avatar parlante con IA:**
            1. Ve a [D-ID Studio](https://www.d-id.com/)
            2. Sube una foto tuya o elige un avatar
            3. Escribe tu texto de presentación
            4. Genera el video parlante
            5. Descarga y sube aquí
            """)
            if st.button("🔗 Abrir D-ID", key="d_id"):
                st.write("➡️ [Ir a D-ID Studio](https://www.d-id.com/)")
        
        with col2:
            st.markdown("""
            **Synthesia - Avatar profesional:**
            1. Ve a [Synthesia](https://www.synthesia.io/)
            2. Crea avatar personalizado
            3. Graba tu mensaje
            4. Exporta el video
            5. Sube la URL aquí
            """)
            if st.button("🔗 Abrir Synthesia", key="synthesia"):
                st.write("➡️ [Ir a Synthesia](https://www.synthesia.io/)")
    
    with tab3:
        st.markdown("#### 📹 Grabar Video Selfie")
        st.markdown("""
        **Crea tu propio video avatar:**
        1. Ve a [Loom](https://www.loom.com/) para grabación rápida
        2. O usa [Vidyard](https://www.vidyard.com/) para videos profesionales
        3. Graba un video de 30-60 segundos presentándote
        4. Comparte el enlace público
        """)
    
    with tab4:
        st.markdown("#### 🎮 Avatar 3D")
        st.markdown("""
        **Ready Player Me:**
        1. Ve a [Ready Player Me](https://readyplayer.me/)
        2. Crea tu avatar 3D personalizado
        3. Exporta como video o imagen
        """)
    
    with tab5:
        st.markdown("#### 📱 Subir Tu Propio Avatar")
        
        st.markdown("""
        **💡 Recomendaciones para tu avatar personal:**
        - **Video**: 30-60 segundos, presentándote de forma natural
        - **Imagen**: Foto clara de tu rostro, buena iluminación
        - **Formatos**: MP4, MOV, GIF, JPG, PNG
        - **Tamaño**: Máximo 200MB
        """)
        
        uploaded_file = st.file_uploader(
            "🎬 Arrastra tu archivo aquí:",
            type=['mp4', 'mov', 'gif', 'jpg', 'png'],
            help="Sube tu video o imagen personal para usar como avatar"
        )
        
        if uploaded_file is not None:
            st.success("✅ ¡Perfecto! Tu avatar personal ha sido cargado")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if uploaded_file.type.startswith('image'):
                    st.image(uploaded_file, width=300, caption="Tu avatar personalizado")
                    st.session_state.avatar_personalizado = uploaded_file
                else:
                    st.video(uploaded_file)
                    st.session_state.avatar_personalizado = uploaded_file
                    st.caption("🎬 Tu video personal como avatar")
            
            with col2:
                st.markdown("""
                **✨ ¡Genial!**
                
                Tu avatar personal ahora aparecerá en la pantalla principal.
                
                **Beneficios:**
                - Experiencia más personal
                - Conexión emocional
                - Identidad única
                """)
            
            st.balloons()
            
        else:
            st.info("📁 Selecciona un archivo para comenzar")
            
            # Opción especial para activar el avatar de la creadora
            st.markdown("---")
            st.markdown("**👩‍💻 ¿Quieres conocer a la creadora de Serenity?**")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("👋 Activar Avatar de Johana", key="avatar_johana", use_container_width=True):
                    # URL de tu foto personal (puedes cambiar esta URL por una foto tuya)
                    st.session_state.avatar_creadora = "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face&q=80"
                    st.session_state.mostrar_avatar_creadora = True
                    st.success("¡Avatar de Johana activado! 🌟")
                    st.rerun()
            
            with col2:
                if st.button("🤖 Usar Avatar IA", key="avatar_ia_default", use_container_width=True):
                    st.session_state.mostrar_avatar_creadora = False
                    st.success("Avatar IA activado ✨")
                    st.rerun()
            
            # Ejemplo visual
            st.markdown("**📸 Ejemplos de avatares efectivos:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("🎬 **Video**<br>Saluda naturalmente", unsafe_allow_html=True)
            with col2:
                st.markdown("📸 **Foto**<br>Sonrisa amigable", unsafe_allow_html=True)
            with col3:
                st.markdown("🎭 **Creativo**<br>Tu estilo único", unsafe_allow_html=True)

def mostrar_serenity_parlante():
    """Muestra el avatar de Serenity con opción de personalización"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🎭 Conoce a Serenity")
    
    with col2:
        if st.button("🎨 Personalizar Avatar", key="personalizar_avatar"):
            st.session_state.mostrar_creator = True
    
    # Mostrar creador si está activado
    if st.session_state.get('mostrar_creator', False):
        crear_avatar_personalizado()
        if st.button("❌ Cerrar Creador"):
            st.session_state.mostrar_creator = False
            st.rerun()
        return
    
    # Avatar actual
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.get('avatar_personalizado'):
            # Avatar personalizado del usuario
            if isinstance(st.session_state.avatar_personalizado, bytes):
                avatar_img = Image.open(io.BytesIO(st.session_state.avatar_personalizado))
                st.image(avatar_img, width=200, caption="Tu avatar personalizado")
            else:
                # Archivo subido
                if hasattr(st.session_state.avatar_personalizado, 'type'):
                    if st.session_state.avatar_personalizado.type.startswith('image'):
                        st.image(st.session_state.avatar_personalizado, width=200, caption="Tu avatar personalizado")
                    else:
                        st.video(st.session_state.avatar_personalizado)
        else:
            # Mostrar avatar principal de Serenity
            st.markdown("#### � ¡Hola! Soy Serenity Johana")
            
            # Tu avatar personal - Tu video
            col_av1, col_av2, col_av3 = st.columns([1, 2, 1])
            with col_av2:
                # Mostrar tu video personal como avatar
                video_local = "johana_avatar.mp4"
                video_downloads = r"c:\Users\johan\Downloads\Untitled video (3).mp4"
                
                try:
                    # Lista de rutas para el video en orden de prioridad
                    video_sources = [
                        video_local,  # Archivo local en el proyecto
                        video_downloads,  # Archivo en Downloads (solo local)
                        "https://github.com/johanavalencia788-boop/serenity-johana-app/raw/main/johana_avatar.mp4"  # GitHub raw
                    ]
                    
                    video_loaded = False
                    
                    for video_source in video_sources:
                        try:
                            if video_source.startswith('http'):
                                # URL de GitHub
                                st.video(video_source, start_time=0)
                                st.markdown("*✨ Johana Valencia - Tu asistente personalizada de bienestar mental*")
                                st.markdown("*🌸 Tu avatar personalizado en video (desde GitHub)*")
                                st.info("🔊 Puedes ajustar el volumen usando los controles del video")
                                video_loaded = True
                                break
                            elif os.path.exists(video_source):
                                # Archivo local
                                st.video(video_source, start_time=0)
                                st.markdown("*✨ Johana Valencia - Tu asistente personalizada de bienestar mental*")
                                st.markdown("*🌸 Tu avatar personalizado en video*")
                                st.info("🔊 Puedes ajustar el volumen usando los controles del video")
                                video_loaded = True
                                break
                        except Exception as video_error:
                            # Continuar con la siguiente fuente si esta falla
                            continue
                    
                    if not video_loaded:
                        # Si no se pudo cargar ningún video, mostrar avatar generado hermoso
                        avatar_img = generar_avatar_personalizado("JV", "Johana Valencia")
                        st.image(avatar_img, width=280, caption="✨ Johana Valencia - Tu asistente personalizada de bienestar mental")
                        st.markdown("*🌸 Tu avatar personalizado*")
                        st.info("💡 Avatar generado - Video disponible localmente")
                            
                except Exception as e:
                    # Si hay cualquier error general, mostrar avatar generado elegante
                    avatar_img = generar_avatar_personalizado("JV", "Johana Valencia")
                    st.image(avatar_img, width=280, caption="✨ Johana Valencia - Tu asistente personalizada de bienestar mental")
                    st.markdown("*🌸 Tu avatar personalizado*")
            
            # Mensaje de bienvenida personalizado
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #E8F5E8, #F0F8F0); border-radius: 15px; margin: 10px 0;">
                <p><strong>💚 Tu compañera digital para el bienestar mental</strong></p>
                <p><em>Estoy aquí para acompañarte en tu viaje hacia el bienestar emocional</em></p>
                <p><small>💡 Puedes personalizar tu avatar usando el botón de arriba</small></p>
            </div>
            """, unsafe_allow_html=True)

def mostrar_header():
    """Muestra el header principal personalizado de la aplicación"""
    st.markdown('<h1 class="main-header">🌱 Serenity App</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Tu compañera digital para el bienestar mental y emocional</p>', unsafe_allow_html=True)
    
    # Frase motivacional personalizada
    frase = random.choice(FRASES_MOTIVACIONALES)
    if 'nombre_usuario' in st.session_state and st.session_state.nombre_usuario:
        st.markdown(f'<div class="motivational-quote">¡Hola {st.session_state.nombre_usuario}! 🌟 {frase}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="motivational-quote">{frase}</div>', unsafe_allow_html=True)



def main():
    """Función principal de la aplicación"""
    
    # Inicializar estados
    if 'mostrar_creator' not in st.session_state:
        st.session_state.mostrar_creator = False
    if 'nombre_usuario' not in st.session_state:
        st.session_state.nombre_usuario = ""
    
    # Si no hay nombre, mostrar bienvenida
    if not st.session_state.nombre_usuario:
        st.markdown("### 🌟 ¡Bienvenido/a a Serenity!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #E8F5E8, #F0F8F0); border-radius: 20px; margin: 20px 0;">
                <h3>🤝 Me encantaría conocerte mejor</h3>
                <p>Para ofrecerte una experiencia personalizada de bienestar mental, ¿cómo te gustaría que te llame?</p>
            </div>
            """, unsafe_allow_html=True)
            
            nombre_input = st.text_input(
                "✨ Tu nombre o como prefieres que te llame:",
                placeholder="Escribe tu nombre aquí...",
                key="nombre_input"
            )
            
            if st.button("🌱 Comenzar mi viaje de bienestar", type="primary", use_container_width=True):
                if nombre_input.strip():
                    st.session_state.nombre_usuario = nombre_input.strip()
                    st.success(f"¡Hola {st.session_state.nombre_usuario}! 🎉 Bienvenido/a a tu espacio personal de bienestar")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Por favor, escribe tu nombre para continuar 😊")
        return
    
    # Una vez que se tiene el nombre, mostrar la aplicación completa
    # Header personalizado
    mostrar_header()
    
    # Avatar de Serenity
    mostrar_serenity_parlante()
    
    # Sección de estado emocional personalizada
    mostrar_estado_emocional()
    
    # Herramientas de bienestar
    mostrar_herramientas_bienestar()

def mostrar_estado_emocional():
    """Muestra la sección de evaluación emocional personalizada"""
    st.markdown("---")
    st.markdown(f"### 💭 {st.session_state.nombre_usuario}, ¿cómo te sientes hoy?")
    
    # Diccionario de emociones con mensajes personalizados
    emociones = {
        "😊": {"nombre": "Feliz", "color": "#4CAF50", "mensaje": f"¡Qué maravilloso, {st.session_state.nombre_usuario}! La felicidad es contagiosa. Comparte tu alegría con otros."},
        "😔": {"nombre": "Triste", "color": "#2196F3", "mensaje": f"Es normal sentirse triste a veces, {st.session_state.nombre_usuario}. Permítete sentir esta emoción, es parte de ser humano."},
        "😰": {"nombre": "Ansioso", "color": "#FF9800", "mensaje": f"{st.session_state.nombre_usuario}, la ansiedad puede ser abrumadora. Respira profundo, estás seguro/a en este momento."},
        "😡": {"nombre": "Enojado", "color": "#F44336", "mensaje": f"{st.session_state.nombre_usuario}, la ira es una emoción válida. ¿Qué puedes aprender de lo que te molesta?"},
        "😴": {"nombre": "Cansado", "color": "#9C27B0", "mensaje": f"{st.session_state.nombre_usuario}, el descanso es fundamental. Escucha a tu cuerpo y date el tiempo que necesitas."},
        "🤔": {"nombre": "Confundido", "color": "#607D8B", "mensaje": f"La confusión puede ser incómoda, {st.session_state.nombre_usuario}, pero también es el primer paso hacia la claridad."}
    }
    
    # Mostrar botones de emociones
    cols = st.columns(len(emociones))
    for i, (emoji, data) in enumerate(emociones.items()):
        with cols[i]:
            if st.button(f"{emoji}\n{data['nombre']}", key=f"emotion_{emoji}", use_container_width=True):
                st.session_state.emocion_actual = emoji
                st.session_state.mensaje_emocion = data['mensaje']
                st.session_state.color_emocion = data['color']
    
    # Mostrar mensaje personalizado si se seleccionó una emoción
    if 'emocion_actual' in st.session_state:
        st.markdown(f"""
        <div style="background: {st.session_state.color_emocion}20; padding: 20px; border-radius: 15px; border-left: 5px solid {st.session_state.color_emocion}; margin: 20px 0;">
            <p style="color: {st.session_state.color_emocion}; font-weight: bold; margin: 0;">
                {st.session_state.mensaje_emocion}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sugerencia de música según la emoción
        if st.session_state.emocion_actual in ["😔", "😰"]:
            st.info("🎵 Te recomiendo escuchar la música relajante de piano para encontrar paz interior.")
        elif st.session_state.emocion_actual == "😊":
            st.success("🎵 ¡Celebra tu felicidad con música ambiental que eleve tu espíritu!")
        elif st.session_state.emocion_actual == "😡":
            st.warning("🎵 La música de meditación puede ayudarte a canalizar y transformar esa energía.")

def mostrar_herramientas_bienestar():
    """Muestra las herramientas principales de bienestar"""
    st.markdown("---")
    st.markdown(f"### 🧠 Herramientas Personalizadas para {st.session_state.nombre_usuario}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>💭 Diario Emocional Personal</h4>
            <p>Registra tus pensamientos y emociones diarias en tu espacio privado</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📖 Abrir mi diario", key="abrir_diario", use_container_width=True):
            st.session_state.mostrar_diario = True
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🧘 Meditación Guiada</h4>
            <p>Ejercicios de relajación y mindfulness personalizados</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🕯️ Comenzar meditación", key="comenzar_meditacion", use_container_width=True):
            st.session_state.mostrar_meditacion = True
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📈 Seguimiento del Humor</h4>
            <p>Monitorea tu estado emocional a lo largo del tiempo</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Ver mi progreso", key="ver_progreso", use_container_width=True):
            st.session_state.mostrar_seguimiento = True
    
    # Mostrar secciones según lo que el usuario haya seleccionado
    if st.session_state.get('mostrar_diario', False):
        mostrar_diario_emocional()
    
    if st.session_state.get('mostrar_meditacion', False):
        mostrar_meditacion_guiada()
        
    if st.session_state.get('mostrar_seguimiento', False):
        mostrar_seguimiento_humor()

def mostrar_diario_emocional():
    """Muestra la funcionalidad del diario emocional personalizado"""
    st.markdown("---")
    st.markdown(f"### 📖 Diario Emocional de {st.session_state.nombre_usuario}")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("❌ Cerrar diario"):
            st.session_state.mostrar_diario = False
            st.rerun()
    
    with col1:
        st.markdown("*Tu espacio seguro para expresar tus pensamientos y emociones*")
    
    # Área de escritura
    entrada_diario = st.text_area(
        f"✍️ ¿Qué tienes en mente hoy, {st.session_state.nombre_usuario}?",
        placeholder=f"Querido diario, hoy {st.session_state.nombre_usuario} se siente...",
        height=150,
        key="entrada_diario"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("💾 Guardar en mi diario", type="primary"):
            if entrada_diario.strip():
                fecha_actual = time.strftime("%Y-%m-%d %H:%M")
                entrada_completa = f"""
📅 Fecha: {fecha_actual}
Usuario: {st.session_state.nombre_usuario}
Emoción actual: {st.session_state.get('emocion_actual', 'No especificada')}

💭 Reflexión:
{entrada_diario}

---
"""
                # Guardar en session state (en producción se podría usar una base de datos)
                if 'entradas_diario' not in st.session_state:
                    st.session_state.entradas_diario = []
                
                st.session_state.entradas_diario.append({
                    'fecha': fecha_actual,
                    'contenido': entrada_diario,
                    'emocion': st.session_state.get('emocion_actual', '🤔')
                })
                
                st.success(f"✅ Entrada guardada en tu diario personal, {st.session_state.nombre_usuario}")
                st.session_state.entrada_diario = ""  # Limpiar el área de texto
    
    with col2:
        if st.button("📚 Ver entradas anteriores"):
            st.session_state.mostrar_historial = True
    
    # Mostrar historial si se solicita
    if st.session_state.get('mostrar_historial', False):
        st.markdown("### 📚 Tus reflexiones anteriores")
        if 'entradas_diario' in st.session_state and st.session_state.entradas_diario:
            for i, entrada in enumerate(reversed(st.session_state.entradas_diario[-5:])):  # Últimas 5 entradas
                st.markdown(f"""
                <div style="background: #f0f8f0; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #4CAF50;">
                    <p><strong>{entrada['emocion']} {entrada['fecha']}</strong></p>
                    <p>{entrada['contenido']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aún no tienes entradas en tu diario. ¡Comienza escribiendo algo hoy!")

def mostrar_meditacion_guiada():
    """Muestra la funcionalidad de meditación guiada personalizada"""
    st.markdown("---")
    st.markdown(f"### 🧘 Meditación Personalizada para {st.session_state.nombre_usuario}")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("❌ Cerrar meditación"):
            st.session_state.mostrar_meditacion = False
            st.rerun()
    
    with col1:
        st.markdown("*Encuentra tu paz interior con ejercicios personalizados*")
    
    # Tipos de meditación
    tipo_meditacion = st.selectbox(
        "🎯 Selecciona tu práctica de hoy:",
        ["Respiración consciente", "Relajación profunda", "Autocompasión", "Transformación de emociones", "Concentración mental"],
        key="tipo_meditacion"
    )
    
    duracion = st.slider("⏰ Duración (minutos):", 5, 20, 10, key="duracion_meditacion")
    
    if st.button("🕯️ Comenzar mi sesión", type="primary", use_container_width=True):
        # Simulación de meditación guiada
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        frases_por_tipo = {
            "Respiración consciente": [
                f"Bienvenido/a {st.session_state.nombre_usuario}, vamos a despertar tu energía interior ⚡",
                "Inhala profundamente... siente cómo el aire llena tus pulmones",
                "Exhala lentamente... libera toda la tensión",
                "Tu respiración es tu ancla al momento presente"
            ],
            "Relajación profunda": [
                f"{st.session_state.nombre_usuario}, es momento de liberar toda tensión 🌊",
                "Relaja tus hombros... déjalos caer suavemente",
                "Siente cómo cada músculo se afloja y descansa",
                "Tu cuerpo merece este momento de paz"
            ],
            "Autocompasión": [
                f"{st.session_state.nombre_usuario}, mereces amor y comprensión 💗",
                "Háblate con la misma gentileza que le hablarías a un buen amigo",
                "Eres humano/a, y está bien no ser perfecto/a",
                "Tu corazón es tu refugio seguro"
            ]
        }
        
        frases = frases_por_tipo.get(tipo_meditacion, frases_por_tipo["Respiración consciente"])
        
        for i in range(duracion):
            progress = (i + 1) / duracion
            progress_bar.progress(progress)
            
            frase = frases[i % len(frases)]
            status_text.markdown(f"🧘 **{frase}**")
            
            time.sleep(1)  # En producción, esto sería más interactivo
        
        progress_bar.progress(1.0)
        status_text.markdown(f"✨ **¡Excelente {st.session_state.nombre_usuario}! Has completado tu meditación personalizada**")
        st.balloons()

def mostrar_seguimiento_humor():
    """Muestra el seguimiento del estado de ánimo"""
    st.markdown("---")
    st.markdown(f"### 📊 Seguimiento Emocional de {st.session_state.nombre_usuario}")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("❌ Cerrar seguimiento"):
            st.session_state.mostrar_seguimiento = False
            st.rerun()
    
    with col1:
        st.markdown("*Monitorea tu bienestar emocional a lo largo del tiempo*")
    
    # Simulación de datos de seguimiento
    if 'historial_emociones' not in st.session_state:
        st.session_state.historial_emociones = []
    
    # Registrar emoción actual si existe
    if 'emocion_actual' in st.session_state:
        fecha_hoy = time.strftime("%Y-%m-%d")
        
        # Verificar si ya se registró hoy
        if not any(entrada['fecha'] == fecha_hoy for entrada in st.session_state.historial_emociones):
            st.session_state.historial_emociones.append({
                'fecha': fecha_hoy,
                'emocion': st.session_state.emocion_actual,
                'timestamp': time.time()
            })
    
    # Mostrar resumen
    if st.session_state.historial_emociones:
        st.markdown("### 📈 Tu progreso emocional:")
        
        for entrada in st.session_state.historial_emociones[-7:]:  # Últimos 7 días
            st.markdown(f"**{entrada['fecha']}**: {entrada['emocion']}")
        
        # Insight personalizado
        total_entries = len(st.session_state.historial_emociones)
        st.info(f"🎯 {st.session_state.nombre_usuario}, has registrado tu estado emocional {total_entries} {'vez' if total_entries == 1 else 'veces'}. ¡Continúa con este gran hábito de autoconocimiento!")
    else:
        st.info(f"¡Hola {st.session_state.nombre_usuario}! Selecciona tu emoción actual arriba para comenzar tu seguimiento personal.")
    
    # Contenido principal de la app
    st.markdown("---")
    st.markdown("### 🧠 Herramientas de Bienestar")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>💭 Diario Emocional</h4>
            <p>Registra tus pensamientos y emociones diarias</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🧘 Meditación Guiada</h4>
            <p>Ejercicios de relajación y mindfulness</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📈 Seguimiento del Humor</h4>
            <p>Monitorea tu estado emocional a lo largo del tiempo</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sección de Música Terapéutica
    mostrar_musica_terapeutica()
    
    # Footer personalizado
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; margin-top: 50px;">
        <p>💚 {st.session_state.nombre_usuario}, cuidamos tu bienestar mental con dedicación</p>
        <p><small>Serenity App © 2024 - Tu compañera personal para el bienestar mental</small></p>
        <p><small>✨ Hecho con amor para tu crecimiento emocional</small></p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_musica_terapeutica():
    """Muestra la sección de música terapéutica personalizada"""
    st.markdown("---")
    st.markdown(f"### 🎵 Música Terapéutica para {st.session_state.nombre_usuario}")
    st.markdown("*Música generada especialmente para tu momento de bienestar*")
    
    # Recomendación basada en el estado emocional
    if 'emocion_actual' in st.session_state:
        recomendaciones = {
            "😊": ("🎹 Piano", "Celebra tu alegría con la hermosa Ballade pour Adeline"),
            "😔": ("🌊 Naturaleza", "Los sonidos naturales pueden reconfortar tu corazón"),
            "😰": ("🧘 Meditación", "Los cuencos tibetanos te ayudarán a encontrar calma"),
            "😡": ("🌌 Ambiental", "Música etérea para transformar esa energía"),
            "😴": ("🎹 Piano", "Melodías suaves para relajar tu mente"),
            "🤔": ("🧘 Meditación", "Sonidos que facilitan la introspección")
        }
        
        if st.session_state.emocion_actual in recomendaciones:
            tipo_rec, mensaje_rec = recomendaciones[st.session_state.emocion_actual]
            st.info(f"💡 **Recomendación personal**: {tipo_rec} - {mensaje_rec}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 🎹 Piano Clásico")
        st.markdown("*Ballade pour Adeline*")
        if st.button("🎼 Escuchar", key="piano_btn", use_container_width=True):
            with st.spinner(f"� Creando música especial para {st.session_state.nombre_usuario}..."):
                audio_data = generar_musica_relajante("piano", 30)
                st.audio(audio_data, format='audio/wav')
                st.success("🎵 Disfruta de esta obra maestra de Richard Clayderman")
    
    with col2:
        st.markdown("### 🌊 Sonidos Naturales")
        st.markdown("*Lluvia y viento suave*")
        if st.button("🌧️ Escuchar", key="natura_btn", use_container_width=True):
            with st.spinner("� Recreando la naturaleza para ti..."):
                audio_data = generar_musica_relajante("naturaleza", 30)
                st.audio(audio_data, format='audio/wav')
                st.success("� Conecta con la serenidad natural")
    
    with col3:
        st.markdown("### 🌌 Música Ambiental")
        st.markdown("*Drones armónicos*")
        if st.button("✨ Escuchar", key="ambient_btn", use_container_width=True):
            with st.spinner("🌟 Generando atmósfera etérea..."):
                audio_data = generar_musica_relajante("ambient", 30)
                st.audio(audio_data, format='audio/wav')
                st.success("� Sumérgete en la calma profunda")
    
    with col4:
        st.markdown("### 🧘 Meditación")
        st.markdown("*Cuencos tibetanos*")
        if st.button("🕉️ Escuchar", key="meditation_btn", use_container_width=True):
            with st.spinner("🎎 Sintonizando cuencos sagrados..."):
                audio_data = generar_musica_relajante("meditacion", 30)
                st.audio(audio_data, format='audio/wav')
                st.success("� Encuentra tu centro interior")

if __name__ == "__main__":
    main()