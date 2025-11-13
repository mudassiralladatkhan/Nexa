@echo off
echo ========================================
echo  🔄 RESTARTING NEXA SERVICES
echo ========================================
echo.

echo 🛑 Stopping any existing services...

REM Kill any Python processes on ports 8000 and 3000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Killing process %%a on port 8000
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do (
    echo Killing process %%a on port 3000
    taskkill /PID %%a /F >nul 2>&1
)

echo ✅ Ports cleared
echo.

echo 🚀 Starting Backend Server...
start "Nexa Backend" cmd /k "cd /d %~dp0backend && python start_server.py"

timeout /t 3 /nobreak >nul

echo 🌐 Starting Frontend Server...
start "Nexa Frontend" cmd /k "cd /d %~dp0frontend && python start-frontend.py"

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo  ✅ NEXA SERVICES RESTARTED!
echo ========================================
echo.
echo 🔗 Backend: http://localhost:8000
echo 🌐 Frontend: http://localhost:3000
echo.
echo Services are running in separate windows.
echo Close the windows to stop the services.
echo.

REM Open browser
start http://localhost:3000

pause
