import streamlit as st
import openai
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

st.title("🌍 Traductor por voz con Whisper (OpenAI)")

idiomas = {
    "Español": "es",
    "Inglés": "en",
    "Francés": "fr",
    "Alemán": "de",
    "Italiano": "it"
}

idioma_origen = st.selectbox("Idioma de origen", list(idiomas.keys()))
idioma_destino = st.selectbox("Idioma de destino", list(idiomas.keys()))

#openai_api_key = st.text_input("🔑 Introduce tu OpenAI API Key", type="password")

openai_api_key="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"
audio_file = st.audio_input("🎤 Graba tu voz")

if audio_file is not None and openai_api_key:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_file.read())
        audio_path = f.name

    st.audio(audio_path, format="audio/wav")

    try:
        openai.api_key = openai_api_key
        with open(audio_path, "rb") as audio:
            transcript = openai.Audio.transcribe("whisper-1", audio)
        texto = transcript["text"]
        st.success(f"📝 Texto transcrito: {texto}")

        resultado = GoogleTranslator(source=idiomas[idioma_origen], target=idiomas[idioma_destino]).translate(texto)
        st.success(f"🌐 Traducción: {resultado}")

        tts = gTTS(text=resultado, lang=idiomas[idioma_destino])
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")

    except Exception as e:
        st.error(f"❌ Error: {e}")
elif audio_file and not openai_api_key:
    st.warning("Por favor, introduce tu OpenAI API Key para transcribir.")
