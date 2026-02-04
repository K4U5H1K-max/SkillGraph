@echo off
echo ================================================
echo  Starting Personalized Learning Roadmap App
echo ================================================
echo.

echo [1/2] Starting Flask Backend API...
start "Backend API" cmd /k "python app.py"

timeout /t 3 /nobreak > nul

echo [2/2] Starting Frontend Server...
cd frontend
start "Frontend Server" cmd /k "python -m http.server 8000"

echo.
echo ================================================
echo  Application Started!
echo ================================================
echo.
echo Backend API: http://localhost:5000
echo Frontend:    http://localhost:8000
echo.
echo Open your browser to: http://localhost:8000
echo.
echo Press Ctrl+C in each terminal window to stop
echo ================================================
