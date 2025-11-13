# Nexa Voice Assistant - Complete Project Launcher (PowerShell)

Write-Host ""
Write-Host "  ███╗   ██╗███████╗██╗  ██╗ █████╗ " -ForegroundColor Cyan
Write-Host "  ████╗  ██║██╔════╝╚██╗██╔╝██╔══██╗" -ForegroundColor Cyan
Write-Host "  ██╔██╗ ██║█████╗   ╚███╔╝ ███████║" -ForegroundColor Cyan
Write-Host "  ██║╚██╗██║██╔══╝   ██╔██╗ ██╔══██║" -ForegroundColor Cyan
Write-Host "  ██║ ╚████║███████╗██╔╝ ██╗██║  ██║" -ForegroundColor Cyan
Write-Host "  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "  🚀 COMPLETE PROJECT LAUNCHER" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to kill processes on specific ports
function Kill-ProcessOnPort($port) {
    try {
        $processes = netstat -ano | Select-String ":$port" | ForEach-Object { ($_ -split '\s+')[-1] }
        foreach ($processId in $processes) {
            if ($processId -and $processId -ne "0") {
                Write-Host "Killing process $processId on port $port" -ForegroundColor Gray
                Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
            }
        }
    } catch {
        Write-Host "No processes found on port $port" -ForegroundColor Gray
    }
}

Write-Host "🛑 Cleaning up existing processes..." -ForegroundColor Yellow
Kill-ProcessOnPort 8000
Kill-ProcessOnPort 8001
Kill-ProcessOnPort 8002
Kill-ProcessOnPort 3000
Kill-ProcessOnPort 3001

Write-Host "✅ Ports cleared" -ForegroundColor Green
Write-Host ""

Write-Host "🔧 Starting Nexa Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; python smart_server.py"

Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 5

Write-Host "🌐 Starting Nexa Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; python simple-server.py"

Write-Host "⏳ Waiting for frontend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ NEXA PROJECT IS NOW RUNNING!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Backend API: http://localhost:8002 (or next available port)" -ForegroundColor Cyan
Write-Host "🌐 Frontend App: http://localhost:3000 (or next available port)" -ForegroundColor Cyan
Write-Host "📚 API Documentation: http://localhost:8002/docs" -ForegroundColor Cyan
Write-Host "🧪 Connection Test: http://localhost:3000/test.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎤 Your complete voice assistant is ready!" -ForegroundColor Magenta
Write-Host ""
Write-Host "📱 Features Available:" -ForegroundColor White
Write-Host "  • Voice Recognition & TTS" -ForegroundColor Gray
Write-Host "  • 58+ App Launcher (Android APK support)" -ForegroundColor Gray
Write-Host "  • 100+ Website Opener" -ForegroundColor Gray
Write-Host "  • Entertainment (Jokes, Facts, Quotes)" -ForegroundColor Gray
Write-Host "  • Weather, News, Music APIs" -ForegroundColor Gray
Write-Host "  • Cross-platform compatibility" -ForegroundColor Gray
Write-Host ""

Write-Host "🌐 Opening web browser..." -ForegroundColor Green
Start-Sleep -Seconds 2
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  🎉 NEXA IS FULLY OPERATIONAL!" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "💡 Both services are running in separate windows" -ForegroundColor Yellow
Write-Host "💡 Close the PowerShell windows to stop Nexa" -ForegroundColor Yellow
Write-Host "💡 Check the new PowerShell windows for server status" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎤 Try these voice commands:" -ForegroundColor White
Write-Host "  • 'Hello Nexa'" -ForegroundColor Gray
Write-Host "  • 'What time is it?'" -ForegroundColor Gray
Write-Host "  • 'Open YouTube'" -ForegroundColor Gray
Write-Host "  • 'Tell me a joke'" -ForegroundColor Gray
Write-Host "  • 'Go to Google'" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to continue"
