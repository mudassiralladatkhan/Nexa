# Nexa Voice Assistant - PowerShell Startup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🚀 STARTING NEXA VOICE ASSISTANT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the nexa directory
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "❌ Error: Please run this from the nexa directory" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "🔧 Starting Nexa Backend Server..." -ForegroundColor Yellow
Write-Host ""

# Start backend in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python start_server.py"

# Wait a moment for backend to start
Start-Sleep -Seconds 3

Write-Host "🌐 Starting Nexa Frontend (Web PWA)..." -ForegroundColor Yellow
Write-Host ""

# Start frontend in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; python -m http.server 3000"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ NEXA SERVICES STARTED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🌐 Frontend Web: http://localhost:3000" -ForegroundColor Cyan
Write-Host "📱 Mobile App: Use APK build script" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Both services are running in separate windows" -ForegroundColor Yellow
Write-Host "💡 Close the PowerShell windows to stop the services" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  🎤 READY FOR VOICE COMMANDS!" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "Try these voice commands:" -ForegroundColor White
Write-Host "• 'What time is it?'" -ForegroundColor Gray
Write-Host "• 'Hello Nexa'" -ForegroundColor Gray
Write-Host "• 'Open YouTube'" -ForegroundColor Gray
Write-Host "• 'Tell me a joke'" -ForegroundColor Gray
Write-Host ""

# Open browser to frontend
Start-Sleep -Seconds 2
Write-Host "🌐 Opening web browser..." -ForegroundColor Green
Start-Process "http://localhost:3000"

Read-Host "Press Enter to continue"
