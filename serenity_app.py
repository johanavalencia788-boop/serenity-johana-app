import streamlit as st
import random
from unidecode import unidecode
import base64
import io
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# GENERADOR DE AVATAR INTEGRADO
# Avatar por defecto (será reemplazado por el generado)
AVATAR_SERENITY_VIDEO = "https://streamable.com/ez13ge"
AVATAR_SERENITY_IMAGEN = "https://cdn-icons-png.flaticon.com/512/4140/4140051.png"

# URLs de servicios para crear avatares
SERVICIOS_AVATAR = {
    "d-id": "https://www.d-id.com/",
    "synthesia": "https://www.synthesia.io/",
    "avatar_maker": "https://avatarmaker.com/",
    "bitmoji": "https://www.bitmoji.com/",
    "memoji": "https://support.apple.com/es-es/102854",
    "ready_player_me": "https://readyplayer.me/",
    "loom": "https://www.loom.com/",
    "vidyard": "https://www.vidyard.com/"
}

# VIDEOS DE EJERCICIO EN ESPAÑOL - URLs FUNCIONALES
VIDEO_RESPIRACION = "https://www.youtube.com/embed/cEeWLDMDqpk"  # Meditación 5 min
VIDEO_MEDITACION = "https://www.youtube.com/embed/jPgBOk8Za9U"   # Sonidos relajantes

# Videos de relajación en ESPAÑOL - URLs FUNCIONALES
VIDEOS_RELAJACION = [
    "https://www.youtube.com/embed/UfcAVejvCgE",  # Música relajante
    "https://www.youtube.com/embed/jPgBOk8Za9U",  # Sonidos naturaleza
    "https://www.youtube.com/embed/cEeWLDMDqpk"   # Meditación guiada
]

# Videos de ejercicios en español - URLs FUNCIONALES
videos_ejercicios_espanol = [
    "https://www.youtube.com/embed/UfcAVejvCgE",  # Música relajante
    "https://www.youtube.com/embed/jPgBOk8Za9U",  # Sonidos para yoga
    "https://www.youtube.com/embed/cEeWLDMDqpk"   # Meditación para ejercicios
]

# SONIDOS DE RELAJACIÓN EN ESPAÑOL - URLs FUNCIONALES
SONIDOS_RELAJACION = [
    "https://www.youtube.com/embed/UfcAVejvCgE",  # Música relajante
    "https://www.youtube.com/embed/jPgBOk8Za9U",  # Sonidos naturaleza
    "https://www.youtube.com/embed/cEeWLDMDqpk"   # Meditación
]

# Frases que indican alegría
frases_alegria = [
    "estoy muy contento", "me siento genial", "qué día tan bueno", "estoy feliz",
    "tengo mucha energía", "qué alegría", "estoy emocionado", "estoy emocionada", 
    "super contento", "super feliz", "muy bien", "excelente", "fantástico"
]

# Mensajes motivacionales en ESPAÑOL ESTRICTO
mensajes_motivacionales = [
    "Eres importante y tu vida tiene mucho valor.",
    "No estás solo, siempre hay alguien dispuesto a escucharte.",
    "Cada día es una nueva oportunidad para sentirte mejor.",
    "Tus emociones son válidas, permítete sentirlas sin juicio.",
    "Pedir ayuda cuando la necesites es un acto de mucha valentía.",
    "Recuerda siempre: después de la tormenta, sale el sol.",
    "Tu bienestar mental es una prioridad, nunca un lujo.",
    "Cada pequeño paso hacia adelante cuenta muchísimo.",
    "Eres más fuerte y resiliente de lo que puedes imaginar.",
    "Hoy es un buen día para cuidar de ti mismo."
]

# PELÍCULAS EN ESPAÑOL RECOMENDADAS
peliculas_espanol = [
    {
        "titulo": "El Secreto de Sus Ojos",
        "genero": "Drama/Suspenso",
        "descripcion": "Una historia sobre la búsqueda de justicia y el poder del amor verdadero.",
        "por_que": "Te ayudará a reflexionar sobre la vida y encontrar esperanza en momentos difíciles."
    },
    {
        "titulo": "Volver",
        "genero": "Drama/Comedia",
        "descripcion": "Una película de Almodóvar sobre familia, perdón y segundas oportunidades.",
        "por_que": "Trata temas de sanación emocional y la importancia de los vínculos familiares."
    },
    {
        "titulo": "El Libro de la Vida",
        "genero": "Animación/Familia",
        "descripcion": "Una hermosa historia sobre el amor, la familia y encontrar tu verdadero propósito.",
        "por_que": "Es muy inspiradora y te llenará de energía positiva y esperanza."
    },
    {
        "titulo": "No Se Aceptan Devoluciones",
        "genero": "Drama/Comedia",
        "descripcion": "Una emotiva historia sobre paternidad, amor y sacrificio personal.",
        "por_que": "Te hará valorar profundamente las relaciones importantes en tu vida."
    },
    {
        "titulo": "Coco",
        "genero": "Animación/Familia",
        "descripcion": "Una película sobre familia, memoria y la importancia de seguir tus sueños.",
        "por_que": "Es muy emotiva y te ayudará a conectar con tus emociones más profundas."
    },
    {
        "titulo": "Roma",
        "genero": "Drama",
        "descripcion": "Una película íntima sobre familia, memoria y diferencias sociales.",
        "por_que": "Es profundamente emotiva y te ayudará a reflexionar sobre la vida."
    },
    {
        "titulo": "El Laberinto del Fauno",
        "genero": "Fantasía/Drama",
        "descripcion": "Una historia sobre la imaginación como escape y la esperanza eterna.",
        "por_que": "Te inspirará a encontrar belleza incluso en los tiempos más difíciles."
    }
]

