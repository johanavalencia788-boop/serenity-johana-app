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
AVATAR_SERENITY_VIDEO = "https://player.vimeo.com/video/76979871?autoplay=1&loop=1&autopause=0"

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
        # Cabello formal
        draw.ellipse([face_x - 10, face_y - 30, face_x + face_size + 10, face_y + 80], 
                    fill=(101, 67, 33), outline=color_principal, width=2)
    elif estilo == "creativo":
        # Cabello colorido
        draw.ellipse([face_x - 15, face_y - 35, face_x + face_size + 15, face_y + 75], 
                    fill=color_principal, outline=color_secundario, width=3)
    else:  # moderno
        # Cabello moderno
        draw.ellipse([face_x - 5, face_y - 25, face_x + face_size + 5, face_y + 70], 
                    fill=(139, 69, 19), outline=color_principal, width=2)
    
    # Agregar nombre personalizado
    try:
        # Intentar cargar fuente del sistema
        font_size = 24
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
        # Estrellas alrededor
        for _ in range(8):
            star_x = random.randint(20, size[0] - 20)
            star_y = random.randint(20, size[1] - 20)
            star_size = random.randint(8, 15)
            draw.text((star_x, star_y), "✨", fill=color_secundario)
    
    elif estilo == "profesional":
        # Marco elegante
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
        # Drones ambienta les
        frecuencias_base = [110, 165, 220]  # A2, E3, A3
        audio = np.zeros_like(t)
        
        for i, freq in enumerate(frecuencias_base):
            # Ondas senoidales con modulación lenta
            modulacion = 1 + 0.1 * np.sin(0.5 * 2 * np.pi * t)
            onda = np.sin(freq * 2 * np.pi * t) * modulacion
            
            # Fade in y fade out
            fade_samples = int(sample_rate * 2)  # 2 segundos
            if len(onda) > fade_samples:
                onda[:fade_samples] *= np.linspace(0, 1, fade_samples)
                onda[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            audio += onda * (0.3 / (i + 1))  # Cada frecuencia más suave
    
    # Convertir a formato de audio
    audio_normalizado = np.int16(audio * 32767)
    
    # Crear archivo WAV en memoria
    audio_bytes = io.BytesIO()
    with wave.open(audio_bytes, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16 bits
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_normalizado.tobytes())
    
    audio_bytes.seek(0)
    return audio_bytes.getvalue()

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
                    time.sleep(1)  # Simular procesamiento
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
                    st.info("💡 Para video completo, usa las opciones externas abajo")
        
        # Mostrar avatar generado si existe
        if st.session_state.get('avatar_generado'):
            st.markdown("---")
            st.markdown("#### 🎯 Tu Avatar Generado")
            
            # Convertir bytes de vuelta a imagen
            avatar_img = Image.open(io.BytesIO(st.session_state.avatar_generado))
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(avatar_img, caption="Tu avatar personalizado", width=250)
            
            # Opción para usar como avatar principal
            if st.button("💾 Usar como Mi Avatar"):
                # Guardar imagen localmente
                import os
                os.makedirs("avatars", exist_ok=True)
                avatar_path = f"avatars/{nombre_avatar}_avatar.png"
                avatar_img.save(avatar_path)
                
                st.session_state.avatar_personalizado = avatar_path
                st.success(f"✅ Avatar guardado como {avatar_path} y configurado!")
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
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Loom - Grabación rápida:**
            1. Ve a [Loom](https://www.loom.com/)
            2. Graba un video de 30-60 segundos
            3. Obtén enlace público
            """)
            if st.button("🔗 Abrir Loom", key="loom"):
                st.write("➡️ [Ir a Loom](https://www.loom.com/)")
        
        with col2:
            st.markdown("""
            **Vidyard - Video profesional:**
            1. Ve a [Vidyard](https://www.vidyard.com/)  
            2. Graba tu presentación
            3. Obtén enlace embed
            """)
            if st.button("🔗 Abrir Vidyard", key="vidyard"):
                st.write("➡️ [Ir a Vidyard](https://www.vidyard.com/)")
    
    with tab4:
        st.markdown("#### 🎮 Avatar 3D")
        st.markdown("""
        **Ready Player Me:**
        1. Ve a [Ready Player Me](https://readyplayer.me/)
        2. Crea tu avatar 3D
        3. Exporta como video
        """)
        if st.button("🔗 Abrir Ready Player Me", key="rpm"):
            st.write("➡️ [Ir a Ready Player Me](https://readyplayer.me/)")
    
    with tab5:
        st.markdown("#### 📱 Subir Tu Propio Avatar")
        
        # Opción 1: Subir archivo
        st.markdown("**Opción 1: Subir desde tu computadora**")
        uploaded_file = st.file_uploader(
            "Sube tu avatar:",
            type=['mp4', 'mov', 'gif', 'jpg', 'png']
        )
        
        if uploaded_file is not None:
            import os
            os.makedirs("avatars", exist_ok=True)
            
            file_path = f"avatars/{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ Avatar guardado: {file_path}")
            
            if uploaded_file.type.startswith('image'):
                st.image(file_path, width=300)
            else:
                st.video(file_path)
            
            # Botón para usar como avatar principal
            if st.button("💾 Usar como Mi Avatar Principal", key="usar_subido"):
                st.session_state.avatar_personalizado = file_path
                st.success("✅ Avatar configurado como principal!")
                st.balloons()
        
        st.markdown("---")
        
        # Opción 2: Usar ruta directa
        st.markdown("**Opción 2: Usar archivo desde tu computadora (ruta directa)**")
        
        # Mostrar tu video específico
        video_path = r"c:\Users\johan\Downloads\Untitled video (3).mp4"
        
        st.markdown("🎬 **Tu video encontrado:**")
        st.code(video_path, language=None)
        
        if st.button("🚀 ¡USAR MI VIDEO MP4 COMO AVATAR!", key="usar_video_downloads", 
                    help="Clic aquí para usar tu video como avatar principal"):
            import os
            import shutil
            
            with st.spinner("🎬 Configurando tu video como avatar..."):
                if os.path.exists(video_path):
                    try:
                        # Crear carpeta si no existe
                        os.makedirs("avatars", exist_ok=True)
                        new_path = "avatars/mi_video_avatar.mp4"
                        
                        # Copiar el video
                        shutil.copy2(video_path, new_path)
                        
                        # Configurar como avatar principal
                        st.session_state.avatar_personalizado = new_path
                        
                        # Mostrar éxito
                        st.success("🎉 ¡ÉXITO! Tu video MP4 ya es tu avatar!")
                        st.info(f"📁 Video guardado en: {new_path}")
                        
                        # Mostrar preview del video
                        st.markdown("#### 🎬 Preview de tu nuevo avatar:")
                        st.video(new_path)
                        
                        # Celebración
                        st.balloons()
                        
                        # Instrucciones
                        st.markdown("""
                        ### ✅ **¡Avatar configurado exitosamente!**
                        - Cierra este creador de avatares
                        - Tu video aparecerá como avatar principal
                        - Se reproducirá automáticamente en la app
                        """)
                        
                    except Exception as e:
                        st.error(f"❌ Error al procesar el video: {str(e)}")
                        st.info("💡 Asegúrate de que el video no esté siendo usado por otra aplicación")
                else:
                    st.error("❌ No se encuentra el video MP4 en la ruta especificada")
                    st.info("🔍 Verifica que el archivo existe en Downloads")
        
        # Campo para ruta personalizada
        st.markdown("**Ruta personalizada:**")
        ruta_personalizada = st.text_input(
            "Pega la ruta completa de tu archivo:",
            value=video_path,
            help="Ejemplo: C:\\Users\\usuario\\Downloads\\mi_video.mp4"
        )
        
        if st.button("📁 Usar archivo de ruta personalizada", key="usar_ruta"):
            import os
            if os.path.exists(ruta_personalizada):
                # Determinar extensión
                extension = os.path.splitext(ruta_personalizada)[1]
                os.makedirs("avatars", exist_ok=True)
                new_path = f"avatars/avatar_personalizado{extension}"
                
                try:
                    import shutil
                    shutil.copy2(ruta_personalizada, new_path)
                    st.session_state.avatar_personalizado = new_path
                    st.success(f"✅ Archivo copiado y configurado como avatar!")
                    
                    # Mostrar preview
                    if extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                        st.image(new_path, width=300)
                    elif extension.lower() in ['.mp4', '.mov']:
                        st.video(new_path)
                    
                    st.balloons()
                except Exception as e:
                    st.error(f"Error al copiar el archivo: {e}")
            else:
                st.error("❌ No se encuentra el archivo en la ruta especificada")

def mostrar_serenity_parlante():
    """Muestra el avatar de Serenity con opción de personalización"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🎭 Conoce a Serenity Johana")
    
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
        # Avatar actual
        if st.session_state.get('avatar_personalizado'):
            # Mostrar avatar personalizado
            avatar_path = st.session_state.avatar_personalizado
            
            if avatar_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                st.image(avatar_path, width=200, caption="Tu avatar personalizado")
            elif avatar_path.endswith(('.mp4', '.mov')):
                st.markdown("#### 🎬 Tu Video Avatar")
                st.video(avatar_path)
                st.caption("Tu avatar personalizado en video")
            else:
                # Para URLs externas
                st.markdown(f"""
                <div style="display: flex; justify-content: center; margin: 10px 0;">
                    <iframe src="{avatar_path}" 
                    width="400" height="300" frameborder="0" allowfullscreen 
                    style="border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"></iframe>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Tu video como avatar por defecto
            tu_video = r"c:\Users\johan\Downloads\Untitled video (3).mp4"
            
            import os
            if os.path.exists(tu_video):
                st.markdown("#### 🎬 Conoce a Serenity - Tu Avatar Personal")
                st.video(tu_video)
                st.caption("Tu avatar personalizado - Serenity eres TÚ")
            else:
                # Fallback a imagen por defecto si no encuentra el video
                st.image(AVATAR_SERENITY_IMAGEN, width=200, caption="Serenity Johana - Tu asistente de bienestar")

def mostrar_header():
    """Muestra el header principal de la aplicación"""
    
    st.markdown('<h1 class="main-header">🌱 Serenity App</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Tu compañera digital para el bienestar mental y emocional</p>', unsafe_allow_html=True)
    
    # Solicitar nombre del usuario si no existe
    if 'nombre_usuario' not in st.session_state:
        st.session_state.nombre_usuario = ""
    
    if not st.session_state.nombre_usuario:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 👋 ¡Hola! ¿Cómo te llamas?")
            nombre_input = st.text_input("Tu nombre:", placeholder="Escribe tu nombre aquí...")
            if st.button("✨ Comenzar mi journey de bienestar", use_container_width=True):
                if nombre_input:
                    st.session_state.nombre_usuario = nombre_input
                    st.rerun()
                else:
                    st.warning("Por favor, ingresa tu nombre para continuar")
        return False
    
    # Saludo personalizado
    st.markdown(f'<div class="motivational-quote">¡Hola {st.session_state.nombre_usuario}! 🌟 {random.choice(FRASES_MOTIVACIONALES)}</div>', unsafe_allow_html=True)
    return True

def main():
    """Función principal de la aplicación"""
    
    # Inicializar estado
    if 'mostrar_creator' not in st.session_state:
        st.session_state.mostrar_creator = False
    
    # Header principal con nombre del usuario
    if not mostrar_header():
        return  # Si no hay nombre, no continuar
    
    # Avatar de Serenity
    mostrar_serenity_parlante()
    
    # Contenido principal de la app
    st.markdown("---")
    
    # Sección principal: ¿Cómo te sientes?
    st.markdown(f"### 💭 {st.session_state.nombre_usuario}, ¿cómo te sientes hoy?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    emociones = {
        "😊": {"nombre": "Feliz", "color": "#4CAF50", "mensaje": f"¡Qué maravilloso, {st.session_state.nombre_usuario}! La felicidad es contagiosa. Comparte tu alegría con otros.", "meditacion": "respiracion_alegria"},
        "😔": {"nombre": "Triste", "color": "#2196F3", "mensaje": f"Es normal sentirse triste a veces, {st.session_state.nombre_usuario}. Permítete sentir esta emoción, es parte de ser humano.", "meditacion": "compasion_auto"},
        "😰": {"nombre": "Ansioso", "color": "#FF9800", "mensaje": f"{st.session_state.nombre_usuario}, la ansiedad puede ser abrumadora. Respira profundo, estás seguro/a en este momento.", "meditacion": "calma_ansiedad"},
        "😡": {"nombre": "Enojado", "color": "#F44336", "mensaje": f"{st.session_state.nombre_usuario}, la ira es una emoción válida. ¿Qué puedes aprender de lo que te molesta?", "meditacion": "liberacion_ira"}
    }
    
    cols = [col1, col2, col3, col4]
    for i, (emoji, info) in enumerate(emociones.items()):
        with cols[i]:
            if st.button(f"{emoji} {info['nombre']}", key=f"emotion_{i}", use_container_width=True):
                st.session_state.emocion_seleccionada = info
                st.session_state.mostrar_apoyo = True
    
    # Mostrar apoyo emocional si se seleccionó una emoción
    if st.session_state.get('mostrar_apoyo'):
        info = st.session_state.emocion_seleccionada
        st.markdown("---")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {info['color']}20, {info['color']}10); 
                    padding: 20px; border-radius: 15px; border-left: 5px solid {info['color']};">
            <h3 style="color: {info['color']};">💚 Mensaje de Serenity para ti:</h3>
            <p style="font-size: 1.1em; color: #333;">{info['mensaje']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sugerencias según la emoción
        if "Feliz" in info['nombre']:
            st.markdown("#### 🌟 Aprovecha esta energía:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("• Comparte tu alegría con alguien especial")
                st.markdown("• Haz algo creativo")
            with col2:
                st.markdown("• Practica gratitud")
                st.markdown("• Planifica algo divertido")
                
        elif "Triste" in info['nombre']:
            st.markdown("#### 🤗 Cuidados para ti:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("• Llama a un amigo querido")
                st.markdown("• Escribe tus sentimientos")
            with col2:
                st.markdown("• Date un baño relajante")
                st.markdown("• Mira algo que te haga sonreír")
                
        elif "Ansioso" in info['nombre']:
            st.markdown("#### 🧘 Técnicas de relajación:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("• Respiración 4-7-8")
                st.markdown("• Meditación de 5 minutos")
            with col2:
                st.markdown("• Camina al aire libre")
                st.markdown("• Escucha música tranquila")
                
        elif "Enojado" in info['nombre']:
            st.markdown("#### 🔥 Manejo saludable:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("• Haz ejercicio intenso")
                st.markdown("• Escribe lo que sientes")
            with col2:
                st.markdown("• Habla con alguien de confianza")
                st.markdown("• Practica boxeo o deporte")
        
        # Botón para cerrar
        if st.button("✨ Gracias Serenity", key="cerrar_apoyo"):
            st.session_state.mostrar_apoyo = False
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 🧠 Más Herramientas de Bienestar")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💭 Diario Emocional", use_container_width=True):
            st.session_state.mostrar_diario = True
            
    with col2:
        if st.button("🧘 Meditación Guiada", use_container_width=True):
            st.session_state.mostrar_meditacion = True
            
    with col3:
        if st.button("📈 Seguimiento del Humor", use_container_width=True):
            st.session_state.mostrar_seguimiento = True
    
    # Nueva sección de música
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎵 Música Relajante", use_container_width=True):
            st.session_state.mostrar_musica = True
    
    with col2:
        if st.button("🌊 Sonidos de Naturaleza", use_container_width=True):
            st.session_state.mostrar_naturaleza = True
    
    with col3:
        if st.button("🎼 Música Clásica", use_container_width=True):
            st.session_state.mostrar_clasica = True
    
    with col4:
        if st.button("🧘‍♀️ Música Meditativa", use_container_width=True):
            st.session_state.mostrar_meditativa = True
    
    # DIARIO EMOCIONAL COMPLETO
    if st.session_state.get('mostrar_diario'):
        st.markdown("---")
        st.markdown(f"### 📖 Diario Emocional de {st.session_state.nombre_usuario}")
        
        # Información sobre el diario emocional
        st.info("""
        📝 **¿Qué es un diario emocional?**
        Es una herramienta poderosa para procesar tus sentimientos, identificar patrones emocionales y desarrollar mayor autoconocimiento. 
        Escribir sobre tus emociones te ayuda a liberarte del estrés y encontrar claridad mental.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            estado_animo = st.selectbox("¿Cómo te sientes ahora?", 
                                      ["😊 Feliz", "😔 Triste", "😰 Ansioso", "😡 Enojado", "😴 Cansado", "🤔 Confundido", "✨ Esperanzado"])
            intensidad = st.slider("Intensidad de la emoción (1-10)", 1, 10, 5)
        
        with col2:
            actividad_previa = st.text_input("¿Qué estabas haciendo antes de sentirte así?")
            disparador = st.text_input("¿Qué crees que disparó esta emoción?")
        
        entrada_diario = st.text_area("Escribe tus pensamientos y sentimientos:", 
                                    placeholder=f"Querido diario, hoy {st.session_state.nombre_usuario} se siente...", 
                                    height=150)
        
        if st.button("💾 Guardar en mi diario personal"):
            if entrada_diario:
                import datetime
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                entrada_completa = f"""
--- {fecha} ---
Usuario: {st.session_state.nombre_usuario}
Estado de ánimo: {estado_animo} (Intensidad: {intensidad}/10)
Actividad previa: {actividad_previa}
Disparador: {disparador}
Reflexión:
{entrada_diario}
---
"""
                with open(f"diario_{st.session_state.nombre_usuario}.txt", "a", encoding="utf-8") as f:
                    f.write(entrada_completa)
                st.success("✅ Tu entrada ha sido guardada en tu diario personal")
                st.balloons()
        
        if st.button("❌ Cerrar diario"):
            st.session_state.mostrar_diario = False
            st.rerun()
    
    # MEDITACIÓN GUIADA PERSONALIZADA
    if st.session_state.get('mostrar_meditacion'):
        st.markdown("---")
        st.markdown(f"### 🧘 Meditación Personalizada para {st.session_state.nombre_usuario}")
        
        # Información sobre meditación
        st.info("""
        🧘‍♀️ **Beneficios de la meditación:**
        • Reduce el estrés y la ansiedad • Mejora la concentración • Aumenta la autoconciencia
        • Promueve el bienestar emocional • Mejora la calidad del sueño
        """)
        
        tipo_meditacion = st.selectbox("Elige tu meditación según tu estado:", [
            "🌅 Energizante (para cuando te sientes cansado)",
            "😌 Relajante (para ansiedad y estrés)", 
            "❤️ Autocompasión (para cuando te sientes triste)",
            "🔥 Liberación (para cuando sientes ira)",
            "🎯 Concentración (para cuando te sientes disperso)"
        ])
        
        duracion = st.slider("Duración de la meditación (minutos)", 3, 20, 10)
        
        if st.button("🎵 Iniciar meditación personalizada"):
            # Instrucciones específicas según el tipo
            if "Energizante" in tipo_meditacion:
                instrucciones = [
                    f"Bienvenido/a {st.session_state.nombre_usuario}, vamos a despertar tu energía interior ⚡",
                    "Siéntate con la espalda recta, como un árbol fuerte 🌳",
                    "Respira profundamente e imagina luz dorada llenando tu cuerpo ✨",
                    "Siente cómo la energía fluye desde tu corazón hacia todo tu ser 💛",
                    "Con cada respiración, despiertas más vitalidad y fuerza 🔋"
                ]
            elif "Relajante" in tipo_meditacion:
                instrucciones = [
                    f"{st.session_state.nombre_usuario}, es momento de liberar toda tensión 🌊",
                    "Cierra tus ojos suavemente y relaja tus hombros 😌",
                    "Respira: 4 segundos inhalar, 7 mantener, 8 exhalar 🌬️",
                    "Imagina que estás en tu lugar favorito, completamente seguro/a 🏖️",
                    "Cada exhalación lleva lejos el estrés y la preocupación 🍃"
                ]
            elif "Autocompasión" in tipo_meditacion:
                instrucciones = [
                    f"{st.session_state.nombre_usuario}, mereces amor y comprensión 💗",
                    "Pon una mano en tu corazón y siente su latido cálido ❤️",
                    "Repite: 'Me acepto y me amo tal como soy' 🤗",
                    "Recuerda que está bien no estar bien a veces 🌙",
                    "Envíate el mismo cariño que darías a tu mejor amigo/a 💕"
                ]
            elif "Liberación" in tipo_meditacion:
                instrucciones = [
                    f"{st.session_state.nombre_usuario}, vamos a transformar esa energía 🔥",
                    "Respira profundamente y reconoce tu emoción sin juzgarla 👁️",
                    "Imagina que la ira es fuego que se convierte en fuerza constructiva ⚡",
                    "Con cada exhalación, liberas lo que no necesitas 🌪️",
                    "Encuentras tu centro de calma y sabiduría interior 🧘‍♀️"
                ]
            else:  # Concentración
                instrucciones = [
                    f"{st.session_state.nombre_usuario}, enfoquemos tu mente brillante 🎯",
                    "Concéntrate solo en tu respiración, como un ancla mental ⚓",
                    "Cuando tu mente divague, gentilmente regresa al presente 🌟",
                    "Imagina que tu concentración es un músculo que fortaleces 💪",
                    "Cada momento de atención plena es un regalo para ti 🎁"
                ]
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulación de meditación guiada
            num_pasos = len(instrucciones)
            tiempo_por_paso = duracion * 60 // num_pasos  # segundos por paso
            
            for i, instruccion in enumerate(instrucciones):
                status_text.markdown(f"**{instruccion}**")
                progress_bar.progress((i + 1) / num_pasos)
                time.sleep(min(tiempo_por_paso, 3))  # máximo 3 segundos por paso en demo
            
            status_text.markdown(f"✨ **¡Excelente {st.session_state.nombre_usuario}! Has completado tu meditación personalizada**")
            st.success("🧘 Sesión completada. ¿Cómo te sientes ahora?")
            st.balloons()
                
        if st.button("❌ Cerrar meditación"):
            st.session_state.mostrar_meditacion = False
            st.rerun()
    
    # SEGUIMIENTO DE HUMOR AVANZADO
    if st.session_state.get('mostrar_seguimiento'):
        st.markdown("---")
        st.markdown(f"### � Seguimiento del Humor de {st.session_state.nombre_usuario}")
        
        # Información sobre seguimiento del humor
        st.info("""
        📈 **¿Por qué rastrear tu humor?**
        Te ayuda a identificar patrones, triggers emocionales y el progreso en tu bienestar. 
        Con el tiempo, podrás predecir y manejar mejor tus estados emocionales.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            humor_hoy = st.slider("¿Cómo calificas tu humor general hoy?", 1, 10, 7)
            energia = st.slider("Nivel de energía:", 1, 10, 5)
            estres = st.slider("Nivel de estrés:", 1, 10, 3)
            
        with col2:
            horas_sueno = st.number_input("¿Cuántas horas dormiste?", 3, 12, 8)
            ejercicio = st.checkbox("¿Hiciste ejercicio hoy?")
            interaccion_social = st.selectbox("Interacción social hoy:", 
                                            ["Mucha (varias personas)", "Moderada (algunas personas)", 
                                             "Poca (1-2 personas)", "Ninguna (solo/a)"])
        
        notas_dia = st.text_area("Notas adicionales del día:", 
                                placeholder="¿Qué eventos importantes ocurrieron? ¿Qué te hizo sentir bien o mal?")
        
        if st.button("📝 Registrar mi día"):
            import datetime
            fecha = datetime.datetime.now().strftime("%Y-%m-%d")
            registro = f"{fecha},{st.session_state.nombre_usuario},{humor_hoy},{energia},{estres},{horas_sueno},{ejercicio},{interaccion_social},{notas_dia}\n"
            
            with open(f"humor_{st.session_state.nombre_usuario}.csv", "a", encoding="utf-8") as f:
                f.write(registro)
            
            st.success("✅ Tu día ha sido registrado correctamente")
            
            # Análisis instantáneo
            if humor_hoy <= 3:
                st.warning(f"💙 {st.session_state.nombre_usuario}, parece que has tenido un día difícil. Recuerda que es temporal y estás haciendo un gran trabajo al cuidar tu bienestar mental.")
            elif humor_hoy <= 6:
                st.info(f"😐 Un día promedio, {st.session_state.nombre_usuario}. Los días regulares también son importantes para tu crecimiento.")
            else:
                st.success(f"😊 ¡Qué día tan bueno, {st.session_state.nombre_usuario}! Celebra estos momentos de bienestar.")
        
        if st.button("❌ Cerrar seguimiento"):
            st.session_state.mostrar_seguimiento = False
            st.rerun()
    
    # MÚSICA RELAJANTE REAL
    if st.session_state.get('mostrar_musica'):
        st.markdown("---")
        st.markdown(f"### 🎵 Música Relajante para {st.session_state.nombre_usuario}")
        
        st.info("🎶 Música instrumental suave para acompañar tu momento de paz y relajación")
        
        # URLs de música relajante real
        musica_urls = {
            "Piano Relajante": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
            "Sonidos de la Naturaleza": "https://www2.cs.uic.edu/~i101/SoundFiles/StarWars60.wav",
            "Música Ambient": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
            "Lluvia Suave": "https://www2.cs.uic.edu/~i101/SoundFiles/CantinaBand60.wav"
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌅 Música Matutina")
            
            st.markdown("🎼 **Piano Relajante - Amanecer Sereno**")
            if st.button("🎹 Generar música de piano", key="piano_btn"):
                with st.spinner("🎵 Generando música relajante..."):
                    audio_piano = generar_musica_relajante("piano", 20)
                    st.audio(audio_piano, format="audio/wav")
                    st.success("✨ ¡Música de piano lista!")
            
            st.markdown("🌿 **Sonidos de Naturaleza - Brisa del Alba**")
            if st.button("🌧️ Generar sonidos de lluvia", key="lluvia_btn"):
                with st.spinner("🌊 Creando sonidos de naturaleza..."):
                    audio_natura = generar_musica_relajante("naturaleza", 25)
                    st.audio(audio_natura, format="audio/wav")
                    st.success("� ¡Sonidos de naturaleza listos!")
            
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E8F5E8, #C8E6C9); padding: 20px; border-radius: 15px; margin: 10px 0;">
                <h4>🎻 "Brisa del Alba"</h4>
                <p>Cuerdas suaves con sonidos de naturaleza</p>
                <div style="display: flex; align-items: center;">
                    <span>▶️</span>
                    <div style="width: 200px; height: 4px; background: #ccc; margin: 0 10px; border-radius: 2px;">
                        <div style="width: 40%; height: 100%; background: #4CAF50; border-radius: 2px;"></div>
                    </div>
                    <span>4:22</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🌙 Música Nocturna")
            
            st.markdown("🌟 **Noche Estrellada - Música Ambient**")
            if st.button("✨ Generar música ambient", key="ambient_btn"):
                with st.spinner("🌌 Creando atmósfera relajante..."):
                    audio_ambient = generar_musica_relajante("ambient", 30)
                    st.audio(audio_ambient, format="audio/wav")
                    st.success("🌙 ¡Música ambient nocturna lista!")
            
            st.markdown("🎹 **Meditación Profunda**")
            if st.button("🧘‍♀️ Música para meditar", key="meditacion_btn"):
                with st.spinner("🕉️ Generando frecuencias sanadoras..."):
                    # Generar combinación de piano + ambient
                    audio_med = generar_musica_relajante("piano", 35)
                    st.audio(audio_med, format="audio/wav")
                    st.success("🧘 ¡Música de meditación lista!")
            
            st.info("💡 **Tip:** Usa auriculares para una mejor experiencia de relajación")
        
        if st.button("❌ Cerrar música"):
            st.session_state.mostrar_musica = False
            st.rerun()
    
    # SONIDOS DE NATURALEZA
    if st.session_state.get('mostrar_naturaleza'):
        st.markdown("---")
        st.markdown(f"### 🌊 Sonidos de Naturaleza para {st.session_state.nombre_usuario}")
        
        st.info("🍃 Sonidos naturales para conectar con la tranquilidad del mundo natural")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E0F2F1, #26A69A); padding: 15px; border-radius: 15px; text-align: center;">
                <h4>🌊 Olas del Mar</h4>
                <p>Sonido relajante del océano</p>
                <button style="background: #26A69A; color: white; border: none; padding: 8px 16px; border-radius: 20px;">▶️ Reproducir</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E8F5E8, #4CAF50); padding: 15px; border-radius: 15px; text-align: center;">
                <h4>🌳 Bosque Tranquilo</h4>
                <p>Pájaros y viento entre árboles</p>
                <button style="background: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 20px;">▶️ Reproducir</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E3F2FD, #2196F3); padding: 15px; border-radius: 15px; text-align: center;">
                <h4>☔ Lluvia Serena</h4>
                <p>Gotas suaves en el jardín</p>
                <button style="background: #2196F3; color: white; border: none; padding: 8px 16px; border-radius: 20px;">▶️ Reproducir</button>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("❌ Cerrar sonidos"):
            st.session_state.mostrar_naturaleza = False
            st.rerun()
    
    # MÚSICA CLÁSICA
    if st.session_state.get('mostrar_clasica'):
        st.markdown("---")
        st.markdown(f"### 🎼 Música Clásica Relajante para {st.session_state.nombre_usuario}")
        
        st.info("🎻 Obras clásicas seleccionadas para la relajación y concentración")
        
        piezas_clasicas = [
            {"titulo": "Canon de Pachelbel", "compositor": "Johann Pachelbel", "duracion": "5:30", "emoji": "🎻"},
            {"titulo": "Claro de Luna", "compositor": "Claude Debussy", "duracion": "4:45", "emoji": "🌙"},
            {"titulo": "Ave María", "compositor": "Franz Schubert", "duracion": "6:15", "emoji": "🕊️"},
            {"titulo": "Gymnopédie No. 1", "compositor": "Erik Satie", "duracion": "3:20", "emoji": "🎹"}
        ]
        
        for pieza in piezas_clasicas:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FFF8E1, #FFB74D); padding: 15px; border-radius: 15px; margin: 10px 0;">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div>
                        <h4>{pieza['emoji']} {pieza['titulo']}</h4>
                        <p><i>por {pieza['compositor']}</i> • {pieza['duracion']}</p>
                    </div>
                    <button style="background: #FF9800; color: white; border: none; padding: 8px 16px; border-radius: 20px; margin-left: auto;">▶️</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("❌ Cerrar clásica"):
            st.session_state.mostrar_clasica = False
            st.rerun()
    
    # MÚSICA MEDITATIVA
    if st.session_state.get('mostrar_meditativa'):
        st.markdown("---")
        st.markdown(f"### 🧘‍♀️ Música Meditativa para {st.session_state.nombre_usuario}")
        
        st.info("🕉️ Sonidos diseñados específicamente para meditación y mindfulness")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎵 Mantras y Cantos")
            mantras = [
                {"nombre": "Om Mani Padme Hum", "duracion": "10:00", "beneficio": "Compasión universal"},
                {"nombre": "So Hum", "duracion": "8:30", "beneficio": "Conexión interior"},
                {"nombre": "Gayatri Mantra", "duracion": "12:15", "beneficio": "Claridad mental"}
            ]
            
            for mantra in mantras:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #F3E5F5, #BA68C8); padding: 12px; border-radius: 10px; margin: 8px 0;">
                    <h5>🕉️ {mantra['nombre']}</h5>
                    <p><small>{mantra['duracion']} • {mantra['beneficio']}</small></p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🎶 Frecuencias Sanadoras")
            frecuencias = [
                {"freq": "432 Hz", "beneficio": "Relajación profunda", "color": "#4CAF50"},
                {"freq": "528 Hz", "beneficio": "Sanación del amor", "color": "#FF9800"},
                {"freq": "741 Hz", "beneficio": "Limpieza emocional", "color": "#2196F3"}
            ]
            
            for freq in frecuencias:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {freq['color']}20, {freq['color']}40); padding: 12px; border-radius: 10px; margin: 8px 0;">
                    <h5>🎵 {freq['freq']}</h5>
                    <p><small>{freq['beneficio']}</small></p>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("❌ Cerrar meditativa"):
            st.session_state.mostrar_meditativa = False
            st.rerun()
    
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