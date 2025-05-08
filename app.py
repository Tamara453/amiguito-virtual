
    import streamlit as st
from transformers import pipeline
from gtts import gTTS
import os

# Configurar la interfaz
st.set_page_config(page_title="Amiguito Virtual", page_icon="🤖", layout="centered")
st.title("👶 Amiguito Virtual")
st.markdown("Hola, soy tu amiguito virtual. ¡Pregúntame lo que quieras!")

# Cargar modelo de lenguaje
chatbot = pipeline("text-generation", model="distilgpt2")

# Función para generar respuesta
def responder(mensaje):
    respuesta = chatbot(mensaje, max_length=100, num_return_sequences=1)[0]["generated_text"]
    return respuesta[len(mensaje):].strip()

# Historial de conversación
if "historial" not in st.session_state:
    st.session_state.historial = []

# Entrada de texto
entrada = st.text_input("Escribe tu mensaje aquí:")

if st.button("Enviar") and entrada:
    respuesta = responder(entrada)

    # Mostrar conversación
    st.session_state.historial.append(("Tú", entrada))
    st.session_state.historial.append(("Amiguito", respuesta))

    # Crear y reproducir audio
    tts = gTTS(text=respuesta, lang="es")
    tts.save("respuesta.mp3")
    audio_file = open("respuesta.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")
    audio_file.close()
    os.remove("respuesta.mp3")

# Mostrar historial
for rol, texto in st.session_state.historial:
    st.markdown(f"**{rol}:** {texto}")


