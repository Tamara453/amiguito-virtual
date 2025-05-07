


import streamlit as st
import random
from gtts import gTTS
import os

st.set_page_config(page_title="Amiguito Virtual", layout="centered")

st.title("🤖 Amiguito Virtual")
st.markdown("¡Toca un botón para hablar conmigo! 👇")

respuestas = {
    "saludo": ["¡Hola Valentina! ¡Hola Luca! 👋😊", "¡Qué gusto verlos! 🥰"],
    "chiste": ["¿Qué hace una abeja en el gimnasio? ¡Zum-ba! 🐝", "¿Por qué el tomate se puso rojo? ¡Porque vio al pepino sin ropa! 🍅😆"],
    "contar": ["Uno, dos, tres, cuatro... ¡muy bien! 👏", "Contemos juntos: uno, dos, tres... 🎉"],
    "despedida": ["¡Hasta pronto! 👋", "¡Un abrazo gigante! 🧸💖"]
}

def hablar(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save("voz.mp3")
    os.system("start voz.mp3" if os.name == "nt" else "mpg123 voz.mp3")

col1, col2, col3, col4 = st.columns(4)

if col1.button("👋 Hola"):
    mensaje = random.choice(respuestas["saludo"])
    st.success(mensaje)
    hablar(mensaje)

if col2.button("😂 Chiste"):
    mensaje = random.choice(respuestas["chiste"])
    st.info(mensaje)
    hablar(mensaje)

if col3.button("🔢 Contar"):
    mensaje = random.choice(respuestas["contar"])
    st.warning(mensaje)
    hablar(mensaje)

if col4.button("👋 Adiós"):
    mensaje = random.choice(respuestas["despedida"])
    st.error(mensaje)
    hablar(mensaje)
