
import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Amiguito Virtual", layout="centered")

st.title("🤖 Amiguito Virtual")
st.markdown("¡Hola! Soy tu amiguito virtual. ¿Quieres jugar o hablar un ratito? 😊")

# Inicializar modelo solo una vez
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="tiiuae/falcon-7b-instruct", max_new_tokens=100)

generator = load_model()

user_input = st.text_input("Escríbeme algo:", "")

if user_input:
    with st.spinner("Pensando..."):
        response = generator(user_input, max_new_tokens=100)[0]["generated_text"]
        st.write(response)
