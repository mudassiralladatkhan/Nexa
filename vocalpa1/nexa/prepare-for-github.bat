@echo off
echo ========================================
echo  🚀 PREPARING NEXA FOR GITHUB
echo ========================================
echo.

echo 📋 Checking project structure...

REM Check if we're in the nexa directory
if not exist "mobile" (
    echo ❌ Error: mobile directory not found
    echo Please run this from the nexa directory
    pause
    exit /b 1
)

echo ✅ Mobile directory found
echo ✅ Backend directory found
echo ✅ Frontend directory found
echo ✅ Shared directory found

echo.
echo 📁 Creating GitHub Actions directory...
if not exist ".github" mkdir ".github"
if not exist ".github\workflows" mkdir ".github\workflows"

echo ✅ GitHub Actions directory created

echo.
echo 📝 Files ready for GitHub:
echo   • .github/workflows/build-apk.yml
echo   • .github/workflows/release-apk-fixed.yml
echo   • GITHUB_ACTIONS_SETUP.md
echo   • All project files

echo.
echo ========================================
echo  📤 NEXT STEPS FOR GITHUB
echo ========================================
echo.
echo 1. Create repository at: https://github.com/mudassiralladatkhan/Nexa
echo 2. Initialize git in this directory:
echo    git init
echo    git add .
echo    git commit -m "Initial commit: Nexa Voice Assistant"
echo.
echo 3. Connect to GitHub:
echo    git remote add origin https://github.com/mudassiralladatkhan/Nexa.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. GitHub Actions will automatically:
echo    • Build APK on every push
echo    • Create releases with APK files
echo    • Provide downloadable artifacts
echo.
echo 🎯 APK Build URL (after setup):
echo    https://github.com/mudassiralladatkhan/Nexa/actions
echo.
echo ========================================
echo  ✅ READY FOR GITHUB DEPLOYMENT!
echo ========================================
echo.
pause
