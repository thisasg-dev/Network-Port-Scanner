@echo off
REM Network Port Scanner - GUI Launcher for Windows
REM Run this file to start the GUI version

cls
echo.
echo ========================================
echo   Network Port Scanner - GUI Edition
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

REM Check if gui.py exists
if not exist "gui.py" (
    echo Error: gui.py not found!
    echo Make sure you're running this from the correct directory.
    pause
    exit /b 1
)

REM Run the GUI scanner
echo Starting Network Port Scanner GUI...
echo Launching in graphical mode...
echo.

python gui.py

if errorlevel 1 (
    echo.
    echo Error running GUI application!
    echo Make sure Tkinter is installed: python -m pip install tk
    pause
)
