from fastapi import FastAPI, File, UploadFile
import requests
import os

app = FastAPI()

BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY")


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Robot Server Running Successfully"
    }


@app.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):

    if not BYTEZ_API_KEY:
        return {"error": "BYTEZ_API_KEY not set"}

    audio_data = await file.read()

    headers = {
        "Authorization": f"Bearer {BYTEZ_API_KEY}"
    }

    files = {
        "file": ("audio.wav", audio_data, "audio/wav"),
        "model": (None, "whisper-large-v3")
    }

    try:
        response = requests.post(
            "https://api.bytez.ai/v1/audio/transcriptions",
            headers=headers,
            files=files,
            timeout=60
        )

        return response.json()

    except Exception as e:
        return {"error": str(e)}








