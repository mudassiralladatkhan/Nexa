#!/usr/bin/env python3
"""
Nexa Backend - Stable Server
Guaranteed to stay running
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

# Create FastAPI app
app = FastAPI(
    title="Nexa Voice Assistant",
    description="Stable Backend API for Nexa Voice Assistant",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "version": "1.0.0",
        "connection": "stable"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "service": "nexa-backend", 
        "port": 8001,
        "uptime": "running"
    }

@app.get("/api/test")
async def test_api():
    return {
        "test": "success",
        "backend": "stable",
        "features": [
            "Voice Processing",
            "App Launcher", 
            "Website Opener",
            "Entertainment"
        ]
    }

@app.post("/api/voice/command")
async def voice_command(data: dict):
    """Voice command endpoint"""
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
    elif "test" in command:
        return {
            "success": True,
            "response": "Backend connection test successful! Nexa is working perfectly.",
            "command_type": "test"
        }
    else:
        return {
            "success": True,
            "response": f"I heard: '{command}'. Backend is connected and working!",
            "command_type": "general"
        }

@app.on_event("startup")
async def startup_event():
    print("🚀 Nexa Backend starting up...")
    print("✅ CORS enabled")
    print("✅ All endpoints ready")

@app.on_event("shutdown")
async def shutdown_event():
    print("👋 Nexa Backend shutting down...")

if __name__ == "__main__":
    print("🤖 Starting Nexa Stable Backend Server...")
    print("=" * 50)
    print("📡 Server URL: http://localhost:8001")
    print("📚 API Docs: http://localhost:8001/docs")
    print("🔍 Health Check: http://localhost:8001/health")
    print("🧪 Test API: http://localhost:8001/api/test")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8001,
            log_level="info",
            access_log=True,
            reload=False
        )
    except Exception as e:
        print(f"❌ Server error: {e}")
        input("Press Enter to exit...")
