/**
 * Nexa Mobile - API Service
 * Handles communication with the Python backend
 */

import axios from 'axios';
import { StorageService } from './StorageService';

class ApiServiceClass {
  constructor() {
    this.baseURL = 'http://192.168.1.100:8000'; // Default local network IP
    this.timeout = 10000;
    this.retryAttempts = 3;
    this.retryDelay = 1000;
    
    // Request interceptors
    this.requestInterceptors = [];
    this.responseInterceptors = [];
    
    // Connection status
    this.isConnected = false;
    this.connectionListeners = [];
    
    // Axios instance
    this.client = null;
  }

  async initialize() {
    try {
      // Load backend URL from storage
      const savedUrl = await StorageService.getItem('backendUrl');
      if (savedUrl) {
        this.baseURL = savedUrl;
      }
      
      // Create axios instance
      this.client = axios.create({
        baseURL: this.baseURL,
        timeout: this.timeout,
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      // Set up request interceptor
      this.client.interceptors.request.use(
        (config) => {
          console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
          return config;
        },
        (error) => {
          console.error('Request interceptor error:', error);
          return Promise.reject(error);
        }
      );
      
      // Set up response interceptor
      this.client.interceptors.response.use(
        (response) => {
          console.log(`API Response: ${response.status} ${response.config.url}`);
          return response;
        },
        (error) => {
          console.error('Response interceptor error:', error);
          return Promise.reject(error);
        }
      );
      
      // Test initial connection
      await this.testConnection();
      
      console.log('API service initialized');
    } catch (error) {
      console.error('Failed to initialize API service:', error);
      throw error;
    }
  }

  // Connection Management
  async testConnection() {
    try {
      const response = await this.client.get('/health', { timeout: 5000 });
      this.setConnectionStatus(true);
      return response.status === 200;
    } catch (error) {
      console.error('Connection test failed:', error);
      this.setConnectionStatus(false);
      return false;
    }
  }

  setConnectionStatus(connected) {
    if (this.isConnected !== connected) {
      this.isConnected = connected;
      this.connectionListeners.forEach(listener => listener(connected));
      console.log(`Backend connection: ${connected ? 'Connected' : 'Disconnected'}`);
    }
  }

  onConnectionChange(listener) {
    this.connectionListeners.push(listener);
    // Call immediately with current status
    listener(this.isConnected);
  }

  setBaseURL(url) {
    this.baseURL = url;
    if (this.client) {
      this.client.defaults.baseURL = url;
    }
    // Save to storage
    StorageService.setItem('backendUrl', url);
  }

  // HTTP Methods with retry logic
  async request(method, endpoint, data = null, options = {}) {
    if (!this.client) {
      throw new Error('API service not initialized');
    }

    let lastError;
    
    // Retry logic
    for (let attempt = 0; attempt <= this.retryAttempts; attempt++) {
      try {
        const config = {
          method: method.toLowerCase(),
          url: endpoint,
          ...options,
        };

        if (data && (method.toLowerCase() === 'post' || method.toLowerCase() === 'put')) {
          config.data = data;
        }

        const response = await this.client.request(config);
        return response.data;

      } catch (error) {
        lastError = error;
        
        console.warn(`API Request failed (attempt ${attempt + 1}):`, error.message);

        // Don't retry on certain errors
        if (error.response?.status === 401 || error.response?.status === 403) {
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
  async login(userId = null, deviceType = 'mobile') {
    try {
      const response = await this.post('/api/v1/auth/login', {
        user_id: userId,
        device_type: deviceType,
        device_info: this.getDeviceInfo(),
      });
      
      if (response.success) {
        await StorageService.setItem('sessionToken', response.session_token);
        await StorageService.setItem('userId', response.user_id);
      }
      
      return response;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  }

  async logout() {
    try {
      await this.post('/api/v1/auth/logout');
    } catch (error) {
      console.warn('Logout request failed:', error);
    } finally {
      await StorageService.removeItem('sessionToken');
      await StorageService.removeItem('userId');
    }
  }

  // Command Processing
  async processCommand(text, metadata = {}) {
    try {
      const response = await this.post('/api/v1/commands/process', {
        text,
        locale: 'en-US',
        metadata: {
          platform: 'mobile',
          timestamp: new Date().toISOString(),
          ...metadata,
        },
      });
      
      return response;
    } catch (error) {
      console.error('Command processing failed:', error);
      throw error;
    }
  }

  async getCommandHistory(limit = 50) {
    try {
      return await this.get(`/api/v1/commands/history?limit=${limit}`);
    } catch (error) {
      console.error('Failed to get command history:', error);
      throw error;
    }
  }

  // Voice Services
  async recognizeSpeech(audioData, format = 'wav') {
    try {
      return await this.post('/api/v1/voice/recognize', {
        audio_data: audioData,
        format,
        language: 'en-US',
      });
    } catch (error) {
      console.error('Speech recognition failed:', error);
      throw error;
    }
  }

  async synthesizeSpeech(text, options = {}) {
    try {
      return await this.post('/api/v1/voice/synthesize', {
        text,
        voice: options.voice || null,
        speed: options.speed || 1.0,
        language: options.language || 'en-US',
      });
    } catch (error) {
      console.error('Speech synthesis failed:', error);
      throw error;
    }
  }

  // Weather Services
  async getCurrentWeather(location, units = 'metric') {
    try {
      return await this.get(`/api/v1/weather/current?location=${encodeURIComponent(location)}&units=${units}`);
    } catch (error) {
      console.error('Weather request failed:', error);
      throw error;
    }
  }

  async getWeatherForecast(location, days = 5, units = 'metric') {
    try {
      return await this.get(`/api/v1/weather/forecast?location=${encodeURIComponent(location)}&days=${days}&units=${units}`);
    } catch (error) {
      console.error('Weather forecast request failed:', error);
      throw error;
    }
  }

  // News Services
  async getNewsHeadlines(country = 'us', category = null, pageSize = 20) {
    try {
      let url = `/api/v1/news/headlines?country=${country}&page_size=${pageSize}`;
      if (category) {
        url += `&category=${category}`;
      }
      return await this.get(url);
    } catch (error) {
      console.error('News headlines request failed:', error);
      throw error;
    }
  }

  async searchNews(query, language = 'en', sortBy = 'publishedAt', pageSize = 20) {
    try {
      return await this.get(`/api/v1/news/search?query=${encodeURIComponent(query)}&language=${language}&sort_by=${sortBy}&page_size=${pageSize}`);
    } catch (error) {
      console.error('News search failed:', error);
      throw error;
    }
  }

  // Music Services
  async searchMusic(query, type = 'track', limit = 20) {
    try {
      return await this.get(`/api/v1/music/search?query=${encodeURIComponent(query)}&type=${type}&limit=${limit}`);
    } catch (error) {
      console.error('Music search failed:', error);
      throw error;
    }
  }

  async controlMusic(action, trackUri = null) {
    try {
      const endpoint = `/api/v1/music/control/${action}`;
      const data = trackUri ? { track_uri: trackUri } : {};
      return await this.post(endpoint, data);
    } catch (error) {
      console.error('Music control failed:', error);
      throw error;
    }
  }

  // Conversations
  async getConversations(limit = 50) {
    try {
      return await this.get(`/api/v1/conversations?limit=${limit}`);
    } catch (error) {
      console.error('Failed to get conversations:', error);
      throw error;
    }
  }

  async getConversationMessages(sessionId, limit = 100) {
    try {
      return await this.get(`/api/v1/conversations/${sessionId}/messages?limit=${limit}`);
    } catch (error) {
      console.error('Failed to get conversation messages:', error);
      throw error;
    }
  }

  async addMessage(sessionId, messageType, content, confidenceScore = null, metadata = null) {
    try {
      return await this.post('/api/v1/conversations/messages', {
        session_id: sessionId,
        message_type: messageType,
        content,
        confidence_score: confidenceScore,
        metadata,
      });
    } catch (error) {
      console.error('Failed to add message:', error);
      throw error;
    }
  }

  // Preferences
  async getPreferences() {
    try {
      return await this.get('/api/v1/preferences');
    } catch (error) {
      console.error('Failed to get preferences:', error);
      throw error;
    }
  }

  async setPreference(key, value, valueType = null) {
    try {
      return await this.post('/api/v1/preferences', {
        key,
        value,
        value_type: valueType,
      });
    } catch (error) {
      console.error('Failed to set preference:', error);
      throw error;
    }
  }

  async setPreferences(preferences) {
    try {
      return await this.post('/api/v1/preferences/batch', preferences);
    } catch (error) {
      console.error('Failed to set preferences:', error);
      throw error;
    }
  }

  // System Status
  async getSystemStatus() {
    try {
      return await this.get('/api/v1/status');
    } catch (error) {
      console.error('Failed to get system status:', error);
      throw error;
    }
  }

  // Utility Methods
  getDeviceInfo() {
    return {
      platform: 'react-native',
      userAgent: 'Nexa Mobile App',
      language: 'en-US',
      timestamp: new Date().toISOString(),
    };
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Health Check
  async healthCheck() {
    try {
      await this.get('/health');
      if (!this.isConnected) {
        this.setConnectionStatus(true);
      }
    } catch (error) {
      if (this.isConnected) {
        this.setConnectionStatus(false);
      }
    }
  }

  // Start periodic health checks
  startHealthCheck(interval = 30000) {
    setInterval(() => {
      this.healthCheck();
    }, interval);
  }
}

// Export singleton instance
export const ApiService = new ApiServiceClass();
