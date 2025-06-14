import streamlit as st
from openai import OpenAI  # Cliente oficial para acceder a la API de OpenAI
from deep_translator import GoogleTranslator # API de traducción automática
from gtts.lang import tts_langs # Lista de idiomas soportados por gTTS
from gtts import gTTS  # Motor de texto a voz de Google
import tempfile # Para crear archivos temporales (audio transcrito y sintetizado)
import traceback # Para capturar detalles de errores si ocurren

# Mostrar título
st.title("🌍 Traductor por voz con Whisper")

# Carga del diccionario
idiomas_gtts = lang.tts_langs()

# Cargamos los idiomas (codigo:nombre)
idiomas_codigo = {nombre.capitalize(): codigo for codigo, nombre in idiomas_gtts.items()}

# Lista de nombres ordenados para mostrar en el selectbox
idiomas_nombres = sorted(idiomas_codigo.keys())

# Mostrar selectboxes
idioma_origen_nombre = st.selectbox("Idioma de origen", idiomas_nombres,index=idiomas_nombres.index("Spanish"))  # <- esto selecciona español por defecto
idioma_destino_nombre = st.selectbox("Idioma de destino", idiomas_nombres, index=idiomas_nombres.index("English"))

# Obtener los códigos de los seleccionados
idioma_origen = idiomas_codigo[idioma_origen_nombre]
idioma_destino = idiomas_codigo[idioma_destino_nombre]

#cargamos la clave de open ia esta se pasa en un campo de streamlit que no se muestra a los usuarios
api_key=st.secrets["APIKEY"]

audio_file = st.audio_input("🎤 Graba tu voz")

# Si hay un audio grabado y la API key está disponible
if audio_file is not None and api_key:
    # Guardamos el archivo de audio temporalmente en formato WAV
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_file.read())
        audio_path = f.name
        
    # Mostramos un reproductor de audio para el archivo grabado
    st.audio(audio_path, format="audio/wav")

    try:
        # Creamos el cliente de OpenAI con nuestra clave
        client = OpenAI(api_key=api_key)

        # Enviamos el archivo de audio a Whisper para transcribir
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
               
        # Extraemos el texto de la transcripción
        texto = transcript.text
        st.success(f"📝 Texto transcrito: {texto}")

        # Traducimos el texto al idioma destino
        resultado = GoogleTranslator(source=idioma_origen, target=idioma_destino).translate(texto)
        st.success(f"🌐 Traducción: {resultado}")
        
        # Usamos gTTS para convertir el texto traducido en voz
        tts = gTTS(text=resultado, lang=idioma_destino)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")

    except Exception:
         # Si algo falla, mostramos la traza completa en consola (útil para debugging)
        print("error: ",traceback.print_exc())
        
 # Si se ha subido audio pero falta la API key       
elif audio_file and not api_key:
    st.warning("Introduce tu API key para transcribir.")
