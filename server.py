from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import requests
import os
from gtts import gTTS

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

STT_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"


@app.post("/robot")
async def robot(file: UploadFile = File(...)):

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    # -------- Speech to Text --------
    audio_data = await file.read()

    stt_files = {
        "file": ("audio.wav", audio_data, "audio/wav")
    }

    stt_data = {
        "model": "whisper-large-v3"
    }

    stt_response = requests.post(
        STT_URL,
        headers=headers,
        files=stt_files,
        data=stt_data
    )

    text = stt_response.json()["text"]

    # -------- AI Chat --------
    chat_headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    chat_data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": text}
        ]
    }

    chat_response = requests.post(
        CHAT_URL,
        headers=chat_headers,
        json=chat_data
    )

    ai_reply = chat_response.json()["choices"][0]["message"]["content"]

    # -------- Text to Speech --------
    tts = gTTS(text=ai_reply, lang="en")

    filename = "reply.mp3"
    tts.save(filename)

    return FileResponse(filename, media_type="audio/mpeg")