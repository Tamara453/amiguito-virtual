
import streamlit as st
from gtts import gTTS
import os

# Respuestas simples basadas en palabras clave
def get_response(user_input):
    respuestas = {
        "hola": "¡Hola! ¿Cómo estás?",
        "cómo te llamas": "Me llamo Amiguito Virtual. 😊",
        "adiós": "¡Hasta pronto! 😄"
    }
    # Si encontramos una respuesta predefinida, la usamos
    for key, value in respuestas.items():
        if key in user_input.lower():
            return value
    return "No entiendo esa pregunta, ¿puedes decirme otra cosa?"

st.title("🤖 Amiguito Virtual")
st.markdown("Escribe un mensaje y el amiguito responderá con voz.")

user_input = st.text_input("Tu mensaje:")

if st.button("Enviar") and user_input:
    respuesta = get_response(user_input)
    st.write("🧸 Amiguito dice:", respuesta)

    # Convertir texto a voz
    tts = gTTS(text=respuesta, lang='es')
    tts.save("respuesta.mp3")
    audio_file = open("respuesta.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")
    audio_file.close()
    os.remove("respuesta.mp3")



