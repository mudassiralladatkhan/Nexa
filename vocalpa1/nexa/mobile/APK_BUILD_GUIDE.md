# 📱 Nexa Mobile APK Build Guide

Complete guide to build and generate APK files for the Nexa Voice Assistant mobile app.

## 🛠️ Prerequisites

### Required Software
1. **Node.js** (v16 or higher)
   - Download: https://nodejs.org/
   - Verify: `node --version`

2. **Android Studio**
   - Download: https://developer.android.com/studio
   - Install Android SDK, Build Tools, and Platform Tools

3. **Java Development Kit (JDK 11)**
   - Included with Android Studio
   - Or download: https://adoptium.net/

### Environment Setup
1. **Set ANDROID_HOME environment variable**
   ```bash
   # Windows
   set ANDROID_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk
   set PATH=%PATH%;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools

   # Add to System Environment Variables permanently
   ```

2. **Verify Android SDK**
   ```bash
   adb --version
   ```

## 🚀 Quick Build (Automated)

### Using Build Script
```bash
cd nexa/mobile
build-apk.bat
```

This script will:
- ✅ Check all prerequisites
- ✅ Install dependencies
- ✅ Clean previous builds
- ✅ Bundle JavaScript
- ✅ Build debug and release APKs
- ✅ Show build results and locations

## 🔧 Manual Build Process

### Step 1: Install Dependencies
```bash
cd nexa/mobile
npm install
```

### Step 2: Update Backend Configuration
Edit `src/services/ApiService.js`:
```javascript
// Replace with your backend IP address
this.baseURL = 'http://YOUR_BACKEND_IP:8000';
```

### Step 3: Bundle JavaScript
```bash
npx react-native bundle \
  --platform android \
  --dev false \
  --entry-file index.js \
  --bundle-output android/app/src/main/assets/index.android.bundle \
  --assets-dest android/app/src/main/res
```

### Step 4: Build APK
```bash
cd android

# Clean previous builds
./gradlew clean

# Build debug APK
./gradlew assembleDebug

# Build release APK
./gradlew assembleRelease
```

## 📦 APK Output Locations

### Debug APKs
```
android/app/build/outputs/apk/debug/
├── Nexa-debug-1.0.0-arm64-v8a-[DATE].apk
├── Nexa-debug-1.0.0-armeabi-v7a-[DATE].apk
├── Nexa-debug-1.0.0-x86-[DATE].apk
└── Nexa-debug-1.0.0-x86_64-[DATE].apk
```

### Release APKs
```
android/app/build/outputs/apk/release/
├── Nexa-release-1.0.0-arm64-v8a-[DATE].apk
├── Nexa-release-1.0.0-armeabi-v7a-[DATE].apk
├── Nexa-release-1.0.0-x86-[DATE].apk
└── Nexa-release-1.0.0-x86_64-[DATE].apk
```

## 📱 APK Installation

### Method 1: Direct Installation
1. Copy APK file to your Android device
2. Enable "Install from Unknown Sources" in Settings
3. Tap the APK file to install

### Method 2: ADB Installation
```bash
# Connect device via USB with USB Debugging enabled
adb devices

# Install APK
adb install "android/app/build/outputs/apk/debug/Nexa-debug-1.0.0-arm64-v8a-[DATE].apk"
```

### Method 3: Wireless Installation
1. Enable "Wireless Debugging" on Android device
2. Connect via ADB wireless
3. Install using ADB command

## 🔒 Release APK Signing

### Generate Signing Key
```bash
cd android/app
keytool -genkeypair -v -storetype PKCS12 -keystore nexa-upload-key.keystore -alias nexa-upload-key -keyalg RSA -keysize 2048 -validity 10000
```

### Configure Signing
Create `android/gradle.properties`:
```properties
NEXA_UPLOAD_STORE_FILE=nexa-upload-key.keystore
NEXA_UPLOAD_KEY_ALIAS=nexa-upload-key
NEXA_UPLOAD_STORE_PASSWORD=your_store_password
NEXA_UPLOAD_KEY_PASSWORD=your_key_password
```

### Build Signed Release APK
```bash
cd android
./gradlew assembleRelease
```

