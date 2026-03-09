from fastapi import FastAPI, File, UploadFile
import requests
import os

app = FastAPI()

# Get API key from Render environment variable
BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY")


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Robot Server Running Successfully"
    }


@app.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):

    # Check if API key exists
    if not BYTEZ_API_KEY:
        return {"error": "BYTEZ_API_KEY environment variable not set"}

    try:
        # Read uploaded audio file
        audio_data = await file.read()

        headers = {
            "Authorization": f"Bearer {BYTEZ_API_KEY}"
        }

        files = {
            "file": ("audio.wav", audio_data, "audio/wav"),
            "model": (None, "whisper-large-v3")
        }

        response = requests.post(
            "https://api.bytez.com/v1/audio/transcriptions",
            headers=headers,
            files=files,
            timeout=60
        )

        # Print raw response for debugging
        print("API RESPONSE STATUS:", response.status_code)
        print("API RESPONSE TEXT:", response.text)

        # Try returning JSON
        try:
            return response.json()
        except:
            return {
                "status_code": response.status_code,
                "response_text": response.text
            }

    except Exception as e:
        return {
            "error": str(e)
        }