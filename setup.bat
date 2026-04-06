@echo off
REM Job Description Pipeline - Quick Start Script for Windows

echo.
echo ================================
echo Job Description Pipeline Setup
echo ================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python found: %PYTHON_VERSION%
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📥 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Create .env from .env.example if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo.
    echo ⚠️  Please edit .env with your API keys:
    echo    - OPENAI_API_KEY
    echo    - SUPABASE_URL
    echo    - SUPABASE_KEY
)

REM Create uploads directory
echo 📁 Creating uploads directory...
if not exist uploads mkdir uploads

echo.
echo ================================
echo ✓ Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Edit .env file with your credentials
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000
echo.
pause
