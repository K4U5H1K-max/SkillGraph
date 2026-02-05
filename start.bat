@echo off
echo ================================================
echo  Starting Personalized Learning Roadmap App
echo ================================================
echo.

echo [1/2] Starting Flask Backend API...
start "Backend API" cmd /k "python app.py"

timeout /t 3 /nobreak > nul

echo.
echo ================================================
echo  Application Started!
echo ================================================
echo.
echo  Backend API: http://localhost:5000
echo  Landing Page: http://localhost:5000
echo.
echo  Opening browser in 3 seconds...
timeout /t 3 /nobreak > nul

start http://localhost:5000

echo.
echo  Press any key to stop all servers...
pause > nul
taskkill /FI "WINDOWTITLE eq Backend API*" /F > nul 2>&1
exit
echo Backend API: http://localhost:5000
echo Frontend:    http://localhost:8000
echo.
echo Open your browser to: http://localhost:8000
echo.
echo Press Ctrl+C in each terminal window to stop
echo ================================================
