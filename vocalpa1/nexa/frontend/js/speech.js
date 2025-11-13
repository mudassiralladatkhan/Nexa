// Nexa Voice Assistant - Speech Recognition and Synthesis

class NexaSpeech {
    constructor() {
        this.recognition = null;
        this.synthesis = null;
        this.isListening = false;
        this.isSpeaking = false;
        this.isInitialized = false;
        
        // Event listeners
        this.listeners = {
            start: [],
            end: [],
            result: [],
            error: [],
            speechStart: [],
            speechEnd: []
        };
        
        // Configuration
        this.config = {
            language: CONFIG.VOICE.LANGUAGE,
            continuous: CONFIG.VOICE.CONTINUOUS_LISTENING,
            interimResults: CONFIG.VOICE.INTERIM_RESULTS,
            maxAlternatives: CONFIG.VOICE.MAX_ALTERNATIVES
        };
        
        // Wake word detection
        this.wakeWords = CONFIG.VOICE.WAKE_WORDS;
        this.wakeWordDetected = false;
        
        // Initialize
        this.init();
    }

    async init() {
        try {
            await this.initSpeechRecognition();
            await this.initSpeechSynthesis();
            this.isInitialized = true;
            
            if (CONFIG.DEBUG.ENABLED) {
                console.log('Speech services initialized successfully');
            }
        } catch (error) {
            console.error('Failed to initialize speech services:', error);
            throw error;
        }
    }

    async initSpeechRecognition() {
        if (!CONFIG.CAPABILITIES.SPEECH_RECOGNITION) {
            throw new Error('Speech recognition not supported');
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Configure recognition
        this.recognition.continuous = this.config.continuous;
        this.recognition.interimResults = this.config.interimResults;
        this.recognition.lang = this.config.language;
        this.recognition.maxAlternatives = this.config.maxAlternatives;

        // Event handlers
        this.recognition.onstart = () => {
            this.isListening = true;
            this.emit('start');
            
            if (CONFIG.DEBUG.LOG_VOICE_EVENTS) {
                console.log('Speech recognition started');
            }
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.emit('end');
            
            if (CONFIG.DEBUG.LOG_VOICE_EVENTS) {
                console.log('Speech recognition ended');
            }
        };

        this.recognition.onresult = (event) => {
            const results = [];
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const result = event.results[i];
                const transcript = result[0].transcript;
                const confidence = result[0].confidence;
                const isFinal = result.isFinal;
                
                results.push({
                    transcript: transcript.trim(),
                    confidence: confidence || 0.9,
                    isFinal,
                    alternatives: Array.from(result).map(alt => ({
                        transcript: alt.transcript.trim(),
                        confidence: alt.confidence || 0.9
                    }))
                });
                
                if (CONFIG.DEBUG.LOG_VOICE_EVENTS) {
                    console.log(`Speech result: "${transcript}" (confidence: ${confidence}, final: ${isFinal})`);
                }
            }
            
            // Check for wake words
            results.forEach(result => {
                if (this.checkWakeWord(result.transcript)) {
                    this.wakeWordDetected = true;
                    if (CONFIG.DEBUG.LOG_VOICE_EVENTS) {
                        console.log('Wake word detected:', result.transcript);
                    }
                }
            });
            
            this.emit('result', results);
        };

        this.recognition.onerror = (event) => {
            const error = {
                error: event.error,
                message: this.getErrorMessage(event.error)
            };
            
            console.error('Speech recognition error:', error);
            this.emit('error', error);
        };

        this.recognition.onspeechstart = () => {
            this.emit('speechStart');
        };

        this.recognition.onspeechend = () => {
            this.emit('speechEnd');
        };
    }

    async initSpeechSynthesis() {
        if (!CONFIG.CAPABILITIES.SPEECH_SYNTHESIS) {
            throw new Error('Speech synthesis not supported');
        }

        this.synthesis = window.speechSynthesis;
        
        // Wait for voices to load
        return new Promise((resolve) => {
            const loadVoices = () => {
                const voices = this.synthesis.getVoices();
                if (voices.length > 0) {
                    // Set default voice
                    const defaultVoice = voices.find(voice => 
                        voice.lang.startsWith(CONFIG.TTS.LANGUAGE.split('-')[0]) && voice.default
                    ) || voices[0];
                    
                    CONFIG.TTS.VOICE = defaultVoice;
                    resolve();
                } else {
                    // Voices not loaded yet, try again
                    setTimeout(loadVoices, 100);
                }
            };
            
            if (this.synthesis.onvoiceschanged !== undefined) {
                this.synthesis.onvoiceschanged = loadVoices;
            }
            
            loadVoices();
        });
    }

    // Speech Recognition Methods
    startListening() {
        if (!this.isInitialized) {
            throw new Error('Speech services not initialized');
        }
        
        if (this.isListening) {
            if (CONFIG.DEBUG.LOG_VOICE_EVENTS) {
                console.warn('Already listening');
            }
            return;
        }

        try {
            this.recognition.start();
        } catch (error) {
            console.error('Failed to start listening:', error);
            throw error;
        }
    }

    stopListening() {
        if (this.isListening && this.recognition) {
            this.recognition.stop();
        }
    }

    abortListening() {
        if (this.isListening && this.recognition) {
            this.recognition.abort();
        }
    }

