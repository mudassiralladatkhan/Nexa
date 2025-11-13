"""
Background service manager - Handles continuous operations
Mirrors VoiceBackgroundService.kt and EnhancedVoiceBackgroundService.kt
"""

import asyncio
import threading
import logging
from typing import Optional, Dict, Any, Callable
from datetime import datetime, timedelta
import schedule
import time

from .voice_service import get_voice_service
from ..app.config import get_settings

logger = logging.getLogger(__name__)


class BackgroundServiceManager:
    """Manages all background services for Nexa"""
    
    def __init__(self):
        self.is_running = False
        self.services = {}
        self.scheduler_thread = None
        self.voice_service = None
        
        # Service callbacks
        self.on_wake_word_detected: Optional[Callable] = None
        self.on_speech_recognized: Optional[Callable] = None
        self.on_service_error: Optional[Callable] = None
        
    def start(self):
        """Start all background services"""
        if self.is_running:
            logger.warning("Background services already running")
            return
        
        logger.info("Starting Nexa background services...")
        
        try:
            # Initialize voice service
            settings = get_settings()
            if settings.enable_background_listening:
                self._start_voice_service()
            
            # Start scheduler
            self._start_scheduler()
            
            # Start monitoring
            self._start_monitoring()
            
            self.is_running = True
            logger.info("Background services started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start background services: {e}")
            self.stop()
            raise
    
    def stop(self):
        """Stop all background services"""
        if not self.is_running:
            return
        
        logger.info("Stopping background services...")
        
        # Stop voice service
        if self.voice_service:
            self.voice_service.stop_listening()
            self.voice_service.cleanup()
        
        # Stop scheduler
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.is_running = False
            self.scheduler_thread.join(timeout=5)
        
        logger.info("Background services stopped")
    
    def _start_voice_service(self):
        """Initialize and start voice service"""
        try:
            settings = get_settings()
            
            # Get or create voice service
            self.voice_service = get_voice_service()
            
            # Set wake words from config
            self.voice_service.set_wake_words(settings.wake_words)
            
            # Set callbacks
            self.voice_service.on_wake_word = self._handle_wake_word
            self.voice_service.on_speech_recognized = self._handle_speech_recognized
            self.voice_service.on_error = self._handle_voice_error
            
            # Start listening
            self.voice_service.start_listening()
            
            logger.info("Voice service started with wake words: %s", settings.wake_words)
            
        except Exception as e:
            logger.error(f"Failed to start voice service: {e}")
            raise
    
    def _start_scheduler(self):
        """Start background task scheduler"""
        def scheduler_loop():
            logger.info("Background scheduler started")
            
            # Schedule periodic tasks
            schedule.every(1).minutes.do(self._health_check)
            schedule.every(5).minutes.do(self._cleanup_old_data)
            schedule.every(1).hours.do(self._system_maintenance)
            
            while self.is_running:
                try:
                    schedule.run_pending()
                    time.sleep(1)
                except Exception as e:
                    logger.error(f"Scheduler error: {e}")
                    time.sleep(5)  # Wait before retrying
            
            logger.info("Background scheduler stopped")
        
        self.scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        self.scheduler_thread.start()
    
    def _start_monitoring(self):
        """Start system monitoring"""
        def monitoring_loop():
            logger.info("System monitoring started")
            
            while self.is_running:
                try:
                    # Monitor system resources
                    self._monitor_resources()
                    
                    # Monitor service health
                    self._monitor_service_health()
                    
                    # Sleep for monitoring interval
                    time.sleep(30)  # Check every 30 seconds
                    
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                    time.sleep(60)  # Wait longer on error
            
            logger.info("System monitoring stopped")
        
        monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitoring_thread.start()
    
    def _handle_wake_word(self, wake_word: str, full_text: str):
        """Handle wake word detection"""
        logger.info(f"Wake word detected: {wake_word}")
        
        # Log event to database
        self._log_system_event(
            "wake_word_detected",
            "voice_service",
            f"Wake word '{wake_word}' detected in text: {full_text}"
        )
        
        # Call external callback if set
        if self.on_wake_word_detected:
            try:
                self.on_wake_word_detected(wake_word, full_text)
            except Exception as e:
                logger.error(f"Wake word callback error: {e}")
    
    def _handle_speech_recognized(self, text: str, is_wake_word: bool):
        """Handle speech recognition"""
        logger.debug(f"Speech recognized: {text} (wake word: {is_wake_word})")
        
        # Only process if it's a wake word activation or continuous mode
        if is_wake_word or self._is_continuous_mode():
            # Call external callback if set
            if self.on_speech_recognized:
                try:
                    self.on_speech_recognized(text, is_wake_word)
                except Exception as e:
                    logger.error(f"Speech recognition callback error: {e}")
    
    def _handle_voice_error(self, error_message: str):
        """Handle voice service errors"""
        logger.error(f"Voice service error: {error_message}")
        
        # Log to database
        self._log_system_event(
            "voice_service_error",
            "voice_service",
            error_message,
            "error"
        )
        
        # Call external callback if set
        if self.on_service_error:
            try:
                self.on_service_error("voice_service", error_message)
            except Exception as e:
                logger.error(f"Error callback failed: {e}")
    
    def _health_check(self):
        """Perform periodic health check"""
        try:
            # Check voice service health
            if self.voice_service:
                status = self.voice_service.get_status()
                if not status["is_listening"] and get_settings().enable_background_listening:
                    logger.warning("Voice service not listening, attempting restart")
                    self.voice_service.start_listening()
            
            # Check database connectivity
            # This would integrate with database health check
            
            logger.debug("Health check completed")
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
    
    def _cleanup_old_data(self):
        """Clean up old data periodically"""
        try:
            # This would integrate with database cleanup
            logger.debug("Data cleanup completed")
            
        except Exception as e:
            logger.error(f"Data cleanup failed: {e}")
    
    def _system_maintenance(self):
        """Perform system maintenance tasks"""
        try:
            # Log system status
            self._log_system_event(
                "system_maintenance",
                "background_service",
                "Periodic system maintenance completed"
            )
            
            logger.info("System maintenance completed")
            
        except Exception as e:
            logger.error(f"System maintenance failed: {e}")
    
    def _monitor_resources(self):
        """Monitor system resources"""
        try:
            import psutil
            
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Log warnings for high resource usage
            if cpu_percent > 80:
                logger.warning(f"High CPU usage: {cpu_percent}%")
            
            if memory.percent > 85:
                logger.warning(f"High memory usage: {memory.percent}%")
            
        except Exception as e:
            logger.error(f"Resource monitoring failed: {e}")
    
    def _monitor_service_health(self):
        """Monitor health of individual services"""
        try:
            # Check voice service
            if self.voice_service:
                status = self.voice_service.get_status()
                if not status["microphone_available"]:
                    logger.error("Microphone not available")
                if not status["tts_available"]:
                    logger.error("TTS engine not available")
            
        except Exception as e:
            logger.error(f"Service health monitoring failed: {e}")
    
    def _is_continuous_mode(self) -> bool:
        """Check if continuous listening mode is enabled"""
        # This would check user preferences
        return False  # Default to wake word mode
    
    def _log_system_event(self, event_type: str, source: str, description: str, severity: str = "info"):
        """Log system event to database"""
        try:
            # This would integrate with the database system event logging
            logger.info(f"System event: {event_type} - {description}")
            
        except Exception as e:
            logger.error(f"Failed to log system event: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all background services"""
        status = {
            "is_running": self.is_running,
            "services": {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Voice service status
        if self.voice_service:
            status["services"]["voice"] = self.voice_service.get_status()
        
        # Scheduler status
        status["services"]["scheduler"] = {
            "running": self.scheduler_thread and self.scheduler_thread.is_alive()
        }
        
        return status
    
    def restart_service(self, service_name: str):
        """Restart a specific service"""
        try:
            if service_name == "voice" and self.voice_service:
                logger.info("Restarting voice service...")
                self.voice_service.stop_listening()
                time.sleep(1)
                self.voice_service.start_listening()
                logger.info("Voice service restarted")
            else:
                logger.warning(f"Unknown service: {service_name}")
                
        except Exception as e:
            logger.error(f"Failed to restart service {service_name}: {e}")
            raise


# Global background service manager
_background_manager: Optional[BackgroundServiceManager] = None


def get_background_manager() -> BackgroundServiceManager:
    """Get global background service manager"""
    global _background_manager
    if _background_manager is None:
        _background_manager = BackgroundServiceManager()
    return _background_manager


def start_background_services():
    """Start all background services"""
    manager = get_background_manager()
    manager.start()
    return manager


def stop_background_services():
    """Stop all background services"""
    global _background_manager
    if _background_manager:
        _background_manager.stop()
        _background_manager = None
