# Task Management API - Backend

A robust FastAPI-based REST API for task management with authentication, email verification, password reset, and comprehensive security features.

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Features](#features)
- [Security](#security)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## Overview

This backend API provides a complete task management system with:

- **User Authentication**: Registration, login, JWT tokens with refresh tokens
- **Email Verification**: Email-based account verification
- **Password Management**: Secure password reset functionality
- **Task Management**: CRUD operations for tasks with filtering, sorting, and pagination
- **Security Features**: Rate limiting, account locking, password validation
- **Caching**: Optional Redis caching for improved performance

---

## Tech Stack

- **Framework**: FastAPI 0.121.2
- **Server**: Uvicorn with auto-reload
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy 2.0.44
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Rate Limiting**: slowapi
- **Email**: aiosmtplib
- **Caching**: Redis (optional)
- **Validation**: Pydantic 2.12.4

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python**: 3.8 or higher (3.11+ recommended)
- **pip**: Python package manager
- **Git**: For version control
- **Virtual Environment**: Python venv module (included with Python 3.3+)

Optional:
- **Redis**: For caching (see [Redis Caching](#redis-caching-optional))
- **PostgreSQL**: For production deployment

---

## Quick Start

### Step 1: Clone and Navigate

```bash
# If you haven't already cloned the repository
git clone <repository-url>
cd task-management-assessment/backend
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create a `.env` file in the `backend` directory:

```bash
# Windows PowerShell
New-Item -ItemType File -Path .env

# Linux/Mac
touch .env
```

Add the following minimum configuration:

```env
# Database
DATABASE_URL=sqlite:///./backend.db
AUTO_CREATE_TABLES=true

# Security (Development - OK to use defaults)
SECRET_KEY=secret-key-change-in-production-MUST-BE-64-CHARS-MINIMUM-PLEASE-CHANGE
ENVIRONMENT=development

# CORS (Development - defaults to localhost if empty)
# CORS_ORIGINS=

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_AUTH_PER_MINUTE=5
```

### Step 5: Run the Application

```bash
# Make sure you're in the backend directory and venv is activated
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:
- **API Base**: http://127.0.0.1:8000
- **Interactive Docs**: http://127.0.0.1:8000/docs (Swagger UI)
- **Alternative Docs**: http://127.0.0.1:8000/redoc (ReDoc)

---

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   └── tasks.py         # Task management endpoints
│   │   └── dependencies.py     # Shared dependencies
│   ├── core/
│   │   ├── config.py            # Application settings
│   │   ├── security.py          # Security utilities
│   │   └── validators.py        # Input validation
│   ├── db/
│   │   ├── session.py           # Database session management
│   │   └── base.py              # Base model
│   ├── models/
│   │   ├── user.py              # User model
│   │   └── task.py              # Task model
│   ├── schemas/
│   │   ├── auth.py              # Auth request/response schemas
│   │   ├── task.py              # Task request/response schemas
│   │   ├── user.py              # User schemas
│   │   └── token.py             # Token schemas
│   ├── services/
│   │   ├── auth.py              # Authentication logic
│   │   ├── tasks.py             # Task business logic
│   │   ├── email.py             # Email sending service
│   │   └── cache.py             # Caching service
│   └── main.py                  # FastAPI application entry point
├── migrations/
│   ├── 001_add_user_security_fields.sql        # PostgreSQL migration
│   └── 001_add_user_security_fields_sqlite.sql # SQLite migration
├── run_migration.py             # Migration script for SQLite
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
└── README.md                    # This file
```

---

## Configuration

### Environment Variables

All configuration is done through environment variables or a `.env` file. Key settings:

#### Required for Development

```env
DATABASE_URL=sqlite:///./backend.db
AUTO_CREATE_TABLES=true
SECRET_KEY=secret-key-change-in-production-MUST-BE-64-CHARS-MINIMUM-PLEASE-CHANGE
ENVIRONMENT=development
```

#### Optional Settings

```env
# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_AUTH_PER_MINUTE=5

# Password Requirements
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_DIGITS=true
PASSWORD_REQUIRE_SPECIAL=true

# Email Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=Task Management
FRONTEND_URL=http://localhost:5173

# Redis Caching (Optional)
REDIS_ENABLED=false
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=300

# Token Expiration
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
```

---

## Database Setup

### Development (SQLite)

SQLite is used by default for development. The database file (`backend.db`) will be created automatically.

**First Run:**
1. Set `AUTO_CREATE_TABLES=true` in `.env`
2. Start the server - tables will be created automatically

**After First Run:**
1. Set `AUTO_CREATE_TABLES=false` in `.env` to prevent accidental table recreation

**If You Have Schema Errors:**

If you encounter errors like `no such column: users.is_verified`, you need to apply migrations:

**Option A: Apply Migration (Recommended if you have existing data)**
```bash
# From backend directory
python run_migration.py
```

**Option B: Recreate Database (Use if you don't have important data)**
```bash
# Stop the server (Ctrl+C)

# Windows PowerShell
Remove-Item backend.db, backend.db-shm, backend.db-wal -ErrorAction SilentlyContinue

# Linux/Mac
rm backend.db backend.db-shm backend.db-wal

# Set AUTO_CREATE_TABLES=true in .env
# Restart the server - it will recreate the database
```

### Production (PostgreSQL)

1. **Install PostgreSQL**

2. **Create Database and User:**
```sql
CREATE DATABASE taskmanagement;
CREATE USER taskuser WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE taskmanagement TO taskuser;
```

3. **Update .env:**
```env
DATABASE_URL=postgresql://taskuser:secure_password@localhost:5432/taskmanagement
AUTO_CREATE_TABLES=false
```

4. **Run Migration:**
```bash
psql -U taskuser -d taskmanagement -f migrations/001_add_user_security_fields.sql
```

---

## Running the Application

### Development Mode

```bash
# Activate virtual environment
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Run with auto-reload
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The `--reload` flag enables automatic reloading when code changes are detected.

### Production Mode

```bash
# Run without reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

For production, use a process manager like:
- **systemd** (Linux)
- **Supervisor**
- **PM2**
- **Docker** with proper orchestration

---

## API Documentation

### Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "SecurePass123!"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=SecurePass123!
```

#### Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "your_refresh_token_here"
}
```

#### Verify Email
```http
POST /api/v1/auth/verify-email
Content-Type: application/json

{
  "token": "verification_token_from_email"
}
```

#### Request Password Reset
```http
POST /api/v1/auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}
```

#### Reset Password
```http
POST /api/v1/auth/reset-password
Content-Type: application/json

{
  "token": "reset_token_from_email",
  "new_password": "NewSecurePass123!"
}
```

### Task Endpoints

#### Get Tasks
```http
GET /api/v1/tasks/?limit=50&offset=0&status=pending&sort_by=created_at&sort_order=desc
Authorization: Bearer <access_token>
```

#### Create Task
```http
POST /api/v1/tasks/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59Z"
}
```

#### Get Task by ID
```http
GET /api/v1/tasks/{task_id}
Authorization: Bearer <access_token>
```

#### Update Task
```http
PUT /api/v1/tasks/{task_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated title",
  "status": "completed"
}
```

#### Delete Task
```http
DELETE /api/v1/tasks/{task_id}
Authorization: Bearer <access_token>
```

---

## Features

### Email Verification & Password Reset

To enable email functionality:

1. **Configure SMTP in .env:**
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=Task Management
FRONTEND_URL=http://localhost:5173
```

2. **For Gmail:**
   - Enable 2-factor authentication
   - Generate an App Password: https://myaccount.google.com/apppasswords
   - Use the App Password in `SMTP_PASSWORD`

3. **Test Email Sending:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "SecurePass123!"
  }'
