@echo off
title Nexa Voice Assistant - Complete Project Launcher
color 0A

echo.
echo  ███╗   ██╗███████╗██╗  ██╗ █████╗ 
echo  ████╗  ██║██╔════╝╚██╗██╔╝██╔══██╗
echo  ██╔██╗ ██║█████╗   ╚███╔╝ ███████║
echo  ██║╚██╗██║██╔══╝   ██╔██╗ ██╔══██║
echo  ██║ ╚████║███████╗██╔╝ ██╗██║  ██║
echo  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
echo.
echo  🚀 COMPLETE PROJECT LAUNCHER
echo ========================================
echo.

REM Kill any existing processes on common ports
echo 🛑 Cleaning up existing processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8002') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3001') do taskkill /PID %%a /F >nul 2>&1

echo ✅ Ports cleared
echo.

echo 🔧 Starting Nexa Backend Server...
start "🤖 Nexa Backend" cmd /k "cd /d %~dp0backend && python smart_server.py"

echo ⏳ Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo 🌐 Starting Nexa Frontend Server...
start "🌐 Nexa Frontend" cmd /k "cd /d %~dp0frontend && python simple-server.py"

echo ⏳ Waiting for frontend to initialize...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo  ✅ NEXA PROJECT IS NOW RUNNING!
echo ========================================
echo.
echo 🔗 Backend API: http://localhost:8002 (or next available port)
echo 🌐 Frontend App: http://localhost:3000 (or next available port)
echo 📚 API Documentation: http://localhost:8002/docs
echo 🧪 Connection Test: http://localhost:3000/test.html
echo.
echo 🎤 Your complete voice assistant is ready!
echo.
echo 📱 Features Available:
echo   • Voice Recognition & TTS
echo   • 58+ App Launcher (Android APK support)
echo   • 100+ Website Opener
echo   • Entertainment (Jokes, Facts, Quotes)
echo   • Weather, News, Music APIs
echo   • Cross-platform compatibility
echo.

echo 🌐 Opening web browser...
timeout /t 2 /nobreak >nul
start http://localhost:3000

echo.
echo ========================================
echo  🎉 NEXA IS FULLY OPERATIONAL!
echo ========================================
echo.
echo 💡 Both services are running in separate windows
echo 💡 Close the service windows to stop Nexa
echo 💡 Check the new command windows for server status
echo.
echo 🎤 Try these voice commands:
echo   • "Hello Nexa"
echo   • "What time is it?"
echo   • "Open YouTube"
echo   • "Tell me a joke"
echo   • "Go to Google"
echo.
pause
