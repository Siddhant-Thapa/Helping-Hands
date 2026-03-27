# Documentation Index

Welcome to the Helping Hands documentation! This folder contains all the guides you need to get started and maintain the project.

## 📚 Documentation Files

### [QUICKSTART.md](QUICKSTART.md) ⚡

Get up and running in 60 seconds. Contains quick setup commands for different operating systems.

**Best for:** First-time users who want to start immediately

### [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) 🚀

Comprehensive setup guide with step-by-step instructions, troubleshooting, and manual setup options.

**Best for:** Detailed setup walkthrough and problem solving

### [DATABASE.md](DATABASE.md) 🗄️

Complete database setup, configuration, and troubleshooting guide for PostgreSQL.

**Best for:** Database-related questions and configuration

### [DEPLOYMENT.md](../deploy/DEPLOYMENT.md) 🌐

Production deployment guide, server setup, and best practices.

**Best for:** Deploying to remote servers and production environments

## 🗂️ Organization

This project follows industry-standard folder structure:

```
Helping_Hands/
├── docs/                          # ← You are here
│   ├── QUICKSTART.md             # Quick 60-second setup
│   ├── SETUP_INSTRUCTIONS.md     # Detailed setup guide
│   ├── DATABASE.md               # Database configuration
│   └── README.md                 # This file
├── deploy/                        # Deployment scripts and guides
│   ├── setup.bat                 # Windows setup script
│   ├── setup.ps1                 # PowerShell setup script
│   ├── setup.sh                  # Bash setup script
│   ├── DEPLOYMENT.md             # Production deployment
│   └── README.md                 # Deploy folder guide
└── [other project files]
```

## 🚀 Quick Navigation

**I want to...**

- **Get started quickly** → [QUICKSTART.md](QUICKSTART.md)
- **Detailed setup walkthrough** → [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)
- **Set up the database** → [DATABASE.md](DATABASE.md)
- **Deploy to production** → [DEPLOYMENT.md](../deploy/DEPLOYMENT.md)
- **Understand the project structure** → See structure above

## 📋 Prerequisites

- Python 3.9 or higher
- PostgreSQL 13 or higher
- Git (recommended)

## ⚡ TL;DR (Quick Start)

```bash
# Windows (PowerShell)
cd deploy
.\setup.ps1

# Linux/macOS
cd deploy
bash setup.sh
```

Then:

1. Configure `.env` file
2. Run `python run.py`
3. Visit `http://localhost:5000`

## 🆘 Troubleshooting

- **Setup issues** → [SETUP_INSTRUCTIONS.md#-troubleshooting](SETUP_INSTRUCTIONS.md#-troubleshooting)
- **Database issues** → [DATABASE.md](DATABASE.md)
- **Deployment issues** → [DEPLOYMENT.md](../deploy/DEPLOYMENT.md)

## 📞 Need Help?

1. Check the relevant documentation file
2. Review the troubleshooting section
3. Check the application logs

---

**Last Updated:** February 2026
