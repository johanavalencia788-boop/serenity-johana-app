import streamlit as st
from pyngrok import ngrok
import time

# Ejecutar tu app y crear túnel público
def crear_tunel_publico():
    st.markdown("## 🌍 Haciendo tu Serenity App Pública")
    
    if st.button("🚀 Crear Enlace Público", use_container_width=True):
        with st.spinner("🔗 Creando enlace público para compartir..."):
            try:
                # Crear túnel ngrok
                public_tunnel = ngrok.connect(8501)
                
                st.success("🎉 ¡Tu aplicación ya es pública!")
                st.markdown(f"""
                ### 🌟 Enlace público de tu Serenity App:
                **{public_tunnel.public_url}**
                
                ✅ Cualquier persona puede acceder
                ✅ Funciona en todos los dispositivos  
                ✅ Tu generador de avatares con IA disponible
                ✅ Comparte este enlace en redes sociales
                
                **¡Tu aplicación de bienestar mental está online para el mundo!** 🌍
                """)
                
                # Mostrar QR code conceptual
                st.info("💡 Copia este enlace y compártelo con quien quieras!")
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("💡 Asegúrate de que tu aplicación esté ejecutándose en el puerto 8501")

if __name__ == "__main__":
    crear_tunel_publico()