@echo off
echo ========================================
echo  🔄 RESETTING NEXA FRONTEND
echo ========================================
echo.

echo 🛑 Stopping any existing frontend servers...

REM Kill any processes on port 3000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do (
    echo Killing process %%a on port 3000
    taskkill /PID %%a /F >nul 2>&1
)

echo ✅ Port 3000 cleared
echo.

echo 🌐 Starting fresh frontend server...
python start-frontend.py

pause
