@echo off
echo ========================================
echo  NEXA MOBILE - QUICK APK BUILD
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "package.json" (
    echo Error: Run this from the mobile app directory
    pause
    exit /b 1
)

echo [1/5] Installing dependencies...
if not exist "node_modules" (
    npm install
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [2/5] Creating required directories...
if not exist "android\app\src\main\assets" mkdir "android\app\src\main\assets"

echo [3/5] Bundling JavaScript...
npx react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res

if errorlevel 1 (
    echo JavaScript bundling failed
    pause
    exit /b 1
)

echo [4/5] Building APK...
cd android
call gradlew assembleDebug
if errorlevel 1 (
    echo APK build failed
    cd ..
    pause
    exit /b 1
)
cd ..

echo [5/5] APK built successfully!
echo.
echo APK Location: android\app\build\outputs\apk\debug\
echo.

if exist "android\app\build\outputs\apk\debug" (
    for %%f in ("android\app\build\outputs\apk\debug\*.apk") do (
        echo Generated: %%~nxf
        for %%s in ("%%f") do echo Size: %%~zs bytes
    )
)

echo.
echo Opening APK directory...
start "" "android\app\build\outputs\apk\debug"

echo.
echo Build complete! Install the APK on your Android device.
pause
