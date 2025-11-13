@echo off
echo ========================================
echo  🚀 STARTING NEXA VOICE ASSISTANT
echo ========================================
echo.

REM Check if we're in the nexa directory
if not exist "backend" (
    echo ❌ Error: Please run this from the nexa directory
    pause
    exit /b 1
)

echo 🔧 Starting Nexa Backend Server...
echo.

REM Start backend in a new window
start "Nexa Backend" cmd /k "cd backend && python start_server.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

echo 🌐 Starting Nexa Frontend (Web PWA)...
echo.

REM Start frontend in a new window
start "Nexa Frontend" cmd /k "cd frontend && python -m http.server 3000"

echo.
echo ========================================
echo  ✅ NEXA SERVICES STARTED!
echo ========================================
echo.
echo 🔗 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🌐 Frontend Web: http://localhost:3000
echo 📱 Mobile App: Use APK build script
echo.
echo 💡 Both services are running in separate windows
echo 💡 Close the command windows to stop the services
echo.
echo ========================================
echo  🎤 READY FOR VOICE COMMANDS!
echo ========================================
echo.
echo Try these voice commands:
echo • "What time is it?"
echo • "Hello Nexa"
echo • "Open YouTube"
echo • "Tell me a joke"
echo.
pause
