@echo off
title SREC Dynamic Syllabus - Live Public HTTPS Tunnel
echo ======================================================================
echo    SANTHIRAM ENGINEERING COLLEGE - LIVE PUBLIC DEPLOYMENT TUNNEL
echo    Exposing local server (http://localhost:8000) to the Internet...
echo ======================================================================
echo.
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:127.0.0.1:8000 nokey@localhost.run
pause
