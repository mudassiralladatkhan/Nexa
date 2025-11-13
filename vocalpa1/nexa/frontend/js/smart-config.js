// Nexa Voice Assistant - Smart Configuration
// Automatically detects backend port

const SMART_CONFIG = {
    // Backend Configuration - Smart Detection
    BACKEND: {
        POSSIBLE_URLS: [
            'http://localhost:8001',
            'http://localhost:8002', 
            'http://localhost:8003',
            'http://localhost:8000'
        ],
        BASE_URL: null, // Will be set dynamically
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
        
        // Voice Commands
        VOICE_COMMAND: '/api/voice/command',
        
        // Authentication (placeholder)
        LOGIN: '/api/auth/login',
        LOGOUT: '/api/auth/logout',
        ME: '/api/auth/me',
        
        // Commands
        PROCESS_COMMAND: '/api/voice/command',
        COMMAND_HISTORY: '/api/commands/history',
        COMMAND_ANALYTICS: '/api/commands/analytics',
        
        // Voice
        VOICE_RECOGNIZE: '/api/voice/recognize',
        VOICE_SYNTHESIZE: '/api/voice/synthesize',
        VOICE_STREAM: '/api/voice/stream',
        VOICE_CONFIG: '/api/voice/config'
    },

    // Voice Configuration
    VOICE: {
        RECOGNITION: {
            LANGUAGE: 'en-US',
            CONTINUOUS: true,
            INTERIM_RESULTS: true,
            MAX_ALTERNATIVES: 1
        },
        SYNTHESIS: {
            VOICE: null, // Use default
            RATE: 1.0,
            PITCH: 1.0,
            VOLUME: 1.0
        },
        WAKE_WORDS: ['hey nexa', 'ok nexa', 'nexa'],
        COMMANDS: {
            STOP_WORDS: ['stop', 'cancel', 'nevermind'],
            TIMEOUT: 5000
        }
    },

    // UI Configuration
    UI: {
        THEME: 'dark',
        ANIMATIONS: true,
        VOICE_VISUALIZER: true,
        QUICK_ACTIONS: true,
        CONVERSATION_HISTORY: true
    },

    // Feature Flags
    FEATURES: {
        WAKE_WORD_DETECTION: true,
        CONTINUOUS_LISTENING: false,
        VOICE_FEEDBACK: true,
        OFFLINE_MODE: false,
        ANALYTICS: true
    }
};

// Smart backend detection function
async function detectBackendURL() {
    console.log('🔍 Detecting backend server...');
    
    for (const url of SMART_CONFIG.BACKEND.POSSIBLE_URLS) {
        try {
            console.log(`Testing: ${url}`);
            const response = await fetch(`${url}/health`, {
                method: 'GET',
                timeout: 3000
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.status === 'healthy') {
                    console.log(`✅ Backend found at: ${url}`);
                    SMART_CONFIG.BACKEND.BASE_URL = url;
                    return url;
                }
            }
        } catch (error) {
            console.log(`❌ ${url} not available:`, error.message);
        }
    }
    
    console.log('❌ No backend server found');
    return null;
}

// Initialize smart config
async function initializeSmartConfig() {
    const backendURL = await detectBackendURL();
    
    if (backendURL) {
        // Update the main CONFIG object if it exists
        if (typeof CONFIG !== 'undefined') {
            CONFIG.BACKEND.BASE_URL = backendURL;
        }
        
        // Dispatch custom event for other components
        window.dispatchEvent(new CustomEvent('backendDetected', {
            detail: { url: backendURL }
        }));
        
        return true;
    } else {
        // Dispatch error event
        window.dispatchEvent(new CustomEvent('backendError', {
            detail: { message: 'No backend server found' }
        }));
        
        return false;
    }
}

// Auto-initialize when script loads
if (typeof window !== 'undefined') {
    window.addEventListener('DOMContentLoaded', initializeSmartConfig);
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SMART_CONFIG, detectBackendURL, initializeSmartConfig };
}
