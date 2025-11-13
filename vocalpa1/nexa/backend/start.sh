#!/bin/bash
# Nexa Backend Startup Script for Linux/Mac
echo "Starting Nexa Voice Assistant Backend..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "Please edit .env file with your API keys before running again"
    exit 1
fi

# Start the server
echo
echo "Starting Nexa backend server..."
python run.py
