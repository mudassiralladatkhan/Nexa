@echo off
echo ========================================
echo  NEXA BACKEND - STARTING SERVER
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

REM Check if we're in the backend directory
if not exist "run.py" (
    echo ❌ Error: run.py not found
    echo Please run this script from the backend directory
    pause
    exit /b 1
)

echo.
echo Installing/updating dependencies...
pip install fastapi uvicorn[standard] sqlalchemy pydantic python-dotenv requests httpx

if errorlevel 1 (
    echo ❌ Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo  STARTING NEXA BACKEND SERVER
echo ========================================
echo.
echo Server will start on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python run.py

pause
