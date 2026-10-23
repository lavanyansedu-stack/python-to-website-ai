
import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://lavanyansedu-stack.github.io"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebsiteRequest(BaseModel):
    code: str
    framework: str = "Streamlit"

@app.get("/")
def home():
    return {"message": "Python-to-Website AI backend is running"}

@app.post("/generate")
def generate(data: WebsiteRequest):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"error": "GROQ_API_KEY is not configured"}

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-oss-120b",
            "messages": [{
                "role": "user",
                "content": (
                    "Create a website using " + data.framework +
                    " from this Python code. Return the complete "
                    "generated code only:\n" + data.code
                )
            }],
            "temperature": 0.2,
        },
        timeout=90,
    )
    response.raise_for_status()
    result = response.json()
    return {
        "generated_code":
            result["choices"][0]["message"]["content"]
    }