    // Speech Synthesis Methods
    speak(text, options = {}) {
        if (!this.isInitialized) {
            throw new Error('Speech services not initialized');
        }

        return new Promise((resolve, reject) => {
            if (this.isSpeaking) {
                this.synthesis.cancel();
            }

            const utterance = new SpeechSynthesisUtterance(text);
            
            // Configure utterance
            utterance.voice = options.voice || CONFIG.TTS.VOICE;
            utterance.rate = options.rate || CONFIG.TTS.RATE;
            utterance.pitch = options.pitch || CONFIG.TTS.PITCH;
            utterance.volume = options.volume || CONFIG.TTS.VOLUME;
            utterance.lang = options.language || CONFIG.TTS.LANGUAGE;

            // Event handlers
            utterance.onstart = () => {
                this.isSpeaking = true;
                this.emit('speechStart');
                
                if (CONFIG.DEBUG.LOG_VOICE_EVENTS) {
                    console.log('Speech synthesis started:', text);
                }
            };

            utterance.onend = () => {
                this.isSpeaking = false;
                this.emit('speechEnd');
                resolve();
                
                if (CONFIG.DEBUG.LOG_VOICE_EVENTS) {
                    console.log('Speech synthesis ended');
                }
            };

            utterance.onerror = (event) => {
                this.isSpeaking = false;
                const error = new Error(`Speech synthesis error: ${event.error}`);
                console.error(error);
                reject(error);
            };

            // Speak
            this.synthesis.speak(utterance);
        });
    }

    stopSpeaking() {
        if (this.isSpeaking && this.synthesis) {
            this.synthesis.cancel();
            this.isSpeaking = false;
        }
    }

    pauseSpeaking() {
        if (this.isSpeaking && this.synthesis) {
            this.synthesis.pause();
        }
    }

    resumeSpeaking() {
        if (this.synthesis && this.synthesis.paused) {
            this.synthesis.resume();
        }
    }

    // Wake Word Detection
    checkWakeWord(text) {
        const lowerText = text.toLowerCase().trim();
        
        return this.wakeWords.some(wakeWord => {
            const lowerWakeWord = wakeWord.toLowerCase();
            
            // Exact match
            if (lowerText === lowerWakeWord) return true;
            
            // Contains wake word
            if (lowerText.includes(lowerWakeWord)) return true;
            
            // Starts with wake word
            if (lowerText.startsWith(lowerWakeWord)) return true;
            
            // Fuzzy match (simple similarity)
            const similarity = this.calculateSimilarity(lowerText, lowerWakeWord);
            return similarity > 0.8;
        });
    }

    calculateSimilarity(str1, str2) {
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;
        
        if (longer.length === 0) return 1.0;
        
        const distance = this.levenshteinDistance(longer, shorter);
        return (longer.length - distance) / longer.length;
    }

    levenshteinDistance(str1, str2) {
        const matrix = [];
        
        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }
        
        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }
        
        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }
        
        return matrix[str2.length][str1.length];
    }

    // Configuration Methods
    setLanguage(language) {
        this.config.language = language;
        if (this.recognition) {
            this.recognition.lang = language;
        }
    }

    setContinuous(continuous) {
        this.config.continuous = continuous;
        if (this.recognition) {
            this.recognition.continuous = continuous;
        }
    }

    setInterimResults(interimResults) {
        this.config.interimResults = interimResults;
        if (this.recognition) {
            this.recognition.interimResults = interimResults;
        }
    }

    setWakeWords(wakeWords) {
        this.wakeWords = wakeWords;
    }

    // Voice Management
    getVoices() {
        return this.synthesis ? this.synthesis.getVoices() : [];
    }

    setVoice(voice) {
        CONFIG.TTS.VOICE = voice;
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

    // Utility Methods
    getErrorMessage(errorCode) {
        const errorMessages = {
            'no-speech': 'No speech was detected',
            'aborted': 'Speech recognition was aborted',
            'audio-capture': 'Audio capture failed',
            'network': 'Network error occurred',
            'not-allowed': 'Microphone permission denied',
            'service-not-allowed': 'Speech recognition service not allowed',
            'bad-grammar': 'Grammar error',
            'language-not-supported': 'Language not supported'
        };
        
        return errorMessages[errorCode] || `Unknown error: ${errorCode}`;
    }

    // Status Methods
    getStatus() {
        return {
            isInitialized: this.isInitialized,
            isListening: this.isListening,
            isSpeaking: this.isSpeaking,
            wakeWordDetected: this.wakeWordDetected,
            capabilities: {
                speechRecognition: CONFIG.CAPABILITIES.SPEECH_RECOGNITION,
                speechSynthesis: CONFIG.CAPABILITIES.SPEECH_SYNTHESIS
            },
            config: this.config
        };
    }

    // Cleanup
    destroy() {
        this.stopListening();
        this.stopSpeaking();
        
        if (this.recognition) {
            this.recognition = null;
        }
        
        this.listeners = {
            start: [],
            end: [],
            result: [],
            error: [],
            speechStart: [],
            speechEnd: []
        };
        
        this.isInitialized = false;
    }
}

// Create global speech instance
const nexaSpeech = new NexaSpeech();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NexaSpeech;
} else {
    window.nexaSpeech = nexaSpeech;
}