def mostrar_video_integrado(url, titulo="Video", ancho=500, alto=280):
    """Función para mostrar videos integrados con múltiples opciones"""
    try:
        # Opción 1: Iframe de YouTube mejorado
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin: 15px 0; padding: 10px;">
                <iframe width="{ancho}" height="{alto}" 
                src="{url}?autoplay=0&mute=0&rel=0&modestbranding=1" 
                title="{titulo}"
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen
                style="border-radius: 12px; box-shadow: 0 6px 12px rgba(0,0,0,0.15); border: 2px solid #4ECDC4;"></iframe>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        # Opción alternativa si falla el iframe
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: #f0f8ff; border-radius: 10px; margin: 15px 0;">
            <h4>🎬 {titulo}</h4>
            <p>📹 <a href="{url.replace('/embed/', '/watch?v=')}" target="_blank" style="color: #1f77b4;">Ver video en YouTube</a></p>
            <p style="font-size: 0.9em; color: #666;">Si el video no se carga, haz clic en el enlace para verlo directamente</p>
        </div>
        """, unsafe_allow_html=True)

def generar_avatar_ia(nombre, estilo="profesional", color_favorito="#4ECDC4"):
    """Genera avatar con IA usando PIL y algoritmos simples"""
    
    # Crear imagen base
    width, height = 300, 300
    
    # Colores basados en el estilo
    if estilo == "profesional":
        bg_color = (245, 245, 250)
        primary_color = tuple(int(color_favorito.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    elif estilo == "amigable":
        bg_color = (255, 248, 225)
        primary_color = (255, 182, 193)
    else:  # relajante
        bg_color = (240, 255, 240)
        primary_color = (152, 251, 152)
    
    # Crear imagen
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Dibujar cara circular
    face_size = 160
    face_x = (width - face_size) // 2
    face_y = (height - face_size) // 2
    
    # Cara base
    draw.ellipse([face_x, face_y, face_x + face_size, face_y + face_size], 
                 fill=primary_color, outline=(100, 100, 100), width=3)
    
    # Ojos
    eye_y = face_y + 50
    draw.ellipse([face_x + 40, eye_y, face_x + 60, eye_y + 20], fill=(0, 0, 0))
    draw.ellipse([face_x + 100, eye_y, face_x + 120, eye_y + 20], fill=(0, 0, 0))
    
    # Pupilas brillantes
    draw.ellipse([face_x + 45, eye_y + 5, face_x + 55, eye_y + 15], fill=(255, 255, 255))
    draw.ellipse([face_x + 105, eye_y + 5, face_x + 115, eye_y + 15], fill=(255, 255, 255))
    
    # Sonrisa
    smile_y = face_y + 100
    draw.arc([face_x + 50, smile_y, face_x + 110, smile_y + 30], 0, 180, fill=(0, 0, 0), width=4)
    
    # Texto del nombre
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), nombre, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    draw.text((text_x, height - 50), nombre, fill=(50, 50, 50), font=font)
    
    # Agregar elementos decorativos
    # Estrellitas alrededor
    for i in range(8):
        x = face_x + random.randint(-30, face_size + 30)
        y = face_y + random.randint(-30, face_size + 30)
        if not (face_x < x < face_x + face_size and face_y < y < face_y + face_size):
            draw.text((x, y), "✨", fill=primary_color, font=font)
    
    return img

def crear_avatar_animado_ia(nombre, personalidad="amigable"):
    """Crea múltiples frames para avatar animado"""
    frames = []
    
    for i in range(4):  # 4 frames para animación simple
        # Variar ligeramente cada frame
        if personalidad == "energetico":
            color = f"#{random.choice(['FF6B9D', '4ECDC4', 'FFE66D', '95E1D3'])}"
        elif personalidad == "relajado":
            color = f"#{random.choice(['B8E6B8', 'E8F4FD', 'FFE5B4', 'FFCCCB'])}"
        else:  # amigable
            color = f"#{random.choice(['87CEEB', 'DDA0DD', 'F0E68C', 'FFB6C1'])}"
        
        frame = generar_avatar_ia(nombre, "amigable", color)
        frames.append(frame)
    
    return frames

def crear_avatar_personalizado():
    """Generador de avatar integrado con IA"""
    st.markdown("### 🎨 Crear Tu Avatar con IA Integrada")
    
    st.success("🤖 **¡Nueva función!** Ahora puedes generar avatares directamente con IA")
    
    # Pestañas para diferentes métodos
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧠 IA Integrada", "🤖 AI Avatar", "📹 Video Selfie", "🎮 Avatar 3D", "📱 Subir Archivo"])
    
    with tab1:
        st.markdown("#### 🧠 Generador de Avatar con IA Integrada")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_avatar = st.text_input("Tu nombre:", value="Serenity", placeholder="Escribe tu nombre")
            
            estilo_avatar = st.selectbox(
                "Estilo del avatar:",
                ["profesional", "amigable", "relajante"],
                index=1
            )
            
            personalidad = st.selectbox(
                "Personalidad:",
                ["amigable", "energetico", "relajado"],
                index=0
            )
            
            color_favorito = st.color_picker("Color favorito:", "#4ECDC4")
            
        with col2:
            if st.button("🎨 Generar Avatar Estático", key="gen_estatico"):
                with st.spinner("Generando avatar con IA..."):
                    avatar_img = generar_avatar_ia(nombre_avatar, estilo_avatar, color_favorito)
                    
                    # Convertir a bytes para mostrar
                    img_buffer = io.BytesIO()
                    avatar_img.save(img_buffer, format='PNG')
                    img_bytes = img_buffer.getvalue()
                    
                    st.image(avatar_img, caption=f"Avatar de {nombre_avatar}", width=300)
                    
                    # Guardar en session state
                    st.session_state.avatar_generado = img_bytes
                    st.success("✅ Avatar generado con IA!")
            
            if st.button("🎬 Generar Avatar Animado", key="gen_animado"):
                with st.spinner("Generando avatares animados con IA..."):
                    frames = crear_avatar_animado_ia(nombre_avatar, personalidad)
                    
                    st.markdown("**Frames del avatar animado:**")
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
                st.markdown("[Ir a D-ID](https://www.d-id.com/)")
        
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
                st.markdown("[Ir a Synthesia](https://www.synthesia.io/)")
    
    with tab3:
        st.markdown("#### 🎥 Subir Video Personal")
        
        video_uploaded = st.file_uploader(
            "📹 Sube tu video personal (opcional)", 
            type=['mp4', 'avi', 'mov'],
            help="Sube un video tuyo para usarlo como avatar personalizado"
        )
        
        if video_uploaded is not None:
            st.success("✅ Video subido correctamente!")
            st.video(video_uploaded)
            st.session_state['video_personal'] = video_uploaded
        else:
            st.info("🤖 Sin video personal, se usará avatar IA generado.")
        
        # Subida de archivo
        uploaded_file = st.file_uploader(
            "Sube tu video/imagen de avatar:",
            type=['mp4', 'mov', 'gif', 'jpg', 'png'],
            help="Formatos soportados: MP4, MOV, GIF, JPG, PNG"
        )
        
        if uploaded_file is not None:
            # Guardar archivo
            import os
            os.makedirs("avatars", exist_ok=True)
            
            file_path = f"avatars/{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ Avatar guardado como: {file_path}")
            st.info("💡 Usa esta ruta en la configuración: " + file_path)
            
            # Mostrar preview
            if uploaded_file.type.startswith('image'):
                st.image(file_path, width=300, caption="Preview de tu avatar")
            else:
                st.video(file_path)

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
            avatar_url = st.session_state.avatar_personalizado
            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin: 10px 0;">
                <iframe src="{avatar_url}" 
                width="400" height="300" frameborder="0" allowfullscreen 
                style="border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"></iframe>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Avatar por defecto - Video local de Johana
            try:
                # Primero intentar mostrar el video local
                st.video("johana_avatar.mp4", format="video/mp4", start_time=0)
                st.caption("🎭 Serenity Johana - Tu asistente de bienestar personal")
            except:
                # Si no funciona el video local, usar imagen por defecto
                st.image(AVATAR_SERENITY_IMAGEN, width=200, caption="Serenity Johana - Tu asistente de bienestar")
                
                # Video alternativo online
                try:
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: center; margin: 10px 0;">
                            <iframe src="https://streamable.com/e/ez13ge" 
                            width="400" height="300" frameborder="0" allowfullscreen 
                            style="border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"></iframe>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                except:
                    st.info("🎭 Usa el botón 'Personalizar Avatar' para crear el tuyo")
    
    # Configuración de avatar personalizado
    st.markdown("---")
    st.markdown("### ⚙️ Configurar Avatar Personalizado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        avatar_url = st.text_input(
            "URL de tu avatar:",
            placeholder="https://streamable.com/tu-avatar o ./avatars/mi-video.mp4",
            help="Pega aquí la URL de tu avatar creado"
        )
        
        if st.button("💾 Guardar Avatar"):
            if avatar_url:
                st.session_state.avatar_personalizado = avatar_url
                st.success("✅ Avatar personalizado guardado!")
                st.rerun()
            else:
                st.warning("⚠️ Ingresa una URL válida")
    
    with col2:
        if st.session_state.get('avatar_personalizado'):
            st.success(f"Avatar actual: {st.session_state.avatar_personalizado}")
            if st.button("🔄 Restaurar Avatar Original"):
                del st.session_state.avatar_personalizado
                st.success("✅ Avatar original restaurado!")
                st.rerun()
        else:
            st.info("💡 No hay avatar personalizado configurado")
    
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(45deg, #FFE5B4, #FFCCCB); 
                padding: 15px; border-radius: 10px; margin: 15px 0;">
        <h4 style="color: #333; margin: 0;">✨ Tu asistente personal para el bienestar emocional ✨</h4>
        <p style="color: #666; margin: 5px 0;">Aquí para escucharte, apoyarte y guiarte hacia un mejor bienestar</p>
    </div>
    """, unsafe_allow_html=True)

