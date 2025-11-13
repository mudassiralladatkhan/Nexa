"""
Nexa Database Models - SQLAlchemy ORM models based on VocalPA data structures
Combines Android SharedPreferences and Web localStorage patterns into unified schema
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """User account and login information - mirrors LoginPreferences.kt"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), unique=True, nullable=False, index=True)
    is_logged_in = Column(Boolean, default=False, nullable=False)
    login_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    preferences = relationship("UserPreference", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    commands = relationship("CommandHistory", back_populates="user", cascade="all, delete-orphan")


class UserPreference(Base):
    """User settings and preferences - mirrors Android SharedPreferences + Web localStorage"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(Text, nullable=True)  # JSON string for complex values
    value_type = Column(String(50), nullable=False)  # 'string', 'boolean', 'number', 'json'
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="preferences")
    
    __table_args__ = (
        # Unique constraint on user_id + key
        {"sqlite_autoincrement": True}
    )


class Conversation(Base):
    """Conversation history - mirrors web app conversation storage"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String(255), nullable=False, index=True)
    title = Column(String(500), nullable=True)
    started_at = Column(DateTime, default=func.now(), nullable=False)
    ended_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    metadata = Column(JSON, nullable=True)  # Additional conversation context
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")


class ConversationMessage(Base):
    """Individual messages within conversations"""
    __tablename__ = "conversation_messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    message_type = Column(String(50), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    confidence_score = Column(Float, nullable=True)  # For speech recognition confidence
    metadata = Column(JSON, nullable=True)  # Additional message context
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class CommandHistory(Base):
    """Command execution history - mirrors CommandProcessor.kt logic"""
    __tablename__ = "command_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    command_text = Column(Text, nullable=False)
    command_type = Column(String(100), nullable=False)  # 'time', 'weather', 'music', etc.
    response_text = Column(Text, nullable=True)
    execution_status = Column(String(50), nullable=False)  # 'success', 'error', 'partial'
    execution_time_ms = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    metadata = Column(JSON, nullable=True)  # Command-specific data
    
    # Relationships
    user = relationship("User", back_populates="commands")


class VoiceSession(Base):
    """Voice interaction sessions - tracks wake word activations and speech sessions"""
    __tablename__ = "voice_sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_type = Column(String(50), nullable=False)  # 'wake_word', 'manual', 'continuous'
    started_at = Column(DateTime, default=func.now(), nullable=False)
    ended_at = Column(DateTime, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    wake_word_detected = Column(String(100), nullable=True)
    recognition_confidence = Column(Float, nullable=True)
    audio_quality_score = Column(Float, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User")


class AppUsage(Base):
    """App launch and usage tracking - mirrors AppLauncher.kt functionality"""
    __tablename__ = "app_usage"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    app_name = Column(String(255), nullable=False)
    package_name = Column(String(255), nullable=True)  # Android package name
    launch_method = Column(String(50), nullable=False)  # 'voice', 'manual', 'shortcut'
    launched_at = Column(DateTime, default=func.now(), nullable=False)
    success = Column(Boolean, nullable=False)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User")


class APIUsage(Base):
    """API call tracking and caching - for weather, news, music services"""
    __tablename__ = "api_usage"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    api_service = Column(String(100), nullable=False)  # 'weather', 'news', 'spotify', etc.
    endpoint = Column(String(500), nullable=False)
    request_data = Column(JSON, nullable=True)
    response_data = Column(JSON, nullable=True)
    response_status = Column(Integer, nullable=False)
    response_time_ms = Column(Integer, nullable=True)
    cached = Column(Boolean, default=False, nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User")


class SystemEvent(Base):
    """System events and background service activity"""
    __tablename__ = "system_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(100), nullable=False)  # 'service_start', 'service_stop', 'error', etc.
    event_source = Column(String(100), nullable=False)  # 'background_service', 'main_app', 'web_app'
    description = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False)  # 'info', 'warning', 'error', 'critical'
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    metadata = Column(JSON, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user = relationship("User")


class DeviceInfo(Base):
    """Device and platform information"""
    __tablename__ = "device_info"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_type = Column(String(50), nullable=False)  # 'android', 'web', 'desktop'
    device_id = Column(String(255), nullable=True)
    platform = Column(String(100), nullable=True)
    os_version = Column(String(100), nullable=True)
    app_version = Column(String(50), nullable=True)
    capabilities = Column(JSON, nullable=True)  # Supported features
    last_seen = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User")


# Indexes for performance
from sqlalchemy import Index

# Create indexes for frequently queried columns
Index('idx_user_preferences_user_key', UserPreference.user_id, UserPreference.key)
Index('idx_conversations_user_session', Conversation.user_id, Conversation.session_id)
Index('idx_messages_conversation_timestamp', ConversationMessage.conversation_id, ConversationMessage.timestamp)
Index('idx_commands_user_timestamp', CommandHistory.user_id, CommandHistory.timestamp)
Index('idx_voice_sessions_user_timestamp', VoiceSession.user_id, VoiceSession.started_at)
Index('idx_api_usage_service_timestamp', APIUsage.api_service, APIUsage.timestamp)
Index('idx_system_events_type_timestamp', SystemEvent.event_type, SystemEvent.timestamp)
