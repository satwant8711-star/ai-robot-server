from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# GROQ API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
WHISPER_URL = "https://api.groq.com/openai/v1/audio/transcriptions"


# -------- Chat Request Model --------
class ChatRequest(BaseModel):
    message: str


# -------- AI Chat Endpoint --------
@app.post("/chat")
def chat(request: ChatRequest):

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": request.message}
        ]
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=data)

        return {
            "status_code": response.status_code,
            "response": response.json()
        }

    except Exception as e:
        return {"error": str(e)}


# -------- Speech to Text Endpoint --------
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    files = {
        "file": (file.filename, await file.read(), "audio/wav")
    }

    data = {
        "model": "whisper-large-v3"
    }

    try:
        response = requests.post(
            WHISPER_URL,
            headers=headers,
            files=files,
            data=data
        )

        return {
            "status_code": response.status_code,
            "response": response.json()
        }

    except Exception as e:
        return {"error": str(e)}


# -------- Root Endpoint --------
@app.get("/")
def home():
    return {"message": "AI Robot Server Running"}