def ejercicio_respiracion(contexto="general"):
    """Ejercicio de respiración con video integrado EN ESPAÑOL"""
    st.write("🧘‍♀️ **Ejercicio de Respiración Guiada en Español**")
    st.write("Sigue estos pasos mientras escuchas la guía completa en español:")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("**Pasos a seguir:**")
        st.write("1. 🌬️ Inhala profundamente por la nariz durante 4 segundos")
        st.write("2. ⏸️ Mantén el aire en tus pulmones durante 4 segundos")
        st.write("3. 💨 Exhala lentamente por la boca durante 6 segundos")
        st.write("4. 🔄 Repite este ciclo entre 5 y 10 veces")
        st.write("5. 😌 Concéntrate solo en tu respiración")
        
        # SONIDO RELAJANTE integrado
        if st.button("🎵 Ver video de sonidos relajantes", key=f"btn_sonido_respiracion_{contexto}"):
            sonido_seleccionado = random.choice(SONIDOS_RELAJACION)
            st.write("**🎶 Video de sonidos relajantes en español:**")
            mostrar_video_integrado(sonido_seleccionado, "Sonidos Relajantes Español", 400, 225)
            st.success("🎶 Disfruta estos sonidos relajantes mientras realizas tu respiración...")
    
        with col2:
            st.write("**🎬 Video de respiración guiada:**")
            if st.button("▶️ Ver Video de Respiración", key=f"play_respiracion_{contexto}"):
                mostrar_video_integrado(VIDEO_RESPIRACION, "Respiración Guiada Español", 400, 225)
            
            # Alternativa sin video
            st.markdown("""
            **� Alternativa sin video:**
            1. **Cuenta mentalmente:** 4 segundos inhalar, 4 mantener, 6 exhalar
            2. **Usa un temporizador:** Pon 5 minutos en tu teléfono
            3. **Música de fondo:** Pon música suave mientras respiras
            4. **Aplicaciones:** Calm, Headspace, Insight Timer
            """)
            st.info("🌟 La respiración profunda funciona incluso sin video")

