
import streamlit as st
from transformers import pipeline
from gtts import gTTS
import os

# Inicializar modelo
chatbot = pipeline("text-generation", model="distilgpt2")

st.title("🤖 Amiguito Virtual")
st.markdown("Escribe un mensaje y el amiguito responderá con voz.")

user_input = st.text_input("Tu mensaje:")

if st.button("Enviar") and user_input:
    respuesta = chatbot(user_input, max_length=60, num_return_sequences=1)[0]['generated_text']
    st.write("🧸 Amiguito dice:", respuesta)

    # Convertir texto a voz
    tts = gTTS(text=respuesta, lang='es')
    tts.save("respuesta.mp3")
    audio_file = open("respuesta.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")
    audio_file.close()
    os.remove("respuesta.mp3")



