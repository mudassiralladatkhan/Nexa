"""
Voice processing routes - Speech recognition, TTS, and wake word detection
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncio
import json
import base64
from datetime import datetime

from ..config import get_settings
from shared.database.connection import get_db_session
from shared.database.repositories import RepositoryFactory
from .auth import get_current_user_id

router = APIRouter()


class VoiceRequest(BaseModel):
    audio_data: str  # Base64 encoded audio
    format: str = "wav"
    sample_rate: int = 16000
    language: str = "en-US"


class VoiceResponse(BaseModel):
    success: bool
    text: str
    confidence: float
    processing_time_ms: int


class TTSRequest(BaseModel):
    text: str
    voice: str = "default"
    speed: float = 1.0
    language: str = "en-US"


class TTSResponse(BaseModel):
    success: bool
    audio_data: str  # Base64 encoded audio
    format: str = "wav"


class WakeWordConfig(BaseModel):
    enabled: bool
    sensitivity: float = 0.5
    wake_words: List[str]


@router.post("/recognize", response_model=VoiceResponse)
async def speech_to_text(
    request: VoiceRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """
    Convert speech to text using speech recognition
    Mirrors VoiceBackgroundService.kt functionality
    """
    import speech_recognition as sr
    import io
    import wave
    import time
    
    start_time = time.time()
    
    try:
        repos = RepositoryFactory(db)
        
        # Start voice session
        voice_session = repos.voice.start_voice_session(user_id, "manual")
        
        # Decode audio data
        audio_bytes = base64.b64decode(request.audio_data)
        
        # Create recognizer
        recognizer = sr.Recognizer()
        
        # Convert audio bytes to AudioFile
        audio_file = sr.AudioFile(io.BytesIO(audio_bytes))
        
        with audio_file as source:
            audio = recognizer.record(source)
        
        # Perform recognition
        try:
            text = recognizer.recognize_google(audio, language=request.language)
            confidence = 0.9  # Google API doesn't return confidence, use default
            success = True
        except sr.UnknownValueError:
            text = ""
            confidence = 0.0
            success = False
        except sr.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Speech recognition error: {e}")
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # End voice session with results
        repos.voice.end_voice_session(
            voice_session.id,
            confidence_score=confidence,
            metadata={"recognized_text": text, "language": request.language}
        )
        
        return VoiceResponse(
            success=success,
            text=text,
            confidence=confidence,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice recognition failed: {str(e)}")


@router.post("/synthesize", response_model=TTSResponse)
async def text_to_speech(
    request: TTSRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Convert text to speech using TTS engine
    """
    import pyttsx3
    import tempfile
    import os
    
    try:
        # Initialize TTS engine
        engine = pyttsx3.init()
        
        # Set properties
        engine.setProperty('rate', int(200 * request.speed))
        
        # Get available voices and set language-appropriate voice
        voices = engine.getProperty('voices')
        if voices:
            # Try to find voice matching language
            for voice in voices:
                if request.language.lower() in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break
        
        # Create temporary file for audio output
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_path = temp_file.name
        
        # Save speech to file
        engine.save_to_file(request.text, temp_path)
        engine.runAndWait()
        
        # Read audio file and encode to base64
        with open(temp_path, 'rb') as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        return TTSResponse(
            success=True,
            audio_data=audio_data,
            format="wav"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")


@router.post("/upload")
async def upload_audio_file(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Upload and process audio file"""
    import speech_recognition as sr
    
    try:
        # Read uploaded file
        audio_data = await file.read()
        
        # Process with speech recognition
        recognizer = sr.Recognizer()
        
        # Save to temporary file for processing
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.wav') as temp_file:
            temp_file.write(audio_data)
            temp_file.flush()
            
            with sr.AudioFile(temp_file.name) as source:
                audio = recognizer.record(source)
            
            text = recognizer.recognize_google(audio)
        
        return {
            "success": True,
            "filename": file.filename,
            "text": text,
            "size": len(audio_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")


@router.websocket("/stream")
async def voice_stream(
    websocket: WebSocket,
    user_id: str = None  # In real implementation, get from token
):
    """
    WebSocket endpoint for real-time voice streaming
    Mirrors continuous listening functionality
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive audio data
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "audio":
                # Process audio chunk
                audio_data = message["data"]
                
                # Here you would process the audio in real-time
                # For now, send back a simple response
                response = {
                    "type": "recognition",
                    "text": "Processing audio...",
                    "confidence": 0.5,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                await websocket.send_text(json.dumps(response))
            
            elif message["type"] == "start_listening":
                # Start continuous listening
                response = {
                    "type": "status",
                    "message": "Started listening",
                    "timestamp": datetime.utcnow().isoformat()
                }
                await websocket.send_text(json.dumps(response))
            
            elif message["type"] == "stop_listening":
                # Stop listening
                response = {
                    "type": "status", 
                    "message": "Stopped listening",
                    "timestamp": datetime.utcnow().isoformat()
                }
                await websocket.send_text(json.dumps(response))
                
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for user: {user_id}")


@router.get("/wake-word/config")
async def get_wake_word_config(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get wake word configuration"""
    repos = RepositoryFactory(db)
    settings = get_settings()
    
    # Get user preferences
    enabled = repos.preferences.get_preference(user_id, "wake_word_enabled", True)
    sensitivity = repos.preferences.get_preference(user_id, "wake_word_sensitivity", 0.5)
    custom_words = repos.preferences.get_preference(user_id, "custom_wake_words", [])
    
    return WakeWordConfig(
        enabled=enabled,
        sensitivity=sensitivity,
        wake_words=settings.wake_words + custom_words
    )


@router.post("/wake-word/config")
async def set_wake_word_config(
    config: WakeWordConfig,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Update wake word configuration"""
    repos = RepositoryFactory(db)
    
    # Save preferences
    repos.preferences.set_preference(user_id, "wake_word_enabled", config.enabled)
    repos.preferences.set_preference(user_id, "wake_word_sensitivity", config.sensitivity)
    repos.preferences.set_preference(user_id, "custom_wake_words", config.wake_words, "json")
    
    return {"success": True, "message": "Wake word configuration updated"}


@router.get("/capabilities")
async def get_voice_capabilities():
    """Get available voice processing capabilities"""
    import speech_recognition as sr
    import pyttsx3
    
    # Check available recognizers
    recognizers = []
    if hasattr(sr, 'recognize_google'):
        recognizers.append("google")
    if hasattr(sr, 'recognize_sphinx'):
        recognizers.append("sphinx")
    
    # Check TTS voices
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        available_voices = [{"id": v.id, "name": v.name, "languages": getattr(v, 'languages', [])} for v in voices] if voices else []
    except:
        available_voices = []
    
    return {
        "speech_recognition": {
            "available": True,
            "engines": recognizers,
            "languages": ["en-US", "en-GB", "es-ES", "fr-FR", "de-DE"]
        },
        "text_to_speech": {
            "available": True,
            "voices": available_voices
        },
        "wake_word_detection": {
            "available": True,
            "engines": ["porcupine", "snowboy"]
        },
        "real_time_streaming": {
            "available": True,
            "websocket_endpoint": "/api/v1/voice/stream"
        }
    }