def ejercicio_meditacion(contexto="general"):
    """Ejercicio de meditación integrado EN ESPAÑOL"""
    st.write("🧘 **Meditación Guiada de 5 Minutos en Español**")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("**Instrucciones completas en español:**")
        st.write("1. 🪑 Siéntate de manera cómoda y relajada")
        st.write("2. 👀 Cierra suavemente los ojos")
        st.write("3. 🧠 Concéntrate únicamente en tu respiración")
        st.write("4. 💭 Permite que los pensamientos pasen sin juzgarlos")
        st.write("5. ⏰ Dedica exactamente 5 minutos a esta meditación")
        st.write("6. 🕊️ Mantén la mente en calma y presente")
        
        if st.button("⏰ Comenzar meditación guiada completa", key=f"btn_temporizador_meditacion_{contexto}"):
            st.success("¡Meditación en español iniciada! Relájate completamente y sigue la guía")
            st.balloons()
    
    with col2:
        st.write("**🎬 Video de meditación guiada:**")
        if st.button("▶️ Ver Video de Meditación", key=f"play_meditacion_{contexto}"):
            mostrar_video_integrado(VIDEO_MEDITACION, "Meditación Guiada Español", 400, 225)
        
        # Meditación sin video
        st.markdown("""
        **🧘‍♀️ Meditación sin video:**
        1. **Timer:** Pon 5 minutos en silencio
        2. **Postura:** Siéntate cómodo, espalda recta
        3. **Respiración:** Observa tu respiración natural
        4. **Pensamientos:** Deja que pasen sin juzgar
        5. **Apps:** Insight Timer, Calm, Headspace
        """)
        st.info("🇪🇸 La meditación es efectiva con o sin guía de video")

def ejercicio_estiramiento(contexto="general"):
    """Ejercicio de estiramiento integrado EN ESPAÑOL"""
    st.write("🤸‍♀️ **Ejercicios de Estiramiento Suave en Español**")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("**Rutina completa de 3 minutos en español:**")
        st.write("1. 🤲 Estira ambos brazos hacia arriba durante 10 segundos")
        st.write("2. 🙄 Gira el cuello suavemente hacia cada lado")
        st.write("3. 🤗 Abraza tu cuerpo y estira toda la espalda")
        st.write("4. 🦵 Estira las piernas mientras permaneces sentado")
        st.write("5. 😌 Respira profundamente entre cada ejercicio")
        st.write("6. 🔄 Repite toda la secuencia dos veces")
        
        if st.button("🎯 Comenzar rutina de estiramiento", key=f"btn_rutina_estiramiento_{contexto}"):
            st.info("¡Perfecto! Sigue todas las instrucciones en español del video integrado")
    
    with col2:
        st.write("**Video de estiramiento en español:**")
        video_ejercicio = random.choice(videos_ejercicios_espanol)
        mostrar_video_integrado(video_ejercicio, "Ejercicios Estiramiento Español", 400, 225)
        st.info("🇪🇸 Ejercicios explicados paso a paso completamente en español")

def mostrar_videos_relajacion():
    """Función para mostrar galería de videos de relajación con alternativas"""
    st.subheader("🎬 Galería de Videos de Relajación en Español")
    st.write("Elige tu video preferido para relajarte:")
    
    # Crear pestañas para diferentes tipos de contenido
    tab1, tab2, tab3 = st.tabs(["🎵 Música Relajante", "🌊 Sonidos Naturales", "🧘 Meditación Guiada"])
    
    with tab1:
        st.markdown("#### 🎵 Música para Relajarse")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎶 Reproducir Música Relajante", key="musica_1"):
                mostrar_video_integrado(VIDEOS_RELAJACION[0], "Música Relajante", 450, 250)
        with col2:
            st.markdown("""
            **🎵 Beneficios de la música relajante:**
            - Reduce el estrés y la ansiedad
            - Mejora la concentración
            - Ayuda a conciliar el sueño
            - Disminuye la presión arterial
            """)
    
    with tab2:
        st.markdown("#### 🌊 Sonidos de la Naturaleza")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌿 Reproducir Sonidos Naturales", key="naturaleza_1"):
                mostrar_video_integrado(VIDEOS_RELAJACION[1], "Sonidos Naturales", 450, 250)
        with col2:
            st.markdown("""
            **� Beneficios de los sonidos naturales:**
            - Conexión con la naturaleza
            - Bloquea ruidos molestos
            - Mejora el estado de ánimo
            - Reduce la fatiga mental
            """)
    
    with tab3:
        st.markdown("#### 🧘 Meditación Guiada")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧘‍♀️ Iniciar Meditación", key="meditacion_video"):
                mostrar_video_integrado(VIDEOS_RELAJACION[2], "Meditación Guiada", 450, 250)
        with col2:
            st.markdown("""
            **🧘 Beneficios de la meditación:**
            - Calma la mente
            - Reduce pensamientos negativos  
            - Mejora la autorregulación emocional
            - Aumenta la atención plena
            """)
    
    # Alternativa si los videos no cargan
    st.markdown("---")
    st.info("""
    💡 **¿Los videos no se cargan?** 
    Puedes usar estos recursos alternativos:
    - 🎧 Aplicación "Calm" o "Headspace"
    - 🌊 Buscar "sonidos relajantes" en Spotify
    - 📱 YouTube: buscar "meditación en español"
    - 🎵 Radio online de música relajante
    """)

def recomendar_pelicula():
    """Recomienda películas en español según el estado de ánimo"""
    st.subheader("🎬 Recomendación de Película en Español")
    
    pelicula = random.choice(peliculas_espanol)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(f"**🎭 {pelicula['titulo']}**")
        st.write(f"**Género:** {pelicula['genero']}")
        st.write(f"**Descripción:** {pelicula['descripcion']}")
    
    with col2:
        st.write(f"**¿Por qué te la recomiendo especialmente?**")
        st.info(pelicula['por_que'])
        st.write("🍿 **Consejo:** Todas nuestras recomendaciones están completamente en español")
    
    if st.button("🎲 Recomendar otra película diferente en español", key="btn_otra_pelicula"):
        st.rerun()

