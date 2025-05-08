import streamlit as st
import random
from gtts import gTTS
import base64
from io import BytesIO
import os
import uuid
import datetime
from streamlit_audio_recorder import audio_recorder
import whisper
import firebase_admin
from firebase_admin import credentials, storage, firestore

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'TU_BUCKET_NAME.appspot.com'  # ← Reemplaza esto
    })
    db = firestore.client()

bucket = storage.bucket()

st.set_page_config(page_title="Amiguito Virtual", layout="centered")
st.title("🤖 Amiguito Virtual")
st.markdown("¡Toca un botón para hablar conmigo o graba tu voz! 👇")

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
    mensaje = random.choice(respuestas["chiste"])
    st.info(mensaje)
    st.markdown(generar_audio(mensaje), unsafe_allow_html=True)

if col3.button("🔢 Contar"):
    mensaje = random.choice(respuestas["contar"])
    st.warning(mensaje)
    st.markdown(generar_audio(mensaje), unsafe_allow_html=True)

if col4.button("👋 Adiós"):
    mensaje = random.choice(respuestas["despedida"])
    st.error(mensaje)
    st.markdown(generar_audio(mensaje), unsafe_allow_html=True)

st.markdown("---")
st.subheader("🎤 ¡Ahora tú puedes hablar!")

audio_data = audio_recorder(pause_threshold=3.0, sample_rate=44100, text="Presiona para grabar")

if audio_data:
    st.audio(audio_data, format="audio/wav")

    filename = f"grabacion_{uuid.uuid4().hex}.wav"
    with open(filename, "wb") as f:
        f.write(audio_data)

    st.success("Grabación guardada localmente")

    with st.spinner("Transcribiendo con IA..."):
        model = whisper.load_model("base")
        result = model.transcribe(filename)
        texto_voz = result["text"].strip()
        st.markdown("**Lo que dijiste fue:**")
        st.success(texto_voz)

    nombre = "niño"
    for palabra in texto_voz.split():
        if palabra.lower() in ["valentina", "luca", "emma", "juan", "sofia"]:
            nombre = palabra.capitalize()
            break

    texto_min = texto_voz.lower()
    if "hola" in texto_min:
        respuesta = random.choice(respuestas["saludo"])
    elif "chiste" in texto_min:
        respuesta = random.choice(respuestas["chiste"])
    elif "contar" in texto_min:
        respuesta = random.choice(respuestas["contar"])
    elif "adiós" in texto_min:
        respuesta = random.choice(respuestas["despedida"])
    else:
        respuesta = "¡Qué bonito lo que dijiste!"

    st.markdown("**Respuesta del amiguito virtual:**")
    st.info(respuesta)
    st.markdown(generar_audio(respuesta), unsafe_allow_html=True)

    blob = bucket.blob(f"grabaciones/{filename}")
    blob.upload_from_filename(filename)
    audio_url = blob.public_url

    doc = {
        "nombre": nombre,
        "texto_transcrito": texto_voz,
        "respuesta_bot": respuesta,
        "archivo_url": audio_url,
        "timestamp": datetime.datetime.utcnow()
    }
    db.collection("interacciones").add(doc)
    st.success("¡Guardado en la nube!")

