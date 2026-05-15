import os
import subprocess
from pydub import AudioSegment
from pydub.utils import which

# Ensure ffmpeg is found (Windows sometimes needs this hint if not in PATH correctly)
AudioSegment.converter = which("ffmpeg") or "ffmpeg"

TEMP_DIR = os.path.join(os.getcwd(), "temp_chunks")

def convert_to_wav(input_path):
    """Converts any input audio/video to 16kHz mono WAV."""
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        
    output_path = os.path.join(TEMP_DIR, "normalized.wav")
    
    command = [
        "ffmpeg", "-y", "-i", input_path,
        "-ar", "16000", 
        "-ac", "1",      
        output_path
    ]
    
    # Hide ffmpeg console window on Windows
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
    return output_path

def chunk_audio(audio_path, chunk_length_ms=600000):
    """Splits audio into chunks if longer than 10 mins."""
    audio = AudioSegment.from_wav(audio_path)
    chunks = []
    
    if len(audio) > chunk_length_ms:
        print(f"Audio length {len(audio)/1000}s is long. Chunking...")
        for i in range(0, len(audio), chunk_length_ms - 10000):
            chunk = audio[i:i + chunk_length_ms]
            chunk_name = os.path.join(TEMP_DIR, f"chunk_{i}.wav")
            chunk.export(chunk_name, format="wav")
            chunks.append(chunk_name)
        return chunks
    else:
        return [audio_path]