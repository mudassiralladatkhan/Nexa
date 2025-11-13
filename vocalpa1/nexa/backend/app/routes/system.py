"""
System management and monitoring routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import psutil
import platform

from shared.database.connection import get_db_session
from shared.database.repositories import RepositoryFactory
from .auth import get_current_user_id

router = APIRouter()


class SystemEvent(BaseModel):
    id: int
    event_type: str
    event_source: str
    description: str
    severity: str
    timestamp: datetime


class SystemInfo(BaseModel):
    platform: str
    cpu_count: int
    memory_total: int
    disk_total: int
    uptime: float


@router.get("/events", response_model=List[SystemEvent])
async def get_system_events(
    limit: int = 100,
    severity: Optional[str] = None,
    db: Session = Depends(get_db_session)
):
    """Get recent system events"""
    repos = RepositoryFactory(db)
    events = repos.system.get_recent_events(limit, severity)
    
    return [
        SystemEvent(
            id=event.id,
            event_type=event.event_type,
            event_source=event.event_source,
            description=event.description,
            severity=event.severity,
            timestamp=event.timestamp
        )
        for event in events
    ]


@router.post("/events")
async def log_system_event(
    event_type: str,
    event_source: str,
    description: str,
    severity: str = "info",
    user_id: Optional[str] = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Log a system event"""
    try:
        repos = RepositoryFactory(db)
        repos.system.log_event(
            event_type=event_type,
            event_source=event_source,
            description=description,
            severity=severity,
            user_id=user_id
        )
        
        return {
            "success": True,
            "message": "Event logged successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log event: {str(e)}")


@router.get("/info", response_model=SystemInfo)
async def get_system_info():
    """Get system information"""
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return SystemInfo(
            platform=f"{platform.system()} {platform.release()}",
            cpu_count=psutil.cpu_count(),
            memory_total=memory.total,
            disk_total=disk.total,
            uptime=psutil.boot_time()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system info: {str(e)}")


@router.get("/performance")
async def get_system_performance():
    """Get current system performance metrics"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu": {
                "usage_percent": cpu_percent,
                "count": psutil.cpu_count(),
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": (disk.used / disk.total) * 100
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance metrics: {str(e)}")


@router.get("/processes")
async def get_running_processes():
    """Get information about running processes"""
    try:
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                proc_info = proc.info
                if proc_info['cpu_percent'] > 0 or proc_info['memory_percent'] > 1:
                    processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        return {
            "processes": processes[:20],  # Top 20 processes
            "total_count": len(processes)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get process info: {str(e)}")


@router.post("/cleanup")
async def cleanup_system_data(
    days_old: int = 30,
    db: Session = Depends(get_db_session)
):
    """Cleanup old system data"""
    from shared.database.models import SystemEvent, CommandHistory, VoiceSession
    from sqlalchemy import and_
    
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        # Clean old system events
        old_events = db.query(SystemEvent).filter(
            SystemEvent.timestamp < cutoff_date
        ).delete()
        
        # Clean old command history (keep successful commands longer)
        old_failed_commands = db.query(CommandHistory).filter(
            and_(
                CommandHistory.timestamp < cutoff_date,
                CommandHistory.execution_status != "success"
            )
        ).delete()
        
        # Clean old voice sessions
        old_voice_sessions = db.query(VoiceSession).filter(
            VoiceSession.started_at < cutoff_date
        ).delete()
        
        db.commit()
        
        return {
            "success": True,
            "cleaned": {
                "system_events": old_events,
                "failed_commands": old_failed_commands,
                "voice_sessions": old_voice_sessions
            },
            "cutoff_date": cutoff_date.isoformat()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")


@router.get("/database/stats")
async def get_database_stats(db: Session = Depends(get_db_session)):
    """Get database statistics"""
    from shared.database.models import (
        User, UserPreference, Conversation, ConversationMessage,
        CommandHistory, VoiceSession, SystemEvent
    )
    
    try:
        stats = {
            "users": db.query(User).count(),
            "preferences": db.query(UserPreference).count(),
            "conversations": db.query(Conversation).count(),
            "messages": db.query(ConversationMessage).count(),
            "commands": db.query(CommandHistory).count(),
            "voice_sessions": db.query(VoiceSession).count(),
            "system_events": db.query(SystemEvent).count()
        }
        
        return {
            "table_counts": stats,
            "total_records": sum(stats.values()),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get database stats: {str(e)}")


@router.post("/backup")
async def backup_database():
    """Create database backup"""
    try:
        # This is a placeholder - implement actual backup logic
        backup_filename = f"nexa_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.db"
        
        return {
            "success": True,
            "backup_file": backup_filename,
            "message": "Database backup created (placeholder implementation)"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {str(e)}")


@router.get("/logs")
async def get_system_logs(
    lines: int = 100,
    level: Optional[str] = None
):
    """Get system logs"""
    try:
        # This is a placeholder - implement actual log reading
        logs = [
            {
                "timestamp": datetime.utcnow().isoformat(),
                "level": "INFO",
                "message": "System running normally",
                "source": "system_monitor"
            }
        ]
        
        return {
            "logs": logs,
            "total_lines": len(logs),
            "filter_level": level
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")
