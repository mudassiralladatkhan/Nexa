@echo off
title Push Nexa to GitHub and Setup APK Build
color 0A

echo.
echo  ███╗   ██╗███████╗██╗  ██╗ █████╗ 
echo  ████╗  ██║██╔════╝╚██╗██╔╝██╔══██╗
echo  ██╔██╗ ██║█████╗   ╚███╔╝ ███████║
echo  ██║╚██╗██║██╔══╝   ██╔██╗ ██╔══██║
echo  ██║ ╚████║███████╗██╔╝ ██╗██║  ██║
echo  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
echo.
echo  🚀 PUSH TO GITHUB & BUILD APK
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/
    pause
    exit /b 1
)

echo ✅ Git found
echo.

REM Check if we're in the nexa directory
if not exist "mobile" (
    echo ❌ Error: mobile directory not found
    echo Please run this from the nexa directory
    pause
    exit /b 1
)

echo ✅ Project structure verified
echo.

echo 🔧 Initializing Git repository...
git init

echo 📝 Adding all files...
git add .

echo 💾 Creating initial commit...
git commit -m "Initial commit: Nexa Voice Assistant with GitHub Actions APK build"

echo 🔗 Adding GitHub remote...
git remote add origin https://github.com/mudassiralladatkhan/Nexa.git

echo 🌿 Setting main branch...
git branch -M main

echo.
echo ========================================
echo  📤 PUSHING TO GITHUB
echo ========================================
echo.

echo 🚀 Pushing to GitHub...
echo.
echo ⚠️  You may be prompted for GitHub credentials
echo    Use your GitHub username and personal access token
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ Push failed. This might be because:
    echo    1. Repository doesn't exist on GitHub
    echo    2. Authentication failed
    echo    3. Network issues
    echo.
    echo 📋 Manual steps:
    echo    1. Go to: https://github.com/mudassiralladatkhan
    echo    2. Click "New repository"
    echo    3. Name it "Nexa"
    echo    4. Make it public
    echo    5. Don't initialize with README
    echo    6. Create repository
    echo    7. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ✅ PUSH SUCCESSFUL!
echo ========================================
echo.

echo 🎉 Your Nexa project is now on GitHub!
echo.
echo 📱 APK Build Setup:
echo    • GitHub Actions workflows are included
echo    • APK builds will trigger automatically
echo    • First build should start in a few minutes
echo.
echo 🔗 Repository URL:
echo    https://github.com/mudassiralladatkhan/Nexa
echo.
echo 🚀 GitHub Actions URL:
echo    https://github.com/mudassiralladatkhan/Nexa/actions
echo.
echo 📥 APK Downloads (after build):
echo    https://github.com/mudassiralladatkhan/Nexa/releases
echo.

echo ========================================
echo  🎯 NEXT STEPS
echo ========================================
echo.
echo 1. 🌐 Visit your repository:
echo    https://github.com/mudassiralladatkhan/Nexa
echo.
echo 2. 🔄 Check GitHub Actions:
echo    • Go to Actions tab
echo    • First build should be running
echo    • Wait ~10-15 minutes for completion
echo.
echo 3. 📱 Download APK:
echo    • Go to completed workflow run
echo    • Download from Artifacts section
echo    • Or wait for automatic release
echo.
echo 4. 🧪 Test APK:
echo    • Install on Android device
echo    • Grant microphone permissions
echo    • Try voice commands
echo.

echo ========================================
echo  🎉 GITHUB SETUP COMPLETE!
echo ========================================
echo.
echo Your Nexa Voice Assistant is now:
echo ✅ Hosted on GitHub
echo ✅ Ready for automatic APK builds
echo ✅ Available for download and distribution
echo.
pause
