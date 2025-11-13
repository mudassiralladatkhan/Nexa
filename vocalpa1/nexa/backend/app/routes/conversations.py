"""
Conversation management routes
Handles conversation history and message storage
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from shared.database.connection import get_db_session
from shared.database.repositories import RepositoryFactory
from .auth import get_current_user_id

router = APIRouter()


class MessageRequest(BaseModel):
    session_id: str
    message_type: str  # 'user', 'assistant', 'system'
    content: str
    confidence_score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class MessageResponse(BaseModel):
    id: int
    message_type: str
    content: str
    timestamp: datetime
    confidence_score: Optional[float]


class ConversationSummary(BaseModel):
    id: int
    session_id: str
    title: str
    started_at: datetime
    ended_at: Optional[datetime]
    is_active: bool
    message_count: int


@router.post("/messages")
async def add_message(
    request: MessageRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Add message to conversation"""
    try:
        repos = RepositoryFactory(db)
        
        message = repos.conversations.add_message(
            user_id=user_id,
            session_id=request.session_id,
            message_type=request.message_type,
            content=request.content,
            confidence_score=request.confidence_score,
            metadata=request.metadata
        )
        
        return MessageResponse(
            id=message.id,
            message_type=message.message_type,
            content=message.content,
            timestamp=message.timestamp,
            confidence_score=message.confidence_score
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add message: {str(e)}")


@router.get("/", response_model=List[ConversationSummary])
async def get_conversations(
    limit: int = 50,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get user's conversation history"""
    repos = RepositoryFactory(db)
    conversations = repos.conversations.get_conversation_history(user_id, limit)
    
    return [
        ConversationSummary(
            id=conv["id"],
            session_id=conv["session_id"],
            title=conv["title"],
            started_at=conv["started_at"],
            ended_at=conv["ended_at"],
            is_active=conv["is_active"],
            message_count=conv["message_count"]
        )
        for conv in conversations
    ]


@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    session_id: str,
    limit: int = 100,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get messages for a specific conversation"""
    repos = RepositoryFactory(db)
    messages = repos.conversations.get_messages(user_id, session_id, limit)
    
    return [
        MessageResponse(
            id=msg.id,
            message_type=msg.message_type,
            content=msg.content,
            timestamp=msg.timestamp,
            confidence_score=msg.confidence_score
        )
        for msg in messages
    ]


@router.post("/{session_id}/end")
async def end_conversation(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """End/close a conversation"""
    try:
        repos = RepositoryFactory(db)
        conversation = repos.conversations.get_conversation(user_id, session_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conversation.is_active = False
        conversation.ended_at = datetime.utcnow()
        db.commit()
        
        return {"success": True, "message": "Conversation ended"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to end conversation: {str(e)}")


@router.delete("/{session_id}")
async def delete_conversation(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Delete a conversation and all its messages"""
    try:
        repos = RepositoryFactory(db)
        conversation = repos.conversations.get_conversation(user_id, session_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Delete conversation (cascade will delete messages)
        db.delete(conversation)
        db.commit()
        
        return {"success": True, "message": "Conversation deleted"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete conversation: {str(e)}")
