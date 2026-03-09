from fastapi import FastAPI, File, UploadFile
import requests
import os

app = FastAPI()

# Get API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Robot Server Running Successfully"
    }


@app.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):

    if not GROQ_API_KEY:
        return {"error": "GROQ_API_KEY not set"}

    try:
        audio_data = await file.read()

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }

        files = {
            "file": ("audio.wav", audio_data, "audio/wav"),
            "model": (None, "whisper-large-v3")
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers=headers,
            files=files,
            timeout=60
        )

        print(response.text)

        try:
            return response.json()
        except:
            return {
                "status_code": response.status_code,
                "response_text": response.text
            }

    except Exception as e:
        return {"error": str(e)}
@app.post("/chat")
async def chat_with_ai(message: str):

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )

    return response.json()