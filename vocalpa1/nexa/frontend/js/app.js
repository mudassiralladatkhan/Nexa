// Nexa Voice Assistant - Main Application

class NexaApp {
    constructor() {
        this.isInitialized = false;
        this.currentSessionId = null;
        this.conversationHistory = [];
        this.isProcessing = false;
        
        // UI Elements
        this.elements = {};
        
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    async init() {
        try {
            // Initialize UI elements
            this.initElements();
            
            // Initialize services
            await this.initServices();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Load user preferences
            await this.loadPreferences();
            
            // Initialize session
            await this.initSession();
            
            // Hide loading screen and show app
            this.showApp();
            
            this.isInitialized = true;
            console.log('Nexa app initialized successfully');
            
        } catch (error) {
            console.error('Failed to initialize Nexa app:', error);
            this.showError('Failed to initialize the application', error.message);
        }
    }

    initElements() {
        // Cache DOM elements
        this.elements = {
            loadingScreen: document.getElementById('loading-screen'),
            app: document.getElementById('app'),
            
            // Header elements
            connectionStatus: document.getElementById('connection-status'),
            themeToggle: document.getElementById('theme-toggle'),
            settingsBtn: document.getElementById('settings-btn'),
            
            // Main content
            statusText: document.getElementById('status-text'),
            micButton: document.getElementById('mic-button'),
            soundWaves: document.getElementById('sound-waves'),
            particles: document.getElementById('particles'),
            voiceCanvas: document.getElementById('voice-canvas'),
            
            // Quick actions
            quickActions: document.querySelectorAll('.quick-action'),
            
            // Conversation
            conversationHistory: document.getElementById('conversation-history'),
            conversationMessages: document.getElementById('conversation-messages'),
            clearHistory: document.getElementById('clear-history'),
            
            // Settings panel
            settingsPanel: document.getElementById('settings-panel'),
            closeSettings: document.getElementById('close-settings'),
            
            // Settings controls
            wakeWordToggle: document.getElementById('wake-word-toggle'),
            continuousListening: document.getElementById('continuous-listening'),
            voiceFeedback: document.getElementById('voice-feedback'),
            speechRate: document.getElementById('speech-rate'),
            backendUrl: document.getElementById('backend-url'),
            testConnection: document.getElementById('test-connection'),
            themeSelect: document.getElementById('theme-select'),
            animationsToggle: document.getElementById('animations-toggle'),
            saveConversations: document.getElementById('save-conversations'),
            clearAllData: document.getElementById('clear-all-data'),
            
            // Status bar
            statusMessage: document.getElementById('status-message'),
            micStatus: document.getElementById('mic-status'),
            backendStatus: document.getElementById('backend-status'),
            
            // Error modal
            errorModal: document.getElementById('error-modal'),
            errorMessage: document.getElementById('error-message'),
            closeError: document.getElementById('close-error'),
            errorOk: document.getElementById('error-ok')
        };
    }

    async initServices() {
        // Initialize API connection
        nexaAPI.onConnectionChange((connected) => {
            this.updateConnectionStatus(connected);
        });
        
        // Initialize speech services
        nexaSpeech.on('start', () => this.onSpeechStart());
        nexaSpeech.on('end', () => this.onSpeechEnd());
        nexaSpeech.on('result', (results) => this.onSpeechResult(results));
        nexaSpeech.on('error', (error) => this.onSpeechError(error));
        nexaSpeech.on('speechStart', () => this.onSpeechDetected());
        nexaSpeech.on('speechEnd', () => this.onSpeechStopped());
        
        // Test backend connection
        try {
            await nexaAPI.testConnection();
        } catch (error) {
            console.warn('Backend connection failed:', error);
        }
    }

    setupEventListeners() {
        // Microphone button
        this.elements.micButton?.addEventListener('click', () => this.toggleListening());
        
        // Quick actions
        this.elements.quickActions?.forEach(button => {
            button.addEventListener('click', (e) => {
                const action = e.currentTarget.dataset.action;
                this.handleQuickAction(action);
            });
        });
        
        // Theme toggle
        this.elements.themeToggle?.addEventListener('click', () => this.toggleTheme());
        
        // Settings
        this.elements.settingsBtn?.addEventListener('click', () => this.showSettings());
        this.elements.closeSettings?.addEventListener('click', () => this.hideSettings());
        
        // Settings controls
        this.elements.testConnection?.addEventListener('click', () => this.testConnection());
        this.elements.clearHistory?.addEventListener('click', () => this.clearConversationHistory());
        this.elements.clearAllData?.addEventListener('click', () => this.clearAllData());
        
        // Speech rate slider
        this.elements.speechRate?.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            CONFIG.TTS.RATE = value;
            const valueSpan = e.target.nextElementSibling;
            if (valueSpan) {
                valueSpan.textContent = `${value}x`;
            }
        });
        
