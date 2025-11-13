// Nexa Voice Assistant - Simple Working App

class SimpleNexaApp {
    constructor() {
        this.backendUrl = 'http://localhost:8000';
        this.isConnected = false;
        this.init();
    }

    async init() {
        console.log('🚀 Initializing Nexa...');
        
        // Hide loading screen immediately and show main interface
        this.hideLoadingScreen();
        
        // Test backend connection
        await this.testConnection();
        
        // Initialize voice recognition
        this.initVoiceRecognition();
        
        console.log('✅ Nexa initialized');
    }

    hideLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        const mainContent = document.getElementById('main-content');
        
        if (loadingScreen) {
            loadingScreen.style.display = 'none';
        }
        
        if (mainContent) {
            mainContent.style.display = 'block';
        } else {
            // Create main content if it doesn't exist
            this.createMainInterface();
        }
    }

    createMainInterface() {
        const body = document.body;
        body.innerHTML = `
            <div id="main-content" style="
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-family: 'Inter', sans-serif;
                text-align: center;
                padding: 20px;
            ">
                <h1 style="font-size: 3em; margin-bottom: 20px;">🤖 Nexa</h1>
                <div id="status" style="
                    padding: 15px 30px;
                    background: rgba(255,255,255,0.2);
                    border-radius: 25px;
                    margin: 20px;
                    font-size: 1.1em;
                ">Testing connection...</div>
                
                <button id="micButton" style="
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                    background: #ff4757;
                    border: none;
                    color: white;
                    font-size: 2em;
                    cursor: pointer;
                    margin: 20px;
                    transition: all 0.3s ease;
                ">🎤</button>
                
                <div id="response" style="
                    max-width: 600px;
                    padding: 20px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 15px;
                    margin: 20px;
                    min-height: 60px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">Ready for voice commands!</div>
                
                <div style="margin: 20px;">
                    <button onclick="nexaApp.testCommand('hello nexa')" style="
                        background: rgba(255,255,255,0.2);
                        border: 1px solid rgba(255,255,255,0.3);
                        color: white;
                        padding: 10px 20px;
                        margin: 5px;
                        border-radius: 25px;
                        cursor: pointer;
                    ">Test Hello</button>
                    <button onclick="nexaApp.testCommand('what time is it')" style="
                        background: rgba(255,255,255,0.2);
                        border: 1px solid rgba(255,255,255,0.3);
                        color: white;
                        padding: 10px 20px;
                        margin: 5px;
                        border-radius: 25px;
                        cursor: pointer;
                    ">Test Time</button>
                </div>
            </div>
        `;

        // Add click handler for mic button
        document.getElementById('micButton').addEventListener('click', () => {
            this.toggleVoiceRecognition();
        });
    }

    async testConnection() {
        try {
            const response = await fetch(`${this.backendUrl}/health`);
            if (response.ok) {
                const data = await response.json();
                this.isConnected = true;
                this.updateStatus(`✅ Connected to backend! Status: ${data.status}`);
                console.log('✅ Backend connected:', data);
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            this.isConnected = false;
            this.updateStatus(`❌ Backend not connected: ${error.message}`);
            console.error('❌ Backend connection failed:', error);
        }
    }

    updateStatus(message) {
        const statusEl = document.getElementById('status');
        if (statusEl) {
            statusEl.textContent = message;
        }
    }

    initVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            this.recognition.onstart = () => {
                console.log('🎤 Voice recognition started');
                this.updateResponse('🎤 Listening...');
                const micBtn = document.getElementById('micButton');
                if (micBtn) micBtn.style.background = '#2ed573';
            };

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                console.log('👂 Heard:', transcript);
                this.updateResponse(`You said: "${transcript}"`);
                this.sendCommand(transcript);
            };

            this.recognition.onerror = (event) => {
                console.error('❌ Speech recognition error:', event.error);
                this.updateResponse(`Speech error: ${event.error}`);
                this.stopListening();
            };

            this.recognition.onend = () => {
                console.log('🔇 Voice recognition ended');
                this.stopListening();
            };

            console.log('✅ Voice recognition initialized');
        } else {
            console.warn('⚠️ Speech recognition not supported');
            this.updateResponse('Speech recognition not supported in this browser');
        }
    }

    toggleVoiceRecognition() {
        if (this.recognition) {
            if (this.isListening) {
                this.stopListening();
            } else {
                this.startListening();
            }
        }
    }

    startListening() {
        if (this.recognition && !this.isListening) {
            this.isListening = true;
            this.recognition.start();
        }
    }

    stopListening() {
        this.isListening = false;
        const micBtn = document.getElementById('micButton');
        if (micBtn) micBtn.style.background = '#ff4757';
        if (this.recognition) {
            this.recognition.stop();
        }
    }

    async sendCommand(command) {
        if (!this.isConnected) {
            this.updateResponse('❌ Backend not connected');
            return;
        }

        try {
            this.updateResponse('🔄 Processing...');
            
            const response = await fetch(`${this.backendUrl}/api/voice/command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command })
            });

            if (response.ok) {
                const data = await response.json();
                const responseText = data.response || 'Command processed successfully';
                this.updateResponse(responseText);
                
                // Text-to-speech
                if ('speechSynthesis' in window) {
                    const utterance = new SpeechSynthesisUtterance(responseText);
                    speechSynthesis.speak(utterance);
                }
                
                console.log('✅ Command processed:', data);
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.error('❌ Command error:', error);
            this.updateResponse(`❌ Error: ${error.message}`);
        }
    }

    testCommand(command) {
        console.log('🧪 Testing command:', command);
        this.updateResponse(`Testing: "${command}"`);
        this.sendCommand(command);
    }

    updateResponse(message) {
        const responseEl = document.getElementById('response');
        if (responseEl) {
            responseEl.textContent = message;
        }
    }
}

// Initialize the app
let nexaApp;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        nexaApp = new SimpleNexaApp();
    });
} else {
    nexaApp = new SimpleNexaApp();
}
