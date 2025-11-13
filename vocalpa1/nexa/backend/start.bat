@echo off
REM Nexa Backend Startup Script for Windows
echo Starting Nexa Voice Assistant Backend...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found
    echo Copying .env.example to .env...
    copy .env.example .env
    echo Please edit .env file with your API keys before running again
    pause
    exit /b 1
)

REM Start the server
echo.
echo Starting Nexa backend server...
python run.py

pause
