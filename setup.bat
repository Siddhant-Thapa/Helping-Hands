@echo off
REM Helping Hands - Project Setup Script for Windows
REM This script sets up the project on Windows systems

echo.
echo =========================================
echo   Helping Hands - Setup Script (Windows)
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo [✓] Python is installed
python --version

REM Check if Git is installed (optional but recommended)
git --version >nul 2>&1
if errorlevel 1 (
    echo [!] Git is not installed (optional, but recommended for version control)
) else (
    echo [✓] Git is installed
)

echo.
echo Step 1: Creating virtual environment...
if exist venv (
    echo [!] Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [✓] Virtual environment created
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [✓] Virtual environment activated

echo.
echo Step 3: Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [✓] Dependencies installed

echo.
echo Step 4: Setting up database...
echo Please ensure PostgreSQL is installed and running on your system.
echo.
set /p db_setup="Do you want to run database migrations? (y/n): "
if /i "%db_setup%"=="y" (
    flask db upgrade
    if errorlevel 1 (
        echo [!] Database migration encountered an issue
        echo Please check your database connection and Flask configuration
    ) else (
        echo [✓] Database migrations completed
    )
)

echo.
set /p seed_db="Do you want to seed the database with sample data? (y/n): "
if /i "%seed_db%"=="y" (
    python seed_db.py
    if errorlevel 1 (
        echo [!] Database seeding encountered an issue
    ) else (
        echo [✓] Database seeded with sample data
    )
)

echo.
echo =========================================
echo    Setup Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Configure your .env file with database credentials and settings
echo 2. Make sure PostgreSQL is running
echo 3. Run the application with: python run.py
echo 4. Open your browser and navigate to: http://localhost:5000
echo.
echo The virtual environment is already activated in this terminal.
echo.
pause
