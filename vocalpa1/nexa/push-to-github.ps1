# Nexa Voice Assistant - Push to GitHub and Setup APK Build

Write-Host ""
Write-Host "  ███╗   ██╗███████╗██╗  ██╗ █████╗ " -ForegroundColor Cyan
Write-Host "  ████╗  ██║██╔════╝╚██╗██╔╝██╔══██╗" -ForegroundColor Cyan
Write-Host "  ██╔██╗ ██║█████╗   ╚███╔╝ ███████║" -ForegroundColor Cyan
Write-Host "  ██║╚██╗██║██╔══╝   ██╔██╗ ██╔══██║" -ForegroundColor Cyan
Write-Host "  ██║ ╚████║███████╗██╔╝ ██╗██║  ██║" -ForegroundColor Cyan
Write-Host "  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "  🚀 PUSH TO GITHUB & BUILD APK" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version 2>$null
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check project structure
if (-not (Test-Path "mobile")) {
    Write-Host "❌ Error: mobile directory not found" -ForegroundColor Red
    Write-Host "Please run this from the nexa directory" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Project structure verified" -ForegroundColor Green
Write-Host ""

Write-Host "🔧 Initializing Git repository..." -ForegroundColor Yellow
git init

Write-Host "📝 Adding all files..." -ForegroundColor Yellow
git add .

Write-Host "💾 Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Nexa Voice Assistant with GitHub Actions APK build"

Write-Host "🔗 Adding GitHub remote..." -ForegroundColor Yellow
git remote add origin https://github.com/mudassiralladatkhan/Nexa.git

Write-Host "🌿 Setting main branch..." -ForegroundColor Yellow
git branch -M main

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  📤 PUSHING TO GITHUB" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  You may be prompted for GitHub credentials" -ForegroundColor Yellow
Write-Host "   Use your GitHub username and personal access token" -ForegroundColor Gray
Write-Host ""

try {
    git push -u origin main
    $pushSuccess = $LASTEXITCODE -eq 0
} catch {
    $pushSuccess = $false
}

if (-not $pushSuccess) {
    Write-Host ""
    Write-Host "❌ Push failed. This might be because:" -ForegroundColor Red
    Write-Host "   1. Repository doesn't exist on GitHub" -ForegroundColor Gray
    Write-Host "   2. Authentication failed" -ForegroundColor Gray
    Write-Host "   3. Network issues" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📋 Manual steps:" -ForegroundColor Yellow
    Write-Host "   1. Go to: https://github.com/mudassiralladatkhan" -ForegroundColor Gray
    Write-Host "   2. Click 'New repository'" -ForegroundColor Gray
    Write-Host "   3. Name it 'Nexa'" -ForegroundColor Gray
    Write-Host "   4. Make it public" -ForegroundColor Gray
    Write-Host "   5. Don't initialize with README" -ForegroundColor Gray
    Write-Host "   6. Create repository" -ForegroundColor Gray
    Write-Host "   7. Run this script again" -ForegroundColor Gray
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ PUSH SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "🎉 Your Nexa project is now on GitHub!" -ForegroundColor Magenta
Write-Host ""
Write-Host "📱 APK Build Setup:" -ForegroundColor White
Write-Host "   • GitHub Actions workflows are included" -ForegroundColor Gray
Write-Host "   • APK builds will trigger automatically" -ForegroundColor Gray
Write-Host "   • First build should start in a few minutes" -ForegroundColor Gray
Write-Host ""
Write-Host "🔗 Repository URL:" -ForegroundColor White
Write-Host "   https://github.com/mudassiralladatkhan/Nexa" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 GitHub Actions URL:" -ForegroundColor White
Write-Host "   https://github.com/mudassiralladatkhan/Nexa/actions" -ForegroundColor Cyan
Write-Host ""
Write-Host "📥 APK Downloads (after build):" -ForegroundColor White
Write-Host "   https://github.com/mudassiralladatkhan/Nexa/releases" -ForegroundColor Cyan
Write-Host ""

Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  🎯 NEXT STEPS" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "1. 🌐 Visit your repository:" -ForegroundColor White
Write-Host "   https://github.com/mudassiralladatkhan/Nexa" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. 🔄 Check GitHub Actions:" -ForegroundColor White
Write-Host "   • Go to Actions tab" -ForegroundColor Gray
Write-Host "   • First build should be running" -ForegroundColor Gray
Write-Host "   • Wait ~10-15 minutes for completion" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 📱 Download APK:" -ForegroundColor White
Write-Host "   • Go to completed workflow run" -ForegroundColor Gray
Write-Host "   • Download from Artifacts section" -ForegroundColor Gray
Write-Host "   • Or wait for automatic release" -ForegroundColor Gray
Write-Host ""
Write-Host "4. 🧪 Test APK:" -ForegroundColor White
Write-Host "   • Install on Android device" -ForegroundColor Gray
Write-Host "   • Grant microphone permissions" -ForegroundColor Gray
Write-Host "   • Try voice commands" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  🎉 GITHUB SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your Nexa Voice Assistant is now:" -ForegroundColor White
Write-Host "✅ Hosted on GitHub" -ForegroundColor Green
Write-Host "✅ Ready for automatic APK builds" -ForegroundColor Green
Write-Host "✅ Available for download and distribution" -ForegroundColor Green
Write-Host ""

# Open GitHub repository in browser
Write-Host "🌐 Opening GitHub repository..." -ForegroundColor Green
Start-Process "https://github.com/mudassiralladatkhan/Nexa"

Read-Host "Press Enter to continue"
