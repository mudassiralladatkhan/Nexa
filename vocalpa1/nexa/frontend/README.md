# Nexa Voice Assistant - Frontend

A modern, responsive web interface for the Nexa Voice Assistant, built with vanilla JavaScript and modern web technologies.

## 🚀 Features

### Core Functionality
- **Voice Recognition** - Browser-based speech recognition with wake word detection
- **Text-to-Speech** - Natural voice responses with configurable settings
- **Real-time Communication** - WebSocket connection to Python backend
- **Progressive Web App** - Installable with offline capabilities

### User Interface
- **Modern Design** - Clean, intuitive interface with Material Design principles
- **Responsive Layout** - Works seamlessly on desktop, tablet, and mobile
- **Dark/Light Theme** - Automatic theme switching with manual override
- **Smooth Animations** - Engaging visual feedback and transitions

### Voice Features
- **Wake Word Detection** - "Hey Nexa", "OK Nexa", custom wake words
- **Continuous Listening** - Always-on voice recognition (optional)
- **Voice Visualization** - Real-time audio waveforms and particles
- **Multi-language Support** - Configurable speech recognition languages

### Smart Commands
- **Natural Language** - Process commands in natural speech
- **Quick Actions** - One-tap shortcuts for common tasks
- **Command History** - Track and review past interactions
- **Context Awareness** - Maintain conversation context

## 📁 Project Structure

```
frontend/
├── index.html              # Main application HTML
├── manifest.json           # PWA manifest
├── sw.js                   # Service worker for offline functionality
├── css/
│   ├── styles.css          # Main stylesheet with CSS variables
│   └── animations.css      # Animation definitions and effects
└── js/
    ├── config.js           # Configuration and constants
    ├── api.js              # Backend API client
    ├── speech.js           # Speech recognition and synthesis
    ├── app.js              # Main application logic
    └── utils.js            # Utility functions
```

## 🛠️ Setup and Installation

### Prerequisites
- Modern web browser with speech recognition support
- Nexa Python backend running (see backend README)
- HTTPS connection (required for speech recognition)

### Local Development

1. **Start the Backend**
   ```bash
   cd ../backend
   python run.py
   ```

2. **Serve the Frontend**
   ```bash
   # Using Python's built-in server
   python -m http.server 3000
   
   # Or using Node.js
   npx serve . -p 3000
   
   # Or using any other static file server
   ```

3. **Access the Application**
   - Open https://localhost:3000 in your browser
   - Grant microphone permissions when prompted
   - The app will automatically connect to the backend

### Production Deployment

1. **Build for Production**
   - Minify CSS and JavaScript files
   - Optimize images and assets
   - Update backend URL in config.js

2. **Deploy to Static Hosting**
   ```bash
   # Deploy to Netlify
   netlify deploy --prod --dir .
   
   # Deploy to Vercel
   vercel --prod
   
   # Deploy to GitHub Pages
   # Push to gh-pages branch
   ```

3. **Configure HTTPS**
   - Ensure HTTPS is enabled (required for speech recognition)
   - Update CORS settings in backend for production domain

## ⚙️ Configuration

### Backend Connection
Edit `js/config.js` to configure the backend connection:

```javascript
CONFIG.BACKEND = {
    BASE_URL: 'https://your-backend-domain.com',
    // ... other settings
};
```

### Voice Settings
Customize voice recognition and synthesis:

```javascript
CONFIG.VOICE = {
    WAKE_WORDS: ['nexa', 'hey nexa', 'ok nexa'],
    LANGUAGE: 'en-US',
    CONTINUOUS_LISTENING: false,
    // ... other settings
};
```

### UI Customization
Modify themes and appearance:

```css
:root {
    --primary-color: #6366F1;
    --secondary-color: #10B981;
    /* ... other CSS variables */
}
```

## 🎤 Voice Commands

### Basic Commands
- **"Hey Nexa, what time is it?"** - Get current time
- **"Nexa, what's the weather like?"** - Weather information
- **"OK Nexa, play music"** - Music control
- **"Nexa, latest news"** - News headlines

### System Commands
- **"Open calculator"** - Launch applications
- **"Calculate 15 plus 27"** - Perform math
- **"Tell me a joke"** - Entertainment
- **"Help"** - Show available commands

### Settings Commands
- **"Turn on continuous listening"** - Voice settings
- **"Switch to dark theme"** - UI preferences
- **"Clear conversation history"** - Data management

