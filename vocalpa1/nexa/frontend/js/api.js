// Nexa Voice Assistant - API Client

class NexaAPI {
    constructor() {
        this.baseURL = CONFIG.BACKEND.BASE_URL;
        this.timeout = CONFIG.BACKEND.TIMEOUT;
        this.retryAttempts = CONFIG.BACKEND.RETRY_ATTEMPTS;
        this.retryDelay = CONFIG.BACKEND.RETRY_DELAY;
        
        // Request interceptors
        this.requestInterceptors = [];
        this.responseInterceptors = [];
        
        // Connection status
        this.isConnected = false;
        this.connectionListeners = [];
        
        // Initialize
        this.init();
    }

    init() {
        // Test initial connection
        this.testConnection();
        
        // Set up periodic health checks
        setInterval(() => this.healthCheck(), 30000);
    }

    // Connection Management
    async testConnection() {
        try {
            const response = await this.get(CONFIG.ENDPOINTS.SYSTEM_HEALTH);
            this.setConnectionStatus(true);
            return response;
        } catch (error) {
            this.setConnectionStatus(false);
            throw error;
        }
    }

    async healthCheck() {
        try {
            await this.get(CONFIG.ENDPOINTS.SYSTEM_HEALTH);
            if (!this.isConnected) {
                this.setConnectionStatus(true);
            }
        } catch (error) {
            if (this.isConnected) {
                this.setConnectionStatus(false);
            }
        }
    }

    setConnectionStatus(connected) {
        if (this.isConnected !== connected) {
            this.isConnected = connected;
            this.connectionListeners.forEach(listener => listener(connected));
            
            if (CONFIG.DEBUG.ENABLED) {
                console.log(`Backend connection: ${connected ? 'Connected' : 'Disconnected'}`);
            }
        }
    }

    onConnectionChange(listener) {
        this.connectionListeners.push(listener);
        // Call immediately with current status
        listener(this.isConnected);
    }

    // HTTP Methods
    async request(method, endpoint, data = null, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            method: method.toUpperCase(),
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        if (data && (method.toUpperCase() === 'POST' || method.toUpperCase() === 'PUT')) {
            config.body = JSON.stringify(data);
        }

        // Add authentication if available
        const token = this.getAuthToken();
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }

        // Apply request interceptors
        for (const interceptor of this.requestInterceptors) {
            await interceptor(config);
        }

        let lastError;
        
        // Retry logic
        for (let attempt = 0; attempt <= this.retryAttempts; attempt++) {
            try {
                if (CONFIG.DEBUG.LOG_API_CALLS) {
                    console.log(`API Request: ${method.toUpperCase()} ${url}`, data);
                }

                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), this.timeout);
                
                config.signal = controller.signal;
                
                const response = await fetch(url, config);
                clearTimeout(timeoutId);

                // Apply response interceptors
                for (const interceptor of this.responseInterceptors) {
                    await interceptor(response);
                }

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const result = await response.json();
                
                if (CONFIG.DEBUG.LOG_API_CALLS) {
                    console.log(`API Response: ${method.toUpperCase()} ${url}`, result);
                }

