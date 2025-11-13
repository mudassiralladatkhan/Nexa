# Nexa Voice Assistant - Mobile App

A React Native mobile application for the Nexa Voice Assistant, providing native voice recognition, text-to-speech, and seamless integration with the Python backend.

## 🚀 Features

### Core Functionality
- **Native Voice Recognition** - Real-time speech-to-text using device capabilities
- **Text-to-Speech** - Natural voice responses with configurable settings
- **Backend Integration** - Full API integration with Python Nexa backend
- **Offline Capabilities** - Local storage and cached responses

### Mobile-Optimized UI
- **Modern Design** - Clean, intuitive interface optimized for mobile
- **Voice Visualizer** - Real-time audio waveforms and visual feedback
- **Quick Actions** - One-tap shortcuts for common voice commands
- **Responsive Layout** - Adapts to different screen sizes and orientations

### Smart Features
- **Wake Word Detection** - "Hey Nexa", "OK Nexa", custom wake words
- **Continuous Listening** - Always-on voice recognition (optional)
- **Conversation History** - Track and review past interactions
- **Settings Management** - Comprehensive configuration options

## 📱 Screenshots

```
[Home Screen]     [Voice Active]    [Settings]       [Conversation]
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│    Nexa     │   │    Nexa     │   │  Settings   │   │Conversation │
│             │   │             │   │             │   │             │
│  ╭─────╮    │   │  ╭~~~~~╮    │   │ ○ Wake Word │   │ User: Hi    │
│  │ 🎤  │    │   │  │ 🎤~ │    │   │ ○ Voice FB  │   │ Nexa: Hello │
│  ╰─────╯    │   │  ╰~~~~~╯    │   │ ○ Language  │   │ User: Time? │
│             │   │ ~~~Waves~~~ │   │ ○ Backend   │   │ Nexa: 3:45  │
│ [Weather]   │   │             │   │             │   │             │
│ [News] [♪]  │   │ Listening.. │   │   [Save]    │   │ [Clear All] │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
```

## 🛠️ Setup and Installation

### Prerequisites
- **Node.js** (v16 or higher)
- **React Native CLI** or **Expo CLI**
- **Android Studio** (for Android development)
- **Xcode** (for iOS development, macOS only)
- **Nexa Python Backend** running

### Installation Steps

1. **Clone and Navigate**
   ```bash
   cd nexa/mobile
   ```

2. **Install Dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Install iOS Dependencies** (iOS only)
   ```bash
   cd ios && pod install && cd ..
   ```

4. **Configure Backend URL**
   
   Edit `src/services/ApiService.js`:
   ```javascript
   // Replace with your backend IP address
   this.baseURL = 'http://YOUR_BACKEND_IP:8000';
   ```

5. **Start Metro Bundler**
   ```bash
   npm start
   # or
   yarn start
   ```

6. **Run on Device/Emulator**
   ```bash
   # Android
   npm run android
   # or
   yarn android
   
   # iOS (macOS only)
   npm run ios
   # or
   yarn ios
   ```

## ⚙️ Configuration

### Backend Connection
The app needs to connect to your Nexa Python backend:

1. **Find Your Backend IP**
   ```bash
   # On Windows
   ipconfig
   
   # On Linux/Mac
   ifconfig
   ```

2. **Update API Service**
   ```javascript
   // src/services/ApiService.js
   this.baseURL = 'http://192.168.1.100:8000'; // Your IP here
   ```

3. **Test Connection**
   - Start the Python backend: `python run.py`
   - Launch the mobile app
   - Check connection status in the app header

### Voice Settings
Configure voice recognition and TTS:

```javascript
// src/services/VoiceService.js
this.config = {
  language: 'en-US',           // Speech recognition language
  wakeWords: ['nexa', 'hey nexa'], // Custom wake words
  speechTimeout: 5000,         // Speech timeout (ms)
  continuous: false,           // Continuous listening
};
```

### Permissions
The app requires these permissions:

