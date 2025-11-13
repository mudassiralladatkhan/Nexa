"""
Command processing routes - Core VocalPA command functionality ported to Python
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import asyncio
import time

from ..config import get_settings
from shared.database.connection import get_db_session
from shared.database.repositories import RepositoryFactory
from shared.command_processor import CommandProcessor, CommandResult
from .auth import get_current_user_id

router = APIRouter()


class CommandRequest(BaseModel):
    text: str
    locale: Optional[str] = "en-US"
    metadata: Optional[Dict[str, Any]] = None


class CommandResponse(BaseModel):
    success: bool
    command_type: str
    response_text: str
    execution_time_ms: int
    metadata: Optional[Dict[str, Any]] = None


class CommandHistoryItem(BaseModel):
    id: int
    command_text: str
    command_type: str
    response_text: Optional[str]
    execution_status: str
    execution_time_ms: Optional[int]
    timestamp: datetime


@router.post("/process", response_model=CommandResponse)
async def process_command(
    request: CommandRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """
    Process voice/text command - mirrors VocalPA CommandProcessor.kt
    """
    start_time = time.time()
    
    try:
        repos = RepositoryFactory(db)
        processor = CommandProcessor()
        
        # Process the command
        result: CommandResult = await processor.process(
            request.text,
            locale=request.locale,
            metadata=request.metadata
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        # Record command in history
        repos.commands.record_command(
            user_id=user_id,
            command_text=request.text,
            command_type=result.command_type,
            response_text=result.response_text,
            execution_status="success" if result.success else "error",
            execution_time_ms=execution_time,
            metadata=result.metadata
        )
        
        return CommandResponse(
            success=result.success,
            command_type=result.command_type,
            response_text=result.response_text,
            execution_time_ms=execution_time,
            metadata=result.metadata
        )
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        
        # Record failed command
        repos = RepositoryFactory(db)
        repos.commands.record_command(
            user_id=user_id,
            command_text=request.text,
            command_type="error",
            response_text=f"Command failed: {str(e)}",
            execution_status="error",
            execution_time_ms=execution_time
        )
        
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=List[CommandHistoryItem])
async def get_command_history(
    limit: int = 50,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get user's command history"""
    repos = RepositoryFactory(db)
    history = repos.commands.get_command_history(user_id, limit)
    
    return [
        CommandHistoryItem(
            id=cmd.id,
            command_text=cmd.command_text,
            command_type=cmd.command_type,
            response_text=cmd.response_text,
            execution_status=cmd.execution_status,
            execution_time_ms=cmd.execution_time_ms,
            timestamp=cmd.timestamp
        )
        for cmd in history
    ]


@router.get("/analytics")
async def get_command_analytics(
    days: int = 30,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get command usage analytics"""
    repos = RepositoryFactory(db)
    analytics = repos.commands.get_command_analytics(user_id, days)
    return analytics


@router.get("/types")
async def get_supported_commands():
    """Get list of supported command types"""
    processor = CommandProcessor()
    return {
        "supported_commands": list(processor._handlers.keys()),
        "examples": {
            "time": ["what time is it", "current time"],
            "weather": ["weather today", "temperature outside"],
            "music": ["play music", "next song"],
            "apps": ["open calculator", "launch chrome"],
            "system": ["battery level", "wifi status"],
            "general": ["hello", "how are you"]
        }
    }


@router.post("/batch")
async def process_batch_commands(
    commands: List[CommandRequest],
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Process multiple commands in batch"""
    results = []
    
    for cmd_request in commands:
        try:
            # Process each command
            start_time = time.time()
            processor = CommandProcessor()
            result = await processor.process(
                cmd_request.text,
                locale=cmd_request.locale,
                metadata=cmd_request.metadata
            )
            execution_time = int((time.time() - start_time) * 1000)
            
            # Record in database
            repos = RepositoryFactory(db)
            repos.commands.record_command(
                user_id=user_id,
                command_text=cmd_request.text,
                command_type=result.command_type,
                response_text=result.response_text,
                execution_status="success" if result.success else "error",
                execution_time_ms=execution_time,
                metadata=result.metadata
            )
            
            results.append({
                "command": cmd_request.text,
                "success": result.success,
                "response": result.response_text,
                "type": result.command_type,
                "execution_time_ms": execution_time
            })
            
        except Exception as e:
            results.append({
                "command": cmd_request.text,
                "success": False,
                "response": f"Error: {str(e)}",
                "type": "error",
                "execution_time_ms": 0
            })
    
    return {"results": results, "total": len(commands)}