        // Error modal
        this.elements.closeError?.addEventListener('click', () => this.hideError());
        this.elements.errorOk?.addEventListener('click', () => this.hideError());
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
        
        // Click outside to close settings
        document.addEventListener('click', (e) => {
            if (this.elements.settingsPanel?.classList.contains('visible') && 
                !this.elements.settingsPanel.contains(e.target) &&
                !this.elements.settingsBtn?.contains(e.target)) {
                this.hideSettings();
            }
        });
    }

    async loadPreferences() {
        try {
            const preferences = await nexaAPI.getPreferences();
            
            // Apply preferences to UI
            if (preferences.theme) {
                this.setTheme(preferences.theme);
            }
            
            if (preferences.wake_word_enabled !== undefined) {
                this.elements.wakeWordToggle.checked = preferences.wake_word_enabled;
            }
            
            if (preferences.continuous_listening !== undefined) {
                this.elements.continuousListening.checked = preferences.continuous_listening;
                CONFIG.VOICE.CONTINUOUS_LISTENING = preferences.continuous_listening;
            }
            
            if (preferences.voice_feedback !== undefined) {
                this.elements.voiceFeedback.checked = preferences.voice_feedback;
            }
            
            if (preferences.speech_rate) {
                CONFIG.TTS.RATE = preferences.speech_rate;
                this.elements.speechRate.value = preferences.speech_rate;
            }
            
        } catch (error) {
            console.warn('Failed to load preferences:', error);
        }
    }

    async initSession() {
        try {
            // Generate session ID
            this.currentSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            
            // Login to backend
            const userId = localStorage.getItem(CONFIG.STORAGE_KEYS.USER_ID) || null;
            await nexaAPI.login(userId, 'web');
            
            // Load conversation history
            await this.loadConversationHistory();
            
        } catch (error) {
            console.warn('Session initialization failed:', error);
        }
    }

    showApp() {
        setTimeout(() => {
            this.elements.loadingScreen?.classList.add('hidden');
            this.elements.app?.classList.remove('hidden');
        }, 1000);
    }

    // Speech Event Handlers
    onSpeechStart() {
        this.elements.micButton?.classList.add('listening');
        this.elements.soundWaves?.classList.remove('hidden');
        this.elements.soundWaves?.classList.add('active');
        this.updateStatus('Listening...');
        this.elements.micStatus?.classList.remove('mic-off');
        this.elements.micStatus?.classList.add('mic-on');
    }

    onSpeechEnd() {
        this.elements.micButton?.classList.remove('listening');
        this.elements.soundWaves?.classList.add('hidden');
        this.elements.soundWaves?.classList.remove('active');
        this.updateStatus('Ready');
        this.elements.micStatus?.classList.add('mic-off');
        this.elements.micStatus?.classList.remove('mic-on');
    }

    onSpeechDetected() {
        // Visual feedback for speech detection
        this.elements.particles?.classList.remove('hidden');
        this.createParticles();
    }

    onSpeechStopped() {
        this.elements.particles?.classList.add('hidden');
    }

    async onSpeechResult(results) {
        for (const result of results) {
            if (result.isFinal && result.transcript.length > 0) {
                await this.processCommand(result.transcript, result.confidence);
            }
        }
    }

    onSpeechError(error) {
        console.error('Speech error:', error);
        this.elements.micButton?.classList.remove('listening');
        this.elements.micButton?.classList.add('error');
        
        setTimeout(() => {
            this.elements.micButton?.classList.remove('error');
        }, 1000);
        
        this.updateStatus(`Error: ${error.message}`);
        this.showError('Speech Recognition Error', error.message);
    }

    // Command Processing
    async processCommand(text, confidence = 1.0) {
        if (this.isProcessing) return;
        
        this.isProcessing = true;
        this.updateStatus('Processing...');
        
        try {
            // Add user message to conversation
            this.addMessage('user', text, confidence);
            
            // Send to backend
            const response = await nexaAPI.processCommand(text, {
                confidence,
                sessionId: this.currentSessionId,
                timestamp: new Date().toISOString()
            });
            
            // Add assistant response
            this.addMessage('assistant', response.response_text);
            
            // Speak response if voice feedback is enabled
            if (this.elements.voiceFeedback?.checked && response.response_text) {
                await nexaSpeech.speak(response.response_text);
            }
            
            this.updateStatus('Ready');
            
        } catch (error) {
            console.error('Command processing failed:', error);
            this.addMessage('assistant', 'Sorry, I had trouble processing that command.');
            this.updateStatus('Error');
            this.showError('Command Processing Error', error.message);
        } finally {
            this.isProcessing = false;
        }
    }

    // UI Methods
    toggleListening() {
        if (nexaSpeech.isListening) {
            nexaSpeech.stopListening();
        } else {
            nexaSpeech.startListening();
        }
    }

    handleQuickAction(action) {
        const actionConfig = CONFIG.QUICK_ACTIONS.find(a => a.id === action);
        if (actionConfig) {
            this.processCommand(actionConfig.command);
        }
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        
        // Update theme toggle icon
        const icon = this.elements.themeToggle?.querySelector('i');
        if (icon) {
            icon.textContent = theme === 'dark' ? 'light_mode' : 'dark_mode';
        }
        
        // Save preference
        nexaAPI.setPreference('theme', theme);
    }

    showSettings() {
        this.elements.settingsPanel?.classList.add('visible');
    }

    hideSettings() {
        this.elements.settingsPanel?.classList.remove('visible');
    }

    updateStatus(message) {
        if (this.elements.statusText) {
            this.elements.statusText.textContent = message;
        }
        if (this.elements.statusMessage) {
            this.elements.statusMessage.textContent = message;
        }
    }

    updateConnectionStatus(connected) {
        const statusElement = this.elements.connectionStatus;
        const backendStatus = this.elements.backendStatus;
        
        if (connected) {
            statusElement?.classList.remove('disconnected');
            statusElement?.classList.add('connected');
            statusElement?.querySelector('i').textContent = 'cloud_done';
            
            backendStatus?.classList.remove('offline');
            backendStatus?.classList.add('online');
            backendStatus?.querySelector('i').textContent = 'cloud_done';
        } else {
            statusElement?.classList.remove('connected');
            statusElement?.classList.add('disconnected');
            statusElement?.querySelector('i').textContent = 'cloud_off';
            
            backendStatus?.classList.remove('online');
            backendStatus?.classList.add('offline');
            backendStatus?.querySelector('i').textContent = 'cloud_off';
        }
    }

    // Conversation Management
    addMessage(type, content, confidence = null) {
        const message = {
            type,
            content,
            confidence,
            timestamp: new Date()
        };
        
        this.conversationHistory.push(message);
        this.renderMessage(message);
        
        // Save to backend
        if (this.elements.saveConversations?.checked) {
            nexaAPI.addMessage(
                this.currentSessionId,
                type,
                content,
                confidence,
                { timestamp: message.timestamp.toISOString() }
            ).catch(error => console.warn('Failed to save message:', error));
        }
        
        // Show conversation history if hidden
        if (this.elements.conversationHistory?.classList.contains('hidden')) {
            this.elements.conversationHistory?.classList.remove('hidden');
        }
        
        // Scroll to bottom
        this.scrollToBottom();
    }

    renderMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${message.type}`;
        
        messageElement.innerHTML = `
            <div class="message-content">
                <p>${this.escapeHtml(message.content)}</p>
                <div class="message-time">${message.timestamp.toLocaleTimeString()}</div>
            </div>
        `;
        
        this.elements.conversationMessages?.appendChild(messageElement);
    }

    async loadConversationHistory() {
        try {
            const conversations = await nexaAPI.getConversations(1);
            if (conversations.length > 0) {
                const messages = await nexaAPI.getConversationMessages(conversations[0].session_id);
                
                messages.forEach(msg => {
                    this.conversationHistory.push({
                        type: msg.message_type,
                        content: msg.content,
                        confidence: msg.confidence_score,
                        timestamp: new Date(msg.timestamp)
                    });
                    this.renderMessage(this.conversationHistory[this.conversationHistory.length - 1]);
                });
                
                if (messages.length > 0) {
                    this.elements.conversationHistory?.classList.remove('hidden');
                }
            }
        } catch (error) {
            console.warn('Failed to load conversation history:', error);
        }
    }

    clearConversationHistory() {
        this.conversationHistory = [];
        if (this.elements.conversationMessages) {
            this.elements.conversationMessages.innerHTML = '';
        }
        this.elements.conversationHistory?.classList.add('hidden');
    }

    scrollToBottom() {
        if (this.elements.conversationMessages) {
            this.elements.conversationMessages.scrollTop = this.elements.conversationMessages.scrollHeight;
        }
    }

    // Utility Methods
    createParticles() {
        const particlesContainer = this.elements.particles;
        if (!particlesContainer) return;
        
        // Clear existing particles
        particlesContainer.innerHTML = '';
        
        // Create new particles
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Random position around the microphone
            const angle = (Math.PI * 2 * i) / 20;
            const radius = 50 + Math.random() * 100;
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;
            
            particle.style.left = `calc(50% + ${x}px)`;
            particle.style.top = `calc(50% + ${y}px)`;
            particle.style.animationDelay = `${Math.random() * 2}s`;
            
            particlesContainer.appendChild(particle);
        }
    }

    async testConnection() {
        const button = this.elements.testConnection;
        const result = this.elements.connectionResult;
        
        if (!button || !result) return;
        
        button.disabled = true;
        button.textContent = 'Testing...';
        result.textContent = '';
        
        try {
            await nexaAPI.testConnection();
            result.textContent = '✅ Connected successfully';
            result.style.color = 'var(--secondary-color)';
        } catch (error) {
            result.textContent = `❌ Connection failed: ${error.message}`;
            result.style.color = 'var(--danger-color)';
        } finally {
            button.disabled = false;
            button.textContent = 'Test Connection';
        }
    }

    clearAllData() {
        if (confirm('Are you sure you want to clear all data? This cannot be undone.')) {
            // Clear local storage
            Object.values(CONFIG.STORAGE_KEYS).forEach(key => {
                localStorage.removeItem(key);
            });
            
            // Clear conversation history
            this.clearConversationHistory();
            
            // Reload page
            window.location.reload();
        }
    }

    handleKeyboard(event) {
        // Space bar to toggle listening
        if (event.code === 'Space' && !event.target.matches('input, textarea')) {
            event.preventDefault();
            this.toggleListening();
        }
        
        // Escape to stop listening
        if (event.code === 'Escape') {
            nexaSpeech.stopListening();
            this.hideSettings();
            this.hideError();
        }
    }

    showError(title, message) {
        if (this.elements.errorModal && this.elements.errorMessage) {
            this.elements.errorMessage.textContent = message;
            this.elements.errorModal.classList.remove('hidden');
        }
    }

    hideError() {
        this.elements.errorModal?.classList.add('hidden');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app
const nexaApp = new NexaApp();

// Export for debugging
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NexaApp;
} else {
    window.nexaApp = nexaApp;
}
