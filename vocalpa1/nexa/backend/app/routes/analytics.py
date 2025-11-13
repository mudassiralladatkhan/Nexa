"""
Analytics and usage statistics routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

from shared.database.connection import get_db_session
from shared.database.repositories import RepositoryFactory
from .auth import get_current_user_id

router = APIRouter()


class UsageStats(BaseModel):
    total_commands: int
    success_rate: float
    commands_by_type: Dict[str, int]
    period_days: int


class ActivitySummary(BaseModel):
    date: str
    commands: int
    conversations: int
    voice_sessions: int


@router.get("/usage", response_model=UsageStats)
async def get_usage_analytics(
    days: int = 30,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get command usage analytics"""
    repos = RepositoryFactory(db)
    analytics = repos.commands.get_command_analytics(user_id, days)
    
    return UsageStats(
        total_commands=analytics["total_commands"],
        success_rate=analytics["success_rate"],
        commands_by_type=analytics["commands_by_type"],
        period_days=analytics["period_days"]
    )


@router.get("/activity")
async def get_activity_summary(
    days: int = 7,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get daily activity summary"""
    from shared.database.models import CommandHistory, Conversation, VoiceSession
    from sqlalchemy import func, and_
    
    try:
        repos = RepositoryFactory(db)
        user = repos.users.get_or_create_user(user_id)
        
        # Get date range
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days-1)
        
        # Query daily activity
        daily_stats = []
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            next_date = current_date + timedelta(days=1)
            
            # Count commands for this day
            commands_count = db.query(CommandHistory).filter(
                and_(
                    CommandHistory.user_id == user.id,
                    CommandHistory.timestamp >= current_date,
                    CommandHistory.timestamp < next_date
                )
            ).count()
            
            # Count conversations for this day
            conversations_count = db.query(Conversation).filter(
                and_(
                    Conversation.user_id == user.id,
                    Conversation.started_at >= current_date,
                    Conversation.started_at < next_date
                )
            ).count()
            
            # Count voice sessions for this day
            voice_sessions_count = db.query(VoiceSession).filter(
                and_(
                    VoiceSession.user_id == user.id,
                    VoiceSession.started_at >= current_date,
                    VoiceSession.started_at < next_date
                )
            ).count()
            
            daily_stats.append(ActivitySummary(
                date=current_date.isoformat(),
                commands=commands_count,
                conversations=conversations_count,
                voice_sessions=voice_sessions_count
            ))
        
        return {
            "daily_activity": daily_stats,
            "period_days": days,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")


@router.get("/performance")
async def get_performance_metrics(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get performance metrics"""
    from shared.database.models import CommandHistory
    from sqlalchemy import func
    
    try:
        repos = RepositoryFactory(db)
        user = repos.users.get_or_create_user(user_id)
        
        # Average execution time
        avg_execution_time = db.query(
            func.avg(CommandHistory.execution_time_ms)
        ).filter(
            and_(
                CommandHistory.user_id == user.id,
                CommandHistory.execution_time_ms.isnot(None)
            )
        ).scalar() or 0
        
        # Command success rate
        total_commands = db.query(CommandHistory).filter(
            CommandHistory.user_id == user.id
        ).count()
        
        successful_commands = db.query(CommandHistory).filter(
            and_(
                CommandHistory.user_id == user.id,
                CommandHistory.execution_status == "success"
            )
        ).count()
        
        success_rate = (successful_commands / total_commands * 100) if total_commands > 0 else 0
        
        # Most used command types
        command_types = db.query(
            CommandHistory.command_type,
            func.count(CommandHistory.id).label('count')
        ).filter(
            CommandHistory.user_id == user.id
        ).group_by(CommandHistory.command_type).order_by(
            func.count(CommandHistory.id).desc()
        ).limit(5).all()
        
        return {
            "average_execution_time_ms": round(avg_execution_time, 2),
            "success_rate": round(success_rate, 2),
            "total_commands": total_commands,
            "successful_commands": successful_commands,
            "top_command_types": [
                {"type": cmd_type, "count": count} 
                for cmd_type, count in command_types
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance metrics error: {str(e)}")


@router.get("/trends")
async def get_usage_trends(
    days: int = 30,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get usage trends over time"""
    from shared.database.models import CommandHistory
    from sqlalchemy import func, and_
    
    try:
        repos = RepositoryFactory(db)
        user = repos.users.get_or_create_user(user_id)
        
        # Weekly usage trends
        weeks_data = []
        for week in range(4):  # Last 4 weeks
            week_start = datetime.utcnow() - timedelta(weeks=week+1)
            week_end = datetime.utcnow() - timedelta(weeks=week)
            
            week_commands = db.query(CommandHistory).filter(
                and_(
                    CommandHistory.user_id == user.id,
                    CommandHistory.timestamp >= week_start,
                    CommandHistory.timestamp < week_end
                )
            ).count()
            
            weeks_data.append({
                "week": f"Week {4-week}",
                "commands": week_commands,
                "start_date": week_start.date().isoformat(),
                "end_date": week_end.date().isoformat()
            })
        
        # Hourly usage pattern (last 7 days)
        hourly_data = []
        for hour in range(24):
            hour_commands = db.query(CommandHistory).filter(
                and_(
                    CommandHistory.user_id == user.id,
                    CommandHistory.timestamp >= datetime.utcnow() - timedelta(days=7),
                    func.extract('hour', CommandHistory.timestamp) == hour
                )
            ).count()
            
            hourly_data.append({
                "hour": hour,
                "commands": hour_commands
            })
        
        return {
            "weekly_trends": weeks_data,
            "hourly_patterns": hourly_data,
            "analysis_period_days": days
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trends analysis error: {str(e)}")


@router.get("/summary")
async def get_analytics_summary(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get comprehensive analytics summary"""
    try:
        repos = RepositoryFactory(db)
        
        # Get user stats
        user_stats = repos.users.get_user_stats(user_id)
        
        # Get recent performance
        performance = await get_performance_metrics(user_id, db)
        
        # Get recent activity (last 7 days)
        activity = await get_activity_summary(7, user_id, db)
        
        return {
            "user_stats": user_stats,
            "performance": performance,
            "recent_activity": activity,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary generation error: {str(e)}")
