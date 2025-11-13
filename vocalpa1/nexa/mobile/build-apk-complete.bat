@echo off
REM ========================================
REM Nexa Mobile - Complete APK Build Script
REM ========================================
echo.
echo  ███╗   ██╗███████╗██╗  ██╗ █████╗ 
echo  ████╗  ██║██╔════╝╚██╗██╔╝██╔══██╗
echo  ██╔██╗ ██║█████╗   ╚███╔╝ ███████║
echo  ██║╚██╗██║██╔══╝   ██╔██╗ ██╔══██║
echo  ██║ ╚████║███████╗██╔╝ ██╗██║  ██║
echo  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
echo.
echo  Building Android APK...
echo ========================================
echo.

REM Set build timestamp
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "build_time=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"

echo Build started at: %build_time%
echo.

REM ========================================
REM STEP 1: Environment Checks
REM ========================================
echo [1/8] Checking environment...

REM Check if we're in the correct directory
if not exist "package.json" (
    echo ❌ Error: package.json not found
    echo Please run this script from the mobile app root directory
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Node.js is not installed
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
) else (
    echo ✅ Node.js found:
    node --version
)

REM Check Java
java -version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Java is not installed
    echo Please install Java JDK 11 or higher
    pause
    exit /b 1
) else (
    echo ✅ Java found:
    java -version 2>&1 | findstr "version"
)

REM Check Android SDK
if not exist "%ANDROID_HOME%\platform-tools\adb.exe" (
    echo ❌ Error: Android SDK not found
    echo Please install Android Studio and set ANDROID_HOME environment variable
    echo Download from: https://developer.android.com/studio
    pause
    exit /b 1
) else (
    echo ✅ Android SDK found at: %ANDROID_HOME%
)

echo.

REM ========================================
REM STEP 2: Install Dependencies
REM ========================================
echo [2/8] Installing dependencies...

