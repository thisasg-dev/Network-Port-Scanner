@echo off
REM Network Port Scanner - Test Suite Launcher for Windows
REM Run this file to verify the scanner is working correctly

cls
echo.
echo ========================================
echo   Network Port Scanner - Test Suite
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

REM Check if test_scanner.py exists
if not exist "test_scanner.py" (
    echo Error: test_scanner.py not found!
    echo Make sure you're running this from the correct directory.
    pause
    exit /b 1
)

REM Run the test suite
echo Running test suite...
echo.

python test_scanner.py

echo.
echo ========================================
echo   Test Suite Complete!
echo ========================================
pause
