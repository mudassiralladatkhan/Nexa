"""
Data repository classes for clean data access patterns
Provides high-level interfaces for database operations
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, and_, or_, func

from .models import (
    User, UserPreference, Conversation, ConversationMessage,
    CommandHistory, VoiceSession, AppUsage, APIUsage, SystemEvent, DeviceInfo
)
from .connection import ensure_user_exists


class UserRepository:
    """Repository for user-related operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_or_create_user(self, user_id: str) -> User:
        """Get existing user or create new one"""
        user = self.session.query(User).filter(User.user_id == user_id).first()
        if not user:
            user = User(user_id=user_id, is_logged_in=True, login_time=datetime.utcnow())
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
        return user
    
    def update_login_status(self, user_id: str, is_logged_in: bool) -> User:
        """Update user login status"""
        user = self.get_or_create_user(user_id)
        user.is_logged_in = is_logged_in
        if is_logged_in:
            user.login_time = datetime.utcnow()
        self.session.commit()
        return user
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        user = self.get_or_create_user(user_id)
        
        # Count various activities
        total_conversations = self.session.query(Conversation).filter(
            Conversation.user_id == user.id
        ).count()
        
        total_commands = self.session.query(CommandHistory).filter(
            CommandHistory.user_id == user.id
        ).count()
        
        total_voice_sessions = self.session.query(VoiceSession).filter(
            VoiceSession.user_id == user.id
        ).count()
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_commands = self.session.query(CommandHistory).filter(
            and_(CommandHistory.user_id == user.id, CommandHistory.timestamp >= week_ago)
        ).count()
        
        return {
            "user_id": user.user_id,
            "is_logged_in": user.is_logged_in,
            "login_time": user.login_time,
            "created_at": user.created_at,
            "total_conversations": total_conversations,
            "total_commands": total_commands,
            "total_voice_sessions": total_voice_sessions,
            "recent_commands_7d": recent_commands
        }


class PreferenceRepository:
    """Repository for user preferences (mirrors SharedPreferences/localStorage)"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_preference(self, user_id: str, key: str, default=None):
        """Get user preference value with type conversion"""
        user_pk = ensure_user_exists(self.session, user_id)
        
        pref = self.session.query(UserPreference).filter(
            and_(UserPreference.user_id == user_pk, UserPreference.key == key)
        ).first()
        
        if not pref:
            return default
        
        # Convert based on stored type
        if pref.value_type == "boolean":
            return pref.value.lower() == "true"
        elif pref.value_type == "number":
            return float(pref.value) if "." in pref.value else int(pref.value)
        elif pref.value_type == "json":
            import json
            return json.loads(pref.value)
        else:
            return pref.value
    
    def set_preference(self, user_id: str, key: str, value, value_type: str = None):
        """Set user preference with automatic type detection"""
        import json
        
        user_pk = ensure_user_exists(self.session, user_id)
        
        # Auto-detect type if not specified
        if value_type is None:
            if isinstance(value, bool):
                value_type = "boolean"
            elif isinstance(value, (int, float)):
                value_type = "number"
            elif isinstance(value, (dict, list)):
                value_type = "json"
            else:
                value_type = "string"
        
        # Convert to string
        if value_type == "json":
            value_str = json.dumps(value)
        else:
            value_str = str(value)
        
        # Update or create
        pref = self.session.query(UserPreference).filter(
            and_(UserPreference.user_id == user_pk, UserPreference.key == key)
        ).first()
        
        if pref:
            pref.value = value_str
            pref.value_type = value_type
        else:
            pref = UserPreference(
                user_id=user_pk,
                key=key,
                value=value_str,
                value_type=value_type
            )
            self.session.add(pref)
        
        self.session.commit()
    
    def get_all_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get all preferences for a user"""
        user_pk = ensure_user_exists(self.session, user_id)
        
        prefs = self.session.query(UserPreference).filter(
            UserPreference.user_id == user_pk
        ).all()
        
        result = {}
        for pref in prefs:
            result[pref.key] = self.get_preference(user_id, pref.key)
        
        return result
    
    def delete_preference(self, user_id: str, key: str):
        """Delete a user preference"""
        user_pk = ensure_user_exists(self.session, user_id)
        
        self.session.query(UserPreference).filter(
            and_(UserPreference.user_id == user_pk, UserPreference.key == key)
        ).delete()
        self.session.commit()


