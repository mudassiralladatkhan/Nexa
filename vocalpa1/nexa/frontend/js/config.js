// Nexa Voice Assistant - Configuration

const CONFIG = {
    // Backend Configuration
    BACKEND: {
        BASE_URL: 'http://localhost:8000',
        API_VERSION: 'v1',
        TIMEOUT: 10000,
        RETRY_ATTEMPTS: 3,
        RETRY_DELAY: 1000
    },

    // API Endpoints
    ENDPOINTS: {
        // Health and Status
        HEALTH: '/health',
        TEST: '/api/test',
        
        // Voice Commands (simplified)
        VOICE_COMMAND: '/api/voice/command',
        
        // Authentication (placeholder)
        LOGIN: '/api/auth/login',
        LOGOUT: '/api/auth/logout',
        ME: '/api/auth/me',
        
        // Commands (simplified)
        PROCESS_COMMAND: '/api/voice/command',
        COMMAND_HISTORY: '/api/commands/history',
        COMMAND_ANALYTICS: '/api/commands/analytics',
        
        // Voice (simplified)
        VOICE_RECOGNIZE: '/api/voice/recognize',
        VOICE_SYNTHESIZE: '/api/voice/synthesize',
        VOICE_STREAM: '/api/voice/stream',
        VOICE_CONFIG: '/api/voice/config',
        
        // Weather
        WEATHER_CURRENT: '/api/v1/weather/current',
        WEATHER_FORECAST: '/api/v1/weather/forecast',
        
        // News
        NEWS_HEADLINES: '/api/v1/news/headlines',
        NEWS_SEARCH: '/api/v1/news/search',
        
        // Music
        MUSIC_SEARCH: '/api/v1/music/search',
        MUSIC_CONTROL: '/api/v1/music/control',
        
        // Conversations
        CONVERSATIONS: '/api/v1/conversations',
        CONVERSATION_MESSAGES: '/api/v1/conversations/{id}/messages',
        
        // Preferences
        PREFERENCES: '/api/v1/preferences',
        PREFERENCES_BATCH: '/api/v1/preferences/batch',
        
        // System
        SYSTEM_STATUS: '/api/v1/status',
        SYSTEM_HEALTH: '/health'
    },

    // Voice Settings
    VOICE: {
        WAKE_WORDS: ['nexa', 'hey nexa', 'ok nexa'],
        LANGUAGE: 'en-US',
        CONTINUOUS_LISTENING: false,
        SPEECH_TIMEOUT: 5000,
        SILENCE_TIMEOUT: 2000,
        MAX_ALTERNATIVES: 3,
        INTERIM_RESULTS: true
    },

    // Speech Synthesis
    TTS: {
        VOICE: null, // Will be set to default voice
        RATE: 1.0,
        PITCH: 1.0,
        VOLUME: 0.8,
        LANGUAGE: 'en-US'
    },

    // UI Settings
    UI: {
        THEME: 'auto', // 'light', 'dark', 'auto'
        ANIMATIONS: true,
        SOUND_EFFECTS: true,
        NOTIFICATIONS: true,
        AUTO_SCROLL: true,
        CONVERSATION_LIMIT: 100
    },

    // WebSocket Configuration
    WEBSOCKET: {
        RECONNECT_INTERVAL: 3000,
        MAX_RECONNECT_ATTEMPTS: 5,
        HEARTBEAT_INTERVAL: 30000
    },

    // Storage Keys
    STORAGE_KEYS: {
        USER_ID: 'nexa_user_id',
        SESSION_TOKEN: 'nexa_session_token',
        PREFERENCES: 'nexa_preferences',
        CONVERSATION_HISTORY: 'nexa_conversations',
        THEME: 'nexa_theme',
        WAKE_WORD_CONFIG: 'nexa_wake_word_config'
    },

    // Feature Flags
    FEATURES: {
        VOICE_RECOGNITION: true,
        TEXT_TO_SPEECH: true,
        WAKE_WORD_DETECTION: true,
        CONTINUOUS_LISTENING: true,
        CONVERSATION_HISTORY: true,
        QUICK_ACTIONS: true,
        SETTINGS_PANEL: true,
        OFFLINE_MODE: false,
        PWA_INSTALL: true
    },

    // Debug Settings
    DEBUG: {
        ENABLED: true,
        LOG_LEVEL: 'info', // 'debug', 'info', 'warn', 'error'
        LOG_API_CALLS: true,
        LOG_VOICE_EVENTS: true,
        MOCK_BACKEND: false
    },

    // Performance Settings
    PERFORMANCE: {
        DEBOUNCE_DELAY: 300,
        THROTTLE_DELAY: 100,
        ANIMATION_DURATION: 300,
        LAZY_LOAD: true,
        CACHE_DURATION: 300000 // 5 minutes
    },

    // Error Messages
    ERRORS: {
        NETWORK_ERROR: 'Network connection failed. Please check your internet connection.',
        BACKEND_ERROR: 'Backend service is unavailable. Please try again later.',
        MICROPHONE_ERROR: 'Microphone access denied. Please enable microphone permissions.',
        SPEECH_ERROR: 'Speech recognition failed. Please try again.',
        TTS_ERROR: 'Text-to-speech is not available.',
        WAKE_WORD_ERROR: 'Wake word detection failed.',
        UNKNOWN_ERROR: 'An unexpected error occurred. Please try again.'
    },

    // Success Messages
    MESSAGES: {
        CONNECTED: 'Connected to Nexa backend',
        LISTENING: 'Listening for your command...',
        PROCESSING: 'Processing your request...',
        SPEAKING: 'Speaking response...',
        READY: 'Ready for your next command'
    },

    // Quick Actions Configuration
    QUICK_ACTIONS: [
        {
            id: 'music',
            icon: 'music_note',
            label: 'Music',
            command: 'play music',
            description: 'Play music or control playback'
        },
        {
            id: 'weather',
            icon: 'cloud',
            label: 'Weather',
            command: 'what\'s the weather',
            description: 'Get current weather information'
        },
        {
            id: 'news',
            icon: 'article',
            label: 'News',
            command: 'latest news',
            description: 'Get latest news headlines'
        },
        {
            id: 'time',
            icon: 'schedule',
            label: 'Time',
            command: 'what time is it',
            description: 'Get current time and date'
        },
        {
            id: 'calculator',
            icon: 'calculate',
            label: 'Math',
            command: 'calculate',
            description: 'Perform calculations'
        },
        {
            id: 'apps',
            icon: 'apps',
            label: 'Apps',
            command: 'open',
            description: 'Launch applications'
        }
    ],

    // Command Examples
    COMMAND_EXAMPLES: {
        TIME: [
            'What time is it?',
            'What\'s the current time?',
            'Tell me the time'
        ],
        WEATHER: [
            'What\'s the weather like?',
            'Weather forecast',
            'Is it going to rain today?'
        ],
        MUSIC: [
            'Play music',
            'Play some jazz',
            'Pause music',
            'Next song'
        ],
        NEWS: [
            'Latest news',
            'Technology news',
            'What\'s happening today?'
        ],
        APPS: [
            'Open calculator',
            'Launch browser',
            'Start notepad'
        ],
        MATH: [
            'Calculate 15 plus 27',
            'What\'s 50 times 3?',
            'Divide 100 by 4'
        ],
        GENERAL: [
            'Hello',
            'How are you?',
            'Tell me a joke',
            'Help'
        ]
    },

    // Animation Timings
    ANIMATIONS: {
        FADE_DURATION: 300,
        SLIDE_DURATION: 250,
        BOUNCE_DURATION: 400,
        PULSE_DURATION: 1500,
        WAVE_DURATION: 2000
    },

    // Color Themes
    THEMES: {
        LIGHT: {
            primary: '#6366F1',
            secondary: '#10B981',
            background: '#FFFFFF',
            surface: '#F8FAFC',
            text: '#1E293B'
        },
        DARK: {
            primary: '#818CF8',
            secondary: '#34D399',
            background: '#0F172A',
            surface: '#1E293B',
            text: '#F8FAFC'
        }
    }
};

// Environment-specific overrides
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    CONFIG.DEBUG.ENABLED = true;
    CONFIG.BACKEND.BASE_URL = 'http://localhost:8000';
} else {
    CONFIG.DEBUG.ENABLED = false;
    // Production backend URL would be set here
}

// Browser capability detection
CONFIG.CAPABILITIES = {
    SPEECH_RECOGNITION: 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window,
    SPEECH_SYNTHESIS: 'speechSynthesis' in window,
    MEDIA_DEVICES: 'mediaDevices' in navigator,
    NOTIFICATIONS: 'Notification' in window,
    SERVICE_WORKER: 'serviceWorker' in navigator,
    WEB_AUDIO: 'AudioContext' in window || 'webkitAudioContext' in window,
    WEBSOCKETS: 'WebSocket' in window,
    LOCAL_STORAGE: 'localStorage' in window,
    GEOLOCATION: 'geolocation' in navigator
};

// Export configuration
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
} else {
    window.CONFIG = CONFIG;
}
