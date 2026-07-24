from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os
print("=" * 60)
print("LOADED NEW MAIN.PY")
print("=" * 60)
# ============================
# Load Environment Variables
# ============================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API Key not found in .env file.")

# ============================
# Initialize Gemini Client
# ============================

client = genai.Client(api_key=API_KEY)

# ============================
# FastAPI App
# ============================

app = FastAPI(title="AI Content Generation Tool")

# ============================
# Enable CORS
# ============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# Request Model
# ============================

class RequestData(BaseModel):
    task: str
    text: str

# ============================
# Home Route
# ============================

@app.get("/")
def home():
    return {
        "message": "AI Content Generation Tool API is Running!"
    }

# ============================
# Generate Route
# ============================

@app.post("/generate")
def generate(data: RequestData):

    task = data.task.lower().strip()
    text = data.text.strip()

    # ------------------------
    # Build Prompt
    # ------------------------

    if task == "summary":
        prompt = f"""
Summarize the following text in clear, concise bullet points.

{text}
"""

    elif task == "email":
        prompt = f"""
Write a professional email based on the following request.

{text}
"""

    elif task == "rewrite":
        prompt = f"""
Rewrite the following text with improved grammar, vocabulary, and clarity.

{text}
"""

    elif task == "article":
        prompt = f"""
Write a detailed article on the following topic.

{text}
"""

    elif task == "creative":
        prompt = f"""
Write a creative story or paragraph based on the following idea.

{text}
"""

    elif task == "notes":
        prompt = f"""
Convert the following content into well-structured study notes with headings and bullet points.

{text}
"""

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid task selected."
        )

    # ------------------------
    # Gemini Model
    # ------------------------

    MODEL = "models/gemini-flash-latest"

    print("=" * 60)
    print("Using model:", MODEL)
    print("=" * 60)

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return {
            "success": True,
            "model": MODEL,
            "task": task,
            "output": response.text
        }

    except Exception as e:

        print("\nGemini Error:")
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Gemini Error: {str(e)}"
        )