@echo off
REM Nexa Mobile APK Build Script
echo Building Nexa Mobile APK...
echo.

REM Check if we're in the correct directory
if not exist "package.json" (
    echo Error: package.json not found
    echo Please run this script from the mobile app root directory
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Android SDK is available
if not exist "%ANDROID_HOME%\platform-tools\adb.exe" (
    echo Error: Android SDK not found
    echo Please install Android Studio and set ANDROID_HOME environment variable
    echo Download from: https://developer.android.com/studio
    pause
    exit /b 1
)

echo Android SDK found at: %ANDROID_HOME%
echo.

REM Check if dependencies are installed
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Clean previous builds
echo Cleaning previous builds...
cd android
call gradlew clean
if errorlevel 1 (
    echo Warning: Clean failed, continuing anyway...
)
cd ..

REM Create assets directory if it doesn't exist
if not exist "android\app\src\main\assets" (
    mkdir "android\app\src\main\assets"
)

REM Bundle JavaScript
echo Bundling JavaScript...
npx react-native bundle ^
    --platform android ^
    --dev false ^
    --entry-file index.js ^
    --bundle-output android/app/src/main/assets/index.android.bundle ^
    --assets-dest android/app/src/main/res

if errorlevel 1 (
    echo Error: JavaScript bundling failed
    pause
    exit /b 1
)

REM Build debug APK
echo Building debug APK...
cd android
call gradlew assembleDebug
if errorlevel 1 (
    echo Error: Debug APK build failed
    cd ..
    pause
    exit /b 1
)
cd ..

REM Build release APK (unsigned)
echo Building release APK...
cd android
call gradlew assembleRelease
if errorlevel 1 (
    echo Error: Release APK build failed
    cd ..
    pause
    exit /b 1
)
cd ..

REM Show build results
echo.
echo ========================================
echo           BUILD COMPLETED!
echo ========================================
echo.

REM List generated APKs
echo Generated APK files:
echo.

if exist "android\app\build\outputs\apk\debug" (
    echo DEBUG APKs:
    for %%f in ("android\app\build\outputs\apk\debug\*.apk") do (
        echo   %%~nxf
        echo   Size: 
        for %%s in ("%%f") do echo   %%~zs bytes
        echo   Location: %%f
        echo.
    )
)

if exist "android\app\build\outputs\apk\release" (
    echo RELEASE APKs:
    for %%f in ("android\app\build\outputs\apk\release\*.apk") do (
        echo   %%~nxf
        echo   Size: 
        for %%s in ("%%f") do echo   %%~zs bytes
        echo   Location: %%f
        echo.
    )
)

echo ========================================
echo           INSTALLATION
echo ========================================
echo.
echo To install the APK on your device:
echo.
echo 1. Enable "Unknown Sources" in Android Settings
echo 2. Copy APK to your device
echo 3. Tap the APK file to install
echo.
echo OR use ADB:
echo   adb install "android\app\build\outputs\apk\debug\[APK_NAME].apk"
echo.
echo ========================================
echo           NEXT STEPS
echo ========================================
echo.
echo 1. Test the APK on your Android device
echo 2. Make sure your Python backend is running
echo 3. Update the backend IP in the app settings
echo 4. Grant microphone permissions when prompted
echo.

REM Open APK output directory
echo Opening APK output directory...
start "" "android\app\build\outputs\apk"

echo Build script completed!
pause