## 🔧 API Integration

### Backend Communication
The frontend communicates with the Python backend via REST API:

```javascript
// Process voice command
const response = await nexaAPI.processCommand(text);

// Get weather information
const weather = await nexaAPI.getCurrentWeather('London');

// Control music playback
await nexaAPI.controlMusic('play');
```

### WebSocket Connection
Real-time features use WebSocket:

```javascript
// Voice streaming
const ws = nexaAPI.createWebSocket('/api/v1/voice/stream');
ws.send(JSON.stringify({ type: 'audio', data: audioData }));
```

## 📱 Progressive Web App

### Installation
- **Desktop**: Click install button in address bar
- **Mobile**: Add to home screen from browser menu
- **Automatic**: PWA install prompt appears after usage

### Offline Functionality
- **Core Features**: Basic UI and settings work offline
- **Cached Responses**: Recent commands cached for offline viewing
- **Background Sync**: Commands sync when connection restored

### Service Worker Features
- **Caching Strategy**: Static files cached, API responses cached temporarily
- **Background Sync**: Offline actions synced when online
- **Push Notifications**: Backend can send notifications (if configured)

## 🎨 Theming and Customization

### CSS Variables
The app uses CSS custom properties for easy theming:

```css
/* Light theme */
:root {
    --primary-color: #6366F1;
    --bg-primary: #FFFFFF;
    --text-primary: #1E293B;
}

/* Dark theme */
[data-theme="dark"] {
    --bg-primary: #0F172A;
    --text-primary: #F8FAFC;
}
```

### Animation Control
Animations can be disabled for accessibility:

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

## 🔒 Security and Privacy

### Permissions
- **Microphone**: Required for voice recognition
- **Notifications**: Optional for background alerts
- **Location**: Optional for location-based features

### Data Handling
- **Local Storage**: Preferences and settings stored locally
- **Session Data**: Conversation history stored temporarily
- **Privacy Mode**: Option to disable data collection

### HTTPS Requirement
- Speech recognition requires HTTPS connection
- Service worker requires secure context
- Production deployment must use SSL/TLS

## 🧪 Testing

### Browser Compatibility
- **Chrome/Edge**: Full feature support
- **Firefox**: Full feature support
- **Safari**: Limited speech recognition support
- **Mobile Browsers**: Touch-optimized interface

### Feature Detection
The app automatically detects browser capabilities:

```javascript
const capabilities = {
    speechRecognition: 'webkitSpeechRecognition' in window,
    speechSynthesis: 'speechSynthesis' in window,
    serviceWorker: 'serviceWorker' in navigator,
    // ... other features
};
```

### Debug Mode
Enable debug logging in `config.js`:

```javascript
CONFIG.DEBUG = {
    ENABLED: true,
    LOG_LEVEL: 'debug',
    LOG_API_CALLS: true,
    LOG_VOICE_EVENTS: true
};
```

## 🚀 Performance Optimization

### Loading Performance
- **Critical CSS**: Inline critical styles
- **Lazy Loading**: Load non-critical resources after initial render
- **Service Worker**: Cache static assets for faster subsequent loads

### Runtime Performance
- **Debouncing**: Prevent excessive API calls
- **Virtual Scrolling**: Handle large conversation histories
- **Memory Management**: Clean up event listeners and resources

### Bundle Size
- **No Framework**: Vanilla JavaScript keeps bundle small
- **Tree Shaking**: Only load required utilities
- **Compression**: Gzip/Brotli compression for production

## 🔧 Troubleshooting

### Common Issues

1. **Microphone Not Working**
   - Check browser permissions
   - Ensure HTTPS connection
   - Try different browser

2. **Backend Connection Failed**
   - Verify backend is running
   - Check CORS configuration
   - Confirm API endpoint URLs

3. **Speech Recognition Not Starting**
   - Grant microphone permissions
   - Check browser compatibility
   - Ensure secure context (HTTPS)

4. **Voice Synthesis Not Working**
   - Check browser support
   - Verify audio output device
   - Try different voice settings

### Debug Tools
- **Browser DevTools**: Check console for errors
- **Network Tab**: Monitor API requests
- **Application Tab**: Inspect service worker and storage

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review browser console for errors
- Ensure backend is properly configured
- Test with different browsers/devices

---

**Nexa Frontend** - Modern voice assistant interface powered by web technologies! 🎤✨