class ConversationRepository:
    """Repository for conversation and message management"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_conversation(self, user_id: str, session_id: str, title: str = None) -> Conversation:
        """Create new conversation"""
        user_pk = ensure_user_exists(self.session, user_id)
        
        conversation = Conversation(
            user_id=user_pk,
            session_id=session_id,
            title=title or f"Conversation {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation
    
    def get_conversation(self, user_id: str, session_id: str) -> Optional[Conversation]:
        """Get conversation by session ID"""
        user_pk = ensure_user_exists(self.session, user_id)
        
        return self.session.query(Conversation).filter(
            and_(
                Conversation.user_id == user_pk,
                Conversation.session_id == session_id
            )
        ).first()
    
    def get_or_create_conversation(self, user_id: str, session_id: str) -> Conversation:
        """Get existing conversation or create new one"""
        conv = self.get_conversation(user_id, session_id)
        if not conv:
            conv = self.create_conversation(user_id, session_id)
        return conv
    
    def add_message(self, user_id: str, session_id: str, message_type: str, 
                   content: str, confidence_score: float = None, 
                   metadata: Dict = None) -> ConversationMessage:
        """Add message to conversation"""
        conversation = self.get_or_create_conversation(user_id, session_id)
        
        message = ConversationMessage(
            conversation_id=conversation.id,
            message_type=message_type,
            content=content,
            confidence_score=confidence_score,
            metadata=metadata
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message
    
    def get_conversation_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get recent conversations with message counts"""
        user_pk = ensure_user_exists(self.session, user_id)
        
        conversations = self.session.query(
            Conversation,
            func.count(ConversationMessage.id).label('message_count')
        ).outerjoin(ConversationMessage).filter(
            Conversation.user_id == user_pk
        ).group_by(Conversation.id).order_by(
            desc(Conversation.started_at)
        ).limit(limit).all()
        
        return [
            {
                "id": conv.id,
                "session_id": conv.session_id,
                "title": conv.title,
                "started_at": conv.started_at,
                "ended_at": conv.ended_at,
                "is_active": conv.is_active,
                "message_count": count
            }
            for conv, count in conversations
        ]
    
    def get_messages(self, user_id: str, session_id: str, limit: int = 100) -> List[ConversationMessage]:
        """Get messages for a conversation"""
        conversation = self.get_conversation(user_id, session_id)
        if not conversation:
            return []
        
        return self.session.query(ConversationMessage).filter(
            ConversationMessage.conversation_id == conversation.id
        ).order_by(asc(ConversationMessage.timestamp)).limit(limit).all()


