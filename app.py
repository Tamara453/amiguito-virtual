
import streamlit as st
from transformers import pipeline
from gtts import gTTS
import os

st.set_page_config(page_title="Amiguito Virtual", layout="centered")

st.title("🤖 Amiguito Virtual")
st.markdown("¡Hola! Soy tu amiguito virtual. ¿Qué quieres preguntarme hoy?")

@st.cache_resource
def cargar_modelo():
    return pipeline("text-generation", model="mrm8488/t5-small-finetuned-spanish-summarization")

modelo = cargar_modelo()

pregunta = st.text_input("Escribe aquí tu pregunta:")

if st.button("Responder"):
    if pregunta.strip() != "":
        with st.spinner("Pensando..."):
            respuesta = modelo(pregunta)[0]["generated_text"].strip()
            st.write("🧒 Amiguito dice:")
            st.success(respuesta)

            tts = gTTS(text=respuesta, lang='es')
            tts.save("respuesta.mp3")
            audio_file = open("respuesta.mp3", "rb")
            st.audio(audio_file.read(), format="audio/mp3")
            audio_file.close()
            os.remove("respuesta.mp3")
    else:
        st.warning("Por favor, escribe una pregunta primero.")

    

