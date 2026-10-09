@echo off
title Push Dynamic Syllabus Project to GitHub
echo ======================================================================
echo    SANTHIRAM ENGINEERING COLLEGE - DYNAMIC SYLLABUS PORTAL
echo    GitHub Repository Push Utility
echo ======================================================================
echo.
echo Step 1: Go to https://github.com/new and create a new empty repository.
echo Step 2: Copy the HTTPS URL of your repository (e.g. https://github.com/username/repo.git)
echo.
set /p REPO_URL="Paste your GitHub Repository URL here: "

if "%REPO_URL%"=="" (
    echo [ERROR] No repository URL provided!
    pause
    exit /b
)

echo.
echo Configuring Git repository and pushing to %REPO_URL% ...
git init
git add .
git commit -m "Complete Frontend and Backend implementation for Dynamic Syllabus Management System" 2>nul
git branch -M main
git remote remove origin 2>nul
git remote add origin "%REPO_URL%"
git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ======================================================================
    echo   [SUCCESS] Project successfully pushed to GitHub!
    echo   Visit: %REPO_URL%
    echo ======================================================================
) else (
    echo ======================================================================
    echo   [INFO] Please check your GitHub URL or sign-in prompt and try again.
    echo ======================================================================
)
pause
