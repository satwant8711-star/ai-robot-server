from fastapi import FastAPI, File, UploadFile
import requests
import os

app = FastAPI()

BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY")

@app.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):

    audio_data = await file.read()

    headers = {
        "Authorization": f"Bearer {BYTEZ_API_KEY}"
    }

    files = {
        "file": ("audio.wav", audio_data, "audio/wav"),
        "model": (None, "whisper-large-v3")
    }

    response = requests.post(
        "https://api.bytez.ai/v1/audio/transcriptions",
        headers=headers,
        files=files
    )

    return response.json()