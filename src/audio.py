import whisper
import io

# Load the base English model once to save resources
model = whisper.load_model("base.en")

def transcribe_audio(audio_bytes):
    """
    Transcribes audio bytes into text using OpenAI's Whisper model.
    """
    if not audio_bytes:
        return ""
    
    try:
        # Create a file-like object from the audio bytes
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "temp_audio.wav" # Whisper needs a named file

        # Transcribe
        result = model.transcribe(audio_file.name, fp16=False)
        return result["text"]
    except Exception as e:
        return f"Audio transcription failed: {e}"