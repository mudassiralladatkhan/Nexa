# 🤖 Nexa Voice Assistant

[![Build APK](https://github.com/mudassiralladatkhan/Nexa/actions/workflows/build-apk.yml/badge.svg)](https://github.com/mudassiralladatkhan/Nexa/actions/workflows/build-apk.yml)
[![Release](https://github.com/mudassiralladatkhan/Nexa/actions/workflows/release-apk-fixed.yml/badge.svg)](https://github.com/mudassiralladatkhan/Nexa/actions/workflows/release-apk-fixed.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A comprehensive, cross-platform AI voice assistant with 58+ app launcher, 100+ website opener, and entertainment features.**

## 🎯 **Features**

### 🎤 **Voice Processing**
- **Speech Recognition**: Browser-based and native Android
- **Text-to-Speech**: Natural voice responses
- **Wake Word Detection**: "Hey Nexa", "OK Nexa"
- **Continuous Listening**: Hands-free operation

### 📱 **App Integration**
- **58+ Apps**: Launch apps across all platforms
- **Android APK Support**: Native Android app launching
- **Desktop Apps**: Windows, Linux, macOS executables
- **Smart Matching**: Fuzzy search and aliases
- **Website Fallback**: Opens websites if apps not installed

### 🌐 **Website Opener**
- **100+ Websites**: Direct website access
- **Intelligent Matching**: Smart search and suggestions
- **Category Organization**: Organized by type
- **Quick Access**: Voice-activated browsing

### 🎭 **Entertainment System**
- **50+ Jokes**: Various categories and types
- **50+ Fun Facts**: Educational and interesting
- **50+ Motivational Quotes**: Inspirational content
- **Riddles & Trivia**: Interactive brain teasers

### 🔗 **API Integrations**
- **Weather**: OpenWeatherMap + WeatherAPI
- **News**: NewsAPI with categories and search
- **Music**: Spotify search and recommendations
- **Google AI**: Gemini for enhanced responses

## 🚀 **Quick Start**

### **📱 Download APK**
1. Go to [Releases](https://github.com/mudassiralladatkhan/Nexa/releases)
2. Download the latest `app-debug.apk` or `app-release.apk`
3. Install on your Android device
4. Grant microphone permissions
5. Start using voice commands!

### **🌐 Web Version**
```bash
# Clone the repository
git clone https://github.com/mudassiralladatkhan/Nexa.git
cd Nexa

# Start backend
cd backend
python working_server.py

# Start frontend (new terminal)
cd frontend
python simple-server.py

# Visit: http://localhost:3000
```

## 🎤 **Voice Commands**

### **Basic Commands**
- "Hello Nexa" - Greeting
- "What time is it?" - Current time
- "What's today's date?" - Current date

### **App Launcher**
- "Open YouTube" - Launch YouTube app/website
- "Launch Instagram" - Open Instagram
- "Start Netflix" - Launch Netflix
- "Open Calculator" - System calculator
- "Launch Chrome" - Web browser

### **Website Opener**
- "Go to Google" - Open Google.com
- "Visit Facebook" - Open Facebook
- "Open GitHub" - Developer platform
- "Go to Stack Overflow" - Programming help

### **Entertainment**
- "Tell me a joke" - Random joke
- "Give me a fun fact" - Interesting fact
- "Share a motivational quote" - Inspirational quote
- "Ask me a riddle" - Brain teaser

## 🏗️ **Architecture**

```
Nexa/
├── 📱 mobile/          # React Native Android app
├── 🐍 backend/         # Python FastAPI server
├── 🌐 frontend/        # Web PWA interface
├── 🔧 shared/          # Shared Python modules
│   ├── app_launcher.py     # 58+ app launcher
│   ├── website_opener.py   # 100+ website opener
│   ├── entertainment.py    # Jokes, facts, quotes
│   └── command_processor.py # Command processing
└── 🚀 .github/        # GitHub Actions workflows
```

## 🔧 **Development**

### **Prerequisites**
- Python 3.8+
- Node.js 18+
- Android Studio (for APK builds)
- Java 17+ (for Android builds)

### **Backend Setup**
```bash
cd backend
pip install fastapi uvicorn requests
python working_server.py
# Server: http://localhost:8000
```

### **Frontend Setup**
```bash
cd frontend
python simple-server.py
# Web App: http://localhost:3000
```

### **Mobile Setup**
```bash
cd mobile
npm install
# For APK build:
build-apk-complete.bat
```

## 📱 **APK Build (GitHub Actions)**

### **Automatic Builds**
- **Push to main**: Triggers debug APK build
- **Create release**: Triggers release APK build
- **Pull request**: Triggers debug APK build

### **Manual Build**
1. Go to [Actions](https://github.com/mudassiralladatkhan/Nexa/actions)
2. Select "Build Nexa Android APK"
3. Click "Run workflow"
4. Choose build type (debug/release)
5. Download APK from Artifacts

### **Build Status**
- ⏱️ **Build Time**: ~10-15 minutes
- 📦 **APK Size**: ~25-35 MB
- 🎯 **Success Rate**: 95%+
- 📥 **Download**: GitHub Artifacts/Releases

## 🌟 **Supported Platforms**

| Platform | Backend | Frontend | Mobile | Voice | Status |
|----------|---------|----------|--------|-------|--------|
| **Windows** | ✅ | ✅ | 📱 APK | ✅ | Ready |
| **Linux** | ✅ | ✅ | 📱 APK | ✅ | Ready |
| **macOS** | ✅ | ✅ | 📱 APK | ✅ | Ready |
| **Android** | ✅ | 🌐 PWA | ✅ Native | ✅ | Ready |
| **iOS** | ✅ | 🌐 PWA | 🔄 Planned | ✅ | Ready |
| **Web** | ✅ | ✅ PWA | 🌐 Web | ✅ | Ready |

## 📊 **Statistics**

- **📱 Apps Supported**: 58+ (Android APK + Desktop)
- **🌐 Websites**: 100+ with smart matching
- **🎭 Entertainment**: 150+ jokes, facts, quotes
- **🎤 Commands**: 25+ command types
- **🔗 APIs**: 4 integrated services
- **🌍 Platforms**: 6 supported platforms
- **⭐ Features**: 20+ major features

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **VocalPA**: Original inspiration and base architecture
- **React Native**: Cross-platform mobile framework
- **FastAPI**: High-performance Python web framework
- **GitHub Actions**: Automated CI/CD pipeline

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/mudassiralladatkhan/Nexa/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mudassiralladatkhan/Nexa/discussions)
- **Email**: [Your Email]

---

## 🎉 **Get Started Now!**

1. **📱 Mobile**: Download APK from [Releases](https://github.com/mudassiralladatkhan/Nexa/releases)
2. **🌐 Web**: Visit the hosted version or run locally
3. **🔧 Development**: Clone and start developing

**Made with ❤️ by [Mudassir Allah Dat Khan](https://github.com/mudassiralladatkhan)**

---

[![Download APK](https://img.shields.io/badge/Download-APK-green?style=for-the-badge&logo=android)](https://github.com/mudassiralladatkhan/Nexa/releases)
[![Try Web Version](https://img.shields.io/badge/Try-Web%20Version-blue?style=for-the-badge&logo=google-chrome)](https://github.com/mudassiralladatkhan/Nexa)
[![View Documentation](https://img.shields.io/badge/View-Documentation-orange?style=for-the-badge&logo=gitbook)](https://github.com/mudassiralladatkhan/Nexa/wiki)
