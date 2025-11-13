"""
Nexa Backend Main Application
FastAPI application with all VocalPA features ported to Python
"""

import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from .config import get_settings, validate_api_keys, get_feature_flags
from .routes import (
    auth, status, commands, voice, weather, news, music, 
    conversations, preferences, analytics, system
)
from ..shared.database.connection import init_database, get_database


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    settings = get_settings()
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Initialize database
    try:
        init_database(settings.database_url)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    # Validate API keys
    missing_keys = validate_api_keys(settings)
    if missing_keys:
        logger.warning(f"Missing API keys: {', '.join(missing_keys)}")
    
    # Log feature availability
    features = get_feature_flags(settings)
    enabled_features = [k for k, v in features.items() if v]
    logger.info(f"Enabled features: {', '.join(enabled_features)}")
    
    # Create upload directory
    os.makedirs(settings.upload_dir, exist_ok=True)
    
    yield
    
    # Shutdown
    logger.info("Shutting down Nexa backend")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        description="Python-based voice assistant with comprehensive AI features",
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan
    )
    
    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(status.router, prefix="/api/v1/status", tags=["System Status"])
    app.include_router(commands.router, prefix="/api/v1/commands", tags=["Commands"])
    app.include_router(voice.router, prefix="/api/v1/voice", tags=["Voice"])
    app.include_router(weather.router, prefix="/api/v1/weather", tags=["Weather"])
    app.include_router(news.router, prefix="/api/v1/news", tags=["News"])
    app.include_router(music.router, prefix="/api/v1/music", tags=["Music"])
    app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["Conversations"])
    app.include_router(preferences.router, prefix="/api/v1/preferences", tags=["Preferences"])
    app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
    app.include_router(system.router, prefix="/api/v1/system", tags=["System"])
    
    # Serve static files
    if os.path.exists("static"):
        app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Basic health check"""
        db = get_database()
        db_healthy = db.health_check()
        
        return {
            "status": "healthy" if db_healthy else "unhealthy",
            "database": "connected" if db_healthy else "disconnected",
            "version": settings.app_version
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint with API information"""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "status": "running",
            "docs": "/docs",
            "features": get_feature_flags(settings)
        }
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
