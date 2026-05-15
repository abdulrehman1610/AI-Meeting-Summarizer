import whisper
import os

def load_model(model_size="base"):
    print(f"Loading Whisper model: {model_size}...")
    # This downloads the model to ~/.cache/whisper on Windows automatically
    return whisper.load_model(model_size)

def transcribe_audio(model, audio_chunks):
    full_transcript = ""
    
    for chunk_path in audio_chunks:
        print(f"Transcribing chunk: {chunk_path}...")
        result = model.transcribe(chunk_path)
        full_transcript += result["text"] + " "
        
    return full_transcript.strip()