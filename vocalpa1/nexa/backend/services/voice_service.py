"""
Voice processing service - Background voice recognition and TTS
Mirrors VoiceBackgroundService.kt functionality
"""

import asyncio
import threading
import queue
import logging
from typing import Optional, Callable, Dict, Any
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import pyaudio
import wave

logger = logging.getLogger(__name__)


class VoiceService:
    """Background voice processing service"""
    
    def __init__(self, wake_words: list = None, sensitivity: float = 0.5):
        self.wake_words = wake_words or ["nexa", "hey nexa"]
        self.sensitivity = sensitivity
        self.is_listening = False
        self.is_processing = False
        
        # Audio components
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.tts_engine = None
        
        # Threading
        self.listen_thread = None
        self.audio_queue = queue.Queue()
        
        # Callbacks
        self.on_wake_word: Optional[Callable] = None
        self.on_speech_recognized: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize audio components"""
        try:
            # Initialize microphone
            self.microphone = sr.Microphone()
            
            # Calibrate for ambient noise
            with self.microphone as source:
                logger.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Initialize TTS engine
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
            
            self.tts_engine.setProperty('rate', 200)
            self.tts_engine.setProperty('volume', 0.8)
            
            logger.info("Voice service components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize voice components: {e}")
            raise
    
    def start_listening(self):
        """Start background listening for wake words"""
        if self.is_listening:
            logger.warning("Voice service is already listening")
            return
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        
        logger.info("Started background voice listening")
    
    def stop_listening(self):
        """Stop background listening"""
        self.is_listening = False
        
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2)
        
        logger.info("Stopped background voice listening")
    
    def _listen_loop(self):
        """Main listening loop - runs in background thread"""
        logger.info("Voice listening loop started")
        
        while self.is_listening:
            try:
                # Listen for audio
                with self.microphone as source:
                    # Adjust for noise periodically
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Process audio in separate thread to avoid blocking
                threading.Thread(
                    target=self._process_audio,
                    args=(audio,),
                    daemon=True
                ).start()
                
            except sr.WaitTimeoutError:
                # Normal timeout, continue listening
                continue
            except Exception as e:
                logger.error(f"Error in listening loop: {e}")
                if self.on_error:
                    self.on_error(f"Listening error: {e}")
                
                # Brief pause before retrying
                threading.Event().wait(1)
    
    def _process_audio(self, audio):
        """Process captured audio for wake words and speech"""
        if self.is_processing:
            return  # Skip if already processing
        
        self.is_processing = True
        
        try:
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language="en-US")
            text_lower = text.lower()
            
            logger.debug(f"Recognized speech: {text}")
            
            # Check for wake words
            wake_word_detected = None
            for wake_word in self.wake_words:
                if wake_word.lower() in text_lower:
                    wake_word_detected = wake_word
                    break
            
            if wake_word_detected:
                logger.info(f"Wake word detected: {wake_word_detected}")
                if self.on_wake_word:
                    self.on_wake_word(wake_word_detected, text)
            
            # Always call speech recognition callback
            if self.on_speech_recognized:
                self.on_speech_recognized(text, wake_word_detected is not None)
                
        except sr.UnknownValueError:
            # Speech not understood - this is normal, don't log as error
            pass
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            if self.on_error:
                self.on_error(f"Recognition service error: {e}")
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            if self.on_error:
                self.on_error(f"Audio processing error: {e}")
        finally:
            self.is_processing = False
    
    def speak(self, text: str, blocking: bool = False):
        """Convert text to speech"""
        try:
            if blocking:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                # Run TTS in separate thread
                threading.Thread(
                    target=self._speak_async,
                    args=(text,),
                    daemon=True
                ).start()
                
        except Exception as e:
            logger.error(f"TTS error: {e}")
            if self.on_error:
                self.on_error(f"TTS error: {e}")
    
    def _speak_async(self, text: str):
        """Async TTS execution"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"Async TTS error: {e}")
    
    def recognize_speech_from_audio(self, audio_data: bytes, format: str = "wav") -> Optional[str]:
        """Recognize speech from audio data"""
        try:
            # Convert audio data to AudioData object
            if format.lower() == "wav":
                audio = sr.AudioData(audio_data, 16000, 2)  # Assume 16kHz, 16-bit
            else:
                raise ValueError(f"Unsupported audio format: {format}")
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language="en-US")
            return text
            
        except sr.UnknownValueError:
            return None
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    def set_wake_words(self, wake_words: list):
        """Update wake words"""
        self.wake_words = wake_words
        logger.info(f"Updated wake words: {wake_words}")
    
    def set_sensitivity(self, sensitivity: float):
        """Update wake word sensitivity"""
        self.sensitivity = max(0.0, min(1.0, sensitivity))
        logger.info(f"Updated sensitivity: {self.sensitivity}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get voice service status"""
        return {
            "is_listening": self.is_listening,
            "is_processing": self.is_processing,
            "wake_words": self.wake_words,
            "sensitivity": self.sensitivity,
            "microphone_available": self.microphone is not None,
            "tts_available": self.tts_engine is not None
        }
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_listening()
        
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass
        
        logger.info("Voice service cleaned up")


# Global voice service instance
_voice_service: Optional[VoiceService] = None


def get_voice_service() -> VoiceService:
    """Get global voice service instance"""
    global _voice_service
    if _voice_service is None:
        _voice_service = VoiceService()
    return _voice_service


def initialize_voice_service(wake_words: list = None, sensitivity: float = 0.5) -> VoiceService:
    """Initialize global voice service"""
    global _voice_service
    _voice_service = VoiceService(wake_words, sensitivity)
    return _voice_service
