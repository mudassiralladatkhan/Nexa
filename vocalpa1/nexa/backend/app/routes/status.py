"""
System status and health monitoring routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
import psutil
import platform
from datetime import datetime

from ..config import get_settings, get_feature_flags
from shared.database.connection import get_db_session, get_database
from shared.database.repositories import RepositoryFactory

router = APIRouter()


class SystemStatus(BaseModel):
    status: str
    timestamp: datetime
    uptime: float
    database: Dict[str, Any]
    system: Dict[str, Any]
    features: Dict[str, bool]
    performance: Dict[str, Any]


@router.get("/", response_model=SystemStatus)
async def get_system_status(db: Session = Depends(get_db_session)):
    """Get comprehensive system status"""
    settings = get_settings()
    db_manager = get_database()
    
    # Database health
    db_healthy = db_manager.health_check()
    
    # System information
    system_info = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor(),
        "python_version": platform.python_version()
    }
    
    # Performance metrics
    performance = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "boot_time": datetime.fromtimestamp(psutil.boot_time())
    }
    
    return SystemStatus(
        status="healthy" if db_healthy else "degraded",
        timestamp=datetime.utcnow(),
        uptime=psutil.boot_time(),
        database={
            "connected": db_healthy,
            "url": settings.database_url.split("://")[0] + "://***"  # Hide credentials
        },
        system=system_info,
        features=get_feature_flags(settings),
        performance=performance
    )


@router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "ok", "timestamp": datetime.utcnow()}


@router.get("/version")
async def get_version():
    """Get application version information"""
    settings = get_settings()
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }
