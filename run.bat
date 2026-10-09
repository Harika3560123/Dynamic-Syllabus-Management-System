@echo off
title Dynamic Syllabus Management System - SREC Nandyal
echo ======================================================================
echo    SANTHIRAM ENGINEERING COLLEGE (AUTONOMOUS) - NANDYAL
echo    Department of Computer Science & Engineering
echo    Dynamic Syllabus Management for Higher Studies
echo ======================================================================
echo.
echo Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH! Please install Python 3.
    pause
    exit /b
)

echo Starting Flask Backend Server (backend/app.py)...
echo Serving Frontend from: frontend/
echo Server URL: http://localhost:5000
echo.

start "" "http://localhost:5000"
cd backend
python app.py

pause
