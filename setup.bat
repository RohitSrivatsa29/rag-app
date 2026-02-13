@echo off
REM RAG Application Setup Script for Windows

echo ================================================
echo RAG Application Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

echo √ Python found
python --version

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo X Node.js is not installed. Please install Node.js 18 or higher.
    pause
    exit /b 1
)

echo √ Node.js found
node --version
echo.

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo X Failed to install Python dependencies
    pause
    exit /b 1
)
echo √ Python dependencies installed successfully
echo.

REM Build frontend
echo Building frontend...
cd frontend
call npm install
if errorlevel 1 (
    echo X Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
)
echo √ Frontend dependencies installed

call npm run build
if errorlevel 1 (
    echo X Failed to build frontend
    cd ..
    pause
    exit /b 1
)
echo √ Frontend built successfully
cd ..
echo.

REM Check for data files
dir /b data\*.json >nul 2>&1
if errorlevel 1 (
    echo ! Warning: No JSON files found in data\ folder
    echo   Please add your data files to data\ folder before running the app
) else (
    echo √ JSON files found in data\ folder
)
echo.

echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo To start the application:
echo   python app.py
echo.
echo Then visit: http://localhost:8000
echo.
echo To deploy to Render:
echo   See DEPLOYMENT.md for detailed instructions
echo.
pause