                return result;

            } catch (error) {
                lastError = error;
                
                if (CONFIG.DEBUG.ENABLED) {
                    console.warn(`API Request failed (attempt ${attempt + 1}):`, error);
                }

                // Don't retry on certain errors
                if (error.name === 'AbortError' || 
                    (error.message && error.message.includes('401'))) {
                    break;
                }

                // Wait before retry
                if (attempt < this.retryAttempts) {
                    await this.delay(this.retryDelay * (attempt + 1));
                }
            }
        }

        throw lastError;
    }

    async get(endpoint, options = {}) {
        return this.request('GET', endpoint, null, options);
    }

    async post(endpoint, data, options = {}) {
        return this.request('POST', endpoint, data, options);
    }

    async put(endpoint, data, options = {}) {
        return this.request('PUT', endpoint, data, options);
    }

    async delete(endpoint, options = {}) {
        return this.request('DELETE', endpoint, null, options);
    }

    // Authentication
    getAuthToken() {
        return localStorage.getItem(CONFIG.STORAGE_KEYS.SESSION_TOKEN);
    }

    setAuthToken(token) {
        if (token) {
            localStorage.setItem(CONFIG.STORAGE_KEYS.SESSION_TOKEN, token);
        } else {
            localStorage.removeItem(CONFIG.STORAGE_KEYS.SESSION_TOKEN);
        }
    }

    async login(userId = null, deviceType = 'web') {
        try {
            const response = await this.post(CONFIG.ENDPOINTS.LOGIN, {
                user_id: userId,
                device_type: deviceType,
                device_info: this.getDeviceInfo()
            });
            
            if (response.success) {
                this.setAuthToken(response.session_token);
                localStorage.setItem(CONFIG.STORAGE_KEYS.USER_ID, response.user_id);
            }
            
            return response;
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    }

    async logout() {
        try {
            await this.post(CONFIG.ENDPOINTS.LOGOUT);
        } catch (error) {
            console.warn('Logout request failed:', error);
        } finally {
            this.setAuthToken(null);
            localStorage.removeItem(CONFIG.STORAGE_KEYS.USER_ID);
        }
    }

    // Command Processing
    async processCommand(text, metadata = {}) {
        return this.post(CONFIG.ENDPOINTS.PROCESS_COMMAND, {
            text,
            locale: CONFIG.VOICE.LANGUAGE,
            metadata
        });
    }

    async getCommandHistory(limit = 50) {
        return this.get(`${CONFIG.ENDPOINTS.COMMAND_HISTORY}?limit=${limit}`);
    }

    async getCommandAnalytics(days = 30) {
        return this.get(`${CONFIG.ENDPOINTS.COMMAND_ANALYTICS}?days=${days}`);
    }

    // Voice Services
    async recognizeSpeech(audioData, format = 'wav') {
        return this.post(CONFIG.ENDPOINTS.VOICE_RECOGNIZE, {
            audio_data: audioData,
            format,
            language: CONFIG.VOICE.LANGUAGE
        });
    }

    async synthesizeSpeech(text, options = {}) {
        return this.post(CONFIG.ENDPOINTS.VOICE_SYNTHESIZE, {
            text,
            voice: options.voice || CONFIG.TTS.VOICE,
            speed: options.speed || CONFIG.TTS.RATE,
            language: options.language || CONFIG.TTS.LANGUAGE
        });
    }

    async getVoiceConfig() {
        return this.get(CONFIG.ENDPOINTS.VOICE_CONFIG);
    }

    async setVoiceConfig(config) {
        return this.post(CONFIG.ENDPOINTS.VOICE_CONFIG, config);
    }

    // Weather Services
    async getCurrentWeather(location, units = 'metric') {
        return this.get(`${CONFIG.ENDPOINTS.WEATHER_CURRENT}?location=${encodeURIComponent(location)}&units=${units}`);
    }

    async getWeatherForecast(location, days = 5, units = 'metric') {
        return this.get(`${CONFIG.ENDPOINTS.WEATHER_FORECAST}?location=${encodeURIComponent(location)}&days=${days}&units=${units}`);
    }

    // News Services
    async getNewsHeadlines(country = 'us', category = null, pageSize = 20) {
        let url = `${CONFIG.ENDPOINTS.NEWS_HEADLINES}?country=${country}&page_size=${pageSize}`;
        if (category) {
            url += `&category=${category}`;
        }
        return this.get(url);
    }

    async searchNews(query, language = 'en', sortBy = 'publishedAt', pageSize = 20) {
        return this.get(`${CONFIG.ENDPOINTS.NEWS_SEARCH}?query=${encodeURIComponent(query)}&language=${language}&sort_by=${sortBy}&page_size=${pageSize}`);
    }

    // Music Services
    async searchMusic(query, type = 'track', limit = 20) {
        return this.get(`${CONFIG.ENDPOINTS.MUSIC_SEARCH}?query=${encodeURIComponent(query)}&type=${type}&limit=${limit}`);
    }

    async controlMusic(action, trackUri = null) {
        const endpoint = `${CONFIG.ENDPOINTS.MUSIC_CONTROL}/${action}`;
        const data = trackUri ? { track_uri: trackUri } : {};
        return this.post(endpoint, data);
    }

    // Conversations
    async getConversations(limit = 50) {
        return this.get(`${CONFIG.ENDPOINTS.CONVERSATIONS}?limit=${limit}`);
    }

    async getConversationMessages(sessionId, limit = 100) {
        return this.get(`${CONFIG.ENDPOINTS.CONVERSATIONS}/${sessionId}/messages?limit=${limit}`);
    }

    async addMessage(sessionId, messageType, content, confidenceScore = null, metadata = null) {
        return this.post(CONFIG.ENDPOINTS.CONVERSATIONS + '/messages', {
            session_id: sessionId,
            message_type: messageType,
            content,
            confidence_score: confidenceScore,
            metadata
        });
    }

    // Preferences
    async getPreferences() {
        return this.get(CONFIG.ENDPOINTS.PREFERENCES);
    }

    async setPreference(key, value, valueType = null) {
        return this.post(CONFIG.ENDPOINTS.PREFERENCES, {
            key,
            value,
            value_type: valueType
        });
    }

    async setPreferences(preferences) {
        return this.post(CONFIG.ENDPOINTS.PREFERENCES_BATCH, preferences);
    }

    async getPreference(key, defaultValue = null) {
        try {
            const response = await this.get(`${CONFIG.ENDPOINTS.PREFERENCES}/${key}`);
            return response.value;
        } catch (error) {
            return defaultValue;
        }
    }

    // System Status
    async getSystemStatus() {
        return this.get(CONFIG.ENDPOINTS.SYSTEM_STATUS);
    }

    // Utility Methods
    getDeviceInfo() {
        return {
            userAgent: navigator.userAgent,
            language: navigator.language,
            platform: navigator.platform,
            screen: {
                width: screen.width,
                height: screen.height
            },
            capabilities: CONFIG.CAPABILITIES
        };
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // WebSocket Connection
    createWebSocket(endpoint) {
        const wsUrl = this.baseURL.replace('http', 'ws') + endpoint;
        const ws = new WebSocket(wsUrl);
        
        ws.onopen = () => {
            if (CONFIG.DEBUG.ENABLED) {
                console.log('WebSocket connected:', endpoint);
            }
        };
        
        ws.onerror = (error) => {
            if (CONFIG.DEBUG.ENABLED) {
                console.error('WebSocket error:', error);
            }
        };
        
        ws.onclose = () => {
            if (CONFIG.DEBUG.ENABLED) {
                console.log('WebSocket disconnected:', endpoint);
            }
        };
        
        return ws;
    }

    // File Upload
    async uploadFile(file, endpoint) {
        const formData = new FormData();
        formData.append('file', file);
        
        const config = {
            method: 'POST',
            body: formData,
            headers: {}
        };
        
        // Add authentication
        const token = this.getAuthToken();
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${this.baseURL}${endpoint}`, config);
        
        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }
        
        return response.json();
    }
}

// Create global API instance
const nexaAPI = new NexaAPI();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NexaAPI;
} else {
    window.nexaAPI = nexaAPI;
}
