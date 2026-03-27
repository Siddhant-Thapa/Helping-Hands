#!/bin/bash

# Helping Hands - Project Setup Script for Linux/macOS
# This script sets up the project on Unix-based systems
# Location: deploy/setup.sh

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions for colored output
print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_info() {
    echo -e "${CYAN}[*]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}=========================================${NC}"
    echo -e "${BLUE}  Helping Hands - Setup Script (Unix)   ${NC}"
    echo -e "${BLUE}=========================================${NC}"
    echo ""
}

# Get the project root directory (parent of deploy folder)
cd "$(dirname "$0")/.."

# Main setup script
print_header

# Check if Python is installed
print_info "Checking if Python is installed..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    echo "Please install Python 3.9+ using your package manager:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-venv"
    echo "  macOS: brew install python3"
    exit 1
fi

python_version=$(python3 --version)
print_success "Python is installed: $python_version"

# Check if Git is installed (optional)
print_info "Checking if Git is installed..."
if command -v git &> /dev/null; then
    git_version=$(git --version)
    print_success "Git is installed: $git_version"
else
    print_warning "Git is not installed (optional, but recommended for version control)"
fi

# Check if pip is installed
print_info "Checking if pip is installed..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed"
    echo "Please install pip3 using your package manager:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-pip"
    echo "  macOS: brew install python3-pip"
    exit 1
fi

print_success "pip3 is installed"

echo ""
print_info "Step 1: Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
fi

echo ""
print_info "Step 2: Activating virtual environment..."
source venv/bin/activate
if [ $? -eq 0 ]; then
    print_success "Virtual environment activated"
else
    print_error "Failed to activate virtual environment"
    exit 1
fi

echo ""
print_info "Step 3: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "Dependencies installed"
else
    print_error "Failed to install dependencies"
    exit 1
fi

echo ""
print_info "Step 4: Setting up database..."
echo "Please ensure PostgreSQL is installed and running on your system."
echo ""

read -p "Do you want to run database migrations? (y/n): " -r db_setup
if [[ $db_setup =~ ^[Yy]$ ]]; then
    flask db upgrade
    if [ $? -eq 0 ]; then
        print_success "Database migrations completed"
    else
        print_warning "Database migration encountered an issue"
        echo "Please check your database connection and Flask configuration"
    fi
fi

echo ""
read -p "Do you want to seed the database with sample data? (y/n): " -r seed_db
if [[ $seed_db =~ ^[Yy]$ ]]; then
    python seed_db.py
    if [ $? -eq 0 ]; then
        print_success "Database seeded with sample data"
    else
        print_warning "Database seeding encountered an issue"
    fi
fi

echo ""
echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}    Setup Complete!${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo "1. Configure your .env file with database credentials and settings"
echo "2. Make sure PostgreSQL is running"
echo "3. Run the application with: python run.py"
echo "4. Open your browser and navigate to: http://localhost:5000"
echo ""
echo "The virtual environment is already activated in this terminal."
echo ""
