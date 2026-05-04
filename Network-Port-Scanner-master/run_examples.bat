@echo off
REM Network Port Scanner - Examples Launcher for Windows
REM Run this file to see example usage patterns

cls
echo.
echo ========================================
echo   Network Port Scanner - Examples
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

REM Check if EXAMPLES.py exists
if not exist "EXAMPLES.py" (
    echo Error: EXAMPLES.py not found!
    echo Make sure you're running this from the correct directory.
    pause
    exit /b 1
)

REM Run the examples
echo Running examples (this will scan localhost)...
echo.

python EXAMPLES.py

if errorlevel 1 (
    echo.
    echo An error occurred while running examples.
    echo Check if you have proper permissions.
    pause
)

echo.
echo ========================================
echo   Examples Complete!
echo ========================================
pause