## 📊 APK Analysis

### APK Size Optimization
- **Debug APK**: ~35-45 MB
- **Release APK**: ~25-35 MB (optimized)

### Architecture Support
- **arm64-v8a**: Modern 64-bit ARM devices (recommended)
- **armeabi-v7a**: Older 32-bit ARM devices
- **x86**: Intel-based devices (rare)
- **x86_64**: 64-bit Intel devices (emulators)

### Features Included
- ✅ Voice recognition (native Android)
- ✅ Text-to-speech (native Android)
- ✅ Background listening service
- ✅ Backend API integration
- ✅ Local data storage
- ✅ Material Design UI
- ✅ Microphone permissions handling

## 🧪 Testing Your APK

### Pre-Installation Checklist
1. **Backend Running**: Ensure Python backend is running
2. **Network Connection**: Device and backend on same network
3. **Permissions**: Grant microphone permissions when prompted
4. **Storage Space**: Ensure sufficient storage (50+ MB)

### Test Scenarios
1. **Voice Recognition**
   - Tap microphone button
   - Say "Hey Nexa, what time is it?"
   - Verify response

2. **Backend Connection**
   - Check connection status in app header
   - Test API commands (weather, news, etc.)

3. **Settings Configuration**
   - Update backend URL in settings
   - Test connection from settings

4. **Background Listening**
   - Enable continuous listening
   - Test wake word detection

## 🚨 Troubleshooting

### Common Build Issues

1. **"Android SDK not found"**
   ```bash
   # Set ANDROID_HOME environment variable
   echo $ANDROID_HOME  # Should show SDK path
   ```

2. **"Gradle build failed"**
   ```bash
   cd android
   ./gradlew clean
   ./gradlew assembleDebug --info
   ```

3. **"JavaScript bundle failed"**
   ```bash
   # Clear Metro cache
   npx react-native start --reset-cache
   ```

4. **"Out of memory"**
   ```bash
   # Increase Gradle memory in android/gradle.properties
   org.gradle.jvmargs=-Xmx4096m
   ```

### Runtime Issues

1. **App crashes on startup**
   - Check device compatibility (Android 5.0+)
   - Verify APK architecture matches device
   - Check device logs: `adb logcat`

2. **Voice recognition not working**
   - Grant microphone permissions
   - Test device microphone with other apps
   - Check Android version compatibility

3. **Backend connection failed**
   - Verify backend IP address in app settings
   - Ensure backend is running and accessible
   - Check network connectivity

## 📈 Performance Optimization

### Build Optimizations
- **ProGuard/R8**: Enabled for release builds
- **Resource shrinking**: Removes unused resources
- **APK splitting**: Separate APKs per architecture
- **Bundle optimization**: Minified JavaScript bundle

### Runtime Optimizations
- **Native modules**: Voice processing uses native Android APIs
- **Background services**: Optimized for battery life
- **Memory management**: Efficient state management
- **Network caching**: API response caching

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Build APK
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - uses: actions/setup-java@v3
        with:
          java-version: '11'
      - name: Setup Android SDK
        uses: android-actions/setup-android@v2
      - name: Install dependencies
        run: npm install
      - name: Build APK
        run: |
          cd android
          ./gradlew assembleRelease
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: nexa-apk
          path: android/app/build/outputs/apk/release/*.apk
```

## 📋 Deployment Checklist

### Pre-Release
- [ ] Update version in `android/app/build.gradle`
- [ ] Test on multiple Android versions
- [ ] Test on different screen sizes
- [ ] Verify all voice commands work
- [ ] Test backend connectivity
- [ ] Check app permissions
- [ ] Verify APK signing

### Release
- [ ] Generate signed release APK
- [ ] Test signed APK on device
- [ ] Create release notes
- [ ] Upload to distribution platform
- [ ] Update documentation

## 🎯 Next Steps

After building your APK:

1. **Test thoroughly** on different Android devices
2. **Configure backend** IP address for your network
3. **Grant permissions** when installing
4. **Test voice commands** with your Python backend
5. **Share with users** or deploy to app stores

---

**Your Nexa Voice Assistant APK is ready to install and use! 📱🎤**
