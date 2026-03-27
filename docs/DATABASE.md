# Database Setup & Configuration Guide

This guide covers all aspects of database setup, configuration, and troubleshooting for the Helping Hands project.

## 📋 Prerequisites

- **PostgreSQL 13 or higher** installed and running
- **psql** command-line tool (usually comes with PostgreSQL)
- **pgAdmin** (optional, for GUI management)

## ✅ Verify PostgreSQL Installation

```bash
# Check PostgreSQL version
psql --version

# Check if PostgreSQL is running
# Windows
sc query postgresql-x64-14  # Replace 14 with your version

# Linux
sudo systemctl status postgresql

# macOS
brew services list | grep postgres
```

---

## 🗄️ Database Creation Methods

### Method 1: Using SQL Scripts (Recommended for Production)

#### Step 1: Connect to PostgreSQL as Admin

```bash
psql -U postgres
```

#### Step 2: Run Database Setup Script

```sql
-- Create database
CREATE DATABASE helping_hands;

-- Create database user
CREATE USER helping_hands_user WITH PASSWORD 'your_secure_password';

-- Set default encoding and transaction settings
ALTER ROLE helping_hands_user SET client_encoding TO 'utf8';
ALTER ROLE helping_hands_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE helping_hands_user SET default_transaction_deferrable TO on;

-- Grant all privileges to the user
GRANT ALL PRIVILEGES ON DATABASE helping_hands TO helping_hands_user;

-- Connect to the new database
\c helping_hands

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO helping_hands_user;

-- Exit psql
\q
```

### Method 2: Using pgAdmin (GUI)

1. **Open pgAdmin** and log in
2. **Right-click on "Databases"** → **Create** → **Database**
3. **Enter details:**
   - Name: `helping_hands`
   - Owner: Create new user with password
4. **Create the database**
5. **Update `.env`** with connection credentials

### Method 3: Using Command Line (Simple)

```bash
# Create database
createdb -U postgres helping_hands

# Create user
psql -U postgres -d helping_hands -c "CREATE USER helping_hands_user WITH PASSWORD 'your_password';"

# Grant privileges
psql -U postgres -d helping_hands -c "GRANT ALL PRIVILEGES ON DATABASE helping_hands TO helping_hands_user;"
```

---

## 🔐 Environment Configuration

### Create .env File

Copy the template:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
# Database URL format:
# postgresql://username:password@host:port/database_name

DATABASE_URL=postgresql://helping_hands_user:your_secure_password@localhost:5432/helping_hands

# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# Optional: Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Security Best Practices

1. **Use strong passwords:**
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, and special characters
   - Example: `P@ssw0rd!SecureDbPw2024`

2. **Don't commit `.env` file:**

   ```bash
   # Check .gitignore contains .env
   grep ".env" .gitignore
   ```

3. **Rotate passwords regularly** in production

4. **Use environment variables** for sensitive data:
   ```bash
   export DATABASE_URL="postgresql://user:pass@host/db"
   export SECRET_KEY="your-secret-key"
   ```

---

## 🚀 Database Initialization

### Step 1: Verify Connection

```bash
# Test database connection
psql -U helping_hands_user -h localhost -d helping_hands -c "SELECT version();"
```

### Step 2: Run Migrations

```bash
# Activate virtual environment first
# Windows
venv\Scripts\activate.bat

# Linux/macOS
source venv/bin/activate

# Run migrations
flask db upgrade
```

### Step 3: Verify Migrations

```bash
# Check migration history
flask db current

# List all migrations
flask db history
```

### Step 4: Seed Sample Data (Optional)

```bash
python seed_db.py
```

---

## 📊 Database Management

### View Database Information

```sql
-- List all databases
\l

-- Connect to a database
\c helping_hands

-- List all tables
\dt

-- Describe a table
\d table_name

-- List all users
\du
```

### Backup Database

#### Using pg_dump

```bash
# Backup entire database
pg_dump -U helping_hands_user -h localhost helping_hands > backup.sql

# Backup with compression
pg_dump -U helping_hands_user -h localhost helping_hands | gzip > backup.sql.gz

# Backup specific table
pg_dump -U helping_hands_user -h localhost -t table_name helping_hands > table_backup.sql
```

#### Using pgAdmin

1. Right-click on database → **Backup**
2. Choose backup format and options
3. Save the backup file

### Restore Database

#### From SQL File

```bash
# Restore entire database
psql -U helping_hands_user -h localhost -d helping_hands < backup.sql

# Restore from compressed file
gunzip < backup.sql.gz | psql -U helping_hands_user -h localhost -d helping_hands
```

