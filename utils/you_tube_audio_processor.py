
import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR,exist_ok = True)

def extract_audio(url :str) ->str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    try:
       with yt_dlp.YoutubeDL(ydl_opts) as ydl:
           info = ydl.extract_info(url, download=True)
           filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
       return filename
    except Exception as e:
        print(f"Error: {e}")
        return None



def convert_to_mono(wav_path: str) -> str:
    """ Convert WAV audio to mono and set sample rate to 16000 Hz."""

    try:
        audio = AudioSegment.from_wav(wav_path)

        mono_audio = (audio.set_channels(1).set_frame_rate(16000))

        mono_path = wav_path.replace(".wav", "_mono.wav")

        mono_audio.export(mono_path, format="wav")

        return mono_path
    except Exception as e:
        print(f"Error: {e}")
        return None



def chunk_audio(wav_path : str , chunk_minutes : int = 5) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 
    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

        chunks.append(chunk_path)
    
    return chunks

def all_audio_process(url: str) -> list:
    if url.startswith("http:") or url.startswith("https:"):
        wav_path = extract_audio(url)
    else:
        wav_path = convert_to_mono(url)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks

# print(all_audio_process("https://www.youtube.com/watch?v=TLKxdTmk-zc&t=118s"))