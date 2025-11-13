/**
 * Nexa Mobile - Voice Service
 * Handles speech recognition and text-to-speech
 */

import Voice from '@react-native-voice/voice';
import Tts from 'react-native-tts';
import { Platform, PermissionsAndroid } from 'react-native';

class VoiceServiceClass {
  constructor() {
    this.isInitialized = false;
    this.isListening = false;
    this.isSpeaking = false;
    
    // Configuration
    this.config = {
      language: 'en-US',
      wakeWords: ['nexa', 'hey nexa', 'ok nexa'],
      speechTimeout: 5000,
      silenceTimeout: 2000,
      continuous: false,
    };
    
    // Event listeners
    this.listeners = {
      speechStart: [],
      speechEnd: [],
      speechResults: [],
      speechError: [],
      speechPartialResults: [],
    };
  }

  async initialize() {
    try {
      // Request microphone permission
      if (Platform.OS === 'android') {
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,
          {
            title: 'Microphone Permission',
            message: 'Nexa needs access to your microphone for voice commands.',
            buttonNeutral: 'Ask Me Later',
            buttonNegative: 'Cancel',
            buttonPositive: 'OK',
          }
        );
        
        if (granted !== PermissionsAndroid.RESULTS.GRANTED) {
          throw new Error('Microphone permission denied');
        }
      }

      // Initialize Voice Recognition
      await this.initializeVoiceRecognition();
      
      // Initialize Text-to-Speech
      await this.initializeTextToSpeech();
      
      this.isInitialized = true;
      console.log('Voice service initialized successfully');
      
    } catch (error) {
      console.error('Failed to initialize voice service:', error);
      throw error;
    }
  }

  async initializeVoiceRecognition() {
    try {
      // Set up Voice recognition event handlers
      Voice.onSpeechStart = this.handleSpeechStart.bind(this);
      Voice.onSpeechEnd = this.handleSpeechEnd.bind(this);
      Voice.onSpeechResults = this.handleSpeechResults.bind(this);
      Voice.onSpeechPartialResults = this.handleSpeechPartialResults.bind(this);
      Voice.onSpeechError = this.handleSpeechError.bind(this);
      Voice.onSpeechRecognized = this.handleSpeechRecognized.bind(this);
      Voice.onSpeechVolumeChanged = this.handleSpeechVolumeChanged.bind(this);

      console.log('Voice recognition initialized');
    } catch (error) {
      console.error('Voice recognition initialization failed:', error);
      throw error;
    }
  }

  async initializeTextToSpeech() {
    try {
      // Initialize TTS
      await Tts.getInitStatus();
      
      // Set default TTS settings
      await Tts.setDefaultLanguage(this.config.language);
      await Tts.setDefaultRate(0.5);
      await Tts.setDefaultPitch(1.0);
      
      // Set up TTS event handlers
      Tts.addEventListener('tts-start', this.handleTtsStart.bind(this));
      Tts.addEventListener('tts-finish', this.handleTtsFinish.bind(this));
      Tts.addEventListener('tts-cancel', this.handleTtsCancel.bind(this));
      
      console.log('Text-to-speech initialized');
    } catch (error) {
      console.error('TTS initialization failed:', error);
      throw error;
    }
  }

  // Voice Recognition Methods
  async startListening() {
    if (!this.isInitialized) {
      throw new Error('Voice service not initialized');
    }
    
    if (this.isListening) {
      console.warn('Already listening');
      return;
    }

    try {
      // Stop any ongoing speech
      if (this.isSpeaking) {
        await this.stopSpeaking();
      }

      await Voice.start(this.config.language);
      this.isListening = true;
      console.log('Started listening');
    } catch (error) {
      console.error('Failed to start listening:', error);
      throw error;
    }
  }

  async stopListening() {
    if (!this.isListening) {
      return;
    }

    try {
      await Voice.stop();
      this.isListening = false;
      console.log('Stopped listening');
    } catch (error) {
      console.error('Failed to stop listening:', error);
      throw error;
    }
  }

  async cancelListening() {
    if (!this.isListening) {
      return;
    }

    try {
      await Voice.cancel();
      this.isListening = false;
      console.log('Cancelled listening');
    } catch (error) {
      console.error('Failed to cancel listening:', error);
      throw error;
    }
  }

  // Text-to-Speech Methods
  async speak(text, options = {}) {
    if (!this.isInitialized) {
      throw new Error('Voice service not initialized');
    }

    if (!text || text.trim().length === 0) {
      return;
    }

    try {
      // Stop any ongoing speech
      if (this.isSpeaking) {
        await Tts.stop();
      }

      // Stop listening while speaking
      if (this.isListening) {
        await this.stopListening();
      }

      const ttsOptions = {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: options.volume || 0.8,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
        iosVoiceId: options.iosVoiceId || '',
        rate: options.rate || 0.5,
        ...options,
      };

      await Tts.speak(text, ttsOptions);
      console.log('Speaking:', text);
    } catch (error) {
      console.error('Failed to speak:', error);
      throw error;
    }
  }

  async stopSpeaking() {
    if (!this.isSpeaking) {
      return;
    }

    try {
      await Tts.stop();
      this.isSpeaking = false;
      console.log('Stopped speaking');
    } catch (error) {
      console.error('Failed to stop speaking:', error);
      throw error;
    }
  }

  // Wake Word Detection
  checkWakeWord(text) {
    if (!text) return false;
    
    const lowerText = text.toLowerCase().trim();
    
    return this.config.wakeWords.some(wakeWord => {
      const lowerWakeWord = wakeWord.toLowerCase();
      
      // Exact match
      if (lowerText === lowerWakeWord) return true;
      
      // Contains wake word
      if (lowerText.includes(lowerWakeWord)) return true;
      
      // Starts with wake word
      if (lowerText.startsWith(lowerWakeWord)) return true;
      
      return false;
    });
  }

  // Event Handlers
  handleSpeechStart() {
    console.log('Speech started');
    this.emit('speechStart');
  }

  handleSpeechEnd() {
    console.log('Speech ended');
    this.isListening = false;
    this.emit('speechEnd');
  }

  handleSpeechResults(event) {
    console.log('Speech results:', event.value);
    
    if (event.value && event.value.length > 0) {
      const results = event.value.map(result => ({
        transcript: result,
        confidence: 0.9, // Android doesn't provide confidence scores
        isFinal: true,
      }));
      
      this.emit('speechResults', results);
    }
  }

  handleSpeechPartialResults(event) {
    console.log('Partial results:', event.value);
    
    if (event.value && event.value.length > 0) {
      const results = event.value.map(result => ({
        transcript: result,
        confidence: 0.8,
        isFinal: false,
      }));
      
      this.emit('speechPartialResults', results);
    }
  }

  handleSpeechError(event) {
    console.error('Speech error:', event.error);
    this.isListening = false;
    
    const error = {
      code: event.error?.code || 'unknown',
      message: this.getErrorMessage(event.error?.code || 'unknown'),
    };
    
    this.emit('speechError', error);
  }

  handleSpeechRecognized() {
    console.log('Speech recognized');
  }

  handleSpeechVolumeChanged(event) {
    // Handle volume changes for voice visualization
    this.emit('volumeChanged', event.value);
  }

  handleTtsStart() {
    console.log('TTS started');
    this.isSpeaking = true;
  }

  handleTtsFinish() {
    console.log('TTS finished');
    this.isSpeaking = false;
  }

  handleTtsCancel() {
    console.log('TTS cancelled');
    this.isSpeaking = false;
  }

  // Configuration Methods
  setLanguage(language) {
    this.config.language = language;
    Tts.setDefaultLanguage(language);
  }

  setWakeWords(wakeWords) {
    this.config.wakeWords = wakeWords;
  }

  setSpeechRate(rate) {
    Tts.setDefaultRate(rate);
  }

  // Event Management
  on(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event].push(callback);
    }
  }

  off(event, callback) {
    if (this.listeners[event]) {
      const index = this.listeners[event].indexOf(callback);
      if (index > -1) {
        this.listeners[event].splice(index, 1);
      }
    }
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in ${event} listener:`, error);
        }
      });
    }
  }

  // Convenience methods for event listeners
  onSpeechStart(callback) {
    this.on('speechStart', callback);
  }

  onSpeechEnd(callback) {
    this.on('speechEnd', callback);
  }

  onSpeechResults(callback) {
    this.on('speechResults', callback);
  }

  onSpeechError(callback) {
    this.on('speechError', callback);
  }

  onSpeechPartialResults(callback) {
    this.on('speechPartialResults', callback);
  }

  onVolumeChanged(callback) {
    this.on('volumeChanged', callback);
  }

  // Utility Methods
  getErrorMessage(errorCode) {
    const errorMessages = {
      '1': 'Network timeout',
      '2': 'Network error',
      '3': 'Audio recording error',
      '4': 'Server error',
      '5': 'Client error',
      '6': 'Speech timeout',
      '7': 'No match found',
      '8': 'Recognition service busy',
      '9': 'Insufficient permissions',
      'unknown': 'Unknown error occurred',
    };
    
    return errorMessages[errorCode] || errorMessages['unknown'];
  }

  getStatus() {
    return {
      isInitialized: this.isInitialized,
      isListening: this.isListening,
      isSpeaking: this.isSpeaking,
      config: this.config,
    };
  }

  // Cleanup
  cleanup() {
    try {
      if (this.isListening) {
        Voice.cancel();
      }
      
      if (this.isSpeaking) {
        Tts.stop();
      }
      
      // Remove event listeners
      Voice.removeAllListeners();
      Tts.removeAllListeners();
      
      // Clear internal listeners
      Object.keys(this.listeners).forEach(event => {
        this.listeners[event] = [];
      });
      
      this.isInitialized = false;
      console.log('Voice service cleaned up');
    } catch (error) {
      console.error('Cleanup error:', error);
    }
  }
}

// Export singleton instance
export const VoiceService = new VoiceServiceClass();
