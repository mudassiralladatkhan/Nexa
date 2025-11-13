#!/usr/bin/env python3
"""
Nexa Backend - Simple Startup Script
Minimal version to get the server running quickly
"""

import os
import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add paths
project_root = Path(__file__).parent
nexa_root = project_root.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(nexa_root))

# Create simple FastAPI app
app = FastAPI(
    title="Nexa Voice Assistant API",
    description="Backend API for Nexa Voice Assistant",
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
    return {"message": "Nexa Voice Assistant Backend is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "nexa-backend"}

@app.get("/api/status")
async def api_status():
    return {
        "status": "running",
        "version": "1.0.0",
        "features": {
            "voice_processing": "available",
            "app_launcher": "available", 
            "website_opener": "available",
            "entertainment": "available"
        }
    }

# Simple voice command endpoint
@app.post("/api/voice/process")
async def process_voice_command(command: dict):
    try:
        # Import the command processor
        from shared.command_processor import CommandProcessor
        
        processor = CommandProcessor()
        result = await processor.process(command.get("text", ""))
        
        return {
            "success": True,
            "result": {
                "command_type": result.command_type,
                "response_text": result.response_text,
                "success": result.success
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Command processing failed"
        }

if __name__ == "__main__":
    print("🚀 Starting Nexa Voice Assistant Backend (Simple Mode)")
    print("=" * 60)
    print("✅ Server starting on: http://localhost:8000")
    print("✅ API Documentation: http://localhost:8000/docs")
    print("✅ Health Check: http://localhost:8000/health")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload to avoid the warning
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down Nexa backend...")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)
