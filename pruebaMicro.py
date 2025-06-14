import streamlit as st
from openai import OpenAI
from deep_translator import GoogleTranslator
from gtts.lang import tts_langs
from gtts import gTTS
import tempfile

# Mostrar título
st.title("🌍 Traductor por voz con Whisper")

# Obtener lista de idiomas soportados por gTTS
idiomas_disponibles = tts_langs()
idiomas_ordenados = sorted(idiomas_disponibles.items(), key=lambda x: x[1].lower())

# Creamos diccionario nombre → código
idiomas_codigo = {nombre.capitalize(): codigo for codigo, nombre in idiomas_ordenados}
idiomas_nombres = list(idiomas_codigo.keys())

# Menús desplegables con búsqueda
idioma_origen_nombre = st.selectbox("Idioma de origen", idiomas_nombres)
idioma_destino_nombre = st.selectbox("Idioma de destino", idiomas_nombres)

idioma_origen = idiomas_codigo[idioma_origen_nombre]
idioma_destino = idiomas_codigo[idioma_destino_nombre]

api_key=st.secrets["APIKEY"]

audio_file = st.audio_input("🎤 Graba tu voz")

if audio_file is not None and api_key:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_file.read())
        audio_path = f.name

    st.audio(audio_path, format="audio/wav")

    try:
        client = OpenAI(api_key=api_key)
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        texto = transcript.text
        st.success(f"📝 Texto transcrito: {texto}")

        resultado = GoogleTranslator(source=idioma_origen, target=idioma_destino).translate(texto)
        tts = gTTS(text=resultado, lang=idioma_destino)

        tts = gTTS(text=resultado, lang=idiomas_codigo[idioma_destino])
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")

    except Exception as e:
        st.error(f"❌ Error: {e}")
elif audio_file and not api_key:
    st.warning("Introduce tu API key para transcribir.")
