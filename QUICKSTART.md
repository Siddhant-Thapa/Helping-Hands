# Quick Start Guide - Helping Hands Setup

## ⚡ 60-Second Setup

### Windows (Batch)

```cmd
setup.bat
```

### Windows (PowerShell)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

### Linux/macOS

```bash
chmod +x setup.sh
./setup.sh
```

---

## 🔍 What the Setup Scripts Do

1. ✅ Check Python installation
2. ✅ Create Python virtual environment
3. ✅ Install all dependencies from `requirements.txt`
4. ✅ (Optional) Run database migrations
5. ✅ (Optional) Seed sample data
6. ✅ Activate virtual environment

---

## 📋 After Setup

### 1. Configure Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
# Edit .env with your database credentials and settings
```

### 2. Ensure PostgreSQL is Running

- **Windows:** Start PostgreSQL service
- **Linux:** `sudo systemctl start postgresql`
- **macOS:** `brew services start postgresql`

### 3. Run the Application

```bash
python run.py
```

### 4. Open in Browser

```
http://localhost:5000
```

---

## 🆕 First Time Using This Project?

1. **Read** [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for detailed setup
2. **Run** the appropriate setup script for your OS
3. **Configure** the `.env` file with your database details
4. **Start** the application with `python run.py`
5. **Visit** http://localhost:5000

---

## 🔄 Running Again

Once setup is complete, to run the app again:

### Windows

```cmd
venv\Scripts\activate.bat
python run.py
```

### Linux/macOS

```bash
source venv/bin/activate
python run.py
```

---

## ❌ Issues?

- **Check** [SETUP_INSTRUCTIONS.md - Troubleshooting](SETUP_INSTRUCTIONS.md#-troubleshooting)
- **Verify** Python & PostgreSQL are installed
- **Ensure** `.env` file has correct database credentials
- **Confirm** PostgreSQL is running

---

## 📁 Important Files

- `setup.bat` - Windows batch setup
- `setup.ps1` - Windows PowerShell setup
- `setup.sh` - Linux/macOS bash setup
- `.env.example` - Environment configuration template
- `SETUP_INSTRUCTIONS.md` - Complete setup guide
- `requirements.txt` - Python dependencies

---

## 📞 Need More Help?

See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for:

- Detailed step-by-step instructions
- Manual setup without scripts
- Database setup guide
- Troubleshooting tips
- Security best practices

---

**Happy coding! 🚀**
