@echo off
REM Nexa Mobile Setup Script for Windows
echo Setting up Nexa Mobile App...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo Node.js version:
node --version
echo.

REM Check if React Native CLI is installed
npx react-native --version >nul 2>&1
if errorlevel 1 (
    echo Installing React Native CLI...
    npm install -g @react-native-community/cli
)

echo React Native CLI version:
npx react-native --version
echo.

REM Install dependencies
echo Installing project dependencies...
npm install

REM Check if Android SDK is available
if exist "%ANDROID_HOME%\platform-tools\adb.exe" (
    echo Android SDK found at: %ANDROID_HOME%
) else (
    echo Warning: Android SDK not found
    echo Please install Android Studio and set ANDROID_HOME environment variable
    echo Download from: https://developer.android.com/studio
)

echo.
echo Setup completed!
echo.
echo Next steps:
echo 1. Start your Python backend: cd ../backend && python run.py
echo 2. Update backend IP in src/services/ApiService.js
echo 3. Start Metro bundler: npm start
echo 4. Run on Android: npm run android
echo.
echo For iOS development (macOS only):
echo 1. Install Xcode from App Store
echo 2. Install CocoaPods: sudo gem install cocoapods
echo 3. Install iOS dependencies: cd ios && pod install
echo 4. Run on iOS: npm run ios
echo.
pause
