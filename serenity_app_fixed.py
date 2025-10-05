import streamlit as st
import time
from unidecode import unidecode
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import io
import colorsys

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