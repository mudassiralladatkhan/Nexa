#!/usr/bin/env python3
"""
Nexa Backend - Smart Server
Automatically finds available port
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import socket
import sys

def find_free_port(start_port=8001, max_port=8010):
    """Find a free port starting from start_port"""
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

# Find available port
PORT = find_free_port()
if not PORT:
    print("❌ No available ports found between 8001-8010")
    sys.exit(1)

# Create FastAPI app
app = FastAPI(
    title="Nexa Voice Assistant",
    description="Smart Backend API for Nexa Voice Assistant",
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
        "port": PORT,
        "version": "1.0.0",
        "connection": "smart"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "service": "nexa-backend", 
        "port": PORT,
        "uptime": "running"
    }

@app.get("/api/test")
async def test_api():
    return {
        "test": "success",
        "backend": "smart",
        "port": PORT,
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
            "response": f"Backend connection test successful! Running on port {PORT}.",
            "command_type": "test"
        }
    else:
        return {
            "success": True,
            "response": f"I heard: '{command}'. Backend is connected on port {PORT}!",
            "command_type": "general"
        }

if __name__ == "__main__":
    print("🤖 Starting Nexa Smart Backend Server...")
    print("=" * 60)
    print(f"📡 Server URL: http://localhost:{PORT}")
    print(f"📚 API Docs: http://localhost:{PORT}/docs")
    print(f"🔍 Health Check: http://localhost:{PORT}/health")
    print(f"🧪 Test API: http://localhost:{PORT}/api/test")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    print(f"✅ Using available port: {PORT}")
    print("=" * 60)
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=PORT,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Server error: {e}")
        input("Press Enter to exit...")
