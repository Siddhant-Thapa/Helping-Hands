# Helping Hands - Project Setup Script for Windows (PowerShell)
# This script sets up the project on Windows systems using PowerShell

# Color output functions
function Write-Success {
    Write-Host "[✓] $args" -ForegroundColor Green
}

function Write-Error {
    Write-Host "[ERROR] $args" -ForegroundColor Red
}

function Write-Warning {
    Write-Host "[!] $args" -ForegroundColor Yellow
}

function Write-Info {
    Write-Host "[*] $args" -ForegroundColor Cyan
}

# Main setup script
Write-Host ""
Write-Host "=========================================" -ForegroundColor Blue
Write-Host "  Helping Hands - Setup Script (PowerShell)" -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue
Write-Host ""

# Check if Python is installed
Write-Info "Checking if Python is installed..."
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python is installed: $pythonVersion"
} catch {
    Write-Error "Python is not installed or not in PATH"
    Write-Host "Please install Python 3.9+ from https://www.python.org/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Git is installed (optional)
Write-Info "Checking if Git is installed..."
try {
    $gitVersion = git --version 2>&1
    Write-Success "Git is installed: $gitVersion"
} catch {
    Write-Warning "Git is not installed (optional, but recommended for version control)"
}

Write-Host ""
Write-Info "Step 1: Creating virtual environment..."
if (Test-Path "venv") {
    Write-Warning "Virtual environment already exists. Skipping creation."
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Virtual environment created"
    } else {
        Write-Error "Failed to create virtual environment"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Info "Step 2: Activating virtual environment..."
& ".\venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -eq 0) {
    Write-Success "Virtual environment activated"
} else {
    Write-Error "Failed to activate virtual environment"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Info "Step 3: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Success "Dependencies installed"
} else {
    Write-Error "Failed to install dependencies"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Info "Step 4: Setting up database..."
Write-Host "Please ensure PostgreSQL is installed and running on your system."
Write-Host ""

$dbSetup = Read-Host "Do you want to run database migrations? (y/n)"
if ($dbSetup -eq "y" -or $dbSetup -eq "Y") {
    flask db upgrade
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Database migrations completed"
    } else {
        Write-Warning "Database migration encountered an issue"
        Write-Host "Please check your database connection and Flask configuration"
    }
}

Write-Host ""
$seedDb = Read-Host "Do you want to seed the database with sample data? (y/n)"
if ($seedDb -eq "y" -or $seedDb -eq "Y") {
    python seed_db.py
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Database seeded with sample data"
    } else {
        Write-Warning "Database seeding encountered an issue"
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Blue
Write-Host "    Setup Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Blue
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Configure your .env file with database credentials and settings"
Write-Host "2. Make sure PostgreSQL is running"
Write-Host "3. Run the application with: python run.py"
Write-Host "4. Open your browser and navigate to: http://localhost:5000"
Write-Host ""
Write-Host "The virtual environment is already activated in this terminal."
Write-Host ""
Read-Host "Press Enter to exit"
