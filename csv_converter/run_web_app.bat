@echo off
REM CSV to Excel Converter - Web App Startup Script

echo.
echo =========================================
echo   CSV to Excel Converter - Web App
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

REM Start the Flask app
echo.
echo =========================================
echo   Starting Web App on http://localhost:5000
echo =========================================
echo.
echo Press CTRL+C to stop the server
echo.

python app.py

pause