@echo off
REM AIOS Backend Setup Script for Windows

echo.
echo 🚀 AIOS Backend Setup
echo =====================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ %PYTHON_VERSION% found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo ✓ Dependencies installed

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo ✓ .env file created (update with your database credentials)
)

echo.
echo ✅ Setup Complete!
echo.
echo Next steps:
echo 1. Update .env file with your PostgreSQL credentials
echo 2. Create PostgreSQL database:
echo    psql -U postgres -c "CREATE USER aios_user WITH PASSWORD 'aios_password';"
echo    psql -U postgres -c "CREATE DATABASE aios_db OWNER aios_user;"
echo.
echo 3. Seed sample data:
echo    python seed_data.py
echo.
echo 4. Run the server:
echo    uvicorn app.main:app --reload
echo.
echo 📖 API Documentation will be available at: http://localhost:8000/docs
echo.
pause
