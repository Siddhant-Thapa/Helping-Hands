# Deployment & Setup Scripts

This folder contains automated setup scripts for deploying and initializing the Helping Hands project on any system.

## 📂 Contents

### Setup Scripts

- **setup.bat** - Windows batch setup script
- **setup.ps1** - Windows PowerShell setup script (recommended for Windows)
- **setup.sh** - Linux/macOS bash setup script

### Documentation

- **DEPLOYMENT.md** - Production deployment guide
- **README.md** - This file

## ⚡ Quick Start

### Windows (Recommended)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

### Windows (Alternative)

```cmd
setup.bat
```

### Linux/macOS

```bash
bash setup.sh
```

## 🚀 What the Setup Scripts Do

The setup scripts automate the following steps:

1. ✅ Verify Python 3.9+ is installed
2. ✅ Verify Git is installed (optional but recommended)
3. ✅ Create Python virtual environment
4. ✅ Activate virtual environment
5. ✅ Install dependencies from `requirements.txt`
6. ✅ Run database migrations (optional, interactive)
7. ✅ Seed sample data (optional, interactive)

## 💡 Features

- **Idempotent**: Safe to run multiple times
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Interactive**: Prompts for optional steps
- **Error Handling**: Validates prerequisites and handles errors gracefully
- **Colored Output**: Clear visual feedback (PowerShell & Bash)

## 📋 System Requirements

### Minimum Requirements

- Python 3.9+
- PostgreSQL 13+
- 50 MB disk space (plus dependencies)
- 512 MB RAM

### Recommended Requirements

- Python 3.10+
- PostgreSQL 14+
- 200 MB disk space
- 1 GB RAM

## 🔍 Script Details

### setup.ps1 (PowerShell - Recommended)

**Advantages:**

- Colored output for better readability
- Better error handling
- Cross-platform compatible
- More modern approach

**Permissions:**

```powershell
# Allow script execution (one-time setup)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use for single script execution
powershell -ExecutionPolicy Bypass -File setup.ps1
```

### setup.bat (Windows Batch)

**Advantages:**

- No permissions needed
- Works on all Windows versions
- Simpler to understand

**Usage:**

```cmd
cd path\to\deploy
setup.bat
```

### setup.sh (Bash - Linux/macOS)

**Advantages:**

- Universal on Unix systems
- Colored output
- Port script options

**Permissions:**

```bash
chmod +x setup.sh
bash setup.sh
```

## 📖 Next Steps

After running setup:

1. **Review Documentation:**
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
   - [../docs/SETUP_INSTRUCTIONS.md](../docs/SETUP_INSTRUCTIONS.md) - Detailed setup
   - [../docs/DATABASE.md](../docs/DATABASE.md) - Database configuration

2. **Configure Application:**
   - Edit `.env` with database credentials
   - Review Flask configuration
   - Set up email (if needed)

3. **Run Application:**

   ```bash
   python run.py
   ```

4. **Access Application:**
   - Open browser: `http://localhost:5000`

## 🐛 Troubleshooting

### Python Not Found

```cmd
# Windows: Reinstall Python with "Add to PATH"
# Linux/macOS: Use python3 instead of python
```

### Permission Denied (PowerShell)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Virtual Environment Issues

```bash
# Delete and recreate
rm -r venv
python -m venv venv
```

### Database Connection Failed

- Ensure PostgreSQL is running
- Check `.env` file contains correct
  credentials
- See [../docs/DATABASE.md](../docs/DATABASE.md)

## 🔐 Security Notes

1. **Environment Variables:**
   - Never commit `.env` file
   - Use strong passwords
   - Rotate credentials regularly

2. **Script Execution:**
   - Review scripts before running
   - Use from trusted sources only
   - Keep updated with project changes

3. **Database:**
   - Use strong passwords
   - Configure PostgreSQL authentication
   - Regular backups

## 📚 Documentation Structure

```
Helping_Hands/
├── deploy/                    ← You are here
│   ├── setup.bat
│   ├── setup.ps1
│   ├── setup.sh
│   ├── DEPLOYMENT.md          # Production deployment
│   └── README.md              # This file
├── docs/                      # Full documentation
│   ├── QUICKSTART.md
│   ├── SETUP_INSTRUCTIONS.md
│   ├── DATABASE.md
│   └── README.md
└── [other project files]
```

## ✅ Post-Setup Checklist

- [ ] Setup script completed successfully
- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] `.env` file configured
- [ ] Database migrations completed
- [ ] Application starts without errors
- [ ] Can access http://localhost:5000
- [ ] Sample data seeded (optional)

## 🆘 Need Help?

1. **Quick Setup:** Check [QUICKSTART.md](../docs/QUICKSTART.md)
2. **Detailed Setup:** Read [SETUP_INSTRUCTIONS.md](../docs/SETUP_INSTRUCTIONS.md)
3. **Database Issues:** See [DATABASE.md](../docs/DATABASE.md)
4. **Production Deploy:** Read [DEPLOYMENT.md](DEPLOYMENT.md)

## 📞 Support Resources

- PostgreSQL: https://www.postgresql.org/docs/
- Flask: https://flask.palletsprojects.com/
- Python: https://docs.python.org/
- Issues: Check project README

---

**Last Updated:** February 2026
