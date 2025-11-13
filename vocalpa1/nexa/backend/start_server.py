#!/usr/bin/env python3
"""
Nexa Backend - Guaranteed Working Server
"""

from fastapi import FastAPI
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Nexa Voice Assistant",
    description="Backend API for Nexa Voice Assistant",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "🤖 Nexa Voice Assistant Backend is running!",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "nexa-backend"}

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
    print("🚀 Starting Nexa Backend Server...")
    print("📡 Server URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("🧪 Test API: http://localhost:8000/api/test")
    print("💡 Press Ctrl+C to stop")
    print("-" * 50)
    
    uvicorn.run(
        "start_server:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        access_log=True
    )
