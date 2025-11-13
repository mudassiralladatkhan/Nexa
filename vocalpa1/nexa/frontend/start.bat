@echo off
REM Nexa Frontend Startup Script for Windows
echo Starting Nexa Voice Assistant Frontend...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if backend is running
echo Checking if backend is running...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo Warning: Backend is not running on http://localhost:8000
    echo Please start the backend first by running:
    echo   cd ../backend
    echo   python run.py
    echo.
    echo Press any key to continue anyway, or Ctrl+C to exit...
    pause >nul
)

REM Start the frontend server
echo Starting frontend server on http://localhost:3000...
echo.
echo Frontend will be available at:
echo   http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

python -m http.server 3000
