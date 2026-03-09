from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import requests
import os
from gtts import gTTS
import tempfile
import wave

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

STT_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"


@app.post("/robot")
async def robot(file: UploadFile = File(...)):

    try:

        # -------- read uploaded raw audio --------
        raw_audio = await file.read()

        # -------- create proper WAV file --------
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

        with wave.open(temp_wav.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)   # 16-bit audio
            wf.setframerate(16000)
            wf.writeframes(raw_audio)

        # -------- Speech to Text --------
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }

        files = {
            "file": ("audio.wav", open(temp_wav.name, "rb"), "audio/wav")
        }

        data = {
            "model": "whisper-large-v3"
        }

        stt_response = requests.post(
            STT_URL,
            headers=headers,
            files=files,
            data=data
        )

        stt_json = stt_response.json()

        if "text" not in stt_json:
            return JSONResponse({
                "error": "Speech recognition failed",
                "details": stt_json
            })

        text = stt_json["text"]

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

        chat_json = chat_response.json()

        ai_reply = chat_json["choices"][0]["message"]["content"]

        # -------- Text to Speech --------
        tts = gTTS(text=ai_reply, lang="en")

        filename = "reply.mp3"
        tts.save(filename)

        return FileResponse(filename, media_type="audio/mpeg")

    except Exception as e:
        return JSONResponse({
            "error": "Server error",
            "details": str(e)
        })