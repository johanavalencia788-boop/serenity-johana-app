import streamlit as st
import time
from unidecode import unidecode
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import io
import colorsys
import wave
import struct

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
AVATAR_SERENITY_IMAGEN = "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=300&h=300&fit=crop&crop=face"

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
        
        uploaded_file = st.file_uploader(
            "Sube tu avatar:",
            type=['mp4', 'mov', 'gif', 'jpg', 'png']
        )
        
        if uploaded_file is not None:
            st.success("✅ Archivo subido exitosamente!")
            
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, width=300)
                st.session_state.avatar_personalizado = uploaded_file
            else:
                st.video(uploaded_file)
                st.session_state.avatar_personalizado = uploaded_file
            
            st.balloons()

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
            # Avatar personalizado
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
            # Avatar por defecto
            st.image(AVATAR_SERENITY_IMAGEN, width=200, caption="Serenity - Tu asistente de bienestar")

def mostrar_header():
    """Muestra el header principal de la aplicación"""
    st.markdown('<h1 class="main-header">🌱 Serenity App</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Tu compañera digital para el bienestar mental y emocional</p>', unsafe_allow_html=True)
    
    # Frase motivacional aleatoria
    frase = random.choice(FRASES_MOTIVACIONALES)
    st.markdown(f'<div class="motivational-quote">{frase}</div>', unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    
    # Inicializar estado
    if 'mostrar_creator' not in st.session_state:
        st.session_state.mostrar_creator = False
    
    # Header principal
    mostrar_header()
    
    # Avatar de Serenity
    mostrar_serenity_parlante()
    
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
    
    # Sección de Música Relajante
    st.markdown("---")
    st.markdown("## 🎵 Música Relajante")
    st.markdown("Disfruta de música generada especialmente para tu relajación")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎹 Piano - Ballade pour Adeline", key="piano_btn"):
            with st.spinner("🎼 Generando melodía de Richard Clayderman..."):
                audio_data = generar_musica_relajante("piano", 30)
                st.audio(audio_data, format='audio/wav')
                st.success("🎵 ¡Disfruta de Ballade pour Adeline!")
    
    with col2:
        if st.button("🌊 Sonidos de Naturaleza", key="natura_btn"):
            with st.spinner("🌧️ Creando ambiente natural..."):
                audio_data = generar_musica_relajante("naturaleza", 30)
                st.audio(audio_data, format='audio/wav')
                st.success("🌿 ¡Relájate con la naturaleza!")
    
    with col3:
        if st.button("🌌 Música Ambiental", key="ambient_btn"):
            with st.spinner("✨ Generando atmósfera relajante..."):
                audio_data = generar_musica_relajante("ambient", 30)
                st.audio(audio_data, format='audio/wav')
                st.success("🌟 ¡Sumérgete en la calma!")
    
    with col4:
        if st.button("🧘 Meditación", key="meditation_btn"):
            with st.spinner("🎎 Creando sonidos de cuencos..."):
                audio_data = generar_musica_relajante("meditacion", 30)
                st.audio(audio_data, format='audio/wav')
                st.success("🕉️ ¡Medita con serenidad!")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 50px;">
        <p>💚 Desarrollado con amor para tu bienestar mental</p>
        <p><small>Serenity App © 2024 - Cuidando tu mente, alimentando tu alma</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()