"""
Nexa Command Processor - Central command handling logic
Ported from VocalPA CommandProcessor.kt with comprehensive Python implementations
"""

from typing import Dict, Any, Optional, Callable, Awaitable, List
from dataclasses import dataclass
from datetime import datetime
import asyncio
import re
import random
import subprocess
import platform
import webbrowser
import logging

# Import our new modules
from .app_launcher import launch_app, find_app
from .website_opener import open_website, find_website
from .entertainment import get_joke, get_fun_fact, get_motivational_quote, get_riddle, get_trivia

logger = logging.getLogger(__name__)


@dataclass
class CommandResult:
    """Result of command processing"""
    success: bool
    command_type: str
    response_text: str
    metadata: Optional[Dict[str, Any]] = None


class CommandProcessor:
    """Central command processor with all VocalPA functionality."""
    
    def __init__(self):
        self._handlers: Dict[str, Callable[[str], Awaitable[CommandResult]]] = {}
        self._fallthrough: Optional[Callable[[str], Awaitable[CommandResult]]] = None
        self._register_all_handlers()
    
    def _register_all_handlers(self):
        """Register all command handlers from VocalPA"""
        # Time and date commands
        self._handlers["time"] = self._handle_time_command
        self._handlers["date"] = self._handle_date_command
        
        # Weather commands
        self._handlers["weather"] = self._handle_weather_command
        
        # Music commands
        self._handlers["music"] = self._handle_music_command
        
        # App launching commands
        self._handlers["app"] = self._handle_app_command
        self._handlers["open"] = self._handle_app_command
        self._handlers["launch"] = self._handle_app_command
        
        # Website opening commands
        self._handlers["website"] = self._handle_website_command
        self._handlers["web"] = self._handle_website_command
        self._handlers["visit"] = self._handle_website_command
        
        # System commands
        self._handlers["system"] = self._handle_system_command
        
        # Communication commands
        self._handlers["call"] = self._handle_call_command
        self._handlers["message"] = self._handle_message_command
        
        # Search commands
        self._handlers["search"] = self._handle_search_command
        self._handlers["google"] = self._handle_search_command
        
        # News commands
        self._handlers["news"] = self._handle_news_command
        
        # Calculator commands
        self._handlers["calculate"] = self._handle_calculate_command
        self._handlers["math"] = self._handle_calculate_command
        
        # Entertainment commands
        self._handlers["joke"] = self._handle_joke_command
        self._handlers["fact"] = self._handle_fact_command
        self._handlers["quote"] = self._handle_quote_command
        self._handlers["riddle"] = self._handle_riddle_command
        self._handlers["trivia"] = self._handle_trivia_command
        
        # Reminder and alarm commands
        self._handlers["reminder"] = self._handle_reminder_command
        self._handlers["alarm"] = self._handle_alarm_command
        
        # Device control commands
        self._handlers["device"] = self._handle_device_command
        
        # Greeting and conversation
        self._handlers["greeting"] = self._handle_greeting_command
        self._handlers["conversation"] = self._handle_conversation_command
        
        # Help and information
        self._handlers["help"] = self._handle_help_command
    
    async def process(self, text: str, *, locale: str | None = None,
                      metadata: dict[str, str] | None = None) -> CommandResult:
        """Process a command and return result"""
        normalized = text.strip().lower()
        
        # Try registered handlers in priority order
        command_type = await self._detect_command_type(normalized)
        
        if command_type and command_type in self._handlers:
            try:
                return await self._handlers[command_type](normalized)
            except Exception as e:
                return CommandResult(
                    success=False,
                    command_type=command_type,
                    response_text=f"Error processing {command_type} command: {str(e)}"
                )
        
        # Fallthrough handler
        if self._fallthrough:
            return await self._fallthrough(normalized)
        
        # Default response for unrecognized commands
        return CommandResult(
            success=False,
            command_type="unknown",
            response_text="I didn't understand that command. Say 'help' to see what I can do."
        )
    
    async def _detect_command_type(self, text: str) -> Optional[str]:
        """Detect command type from text - mirrors VocalPA logic"""
        # Time commands
        if any(word in text for word in ["time", "clock", "hour", "minute", "what time"]):
            return "time"
        
        # Date commands
        if any(word in text for word in ["date", "today", "day", "what day"]):
            return "date"
        
        # Weather commands
        if any(word in text for word in ["weather", "temperature", "rain", "sunny", "cloudy", "forecast"]):
            return "weather"
        
        # Music commands
        if any(word in text for word in ["play", "music", "song", "artist", "album", "pause", "stop", "next", "previous"]):
            return "music"
        
        # App launching - enhanced detection
        if any(word in text for word in ["open", "launch", "start", "run"]):
            # Check if it's a website first
            if any(word in text for word in ["website", "site", ".com", "www", "http"]):
                return "website"
            # Check for specific apps
            elif any(word in text for word in ["calculator", "notepad", "browser", "chrome", "firefox", "app", "application", "program"]):
                return "app"
            # Try to detect if it's a website name
            elif find_website(text):
                return "website"
            # Default to app
            else:
                return "app"
        
        # System commands
        if any(word in text for word in ["battery", "wifi", "bluetooth", "volume", "brightness", "settings"]):
            return "system"
        
        # Communication
        if any(word in text for word in ["call", "phone", "dial"]):
            return "call"
        if any(word in text for word in ["message", "text", "sms", "send"]):
            return "message"
        
        # Entertainment commands - new detection
        if any(word in text for word in ["joke", "funny", "make me laugh", "tell me a joke"]):
            return "joke"
        if any(word in text for word in ["fact", "fun fact", "interesting", "did you know"]):
            return "fact"
        if any(word in text for word in ["quote", "motivational", "inspiration", "inspire me"]):
            return "quote"
        if any(word in text for word in ["riddle", "puzzle", "brain teaser"]):
            return "riddle"
        if any(word in text for word in ["trivia", "quiz", "question"]):
            return "trivia"
        
        # Search and web
        if any(word in text for word in ["search", "google", "find", "look up"]):
            return "search"
        if any(word in text for word in ["website", "browse", "internet", "web"]) or find_website(text):
            return "website"
        
        # News
        if any(word in text for word in ["news", "headlines", "breaking", "latest"]):
            return "news"
        
        # Calculator
        if any(word in text for word in ["calculate", "math", "plus", "minus", "multiply", "divide", "equals"]) or re.search(r'\d+\s*[\+\-\*\/]\s*\d+', text):
            return "calculate"
        
        # Reminders and alarms
        if any(word in text for word in ["remind", "reminder", "remember"]):
            return "reminder"
        if any(word in text for word in ["alarm", "wake me", "set timer"]):
            return "alarm"
        
        # Device control
        if any(word in text for word in ["turn on", "turn off", "enable", "disable", "activate", "deactivate"]):
            return "device"
        
        # Greetings
        if any(word in text for word in ["hello", "hi", "hey", "good morning", "good evening", "good afternoon"]):
            return "greeting"
        
        # Help
        if any(word in text for word in ["help", "what can you do", "commands", "assistance"]):
            return "help"
        
        # General conversation
        if any(word in text for word in ["how are you", "what's up", "thank you", "thanks", "goodbye", "bye"]):
            return "conversation"
        
        return None
    
    # Command Handlers - All VocalPA functionality
    
    async def _handle_time_command(self, text: str) -> CommandResult:
        """Handle time-related commands"""
        now = datetime.now()
        
        if "timezone" in text or "zone" in text:
            response = f"The current time is {now.strftime('%I:%M %p')} in your local timezone ({now.astimezone().tzname()})"
        else:
            response = f"The current time is {now.strftime('%I:%M %p')}"
        
        return CommandResult(
            success=True,
            command_type="time",
            response_text=response,
            metadata={"timestamp": now.isoformat(), "format": "12hour"}
        )
    
    async def _handle_date_command(self, text: str) -> CommandResult:
        """Handle date-related commands"""
        now = datetime.now()
        
        if "full" in text or "complete" in text:
            response = f"Today is {now.strftime('%A, %B %d, %Y')}"
        else:
            response = f"Today is {now.strftime('%A, %B %d')}"
        
        return CommandResult(
            success=True,
            command_type="date",
            response_text=response,
            metadata={"date": now.date().isoformat(), "day_of_week": now.strftime('%A')}
        )
    
    async def _handle_weather_command(self, text: str) -> CommandResult:
        """Handle weather commands - integrates with weather API"""
        # Extract location if mentioned
        location = "your location"  # Default
        
        return CommandResult(
            success=True,
            command_type="weather",
            response_text=f"To get weather information for {location}, please configure weather API keys in settings.",
            metadata={"requires_api": "weather", "location": location}
        )
    
    async def _handle_music_command(self, text: str) -> CommandResult:
        """Handle music commands"""
        if "play" in text:
            action = "play"
            response = "Starting music playback"
        elif "pause" in text or "stop" in text:
            action = "pause"
            response = "Pausing music"
        elif "next" in text:
            action = "next"
            response = "Skipping to next track"
        elif "previous" in text or "back" in text:
            action = "previous"
            response = "Going to previous track"
        else:
            action = "search"
            response = "Searching for music"
        
        return CommandResult(
            success=True,
            command_type="music",
            response_text=response,
            metadata={"action": action, "requires_api": "music"}
        )
    
    async def _handle_app_command(self, text: str) -> CommandResult:
        """Handle app launching commands using app launcher module"""
        try:
            # Use the app launcher module
            result = launch_app(text)
            
            return CommandResult(
                success=result['success'],
                command_type="app",
                response_text=result['message'],
                metadata={
                    "app": result.get('app_name'),
                    "command": result.get('command'),
                    "suggestions": result.get('suggestions', [])
                }
            )
        except Exception as e:
            logger.error(f"Error in app command handler: {str(e)}")
            return CommandResult(
                success=False,
                command_type="app",
                response_text=f"Error launching app: {str(e)}"
            )

    async def _handle_website_command(self, text: str) -> CommandResult:
        """Handle website opening commands using website opener module"""
        try:
            # Use the website opener module
            result = open_website(text)
            
            return CommandResult(
                success=result['success'],
                command_type="website",
                response_text=result['message'],
                metadata={
                    "website_name": result.get('website_name'),
                    "url": result.get('url'),
                    "confidence": result.get('confidence'),
                    "suggestions": result.get('suggestions', [])
                }
            )
        except Exception as e:
            logger.error(f"Error in website command handler: {str(e)}")
            return CommandResult(
                success=False,
                command_type="website",
                response_text=f"Error opening website: {str(e)}"
            )
    
    async def _handle_system_command(self, text: str) -> CommandResult:
        """Handle system information commands"""
        if "battery" in text:
            # Placeholder - would integrate with system battery API
            response = "Battery information requires system integration"
        elif "wifi" in text:
            response = "WiFi status requires system integration"
        elif "bluetooth" in text:
            response = "Bluetooth status requires system integration"
        elif "volume" in text:
            response = "Volume control requires system integration"
        else:
            response = "System command recognized but not implemented"
        
        return CommandResult(
            success=True,
            command_type="system",
            response_text=response,
            metadata={"requires_system_api": True}
        )
    
    async def _handle_search_command(self, text: str) -> CommandResult:
        """Handle search commands"""
        # Extract search query
        query_patterns = [
            r"search for (.+)",
            r"google (.+)",
            r"find (.+)",
            r"look up (.+)"
        ]
        
        query = None
        for pattern in query_patterns:
            match = re.search(pattern, text)
            if match:
                query = match.group(1)
                break
        
        if query:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            response = f"Searching for '{query}'"
        else:
            response = "What would you like me to search for?"
        
        return CommandResult(
            success=True,
            command_type="search",
            response_text=response,
            metadata={"query": query}
        )
    
    async def _handle_news_command(self, text: str) -> CommandResult:
        """Handle news commands"""
        return CommandResult(
            success=True,
            command_type="news",
            response_text="To get news updates, please configure news API keys in settings.",
            metadata={"requires_api": "news"}
        )
    
    async def _handle_calculate_command(self, text: str) -> CommandResult:
        """Handle calculation commands"""
        # Extract mathematical expression
        math_match = re.search(r'(\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(\d+(?:\.\d+)?)', text)
        
        if math_match:
            num1, operator, num2 = math_match.groups()
            try:
                num1, num2 = float(num1), float(num2)
                
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 != 0:
                        result = num1 / num2
                    else:
                        return CommandResult(
                            success=False,
                            command_type="calculate",
                            response_text="Cannot divide by zero"
                        )
                
                # Format result
                if result == int(result):
                    result_str = str(int(result))
                else:
                    result_str = f"{result:.2f}"
                
                response = f"{num1} {operator} {num2} equals {result_str}"
                
                return CommandResult(
                    success=True,
                    command_type="calculate",
                    response_text=response,
                    metadata={"expression": f"{num1} {operator} {num2}", "result": result}
                )
            except Exception as e:
                return CommandResult(
                    success=False,
                    command_type="calculate",
                    response_text=f"Calculation error: {str(e)}"
                )
        
        return CommandResult(
            success=False,
            command_type="calculate",
            response_text="I couldn't understand the calculation. Try saying something like 'calculate 5 plus 3'."
        )
    
    async def _handle_greeting_command(self, text: str) -> CommandResult:
        """Handle greeting commands"""
        greetings = {
            "morning": ["Good morning! How can I help you today?", "Morning! What can I do for you?"],
            "afternoon": ["Good afternoon! How may I assist you?", "Afternoon! What would you like to do?"],
            "evening": ["Good evening! How can I help?", "Evening! What can I do for you?"],
            "general": ["Hello! How can I help you today?", "Hi there! What would you like to do?", "Hey! I'm here to assist you."]
        }
        
        current_hour = datetime.now().hour
        
        if "morning" in text or (6 <= current_hour < 12):
            responses = greetings["morning"]
        elif "afternoon" in text or (12 <= current_hour < 17):
            responses = greetings["afternoon"]
        elif "evening" in text or (17 <= current_hour < 22):
            responses = greetings["evening"]
        else:
            responses = greetings["general"]
        
        response = random.choice(responses)
        
        return CommandResult(
            success=True,
            command_type="greeting",
            response_text=response,
            metadata={"greeting_type": "friendly", "time_of_day": current_hour}
        )
    
    async def _handle_conversation_command(self, text: str) -> CommandResult:
        """Handle conversational commands"""
        responses = {
            "how are you": ["I'm doing well, thank you for asking!", "I'm great! How are you?"],
            "thank you": ["You're welcome!", "Happy to help!", "My pleasure!"],
            "goodbye": ["Goodbye! Have a great day!", "See you later!", "Take care!"],
            "what's up": ["Not much, just here to help you!", "Ready to assist with whatever you need!"]
        }
        
        for pattern, reply_options in responses.items():
            if pattern in text:
                response = random.choice(reply_options)
                return CommandResult(
                    success=True,
                    command_type="conversation",
                    response_text=response,
                    metadata={"conversation_type": pattern}
                )
        
        # Default conversational response
        return CommandResult(
            success=True,
            command_type="conversation",
            response_text="I'm here and ready to help! What would you like to do?",
            metadata={"conversation_type": "general"}
        )
    
    async def _handle_help_command(self, text: str) -> CommandResult:
        """Handle help commands"""
        help_text = """I can help you with:
• Time and date - "What time is it?" or "What's today's date?"
• Weather - "What's the weather like?"
• Music - "Play music" or "Pause music"
• Apps - "Open calculator" or "Launch browser"
• Search - "Search for cats" or "Google Python tutorials"
• Math - "Calculate 15 plus 27"
• System info - "Battery level" or "WiFi status"
• News - "Latest news"
• And much more! Just ask naturally."""
        
        return CommandResult(
            success=True,
            command_type="help",
            response_text=help_text,
            metadata={"help_type": "general"}
        )
    
    # Placeholder handlers for additional VocalPA features
    
    async def _handle_call_command(self, text: str) -> CommandResult:
        """Handle call commands"""
        return CommandResult(
            success=True,
            command_type="call",
            response_text="Call functionality requires phone integration.",
            metadata={"requires_integration": "phone"}
        )
    
    async def _handle_message_command(self, text: str) -> CommandResult:
        """Handle messaging commands"""
        return CommandResult(
            success=True,
            command_type="message",
            response_text="Messaging functionality requires SMS integration.",
            metadata={"requires_integration": "sms"}
        )
    
    async def _handle_reminder_command(self, text: str) -> CommandResult:
        """Handle reminder commands"""
        return CommandResult(
            success=True,
            command_type="reminder",
            response_text="Reminder functionality will be implemented with notification system.",
            metadata={"requires_feature": "notifications"}
        )
    
    async def _handle_alarm_command(self, text: str) -> CommandResult:
        """Handle alarm commands"""
        return CommandResult(
            success=True,
            command_type="alarm",
            response_text="Alarm functionality will be implemented with scheduling system.",
            metadata={"requires_feature": "scheduler"}
        )
    
    async def _handle_device_command(self, text: str) -> CommandResult:
        """Handle device control commands"""
        return CommandResult(
            success=True,
            command_type="device",
            response_text="Device control requires hardware integration.",
            metadata={"requires_integration": "hardware"}
        )
    
    async def _handle_joke_command(self, text: str) -> CommandResult:
        """Handle joke commands using entertainment module"""
        try:
            # Extract category if mentioned
            category = None
            if "tech" in text or "computer" in text or "programming" in text:
                category = "tech"
            
            result = get_joke(category)
            
            return CommandResult(
                success=result['success'],
                command_type="joke",
                response_text=result['content'] if result['success'] else result['message'],
                metadata={"category": result.get('category'), "type": "entertainment"}
            )
        except Exception as e:
            logger.error(f"Error in joke command handler: {str(e)}")
            return CommandResult(
                success=False,
                command_type="joke",
                response_text="Sorry, I couldn't get a joke right now."
            )

    async def _handle_fact_command(self, text: str) -> CommandResult:
        """Handle fun fact commands using entertainment module"""
        try:
            # Extract category if mentioned
            category = None
            if "science" in text:
                category = "science"
            elif "tech" in text or "technology" in text:
                category = "tech"
            elif "space" in text:
                category = "space"
            elif "animal" in text:
                category = "animal"
            
            result = get_fun_fact(category)
            
            return CommandResult(
                success=result['success'],
                command_type="fact",
                response_text=result['content'] if result['success'] else result['message'],
                metadata={"category": result.get('category'), "type": "entertainment"}
            )
        except Exception as e:
            logger.error(f"Error in fact command handler: {str(e)}")
            return CommandResult(
                success=False,
                command_type="fact",
                response_text="Sorry, I couldn't get a fun fact right now."
            )

    async def _handle_quote_command(self, text: str) -> CommandResult:
        """Handle motivational quote commands using entertainment module"""
        try:
            # Extract category if mentioned
            category = None
            if "tech" in text or "technology" in text:
                category = "tech"
            elif "success" in text or "achievement" in text:
                category = "success"
            
            result = get_motivational_quote(category)
            
            return CommandResult(
                success=result['success'],
                command_type="quote",
                response_text=result['content'] if result['success'] else result['message'],
                metadata={"category": result.get('category'), "type": "entertainment"}
            )
        except Exception as e:
            logger.error(f"Error in quote command handler: {str(e)}")
            return CommandResult(
                success=False,
                command_type="quote",
                response_text="Sorry, I couldn't get a motivational quote right now."
            )

    async def _handle_riddle_command(self, text: str) -> CommandResult:
        """Handle riddle commands using entertainment module"""
        try:
            result = get_riddle()
            
            if result['success']:
                response_text = f"Here's a riddle for you: {result['question']} Think about it, and ask me for the answer when you're ready!"
            else:
                response_text = result['message']
            
            return CommandResult(
                success=result['success'],
                command_type="riddle",
                response_text=response_text,
                metadata={
                    "question": result.get('question'),
                    "answer": result.get('answer'),
                    "type": "entertainment"
                }
            )
        except Exception as e:
            logger.error(f"Error in riddle command handler: {str(e)}")
            return CommandResult(
                success=False,
                command_type="riddle",
                response_text="Sorry, I couldn't get a riddle right now."
            )

    async def _handle_trivia_command(self, text: str) -> CommandResult:
        """Handle trivia commands using entertainment module"""
        try:
            result = get_trivia()
            
            if result['success']:
                response_text = f"Here's a trivia question: {result['question']} Do you know the answer?"
            else:
                response_text = result['message']
            
            return CommandResult(
                success=result['success'],
                command_type="trivia",
                response_text=response_text,
                metadata={
                    "question": result.get('question'),
                    "answer": result.get('answer'),
                    "type": "entertainment"
                }
            )
        except Exception as e:
            logger.error(f"Error in trivia command handler: {str(e)}")
            return CommandResult(
                success=False,
                command_type="trivia",
                response_text="Sorry, I couldn't get a trivia question right now."
            )

    async def _handle_greeting_command(self, text: str) -> CommandResult:
        """Handle greeting commands"""
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! I'm here to assist you.",
            "Good to see you! How may I help?",
            "Hello! Ready to help with whatever you need."
        ]
        
        # Time-based greetings
        hour = datetime.now().hour
        if "morning" in text or (6 <= hour < 12):
            response = "Good morning! How can I help you start your day?"
        elif "afternoon" in text or (12 <= hour < 17):
            response = "Good afternoon! What can I do for you?"
        elif "evening" in text or (17 <= hour < 22):
            response = "Good evening! How may I assist you?"
        else:
            response = random.choice(greetings)
        
        return CommandResult(
            success=True,
            command_type="greeting",
            response_text=response,
            metadata={"time_of_day": hour}
        )

    async def _handle_conversation_command(self, text: str) -> CommandResult:
        """Handle general conversation commands"""
        responses = {
            "how are you": "I'm doing great, thank you for asking! How are you?",
            "what's up": "Just here ready to help! What can I do for you?",
            "thank you": "You're very welcome! Happy to help anytime.",
            "thanks": "My pleasure! Let me know if you need anything else.",
            "goodbye": "Goodbye! Have a great day!",
            "bye": "See you later! Take care!"
        }
        
        for phrase, response in responses.items():
            if phrase in text:
                return CommandResult(
                    success=True,
                    command_type="conversation",
                    response_text=response
                )
        
        # Default conversation response
        return CommandResult(
            success=True,
            command_type="conversation",
            response_text="I'm here and ready to chat! What would you like to talk about?"
        )

    async def _handle_help_command(self, text: str) -> CommandResult:
        """Handle help commands"""
        help_text = """Here's what I can help you with:

🕐 Time & Date: "What time is it?" or "What's today's date?"
🌤️ Weather: "What's the weather like?" (requires API setup)
🎵 Music: "Play music" or "Pause music" (requires Spotify)
📱 Apps: "Open calculator" or "Launch browser"
🌐 Websites: "Open YouTube" or "Go to Google"
📰 News: "Latest news" (requires API setup)
🧮 Math: "Calculate 15 plus 27" or "What's 5 times 8?"
😂 Entertainment: "Tell me a joke", "Fun fact", "Motivational quote"
🔍 Search: "Search for cats" or "Google something"
❓ Help: "What can you do?" or "Help"

Just speak naturally! I understand many different ways to ask for things."""
        
        return CommandResult(
            success=True,
            command_type="help",
            response_text=help_text,
            metadata={"command_categories": [
                "time", "weather", "music", "apps", "websites", 
                "news", "math", "entertainment", "search", "help"
            ]}
        )