```

### Redis Caching (Optional)

1. **Install Redis:**
```bash
# Windows (using Chocolatey)
choco install redis-64

# macOS
brew install redis

# Ubuntu/Debian
sudo apt-get install redis-server
```

2. **Start Redis:**
```bash
redis-server
```

3. **Enable in .env:**
```env
REDIS_ENABLED=true
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=300
```

### Rate Limiting

Rate limiting is enabled by default:
- **General API**: 60 requests/minute
- **Auth endpoints**: 5 requests/minute

To adjust limits:
```env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_AUTH_PER_MINUTE=5
```

To disable (not recommended):
```env
RATE_LIMIT_ENABLED=false
```

### Password Requirements

Default password requirements:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

To customize:
```env
PASSWORD_MIN_LENGTH=10
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_DIGITS=true
PASSWORD_REQUIRE_SPECIAL=false
```

---

## Security

### Development ✅

- [x] Default SECRET_KEY is acceptable
- [x] CORS_ORIGINS can be empty (defaults to localhost)
- [x] SMTP can be unconfigured (emails won't send)
- [x] Redis can be disabled
- [x] Rate limiting is active

### Production ⚠️

Before deploying to production, ensure:

- [ ] **CRITICAL**: Generate and set a strong SECRET_KEY (64+ characters)
  ```bash
  python -c 'import secrets; print(secrets.token_urlsafe(64))'
  ```
- [ ] **CRITICAL**: Set `ENVIRONMENT=production`
- [ ] **CRITICAL**: Set specific `CORS_ORIGINS` (comma-separated)
- [ ] **CRITICAL**: Configure SMTP with valid credentials
- [ ] Set up PostgreSQL database
- [ ] Set `AUTO_CREATE_TABLES=false`
- [ ] Run database migrations
- [ ] Enable Redis caching (recommended)
- [ ] Configure HTTPS/TLS
- [ ] Set up monitoring (Sentry, etc.)
- [ ] Configure logging aggregation
- [ ] Set up database backups
- [ ] Review rate limits for your expected traffic

---

## Testing

### Test Registration with Password Validation

```bash
# This should FAIL (weak password)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "weak"
  }'