#### Using pgAdmin

1. Right-click on database → **Restore**
2. Select backup file
3. Configure restore options
4. Execute restore

---

## 🔧 Database Maintenance

### Check Database Health

```sql
-- Connect to database
psql -U helping_hands_user -h localhost -d helping_hands

-- Check database size
SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname))
FROM pg_database;

-- Analyze query performance
ANALYZE;

-- Vacuum (cleanup dead rows)
VACUUM ANALYZE;
```

### Reset Database (Development Only)

```bash
# Drop and recreate database
dropdb -U postgres helping_hands
createdb -U postgres helping_hands
psql -U postgres -d helping_hands -c "GRANT ALL PRIVILEGES ON DATABASE helping_hands TO helping_hands_user;"

# Run migrations from scratch
flask db upgrade
python seed_db.py
```

---

## 🐛 Troubleshooting

### Connection Refused

**Error:** `psql: could not connect to server: Connection refused`

**Solutions:**

1. **Check PostgreSQL is running:**

   ```bash
   # Windows
   sc start postgresql-x64-14

   # Linux
   sudo systemctl start postgresql

   # macOS
   brew services start postgresql
   ```

2. **Verify connection parameters:**

   ```bash
   # Test connection
   psql -U helping_hands_user -h localhost -d helping_hands

   # Check .env file for correct credentials
   cat .env | grep DATABASE_URL
   ```

### Authentication Failed

**Error:** `error: FATAL: password authentication failed`

**Solutions:**

1. **Verify password is correct:**

   ```bash
   psql -U helping_hands_user -h localhost -d helping_hands
   # Enter password at prompt
   ```

2. **Reset user password:**

   ```sql
   -- Connect as postgres
   psql -U postgres

   -- Reset password
   ALTER USER helping_hands_user WITH PASSWORD 'new_secure_password';

   -- Update .env file with new password
   ```

3. **Check pg_hba.conf:**
   - Location: `/etc/postgresql/*/main/pg_hba.conf` (Linux)
   - Location: `C:\Program Files\PostgreSQL\14\data\pg_hba.conf` (Windows)
   - Ensure connection method allows password authentication

### Database Already Exists

**Error:** `ERROR: database "helping_hands" already exists`

**Solutions:**

```bash
# Check existing databases
psql -U postgres -l

# Drop existing database (WARNING: data loss!)
dropdb -U postgres helping_hands

# Or use in psql
psql -U postgres
DROP DATABASE helping_hands;
```

### Permission Denied

**Error:** `ERROR: permission denied to create database`

**Solution:**

```sql
-- Connect as postgres
psql -U postgres

-- Grant superuser or createdb role
ALTER USER helping_hands_user CREATEDB;

-- Or use postgres user to create database
CREATE DATABASE helping_hands OWNER helping_hands_user;
```

### Migration Failures

**Error:** `ImportError` or `ModuleNotFoundError` during migration

**Solutions:**

1. **Reinstall dependencies:**

   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

2. **Check Flask-SQLAlchemy configuration:**
   - Verify `DATABASE_URL` in `.env`
   - Ensure database exists and user has permissions

3. **Run migrations with verbose output:**
   ```bash
   flask db upgrade --verbose
   ```

### Port Already in Use

**Error:** `ERROR: could not bind IPv4 socket`

**Solution:**

```bash
# Find process using port 5432 (default PostgreSQL port)
# Windows
netstat -ano | findstr :5432

# Linux/macOS
lsof -i :5432

# Kill process and restart PostgreSQL
```

---

## 📈 Performance Tuning

### Basic Optimization

```sql
-- Update query statistics
ANALYZE;

-- Clean up dead rows
VACUUM ANALYZE;

-- Create indexes for frequently queried columns
-- (done via migrations, not here)
```

### Monitor Connections

```sql
-- View active connections
SELECT pid, usename, application_name, state, query
FROM pg_stat_activity;

-- Terminate long-running query
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE pid <> pg_backend_pid();
```

---

## 🔐 Security Checklist

- [ ] Database user has strong password
- [ ] Database credentials in `.env` (not in code)
- [ ] `.env` is in `.gitignore`
- [ ] PostgreSQL is configured for authentication
- [ ] Regular backups are performed
- [ ] User has minimal required privileges
- [ ] Connections use passwords (not trust authentication)
- [ ] Consider SSL connections for remote PostgreSQL

---

## 📚 Additional Resources

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

**Last Updated:** February 2026
