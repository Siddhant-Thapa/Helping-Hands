# Helping Hands - Setup Instructions

This document provides step-by-step instructions for setting up the Helping Hands project on any system.

## 📋 Prerequisites

Before running the setup script, please ensure you have the following installed:

### Required

- **Python 3.9 or higher** - [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 13 or higher** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git** (optional but recommended) - [Download Git](https://git-scm.com/downloads)

### Verify Installation

Run these commands to verify everything is installed:

```bash
# Check Python version
python --version
# or
python3 --version

# Check PostgreSQL version
psql --version

# Check Git version (optional)
git --version
```

---

## 🚀 Quick Setup Guide

### Option 1: Windows (Batch Script)

1. **Open Command Prompt** (cmd.exe) or **PowerShell**
2. **Navigate to the project directory:**
   ```cmd
   cd path\to\Helping_Hands
   ```
3. **Run the setup script:**
   ```cmd
   setup.bat
   ```
4. **Follow the prompts** - The script will:
   - Create a virtual environment
   - Install all dependencies
   - Optionally run database migrations
   - Optionally seed sample data

### Option 2: Windows (PowerShell)

1. **Open PowerShell as Administrator**
2. **Navigate to the project directory:**
   ```powershell
   cd path\to\Helping_Hands
   ```
3. **Enable script execution (if needed):**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
4. **Run the setup script:**
   ```powershell
   .\setup.ps1
   ```
5. **Follow the prompts**

### Option 3: Linux/macOS (Bash)

1. **Open Terminal**
2. **Navigate to the project directory:**
   ```bash
   cd /path/to/Helping_Hands
   ```
3. **Make the script executable:**
   ```bash
   chmod +x setup.sh
   ```
4. **Run the setup script:**
   ```bash
   ./setup.sh
   ```
5. **Follow the prompts**

---

## 🔧 Manual Setup (Step-by-Step)

If you prefer to set up manually or encounter issues with the scripts:

### 1. Create Virtual Environment

**Windows:**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Database

**Create a PostgreSQL database:**

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE helping_hands;

-- Create user (if needed)
CREATE USER helping_hands_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
ALTER ROLE helping_hands_user SET client_encoding TO 'utf8';
ALTER ROLE helping_hands_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE helping_hands_user SET default_transaction_deferrable TO on;
ALTER ROLE helping_hands_user SET default_transaction_read_committed TO off;
GRANT ALL PRIVILEGES ON DATABASE helping_hands TO helping_hands_user;
```

### 4. Configure Environment Variables

**Create a `.env` file in the project root:**

```env
# Database Configuration
DATABASE_URL=postgresql://helping_hands_user:your_secure_password@localhost:5432/helping_hands

# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-this-in-production

# Email Configuration (if using email features)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# App Configuration
APP_TITLE=Helping Hands
APP_DEBUG=True
```

### 5. Run Database Migrations

```bash
flask db upgrade
```

### 6. Seed Sample Data (Optional)

```bash
python seed_db.py
```

### 7. Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

---

## 📊 Database Setup Details

### Creating the Database Manually

If the setup script doesn't handle database creation, follow these steps:

#### Using psql (Command Line)

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE helping_hands;
CREATE USER helping_hands_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE helping_hands TO helping_hands_user;

# Exit psql
\q
```

#### Using pgAdmin (GUI Application)

1. Open pgAdmin
2. Right-click on "Databases" → "Create" → "Database"
3. Enter name: `helping_hands`
4. Create a user for the database
5. Update your `.env` file with connection details

---

## ✅ Verification Checklist

After setup, verify everything is working:

- [ ] Virtual environment is created and activated
- [ ] All dependencies are installed (`pip list` should show Flask, SQLAlchemy, etc.)
- [ ] PostgreSQL is running and accessible
- [ ] Database is created and migrations are applied
- [ ] Application starts without errors (`python run.py`)
- [ ] You can access the app at `http://localhost:5000`
- [ ] Database migrations completed successfully
- [ ] (Optional) Sample data is seeded

---

## 🐛 Troubleshooting

### Python Not Found

**Problem:** "Python is not installed or not in PATH"

**Solution:**

- Reinstall Python and ensure "Add Python to PATH" is checked during installation
- For macOS/Linux, use `python3` instead of `python`

### Virtual Environment Not Activating

**Windows (Batch):**

```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### Database Connection Error

**Problem:** "Could not connect to database"

**Solution:**

- Ensure PostgreSQL is running
- Verify credentials in `.env` file
- Check if database exists: `psql -U postgres -l`
- Test connection: `psql -U helping_hands_user -h localhost -d helping_hands`

### Missing Dependencies

**Problem:** "ModuleNotFoundError: No module named..."

**Solution:**

```bash
# Ensure virtual environment is activated
pip install -r requirements.txt

# Or install specific package
pip install package_name
```

### Port 5000 Already in Use

**Problem:** "Address already in use"

**Solution:**

- Change the port in `run.py` or use:
  ```bash
  python run.py --port 5001
  ```
- Or kill the process using port 5000

### Permissions Error on Linux/macOS

**Problem:** "Permission denied" when running setup.sh

**Solution:**

```bash
chmod +x setup.sh
./setup.sh
```

---

## 📁 Project Structure

```
Helping_Hands/
├── app/                    # Main application package
│   ├── models.py          # Database models
│   ├── routes/            # Route handlers
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, images
│   └── utils/             # Helper functions
├── migrations/            # Database migration files
├── venv/                  # Virtual environment (created during setup)
├── requirements.txt       # Python dependencies
├── run.py                 # Application entry point
├── seed_db.py            # Database seeding script
├── setup.bat             # Windows batch setup script
├── setup.ps1             # Windows PowerShell setup script
├── setup.sh              # Linux/macOS bash setup script
└── README.md             # Project documentation
```

---

## 🚀 Running the Application

After setup is complete:

### Start the Application

**Windows (with virtual environment activated):**

```cmd
python run.py
```

**Linux/macOS:**

```bash
python run.py
```

### Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

### Default Credentials

Check the `seed_db.py` file or README.md for default admin credentials if sample data was seeded.

---

## 📦 Updating Dependencies

If you need to update dependencies later:

```bash
# Activate virtual environment (if not already active)
# Windows: venv\Scripts\activate.bat
# Linux/macOS: source venv/bin/activate

# Install new/updated dependencies
pip install -r requirements.txt

# Update requirements.txt with current versions
pip freeze > requirements.txt
```

---

## 🔐 Security Considerations

1. **Never commit `.env` file** - Add it to `.gitignore`
2. **Change `SECRET_KEY`** in production
3. **Use strong database passwords**
4. **Enable HTTPS** in production
5. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt` regularly

---

## ❓ Need Help?

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Verify all prerequisites are installed
3. Check the application logs for error messages
4. Review the main [README.md](README.md) for project-specific documentation

---

## 📝 Notes

- Scripts are designed to be idempotent (safe to run multiple times)
- Virtual environment is automatically activated by the scripts
- Database migrations are optional during setup (you can run them later)
- Sample data seeding is interactive and optional

---

**Happy Coding! 🎉**
