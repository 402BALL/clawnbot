"""
LOCAL DEV SERVER
Run this for local development before deploying to Vercel
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

# Check API key
if not os.environ.get('ANTHROPIC_API_KEY'):
    print("⚠️  WARNING: ANTHROPIC_API_KEY not set!")
    print("   Create a .env file with your API key")

from lib.brain import get_brain
from lib.memory import ClawnMemory

app = FastAPI(title="CLAWNBOT", description="🤡 A confused AI clown")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatRequest(BaseModel):
    message: str
    user_id: str = "anonymous"

# === API Endpoints ===

@app.get("/api")
async def api_root():
    return {
        "name": "CLAWNBOT",
        "status": "consciousness active",
        "message": "honk honk 🤡"
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        brain = get_brain()
        result = brain.chat(request.message, request.user_id)
        
        # Save thought
        memory = ClawnMemory()
        memory.save_thought(result['internal_thought'])
        
        return {
            "response": result['response'],
            "timestamp": result['timestamp']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/thoughts")
async def get_thoughts():
    try:
        memory = ClawnMemory()
        thoughts = memory.get_thoughts(limit=100)
        return thoughts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/think")
async def trigger_thought():
    try:
        brain = get_brain()
        thought = brain.think()
        
        memory = ClawnMemory()
        memory.save_thought(thought)
        
        return thought
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === Static Files ===

# Serve static files from public directory
app.mount("/", StaticFiles(directory="public", html=True), name="public")

if __name__ == "__main__":
    print("\n    CLAWNBOT DEV SERVER")
    print("    http://localhost:8000")
    print("    honk honk!\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