# This should SUCCESS (strong password)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "SecurePass123!"
  }'
```

### Test Rate Limiting

```bash
# Try 6 rapid requests (6th should be rate limited)
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/v1/auth/login \
    -d "username=test@example.com&password=wrong"
  echo "Request $i"
done
```

### Test Token Refresh

```bash
# 1. Login to get tokens
ACCESS_TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=test@example.com&password=SecurePass123!" \
  | jq -r '.token.access_token')

REFRESH_TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=test@example.com&password=SecurePass123!" \
  | jq -r '.token.refresh_token')

# 2. Use refresh token to get new access token
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\": \"$REFRESH_TOKEN\"}"
```

---

## Troubleshooting

### "no such column: users.is_verified" or similar schema errors

**Solution**: Your database schema is out of date. Apply the migration:
```bash
# From backend directory
python run_migration.py
```

If the migration script doesn't work, you can recreate the database:
```bash
# Stop the server first (Ctrl+C)
# Delete database files

# Windows PowerShell
Remove-Item backend.db, backend.db-shm, backend.db-wal -ErrorAction SilentlyContinue

# Linux/Mac
rm backend.db backend.db-shm backend.db-wal

# Set AUTO_CREATE_TABLES=true in .env
# Restart the server - it will recreate the database
```

### "SECRET_KEY must be at least 64 characters in production"

**Solution**: Generate a strong secret key:
```bash
python -c 'import secrets; print(secrets.token_urlsafe(64))'
```

Add it to your `.env` file:
```env
SECRET_KEY=your_generated_key_here
```

### "CORS_ORIGINS must be set in production"

**Solution**: Set explicit CORS origins in `.env`:
```env
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Emails not sending

**Common Issues:**
1. Check SMTP credentials are correct
2. For Gmail, ensure you're using an App Password (not your regular password)
3. Check `SMTP_HOST` and `SMTP_PORT` are correct
4. Verify firewall allows outbound connections on port 587
5. Check application logs for error messages

### Rate limiting too strict

**Solution**: Adjust limits in `.env`:
```env
RATE_LIMIT_PER_MINUTE=120  # Increase general limit
RATE_LIMIT_AUTH_PER_MINUTE=10  # Increase auth limit
```

### Redis connection errors

**Solution:**
1. Ensure Redis is running: `redis-cli ping` (should return PONG)
2. Check `REDIS_URL` is correct in `.env`
3. If not using Redis, set `REDIS_ENABLED=false`

### Module not found errors

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check you're running commands from the `backend` directory

### Port already in use

**Solution:**
1. Find the process using port 8000:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/Mac
   lsof -i :8000
   ```
2. Kill the process or use a different port:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
   ```

---

## Production Deployment

### Checklist

1. **Environment Configuration**
   - Set `ENVIRONMENT=production`
   - Generate and set strong `SECRET_KEY`
   - Configure `CORS_ORIGINS`
   - Set `AUTO_CREATE_TABLES=false`

2. **Database**
   - Set up PostgreSQL
   - Run migrations
   - Configure backups

3. **Security**
   - Enable HTTPS/TLS
   - Configure firewall rules
   - Set up monitoring and alerting

4. **Performance**
   - Enable Redis caching
   - Configure appropriate rate limits
   - Set up load balancing if needed

5. **Monitoring**
   - Set up error tracking (Sentry, etc.)
   - Configure logging aggregation
   - Set up health checks

### Docker Deployment (Example)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Support

- **API Documentation**: http://localhost:8000/docs (when server is running)
- **Issues**: Review code comments for additional context
- **Logs**: Check application logs for detailed error messages

---

**Version**: 2.0.0  
**Last Updated**: November 19, 2025