**Android** (`android/app/src/main/AndroidManifest.xml`):
```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

**iOS** (`ios/NexaMobile/Info.plist`):
```xml
<key>NSMicrophoneUsageDescription</key>
<string>Nexa needs microphone access for voice commands</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>Nexa needs location for weather information</string>
```

## 🎤 Voice Commands

### Basic Commands
- **"Hey Nexa, what time is it?"** - Get current time
- **"Nexa, what's the weather like?"** - Weather information
- **"OK Nexa, play music"** - Music control
- **"Nexa, latest news"** - News headlines

### Quick Actions
- **Weather** - "What's the weather like?"
- **News** - "Latest news headlines"
- **Music** - "Play some music"
- **Time** - "What time is it?"
- **Math** - "Calculate 15 plus 27"
- **Help** - "What can you do?"

### System Commands
- **"Open calculator"** - Launch apps
- **"Tell me a joke"** - Entertainment
- **"Help"** - Show available commands

## 📁 Project Structure

```
mobile/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── VoiceVisualizer.js
│   │   ├── QuickActions.js
│   │   ├── StatusIndicator.js
│   │   └── MessageBubble.js
│   ├── screens/             # App screens
│   │   ├── HomeScreen.js
│   │   ├── SettingsScreen.js
│   │   └── ConversationScreen.js
│   ├── services/            # Business logic services
│   │   ├── VoiceService.js
│   │   ├── ApiService.js
│   │   └── StorageService.js
│   ├── context/             # React Context for state
│   │   └── AppContext.js
│   └── styles/              # Theme and styling
│       └── theme.js
├── android/                 # Android-specific code
├── ios/                     # iOS-specific code
├── package.json
└── README.md
```

## 🔧 Development

### Running in Development
```bash
# Start Metro bundler
npm start

# Run on Android
npm run android

# Run on iOS (macOS only)
npm run ios

# Run tests
npm test
```

### Building for Production

**Android APK:**
```bash
cd android
./gradlew assembleRelease
# APK location: android/app/build/outputs/apk/release/
```

**iOS Archive:**
```bash
cd ios
xcodebuild -workspace NexaMobile.xcworkspace \
  -scheme NexaMobile \
  -configuration Release \
  -destination generic/platform=iOS \
  -archivePath NexaMobile.xcarchive archive
```

### Debugging
- **React Native Debugger** - Visual debugging tool
- **Flipper** - Mobile app debugging platform
- **Chrome DevTools** - For JavaScript debugging
- **Android Studio** - Android-specific debugging
- **Xcode** - iOS-specific debugging

## 🔒 Security and Privacy

### Permissions
- **Microphone** - Required for voice recognition
- **Internet** - Required for backend communication
- **Location** - Optional for location-based features

### Data Handling
- **Local Storage** - Preferences and conversations stored locally
- **Backend Communication** - Encrypted HTTPS communication
- **Voice Data** - Processed locally, not stored permanently

### Privacy Features
- **Offline Mode** - Core features work without internet
- **Data Control** - Clear conversations and preferences
- **Permission Management** - Granular permission control

## 📱 Platform Support

### Android
- **Minimum SDK**: 21 (Android 5.0)
- **Target SDK**: 34 (Android 14)
- **Architecture**: arm64-v8a, armeabi-v7a, x86_64

### iOS
- **Minimum Version**: iOS 12.0
- **Architecture**: arm64, x86_64 (simulator)
- **Devices**: iPhone, iPad

## 🚀 Performance Optimization

### App Size
- **Android APK**: ~25MB (release)
- **iOS IPA**: ~30MB (release)
- **Bundle Splitting** - Separate bundles for different architectures

### Runtime Performance
- **Memory Usage** - Optimized for low memory devices
- **Battery Life** - Efficient voice processing
- **Network Usage** - Minimal data consumption

### Voice Processing
- **Local Processing** - Speech recognition on device
- **Background Listening** - Optimized for battery life
- **Audio Quality** - Noise cancellation and filtering

## 🔧 Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   - Check if Python backend is running
   - Verify IP address in ApiService.js
   - Ensure devices are on same network

2. **Microphone Not Working**
   - Grant microphone permissions
   - Check device microphone settings
   - Test with other voice apps

3. **Voice Recognition Not Starting**
   - Verify microphone permissions
   - Check device compatibility
   - Restart the app

4. **App Crashes on Startup**
   - Clear app data and cache
   - Reinstall the app
   - Check device compatibility

### Debug Commands
```bash
# View logs
npx react-native log-android  # Android
npx react-native log-ios      # iOS

# Clear cache
npx react-native start --reset-cache

# Clean build
cd android && ./gradlew clean  # Android
cd ios && xcodebuild clean     # iOS
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on both platforms
5. Submit a pull request

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review device logs for errors
- Ensure backend is properly configured
- Test with different devices

---

**Nexa Mobile** - Your AI voice assistant, now in your pocket! 📱🎤
