import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

st.title("🌍 Traductor desde voz (compatible con móvil y nube)")

idiomas = {
    "Español": "es",
    "Inglés": "en",
    "Francés": "fr",
    "Alemán": "de",
    "Italiano": "it"
}

idioma_origen = st.selectbox("Idioma de origen", list(idiomas.keys()))
idioma_destino = st.selectbox("Idioma de destino", list(idiomas.keys()))

# Graba desde navegador (funciona en móvil y PC)
audio_file = st.audio_input("🎤 Graba tu voz en el idioma seleccionado")

if audio_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_file.read())
        audio_path = f.name

    st.audio(audio_path, format="audio/wav")

    # Aquí iría la transcripción con Whisper o API externa.
    # Como ejemplo, ponemos un texto simulado.
    texto = "Hola, ¿cómo estás?"
    st.markdown(f"📝 Texto reconocido (simulado): `{texto}`")

    # Traducción
    resultado = GoogleTranslator(source=idiomas[idioma_origen], target=idiomas[idioma_destino]).translate(texto)
    st.success(f"Traducción: {resultado}")

    # Conversión a voz
    tts = gTTS(text=resultado, lang=idiomas[idioma_destino])
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")
