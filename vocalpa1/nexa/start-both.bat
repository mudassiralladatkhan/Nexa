@echo off
echo ========================================
echo  🚀 STARTING NEXA VOICE ASSISTANT
echo ========================================
echo.

echo 🔧 Starting Backend Server...
start "Nexa Backend" cmd /k "cd /d %~dp0backend && python stable_server.py"

echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo 🌐 Starting Frontend Server...
start "Nexa Frontend" cmd /k "cd /d %~dp0frontend && python simple-server.py"

echo ⏳ Waiting for frontend to start...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo  ✅ NEXA IS NOW RUNNING!
echo ========================================
echo.
echo 🔗 Backend API: http://localhost:8001
echo 🌐 Frontend App: http://localhost:3000
echo 📚 API Docs: http://localhost:8001/docs
echo.
echo 🎤 Your voice assistant is ready!
echo.
echo Opening web browser...
start http://localhost:3000

echo.
echo Both services are running in separate windows.
echo Close the command windows to stop the services.
echo.
pause