if not exist "node_modules" (
    echo Installing npm dependencies...
    npm install
    if errorlevel 1 (
        echo ❌ Error: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo ✅ Dependencies already installed
)

echo.

REM ========================================
REM STEP 3: Clean Previous Builds
REM ========================================
echo [3/8] Cleaning previous builds...

REM Clean React Native cache
echo Cleaning React Native cache...
npx react-native start --reset-cache --port 8082 >nul 2>&1 &
timeout /t 2 >nul
taskkill /f /im node.exe >nul 2>&1

REM Clean Android build
if exist "android" (
    cd android
    echo Cleaning Android build...
    call gradlew clean
    if errorlevel 1 (
        echo ⚠️ Warning: Android clean failed, continuing...
    ) else (
        echo ✅ Android build cleaned
    )
    cd ..
) else (
    echo ❌ Error: Android directory not found
    pause
    exit /b 1
)

echo.

REM ========================================
REM STEP 4: Create Required Directories
REM ========================================
echo [4/8] Creating required directories...

REM Create assets directory
if not exist "android\app\src\main\assets" (
    mkdir "android\app\src\main\assets"
    echo ✅ Created assets directory
)

REM Create drawable directories
if not exist "android\app\src\main\res\drawable" (
    mkdir "android\app\src\main\res\drawable"
    echo ✅ Created drawable directory
)

REM Create mipmap directories for different densities
for %%d in (mdpi hdpi xhdpi xxhdpi xxxhdpi) do (
    if not exist "android\app\src\main\res\mipmap-%%d" (
        mkdir "android\app\src\main\res\mipmap-%%d"
        echo ✅ Created mipmap-%%d directory
    )
)

echo.

REM ========================================
REM STEP 5: Bundle JavaScript
REM ========================================
echo [5/8] Bundling JavaScript...

echo Creating production JavaScript bundle...
npx react-native bundle ^
    --platform android ^
    --dev false ^
    --entry-file index.js ^
    --bundle-output android/app/src/main/assets/index.android.bundle ^
    --assets-dest android/app/src/main/res ^
    --sourcemap-output android/app/src/main/assets/index.android.bundle.map ^
    --verbose

if errorlevel 1 (
    echo ❌ Error: JavaScript bundling failed
    pause
    exit /b 1
) else (
    echo ✅ JavaScript bundle created successfully
)

echo.

REM ========================================
REM STEP 6: Build Debug APK
REM ========================================
echo [6/8] Building debug APK...

cd android
echo Building debug APK...
call gradlew assembleDebug --console=plain

if errorlevel 1 (
    echo ❌ Error: Debug APK build failed
    cd ..
    pause
    exit /b 1
) else (
    echo ✅ Debug APK built successfully
)
cd ..

echo.

REM ========================================
REM STEP 7: Build Release APK
REM ========================================
echo [7/8] Building release APK...

cd android
echo Building release APK...
call gradlew assembleRelease --console=plain

if errorlevel 1 (
    echo ❌ Error: Release APK build failed
    cd ..
    pause
    exit /b 1
) else (
    echo ✅ Release APK built successfully
)
cd ..

echo.

REM ========================================
REM STEP 8: Show Results
REM ========================================
echo [8/8] Build completed!

echo.
echo ========================================
echo           BUILD RESULTS
echo ========================================
echo.
echo Build completed at: 
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
echo %YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%
echo.

REM List generated APKs with details
echo Generated APK files:
echo.

if exist "android\app\build\outputs\apk\debug" (
    echo 📱 DEBUG APKs:
    for %%f in ("android\app\build\outputs\apk\debug\*.apk") do (
        echo   📦 %%~nxf
        for %%s in ("%%f") do (
            set /a size_mb=%%~zs/1024/1024
            echo   📏 Size: %%~zs bytes (~!size_mb! MB^)
        )
        echo   📂 Location: %%f
        echo.
    )
)

if exist "android\app\build\outputs\apk\release" (
    echo 🚀 RELEASE APKs:
    for %%f in ("android\app\build\outputs\apk\release\*.apk") do (
        echo   📦 %%~nxf
        for %%s in ("%%f") do (
            set /a size_mb=%%~zs/1024/1024
            echo   📏 Size: %%~zs bytes (~!size_mb! MB^)
        )
        echo   📂 Location: %%f
        echo.
    )
)

echo ========================================
echo           INSTALLATION GUIDE
echo ========================================
echo.
echo 📱 To install the APK on your Android device:
echo.
echo Method 1 - Direct Installation:
echo   1. Enable "Install from Unknown Sources" in Android Settings
echo   2. Copy APK file to your device
echo   3. Tap the APK file to install
echo.
echo Method 2 - ADB Installation:
echo   1. Connect device via USB with USB Debugging enabled
echo   2. Run: adb install "path\to\your\apk\file.apk"
echo.
echo Method 3 - Wireless Installation:
echo   1. Enable "Wireless Debugging" on Android device
echo   2. Connect via ADB wireless
echo   3. Install using ADB command
echo.

echo ========================================
echo           NEXT STEPS
echo ========================================
echo.
echo 🔧 Setup Instructions:
echo   1. Install the APK on your Android device
echo   2. Start your Python backend: cd ..\backend ^&^& python run.py
echo   3. Update backend IP in the mobile app settings
echo   4. Grant microphone permissions when prompted
echo   5. Test voice commands: "Hey Nexa, what time is it?"
echo.
echo 🎤 Voice Commands to Try:
echo   • "Open YouTube"
echo   • "What's the weather like?"
echo   • "Tell me a joke"
echo   • "Launch calculator"
echo   • "Go to Google"
echo.

REM Copy APKs to easy access location
if not exist "built-apks" mkdir "built-apks"
if exist "android\app\build\outputs\apk\debug" (
    copy "android\app\build\outputs\apk\debug\*.apk" "built-apks\" >nul 2>&1
)
if exist "android\app\build\outputs\apk\release" (
    copy "android\app\build\outputs\apk\release\*.apk" "built-apks\" >nul 2>&1
)

echo 📁 APKs copied to: %cd%\built-apks\
echo.

REM Open APK directory
echo Opening APK directory...
start "" "built-apks"

echo ========================================
echo    🎉 NEXA MOBILE APK BUILD COMPLETE! 🎉
echo ========================================
echo.
echo Your Nexa Voice Assistant mobile app is ready!
echo.
pause