class CommandRepository:
    """Repository for command history and analytics"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def record_command(self, user_id: str, command_text: str, command_type: str,
                      response_text: str = None, execution_status: str = "success",
                      execution_time_ms: int = None, metadata: Dict = None) -> CommandHistory:
        """Record command execution"""
        user_pk = ensure_user_exists(self.session, user_id)
        
        command = CommandHistory(
            user_id=user_pk,
            command_text=command_text,
            command_type=command_type,
            response_text=response_text,
            execution_status=execution_status,
            execution_time_ms=execution_time_ms,
            metadata=metadata
        )
        self.session.add(command)
        self.session.commit()
        self.session.refresh(command)
        return command
    
    def get_command_history(self, user_id: str, limit: int = 50) -> List[CommandHistory]:
        """Get recent command history"""
        user_pk = ensure_user_exists(self.session, user_id)
        
        return self.session.query(CommandHistory).filter(
            CommandHistory.user_id == user_pk
        ).order_by(desc(CommandHistory.timestamp)).limit(limit).all()
    
    def get_command_analytics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get command usage analytics"""
        user_pk = ensure_user_exists(self.session, user_id)
        since = datetime.utcnow() - timedelta(days=days)
        
        # Total commands
        total = self.session.query(CommandHistory).filter(
            and_(CommandHistory.user_id == user_pk, CommandHistory.timestamp >= since)
        ).count()
        
        # Commands by type
        by_type = self.session.query(
            CommandHistory.command_type,
            func.count(CommandHistory.id).label('count')
        ).filter(
            and_(CommandHistory.user_id == user_pk, CommandHistory.timestamp >= since)
        ).group_by(CommandHistory.command_type).all()
        
        # Success rate
        success_count = self.session.query(CommandHistory).filter(
            and_(
                CommandHistory.user_id == user_pk,
                CommandHistory.timestamp >= since,
                CommandHistory.execution_status == "success"
            )
        ).count()
        
        return {
            "total_commands": total,
            "success_rate": (success_count / total * 100) if total > 0 else 0,
            "commands_by_type": {cmd_type: count for cmd_type, count in by_type},
            "period_days": days
        }


class VoiceRepository:
    """Repository for voice session tracking"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def start_voice_session(self, user_id: str, session_type: str = "manual",
                           wake_word: str = None) -> VoiceSession:
        """Start new voice session"""
        user_pk = ensure_user_exists(self.session, user_id)
        
        session_obj = VoiceSession(
            user_id=user_pk,
            session_type=session_type,
            wake_word_detected=wake_word
        )
        self.session.add(session_obj)
        self.session.commit()
        self.session.refresh(session_obj)
        return session_obj
    
    def end_voice_session(self, session_id: int, confidence_score: float = None,
                         audio_quality: float = None, metadata: Dict = None):
        """End voice session with results"""
        session_obj = self.session.query(VoiceSession).filter(
            VoiceSession.id == session_id
        ).first()
        
        if session_obj:
            session_obj.ended_at = datetime.utcnow()
            if session_obj.started_at:
                duration = session_obj.ended_at - session_obj.started_at
                session_obj.duration_ms = int(duration.total_seconds() * 1000)
            session_obj.recognition_confidence = confidence_score
            session_obj.audio_quality_score = audio_quality
            session_obj.metadata = metadata
            self.session.commit()


class SystemRepository:
    """Repository for system events and monitoring"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def log_event(self, event_type: str, event_source: str, description: str,
                  severity: str = "info", user_id: str = None, metadata: Dict = None):
        """Log system event"""
        user_pk = None
        if user_id:
            user_pk = ensure_user_exists(self.session, user_id)
        
        event = SystemEvent(
            event_type=event_type,
            event_source=event_source,
            description=description,
            severity=severity,
            user_id=user_pk,
            metadata=metadata
        )
        self.session.add(event)
        self.session.commit()
    
    def get_recent_events(self, limit: int = 100, severity: str = None) -> List[SystemEvent]:
        """Get recent system events"""
        query = self.session.query(SystemEvent)
        
        if severity:
            query = query.filter(SystemEvent.severity == severity)
        
        return query.order_by(desc(SystemEvent.timestamp)).limit(limit).all()


# Repository factory for dependency injection
class RepositoryFactory:
    """Factory for creating repository instances"""
    
    def __init__(self, session: Session):
        self.session = session
    
    @property
    def users(self) -> UserRepository:
        return UserRepository(self.session)
    
    @property
    def preferences(self) -> PreferenceRepository:
        return PreferenceRepository(self.session)
    
    @property
    def conversations(self) -> ConversationRepository:
        return ConversationRepository(self.session)
    
    @property
    def commands(self) -> CommandRepository:
        return CommandRepository(self.session)
    
    @property
    def voice(self) -> VoiceRepository:
        return VoiceRepository(self.session)
    
    @property
    def system(self) -> SystemRepository:
        return SystemRepository(self.session)