def frase_apoyo():
    frases = [
        "Recuerda siempre: esto también pasará.",
        "Eres mucho más fuerte de lo que puedes creer.",
        "Respira profundamente, todo estará bien.",
        "No estás solo en esto, estoy aquí contigo.",
        "Cada pequeño paso que das cuenta muchísimo.",
        "Tu bienestar es realmente importante.",
        "Mereces amor y cuidado, especialmente de ti mismo.",
        "Las tormentas no duran para siempre, pero tú sí.",
        "Tu historia aún se está escribiendo, no termines el libro ahora.",
        "Hoy es un buen día para ser amable contigo mismo."
    ]
    return random.choice(frases)

def mostrar_contacto_emergencia():
    st.warning("🚨 ¿Necesitas ayuda urgente? Puedes comunicarte inmediatamente con:")
    st.markdown("- **Línea Nacional para la Prevención del Suicidio (Colombia):** 01 8000 113 113")
    st.markdown("- **Línea de Emergencias 123 (Bogotá):** Marca 123 y solicita ayuda en salud mental")
    st.markdown("- **Línea de atención psicológica gratuita (Colombia):** 106")
    st.markdown("- **Red Nacional de Salud Mental:** [Ver todos los recursos disponibles](https://www.minsalud.gov.co/salud/publica/SaludMental/Paginas/lineas-de-atencion.aspx)")
    st.info("Si no puedes comunicarte por teléfono, acude inmediatamente al hospital o centro de salud más cercano.")

