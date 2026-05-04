@echo off
REM Network Port Scanner - CLI Launcher for Windows
REM Run this file to start the CLI version

cls
echo.
echo ========================================
echo   Network Port Scanner - CLI Edition
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo Error: main.py not found!
    echo Make sure you're running this from the correct directory.
    pause
    exit /b 1
)

REM Run the scanner
echo Starting Network Port Scanner...
echo.

python main.py

echo.
echo ========================================
echo   Scan Complete!
echo ========================================
pause
