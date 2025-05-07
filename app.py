
import streamlit as st
import random
from gtts import gTTS
import base64
from io import BytesIO

st.set_page_config(page_title="Amiguito Virtual", layout="centered")

st.title("🤖 Amiguito Virtual")
st.markdown("¡Toca un botón para hablar conmigo! 👇")

respuestas = {
    "saludo": ["¡Hola Valentina! ¡Hola Luca! 👋😊", "¡Qué gusto verlos! 🥰"],
    "chiste": ["¿Qué hace una abeja en el gimnasio? ¡Zum-ba! 🐝", "¿Por qué el tomate se puso rojo? ¡Porque vio al pepino sin ropa! 🍅😆"],
    "contar": ["Uno, dos, tres, cuatro... ¡muy bien! 👏", "Contemos juntos: uno, dos, tres... 🎉"],
    "despedida": ["¡Hasta pronto! 👋", "¡Un abrazo gigante! 🧸💖"]
}

def generar_audio(texto):
    tts = gTTS(text=texto, lang='es')
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    audio_b64 = base64.b64encode(audio_bytes.read()).decode()
    audio_html = f'<audio controls autoplay><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
    return audio_html

col1, col2, col3, col4 = st.columns(4)

if col1.button("👋 Hola"):
    mensaje = random.choice(respuestas["saludo"])
    st.success(mensaje)
    st.markdown(generar_audio(mensaje), unsafe_allow_html=True)

if col2.button("😂 Chiste"):

