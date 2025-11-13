#!/usr/bin/env python3
"""
Nexa Backend - Alternative Port 8001
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Nexa Voice Assistant",
    description="Backend API for Nexa Voice Assistant",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🤖 Nexa Voice Assistant Backend is running!",
        "status": "healthy",
        "port": 8001,
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "nexa-backend", "port": 8001}

@app.get("/api/test")
async def test_api():
    return {
        "test": "success",
        "features": [
            "Voice Processing",
            "App Launcher", 
            "Website Opener",
            "Entertainment"
        ]
    }

@app.post("/api/voice/command")
async def voice_command(data: dict):
    """Simple voice command endpoint"""
    command = data.get("command", "").lower()
    
    if "time" in command:
        from datetime import datetime
        now = datetime.now()
        return {
            "success": True,
            "response": f"The current time is {now.strftime('%I:%M %p')}",
            "command_type": "time"
        }
    elif "hello" in command or "hi" in command:
        return {
            "success": True,
            "response": "Hello! I'm Nexa, your voice assistant. How can I help you?",
            "command_type": "greeting"
        }
    else:
        return {
            "success": True,
            "response": f"I heard: '{command}'. This is a test response from Nexa backend!",
            "command_type": "general"
        }

if __name__ == "__main__":
    print("🚀 Starting Nexa Backend Server on Port 8001...")
    print("📡 Server URL: http://localhost:8001")
    print("📚 API Docs: http://localhost:8001/docs")
    print("🔍 Health Check: http://localhost:8001/health")
    print("🧪 Test API: http://localhost:8001/api/test")
    print("💡 Press Ctrl+C to stop")
    print("-" * 50)
    
    uvicorn.run(
        "start_backend_8001:app",
        host="127.0.0.1",
        port=8001,
        log_level="info",
        access_log=True
    )
