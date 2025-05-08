import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage

# Inicializar Firebase (si no se ha hecho)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'TU_BUCKET_NAME.appspot.com'  # ← Reemplaza con tu bucket
    })

db = firestore.client()
bucket = storage.bucket()

st.set_page_config(page_title="Historial", layout="centered")
st.title("📚 Historial de Conversaciones")

st.markdown("Aquí puedes ver y borrar grabaciones guardadas por los niños.")

interacciones_ref = db.collection("interacciones").order_by("timestamp", direction=firestore.Query.DESCENDING)
interacciones = list(interacciones_ref.stream())

if not interacciones:
    st.info("No hay interacciones guardadas.")
else:
    for doc in interacciones:
        datos = doc.to_dict()
        doc_id = doc.id
        st.markdown("---")
        st.subheader(f"👤 {datos.get('nombre', 'Niño desconocido')}")
        st.write(f"🕒 {datos.get('timestamp').strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"🗣️ Dijo: {datos.get('texto_transcrito')}")
        st.write(f"🤖 Respuesta: {datos.get('respuesta_bot')}")
        st.audio(datos.get("archivo_url"), format="audio/mp3")

        if st.button(f"🗑️ Borrar esta grabación", key=doc_id):
            # Borrar de Storage
            archivo_url = datos.get("archivo_url")
            if archivo_url:
                nombre_blob = archivo_url.split("/")[-1].split("?")[0]
                blob = bucket.blob(f"grabaciones/{nombre_blob}")
                blob.delete()

            # Borrar de Firestore
            db.collection("interacciones").document(doc_id).delete()
            st.success("Grabación eliminada. Recarga la página.")
            st.stop()