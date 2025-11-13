#!/usr/bin/env python3
"""
Nexa Backend Startup Script
Run this to start the Nexa voice assistant backend server
"""

import os
import sys
import uvicorn
import logging
from pathlib import Path

# Add the project root and parent directory to Python path
project_root = Path(__file__).parent
nexa_root = project_root.parent  # This is the nexa directory
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(nexa_root))

from app.config import get_settings
from app.main import app


def setup_logging():
    """Configure logging for the application"""
    settings = get_settings()
    
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if settings.log_file:
        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper()),
            format=log_format,
            handlers=[
                logging.FileHandler(settings.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
    else:
        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper()),
            format=log_format,
            handlers=[logging.StreamHandler(sys.stdout)]
        )


def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'sqlalchemy', 'httpx', 
        'speechrecognition', 'pyttsx3', 'psutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    return True


def check_environment():
    """Check environment configuration"""
    settings = get_settings()
    
    print("🔧 Environment Configuration:")
    print(f"   Debug Mode: {settings.debug}")
    print(f"   Host: {settings.host}")
    print(f"   Port: {settings.port}")
    print(f"   Database: {settings.database_url.split('://')[0]}://***")
    
    # Check API keys
    api_status = []
    if settings.openweather_api_key or settings.weatherapi_key:
        api_status.append("✅ Weather API")
    else:
        api_status.append("❌ Weather API (no keys)")
    
    if settings.newsapi_key:
        api_status.append("✅ News API")
    else:
        api_status.append("❌ News API (no key)")
    
    if settings.spotify_client_id and settings.spotify_client_secret:
        api_status.append("✅ Spotify API")
    else:
        api_status.append("❌ Spotify API (no keys)")
    
    print("🔑 API Keys Status:")
    for status in api_status:
        print(f"   {status}")
    
    return True


def main():
    """Main startup function"""
    print("🚀 Starting Nexa Voice Assistant Backend")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup logging
    setup_logging()
    
    # Check environment
    check_environment()
    
    # Get settings
    settings = get_settings()
    
    print("\n📡 Starting server...")
    print(f"   URL: http://{settings.host}:{settings.port}")
    print(f"   Docs: http://{settings.host}:{settings.port}/docs")
    print(f"   Health: http://{settings.host}:{settings.port}/health")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the server
    try:
        uvicorn.run(
            app,
            host=settings.host,
            port=settings.port,
            reload=settings.debug,
            log_level=settings.log_level.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down Nexa backend...")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
