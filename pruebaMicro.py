import streamlit as st
import speech_recognition as sr
import tempfile

st.title("🎤 Traductor con entrada de voz en navegador")

# Grabación desde navegador
audio_file = st.audio_input("Graba tu voz:")

if audio_file is not None:
    st.audio(audio_file)

    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio.flush()
        with sr.AudioFile(temp_audio.name) as source:
            audio = recognizer.record(source)

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        st.success(f"Texto reconocido: {texto}")
    except sr.UnknownValueError:
        st.error("No se entendió el audio.")
    except sr.RequestError:
        st.error("Error al conectar con el servicio de reconocimiento.")