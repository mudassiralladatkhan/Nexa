@echo off
echo ========================================
echo  🚀 MANUAL GITHUB PUSH
echo ========================================
echo.

echo 📋 STEP 1: Create GitHub Repository
echo.
echo 1. Go to: https://github.com/mudassiralladatkhan
echo 2. Click "New repository"
echo 3. Name: Nexa
echo 4. Make it PUBLIC
echo 5. Don't initialize with README
echo 6. Click "Create repository"
echo.
pause

echo.
echo 📤 STEP 2: Initialize and Push
echo.

echo Initializing git...
git init

echo Adding files...
git add .

echo Creating commit...
git commit -m "Initial commit: Nexa Voice Assistant"

echo Adding remote...
git remote add origin https://github.com/mudassiralladatkhan/Nexa.git

echo Setting main branch...
git branch -M main

echo.
echo 🔐 You will be prompted for GitHub credentials:
echo    Username: mudassiralladatkhan
echo    Password: [Use Personal Access Token]
echo.
echo Creating Personal Access Token:
echo 1. Go to: https://github.com/settings/tokens
echo 2. Generate new token (classic)
echo 3. Select: repo, workflow
echo 4. Copy token and use as password
echo.
pause

echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo  ✅ PUSH COMPLETE!
echo ========================================
echo.
echo 🌐 Repository: https://github.com/mudassiralladatkhan/Nexa
echo 🚀 Actions: https://github.com/mudassiralladatkhan/Nexa/actions
echo 📱 APK builds will start automatically!
echo.
pause
