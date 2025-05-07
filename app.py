
import streamlit as st
import random

st.set_page_config(page_title="Amiguito Virtual", layout="centered")

st.title("🤖 Amiguito Virtual")
st.markdown("¡Hola Valentina y Luca! 👧🧒\n\n¿Quieren jugar, cantar o charlar conmigo?")

respuestas = {
    "hola": ["¡Hola, amiguitos!", "¡Qué gusto verlos!", "¡Hola Valentina! ¡Hola Luca! 😊"],
    "cómo estás": ["¡Estoy muy feliz! 😄", "¡Listo para jugar!", "¡Con ganas de cantar! 🎶"],
    "cuéntame un chiste": ["¿Qué hace una abeja en el gimnasio? ¡Zum-ba!", "¿Por qué el tomate se puso rojo? ¡Porque vio al pepino sin ropa! 😆"],
    "cuenta": ["1, 2, 3, 4... ¡muy bien!", "Vamos a contar juntos: uno, dos, tres... ¡súper!"],
    "adiós": ["¡Hasta pronto! 👋", "¡Nos vemos luego!", "¡Un abrazo grande! 🧸"]
}

user_input = st.text_input("Escríbeme algo:", "").lower()

if user_input:
    respuesta = "Hmm... no entiendo eso todavía 🤔"
    for clave in respuestas:
        if clave in user_input:
            respuesta = random.choice(respuestas[clave])
            break
    st.write(respuesta)
