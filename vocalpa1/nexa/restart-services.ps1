# Nexa Services Restart Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🔄 RESTARTING NEXA SERVICES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🛑 Stopping any existing services..." -ForegroundColor Yellow

# Kill processes on port 8000
try {
    $processes8000 = netstat -ano | Select-String ":8000" | ForEach-Object { ($_ -split '\s+')[-1] }
    foreach ($processId in $processes8000) {
        if ($processId -and $processId -ne "0") {
            Write-Host "Killing process $processId on port 8000" -ForegroundColor Gray
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
    }
} catch {
    Write-Host "No processes found on port 8000" -ForegroundColor Gray
}

# Kill processes on port 3000
try {
    $processes3000 = netstat -ano | Select-String ":3000" | ForEach-Object { ($_ -split '\s+')[-1] }
    foreach ($processId in $processes3000) {
        if ($processId -and $processId -ne "0") {
            Write-Host "Killing process $processId on port 3000" -ForegroundColor Gray
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
    }
} catch {
    Write-Host "No processes found on port 3000" -ForegroundColor Gray
}

Write-Host "✅ Ports cleared" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Starting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; python start_server.py"

Start-Sleep -Seconds 3

Write-Host "🌐 Starting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; python start-frontend.py"

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ NEXA SERVICES RESTARTED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services are running in separate windows." -ForegroundColor Yellow
Write-Host "Close the PowerShell windows to stop the services." -ForegroundColor Yellow
Write-Host ""

# Open browser
Write-Host "🌐 Opening browser..." -ForegroundColor Green
Start-Process "http://localhost:3000"

Read-Host "Press Enter to continue"
