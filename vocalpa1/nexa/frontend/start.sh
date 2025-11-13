#!/bin/bash
# Nexa Frontend Startup Script for Linux/Mac
echo "Starting Nexa Voice Assistant Frontend..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check if backend is running
echo "Checking if backend is running..."
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "Warning: Backend is not running on http://localhost:8000"
    echo "Please start the backend first by running:"
    echo "  cd ../backend"
    echo "  python run.py"
    echo
    echo "Press Enter to continue anyway, or Ctrl+C to exit..."
    read
fi

# Start the frontend server
echo "Starting frontend server on http://localhost:3000..."
echo
echo "Frontend will be available at:"
echo "  http://localhost:3000"
echo
echo "Press Ctrl+C to stop the server"
echo

python3 -m http.server 3000
