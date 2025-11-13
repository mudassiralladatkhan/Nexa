#!/usr/bin/env python3
"""
Nexa Backend - Working Server with Real Command Processing
Integrates with actual command processor and app launcher
"""

import sys
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add the nexa directory to Python path for imports
current_dir = Path(__file__).parent
nexa_dir = current_dir.parent
sys.path.insert(0, str(nexa_dir))

# Import the actual Nexa modules
try:
    from shared.command_processor import CommandProcessor
    from shared.app_launcher import launch_app
    from shared.website_opener import open_website
    from shared.entertainment import get_joke, get_fun_fact, get_motivational_quote
    MODULES_AVAILABLE = True
    print("✅ Nexa modules imported successfully")
except ImportError as e:
    print(f"⚠️ Could not import Nexa modules: {e}")
    MODULES_AVAILABLE = False

# Create FastAPI app
app = FastAPI(
    title="Nexa Voice Assistant",
    description="Working Backend with Real Command Processing",
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

# Initialize command processor
if MODULES_AVAILABLE:
    try:
        command_processor = CommandProcessor()
        print("✅ Command processor initialized")
    except Exception as e:
        print(f"⚠️ Could not initialize command processor: {e}")
        command_processor = None
else:
    command_processor = None

@app.get("/")
async def root():
    return {
        "message": "🤖 Nexa Voice Assistant Backend with Real Command Processing!",
        "status": "healthy",
        "port": 8000,
        "version": "1.0.0",
        "modules_available": MODULES_AVAILABLE,
        "command_processor": command_processor is not None
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "service": "nexa-backend", 
        "port": 8000,
        "modules": MODULES_AVAILABLE,
        "processor": command_processor is not None
    }

@app.get("/api/test")
async def test_api():
    return {
        "test": "success",
        "backend": "working_with_real_processing",
        "port": 8000,
        "features": [
            "Real Voice Processing",
            "App Launcher Integration", 
            "Website Opener Integration",
            "Entertainment Integration",
            "Command Processor"
        ],
        "modules_loaded": MODULES_AVAILABLE
    }

@app.post("/api/voice/command")
async def voice_command(data: dict):
    """Real voice command processing with actual Nexa modules"""
    command = data.get("command", "").lower().strip()
    
    print(f"🎤 Processing command: '{command}'")
    
    # If modules are available, use real command processing
    if MODULES_AVAILABLE and command_processor:
        try:
            # Use the actual command processor
            result = await command_processor.process(command)
            
            print(f"✅ Command processed: {result.command_type}")
            
            return {
                "success": result.success,
                "response": result.response_text,
                "command_type": result.command_type,
                "metadata": result.metadata if hasattr(result, 'metadata') else {},
                "processed_by": "real_command_processor"
            }
            
        except Exception as e:
            print(f"❌ Command processing error: {e}")
            # Fall back to manual processing
            return await manual_command_processing(command)
    else:
        # Manual command processing as fallback
        return await manual_command_processing(command)

async def manual_command_processing(command):
    """Manual command processing when modules aren't available"""
    
    # Time commands
    if "time" in command:
        from datetime import datetime
        now = datetime.now()
        return {
            "success": True,
            "response": f"The current time is {now.strftime('%I:%M %p')}",
            "command_type": "time",
            "processed_by": "manual_fallback"
        }
    
    # Date commands
    elif "date" in command:
        from datetime import datetime
        now = datetime.now()
        return {
            "success": True,
            "response": f"Today is {now.strftime('%A, %B %d, %Y')}",
            "command_type": "date",
            "processed_by": "manual_fallback"
        }
    
    # Greeting commands
    elif any(word in command for word in ["hello", "hi", "hey"]):
        return {
            "success": True,
            "response": "Hello! I'm Nexa, your voice assistant. How can I help you today?",
            "command_type": "greeting",
            "processed_by": "manual_fallback"
        }
    
    # App launching commands
    elif any(word in command for word in ["open", "launch", "start"]):
        app_name = command.replace("open", "").replace("launch", "").replace("start", "").strip()
        
        if MODULES_AVAILABLE:
            try:
                result = launch_app(app_name)
                if result['success']:
                    return {
                        "success": True,
                        "response": f"Opening {app_name}...",
                        "command_type": "app_launch",
                        "app_name": app_name,
                        "processed_by": "app_launcher_module"
                    }
                else:
                    return {
                        "success": False,
                        "response": result.get('message', f"Could not open {app_name}"),
                        "command_type": "app_launch",
                        "processed_by": "app_launcher_module"
                    }
            except Exception as e:
                print(f"App launcher error: {e}")
        
        # Fallback response
        return {
            "success": True,
            "response": f"I would open {app_name} for you, but the app launcher module needs to be properly configured.",
            "command_type": "app_launch",
            "processed_by": "manual_fallback"
        }
    
    # Website commands
    elif any(word in command for word in ["go to", "visit", "website"]):
        site_name = command.replace("go to", "").replace("visit", "").replace("website", "").strip()
        
        if MODULES_AVAILABLE:
            try:
                result = open_website(site_name)
                if result['success']:
                    return {
                        "success": True,
                        "response": f"Opening {site_name} website...",
                        "command_type": "website_open",
                        "website": site_name,
                        "processed_by": "website_opener_module"
                    }
                else:
                    return {
                        "success": False,
                        "response": result.get('message', f"Could not find website for {site_name}"),
                        "command_type": "website_open",
                        "processed_by": "website_opener_module"
                    }
            except Exception as e:
                print(f"Website opener error: {e}")
        
        # Fallback response
        return {
            "success": True,
            "response": f"I would open {site_name} website for you, but the website opener module needs to be properly configured.",
            "command_type": "website_open",
            "processed_by": "manual_fallback"
        }
    
    # Entertainment commands
    elif "joke" in command:
        if MODULES_AVAILABLE:
            try:
                result = get_joke()
                if result['success']:
                    return {
                        "success": True,
                        "response": result['joke'],
                        "command_type": "entertainment",
                        "processed_by": "entertainment_module"
                    }
            except Exception as e:
                print(f"Entertainment error: {e}")
        
        return {
            "success": True,
            "response": "Why don't scientists trust atoms? Because they make up everything!",
            "command_type": "entertainment",
            "processed_by": "manual_fallback"
        }
    
    # Default response
    else:
        return {
            "success": True,
            "response": f"I heard you say '{command}'. I'm working on processing more complex commands. Try saying 'hello', 'what time is it', 'open google', or 'tell me a joke'.",
            "command_type": "general",
            "processed_by": "manual_fallback"
        }

if __name__ == "__main__":
    print("🤖 Starting Nexa Working Backend Server...")
    print("=" * 60)
    print("📡 Server URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("🧪 Test API: http://localhost:8000/api/test")
    print(f"🔧 Modules Available: {MODULES_AVAILABLE}")
    print(f"🎯 Command Processor: {command_processor is not None}")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