def registrar_emocion(nombre, emocion):
    if emocion:
        with open("emociones.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"{nombre}: {emocion}\n")
        st.success("¡Muchísimas gracias por compartir conmigo cómo te sientes!")

def mostrar_historial(nombre):
    try:
        with open("emociones.txt", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
        historial = [linea for linea in lineas if linea.startswith(nombre + ":")]
        if historial:
            st.subheader("Tu historial completo de emociones:")
            for linea in historial:
                st.write(linea.replace(nombre + ":", "").strip())
        else:
            st.info("Aún no tienes emociones registradas en tu historial.")
    except FileNotFoundError:
        st.info("Aún no tienes emociones registradas en tu historial.")

def recomendar_recursos(emocion):
    if not emocion:
        return
    st.subheader("🎯 Recomendaciones personalizadas para ti:")
    
    palabras_depresion = [
        "triste", "deprimido", "depresion", "decaido", "melancolico", "desanimado",
        "sin ganas", "vacio", "solo", "soledad", "llorar", "llorando", "desesperanza",
        "abatido", "desmotivado", "inutil", "culpa", "culpable", "fracaso", "oscuro",
        "sufro", "sufrimiento", "no puedo mas", "no quiero vivir", "no tengo fuerzas",
        "quiero morir", "quitarme la vida", "suicidar", "suicidio", "no encuentro sentido"
    ]
    
    palabras_riesgo = [
        "quitarme la vida", "suicidar", "suicidio", "no quiero vivir", "quiero morir", 
        "me quiero morir", "no encuentro sentido", "acabar con todo"
    ]
    
    emocion_limpio = unidecode(emocion.lower())
    
    if any(frase in emocion_limpio for frase in palabras_riesgo):
        st.error("⚠️ Si tienes pensamientos de hacerte daño, por favor busca ayuda inmediata. No estás solo en esto.")
        mostrar_contacto_emergencia()
        st.write("Te recomiendo encarecidamente buscar apoyo profesional. Tu vida es muy valiosa e importante.")
        ejercicio_respiracion("emergencia")
        return
        
    if "ansioso" in emocion_limpio or "ansiedad" in emocion_limpio:
        st.write("**Para ayudarte con la ansiedad te recomiendo especialmente:**")
        ejercicio_respiracion("ansiedad")
        ejercicio_meditacion("ansiedad")
        
    elif any(palabra in emocion_limpio for palabra in palabras_depresion):
        st.write("**Para mejorar tu estado de ánimo te sugiero:**")
        ejercicio_respiracion("depresion")
        ejercicio_estiramiento("depresion")
        recomendar_pelicula()
        st.write("- Habla con un amigo cercano o familiar de confianza.")
        st.write("- Considera seriamente buscar ayuda profesional, recuerda que no estás solo en esto.")
        mostrar_contacto_emergencia()
        
    elif "feliz" in emocion_limpio or "alegre" in emocion_limpio:
        st.write("- ¡Sigue exactamente así! Comparte tu alegría con otras personas.")
        st.balloons()
        st.write("¿Qué tal si celebramos juntos con una buena película en español? 🎵")
        recomendar_pelicula()
        
    else:
        st.write("**Te recomiendo estos ejercicios de bienestar completamente en español:**")
        ejercicio_respiracion("bienestar")

def responder_mensaje(mensaje):
    mensaje_limpio = unidecode(mensaje.lower())
    palabras_riesgo = [
        "quitarme la vida", "suicidar", "suicidio", "no quiero vivir", "quiero morir", 
        "me quiero morir", "no encuentro sentido", "acabar con todo"
    ]
    
    # ERROR CORREGIDO: Cambié "en" por "in"
    if any(frase in mensaje_limpio for frase in palabras_riesgo):
        return ("⚠️ Si tienes pensamientos de hacerte daño, por favor busca ayuda inmediata. "
                "No estás solo en esto. Puedes comunicarte con la Línea Nacional para la Prevención del Suicidio (01 8000 113 113), "
                "la Línea 123 en Bogotá, o el 106 en Colombia. Tu vida es extremadamente valiosa e importante.")
    
    if any(frase in mensaje_limpio for frase in frases_alegria):
        return ("¡Me alegro muchísimo de escuchar eso! La felicidad realmente se contagia. "
                "Con esa energía tan positiva, ¿qué tal si hacemos algunos ejercicios de bienestar o vemos una buena película en español? "
                "¡Mantengamos juntos esa buena energía! ✨")
    
    if "respirar" in mensaje_limpio or "respiracion" in mensaje_limpio:
        return "¿Te gustaría hacer un ejercicio de respiración guiado completamente en español? Escribe 'sí' para comenzar inmediatamente."
    elif "meditacion" in mensaje_limpio or "meditar" in mensaje_limpio:
        return "La meditación es excelente para conseguir calma mental. ¿Quieres que te guíe en una meditación completa en español?"
    elif "ejercicio" in mensaje_limpio or "estiramiento" in mensaje_limpio:
        return "Los ejercicios suaves ayudan muchísimo a relajar todas las tensiones. ¿Te interesa una rutina de estiramiento explicada completamente en español?"
    elif "pelicula" in mensaje_limpio or "película" in mensaje_limpio:
        return "¡Excelente idea! Las películas pueden ser muy terapéuticas. ¿Te gustaría que te recomiende una película interesante en español?"
    elif "si" in mensaje_limpio and "respirar" in st.session_state.get("last_message", ""):
        return ("Perfecto. Vamos a hacer juntos un ejercicio de respiración guiado completamente en español.\n"
                "Inhala profundamente por la nariz durante exactamente 4 segundos...\n"
                "Mantén el aire en tus pulmones durante 4 segundos...\n"
                "Exhala muy lentamente por la boca durante 6 segundos...\n"
                "Repite este ciclo completo varias veces. Te ayudará a sentirte mucho más tranquilo.")
    elif "frase" in mensaje_limpio or "apoyo" in mensaje_limpio:
        return frase_apoyo()
    elif any(palabra in mensaje_limpio for palabra in [
        "triste", "deprimido", "depresion", "decaido", "melancolico", "desanimado",
        "sin ganas", "vacio", "solo", "soledad", "llorar", "llorando", "desesperanza",
        "abatido", "desmotivado", "inutil", "culpa", "culpable", "fracaso", "oscuro",
        "sufro", "sufrimiento", "no puedo mas", "no quiero vivir", "no tengo fuerzas",
        "quiero morir", "me quiero morir"
    ]):
        return ("Lamento mucho que te sientas de esa manera. Recuerda que no estás solo en esto. "
                "Hablar con alguien de confianza o un profesional puede ayudarte enormemente. "
                "¿Quieres que te recomiende algunos ejercicios de relajación en español o una película que te ayude a levantar el ánimo?")
    elif "gracias" in mensaje_limpio:
        return "¡De nada! Estoy aquí para ayudarte siempre que me necesites."
    elif "adios" in mensaje_limpio or "salir" in mensaje_limpio:
        return "¡Muchísimas gracias por hablar conmigo! Cuídate mucho y recuerda que siempre estaré aquí cuando me necesites."
    else:
        return "Cuéntame más detalles sobre cómo te sientes o pide un 'ejercicio de respiración', 'meditación', 'película' o una 'frase de apoyo' - todo completamente en español."

# INTERFAZ PRINCIPAL MEJORADA
st.set_page_config(
    page_title="🌟 Serenity Johana",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Banner principal mejorado
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 30px; border-radius: 15px; margin-bottom: 30px; text-align: center;">
    <h1 style="color: white; margin: 0; font-size: 3em;">🌟 Serenity Johana 🌟</h1>
    <p style="color: white; font-size: 1.2em; margin: 10px 0;">Tu Asistente Personal para el Bienestar Emocional</p>
    <p style="color: #B8E6B8; font-size: 1em; margin: 0;">✨ Completamente en Español • Apoyo 24/7 • Recursos Profesionales ✨</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con información importante
st.sidebar.markdown("## 🏠 Navegación Rápida")
st.sidebar.markdown("### 🚨 Emergencias")
if st.sidebar.button("☎️ Líneas de Crisis", help="Contactos de emergencia inmediatos"):
    st.session_state.mostrar_emergencia = True

st.sidebar.markdown("### 🎯 Acceso Directo")
acceso_rapido = st.sidebar.selectbox(
    "Ir directamente a:",
    ["Seleccionar...", "Respiración", "Meditación", "Videos Relajantes", "Chat", "Películas", "Mi Historial"]
)

st.sidebar.markdown("### 📊 Tu Progreso")
if 'total_sesiones' not in st.session_state:
    st.session_state.total_sesiones = 0
st.sidebar.metric("Sesiones completadas", st.session_state.total_sesiones)

# Mostrar avatar parlante en TAMAÑO REDUCIDO
mostrar_serenity_parlante()

# Mensaje motivacional con diseño mejorado
mensaje_diario = random.choice(mensajes_motivacionales)
st.markdown(f"""
<div style="background: linear-gradient(45deg, #FFE5B4, #FFCCCB); 
            padding: 20px; border-radius: 10px; border-left: 5px solid #FF6B9D; margin: 20px 0;">
    <p style="margin: 0; font-size: 1.1em; font-style: italic; color: #333;">💫 {mensaje_diario}</p>
</div>
""", unsafe_allow_html=True)

# Manejo de emergencias desde sidebar
if st.session_state.get('mostrar_emergencia', False):
    st.error("🚨 LÍNEAS DE CRISIS Y EMERGENCIA")
    mostrar_contacto_emergencia()
    if st.button("❌ Cerrar"):
        st.session_state.mostrar_emergencia = False
        st.rerun()

# Sección de perfil mejorada
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 👤 Tu Perfil de Bienestar")
    nombre = st.text_input("¿Cómo te llamas?", placeholder="Escribe tu nombre aquí...")

with col2:
    if nombre:
        st.markdown("### 🎯 Estado Actual")
        st.success(f"¡Bienvenido, {nombre}! 👋")

if nombre:
    # Evaluación rápida del estado de ánimo
    st.markdown("### 🌈 ¿Cómo te sientes hoy?")
    
    tab1, tab2, tab3 = st.tabs(["😊 Evaluación Rápida", "📝 Descripción Detallada", "📊 Mi Historial"])
    
    with tab1:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        estados = {
            "😢": "Muy triste",
            "😕": "Un poco bajo",
            "😐": "Neutral",
            "😊": "Bien",
            "😄": "Muy bien"
        }
        
        estado_seleccionado = None
        
        with col1:
            if st.button("😢", help="Muy triste", key="muy_triste"):
                estado_seleccionado = "muy triste"
        with col2:
            if st.button("😕", help="Un poco bajo", key="poco_bajo"):
                estado_seleccionado = "un poco bajo"
        with col3:
            if st.button("😐", help="Neutral", key="neutral"):
                estado_seleccionado = "neutral"
        with col4:
            if st.button("😊", help="Bien", key="bien"):
                estado_seleccionado = "bien"
        with col5:
            if st.button("😄", help="Muy bien", key="muy_bien"):
                estado_seleccionado = "muy bien"
        
        if estado_seleccionado:
            st.success(f"Has seleccionado: {estado_seleccionado}")
            registrar_emocion(nombre, estado_seleccionado)
            recomendar_recursos(estado_seleccionado)
            st.session_state.total_sesiones += 1
    
    with tab2:
        emocion = st.text_area(
            "Describe con más detalle cómo te sientes:",
            placeholder="Por ejemplo: Me siento ansioso por el trabajo, tengo mucho estrés...",
            height=100
        )
        
        if st.button("💾 Registrar descripción detallada", key="btn_registrar_detallada"):
            if emocion:
                registrar_emocion(nombre, emocion)
                recomendar_recursos(emocion)
                st.success("✅ Tu estado emocional ha sido registrado")
                st.session_state.total_sesiones += 1
            else:
                st.warning("⚠️ Por favor describe cómo te sientes")
    
    with tab3:
        mostrar_historial(nombre)

    # Verificar acceso rápido desde sidebar
    if acceso_rapido != "Seleccionar...":
        if acceso_rapido == "Respiración":
            opcion = "Ejercicio de respiración"
        elif acceso_rapido == "Meditación":
            opcion = "Meditación guiada"
        elif acceso_rapido == "Videos Relajantes":
            opcion = "Ver galería de videos de relajación"
        elif acceso_rapido == "Chat":
            opcion = "Chat en tiempo real"
        elif acceso_rapido == "Películas":
            opcion = "Recomendación de película"
        elif acceso_rapido == "Mi Historial":
            mostrar_historial(nombre)
            opcion = "Nada más por ahora"
    else:
        # Interfaz principal mejorada con tarjetas
        st.markdown("### 🎯 ¿Qué te gustaría hacer ahora?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧘‍♀️ Respiración", key="card_respiracion", help="Ejercicios de respiración guiada"):
                opcion = "Ejercicio de respiración"
            if st.button("🎬 Videos Relajantes", key="card_videos", help="Galería de videos de relajación"):
                opcion = "Ver galería de videos de relajación"
            if st.button("💝 Frase de Apoyo", key="card_frase", help="Recibe una frase motivacional"):
                opcion = "Recibir una frase de apoyo"
        
        with col2:
            if st.button("🧘 Meditación", key="card_meditacion", help="Meditación guiada en español"):
                opcion = "Meditación guiada"
            if st.button("🎭 Películas", key="card_peliculas", help="Recomendación personalizada"):
                opcion = "Recomendación de película"
            if st.button("💬 Chat", key="card_chat", help="Conversa con Serenity Johana"):
                opcion = "Chat en tiempo real"
        
        with col3:
            if st.button("🤸‍♀️ Estiramiento", key="card_estiramiento", help="Ejercicios suaves de estiramiento"):
                opcion = "Estiramiento suave"
            if st.button("📊 Mi Progreso", key="card_progreso", help="Ver tu historial completo"):
                mostrar_historial(nombre)
                opcion = "Nada más por ahora"
            if st.button("😌 Descansar", key="card_descansar", help="Finalizar sesión"):
                opcion = "Nada más por ahora"

    # Procesar la opción seleccionada
    if 'opcion' in locals():
        if opcion == "Ejercicio de respiración":
            st.markdown("---")
            ejercicio_respiracion("opcion_principal")
        elif opcion == "Meditación guiada":
            st.markdown("---")
            ejercicio_meditacion("opcion_principal")
        elif opcion == "Estiramiento suave":
            st.markdown("---")
            ejercicio_estiramiento("opcion_principal")
        elif opcion == "Ver galería de videos de relajación":
            st.markdown("---")
            mostrar_videos_relajacion()
        elif opcion == "Recomendación de película":
            st.markdown("---")
            recomendar_pelicula()
        elif opcion == "Recibir una frase de apoyo":
            st.markdown("---")
            st.markdown(f"""
            <div style="background: linear-gradient(45deg, #FFE5B4, #FFCCCB); 
                        padding: 25px; border-radius: 15px; text-align: center; margin: 20px 0;">
                <h3 style="color: #333; margin: 0;">💝 Mensaje para ti:</h3>
                <p style="color: #333; font-size: 1.2em; font-style: italic; margin: 10px 0;">"{frase_apoyo()}"</p>
            </div>
            """, unsafe_allow_html=True)
        elif opcion == "Chat en tiempo real":
            st.markdown("---")
            st.subheader("💬 Chat con Serenity Johana")
            
            if "chat" not in st.session_state:
                st.session_state.chat = []
            
            # Área de chat mejorada
            chat_container = st.container()
            
            with chat_container:
                for i, (remitente, mensaje) in enumerate(st.session_state.chat):
                    if remitente == "Serenity Johana":
                        col1, col2 = st.columns([1, 6])
                        with col1:
                            st.image(AVATAR_SERENITY_IMAGEN, width=60)
                        with col2:
                            st.markdown(f"""
                            <div style="background: #E8F4FD; padding: 15px; border-radius: 10px; margin: 5px 0;">
                                <p style="margin: 0; color: #333;"><strong>{remitente}:</strong> {mensaje}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: #F0F8FF; padding: 15px; border-radius: 10px; margin: 5px 0; margin-left: 60px;">
                            <p style="margin: 0; color: #333;"><strong>{remitente}:</strong> {mensaje}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Input de chat mejorado
            col1, col2 = st.columns([5, 1])
            with col1:
                mensaje_usuario = st.text_input("Escribe tu mensaje:", key="chat_input", placeholder="¿Cómo te sientes? ¿En qué puedo ayudarte?")
            with col2:
                enviar = st.button("📤 Enviar", key="enviar_chat")
            
            if enviar and mensaje_usuario:
                st.session_state.chat.append(("Tú", mensaje_usuario))
                respuesta = responder_mensaje(mensaje_usuario)
                st.session_state.chat.append(("Serenity Johana", respuesta))
                st.session_state.last_message = mensaje_usuario
                st.rerun()
        elif opcion == "Nada más por ahora":
            st.markdown("""
            <div style="background: linear-gradient(45deg, #B8E6B8, #C8E8C8); 
                        padding: 25px; border-radius: 15px; text-align: center; margin: 20px 0;">
                <h3 style="color: #333; margin: 0;">💙 ¡Gracias por tu tiempo!</h3>
                <p style="color: #333; margin: 10px 0;">Recuerda que siempre estaré aquí cuando me necesites.</p>
                <p style="color: #555; margin: 0;"><em>Cuídate mucho y que tengas un día lleno de paz. ✨</em></p>
            </div>
            """, unsafe_allow_html=True)

# Panel de estadísticas y recursos adicionales
st.markdown("---")
st.markdown("### 📊 Tu Bienestar en Números")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🧘 Sesiones Completadas", st.session_state.get('total_sesiones', 0))
with col2:
    # Contar emociones registradas
    try:
        with open("emociones.txt", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
        emociones_usuario = [linea for linea in lineas if nombre and linea.startswith(nombre + ":")]
        total_emociones = len(emociones_usuario)
    except:
        total_emociones = 0
    st.metric("📝 Emociones Registradas", total_emociones)
with col3:
    st.metric("🎯 Días de Uso", "1")  # Puedes mejorar esto con fechas reales
with col4:
    st.metric("⭐ Nivel de Bienestar", "Creciendo" if total_emociones > 0 else "Comenzando")

# Recursos adicionales
st.markdown("### 🔗 Recursos Adicionales de Bienestar")

recursos_tabs = st.tabs(["🆘 Crisis", "📚 Educación", "🏥 Profesionales", "📱 Apps Recomendadas"])

with recursos_tabs[0]:
    st.markdown("#### 🚨 ¿Necesitas ayuda inmediata?")
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **📞 Líneas de Crisis (Colombia):**
        - Nacional: 01 8000 113 113
        - Bogotá: 123
        - WhatsApp: 300 754 8933
        """)
    with col2:
        st.warning("""
        **🏥 Cuándo buscar ayuda:**
        - Pensamientos de autolesión
        - Pérdida de control emocional
        - Aislamiento extremo
        - Cambios drásticos de comportamiento
        """)

with recursos_tabs[1]:
    st.markdown("#### 📖 Aprende sobre Salud Mental")
    st.markdown("""
    - **Ansiedad:** Reacciones normales del cuerpo ante el estrés
    - **Depresión:** No es solo tristeza, es una condición médica
    - **Mindfulness:** Técnica de atención plena para el presente
    - **Autocuidado:** Actividades que mejoran tu bienestar físico y mental
    """)

with recursos_tabs[2]:
    st.markdown("#### 👨‍⚕️ Encuentra Ayuda Profesional")
    st.info("""
    **¿Cuándo considerar terapia?**
    - Síntomas que duran más de 2 semanas
    - Interfieren con trabajo/estudios/relaciones
    - No mejoran con autocuidado
    - Afectan tu sueño o apetito significativamente
    """)
    
    st.markdown("""
    **Tipos de profesionales:**
    - 🧠 **Psicólogo:** Terapia y apoyo emocional
    - 💊 **Psiquiatra:** Diagnóstico y medicación
    - 👥 **Trabajador Social:** Apoyo integral
    """)

with recursos_tabs[3]:
    st.markdown("#### 📱 Apps Complementarias Recomendadas")
    st.markdown("""
    - **Headspace:** Meditación guiada
    - **Calm:** Relajación y sueño
    - **Youper:** Seguimiento del estado de ánimo
    - **Sanvello:** Manejo de ansiedad
    - **MindShift:** Técnicas de CBT
    """)

# Encuesta mejorada
st.markdown("---")
st.markdown("### 💬 Ayúdanos a Mejorar Serenity")

with st.expander("📝 Comparte tu opinión (opcional)"):
    col1, col2 = st.columns(2)
    
    with col1:
        satisfaccion = st.slider("¿Qué tan útil fue Serenity hoy?", 1, 5, 3)
        
        opciones = [
            "Más ejercicios de relajación",
            "Música personalizada",
            "Consejos de alimentación",
            "Más ejercicios físicos",
            "Más películas/series",
            "Conexión con profesionales",
            "Recordatorios diarios"
        ]
        
        seleccion = st.multiselect("¿Qué te gustaría agregar?", opciones)
    
    with col2:
        sugerencia = st.text_area("Sugerencias específicas:", placeholder="Comparte tus ideas para mejorar...")
        
        if st.button("💌 Enviar Feedback", key="btn_enviar_encuesta"):
            st.success("¡Gracias por tu feedback! Serenity seguirá mejorando. 💖")
            st.balloons()

# Footer final
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 30px; background: #F8F9FA; border-radius: 10px;">
    <h4 style="color: #4A5568; margin-bottom: 15px;">🌟 Serenity Johana</h4>
    <p style="margin: 5px 0;">Tu bienestar mental es nuestra prioridad</p>
    <p style="margin: 5px 0; font-size: 0.9em;">Desarrollado con ❤️ para apoyar tu salud emocional</p>
    <p style="margin: 5px 0; font-size: 0.8em;">⚠️ Recuerda: Esta app complementa pero no reemplaza la ayuda profesional</p>
</div>
""", unsafe_allow_html=True)