# Setup Guide

Comprehensive installation, configuration, and deployment guide for ConversAI.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Docker Deployment](#docker-deployment)
6. [Production Deployment](#production-deployment)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **OS:** Windows 10+, macOS 10.15+, Ubuntu 20.04+
- **Python:** 3.11 or higher
- **Node.js:** 18.0 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 2GB for dependencies and database

### Optional Requirements

- **Docker:** 20.10+ (for containerized deployment)
- **PostgreSQL:** 13+ (for production database)

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/Shamzzz-star/API-To-ChatBot.git
cd conversai
```

### 2. Backend Setup

#### Create Virtual Environment

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate.bat
```

#### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If you encounter errors:**
```bash
# Install build tools (Ubuntu/Debian)
sudo apt-get install python3-dev build-essential

# Install build tools (macOS)
xcode-select --install

# Install build tools (Windows)
# Download and install Microsoft C++ Build Tools
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install
```

**If npm install fails:**
```bash
# Clear npm cache
npm cache clean --force

# Try again
npm install

# Or use yarn
npm install -g yarn
yarn install
```

---

## Configuration

### Backend Configuration

#### 1. Create Environment File

```bash
cd backend
cp .env.example .env
```

#### 2. Edit `.env` File

Open `.env` in your text editor and configure:

```bash
# ============================================
# REQUIRED SETTINGS
# ============================================

# Get from: https://console.groq.com
GROQ_API_KEY=gsk_your_actual_groq_api_key_here

# Generate 32-character key for encryption
ENCRYPTION_KEY=your-32-character-encryption-key-here

# ============================================
# SECURITY (Required for Production)
# ============================================

JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================
# DATABASE
# ============================================

# Development (SQLite)
DATABASE_URL=sqlite:///./conversai.db

# Production (PostgreSQL)
# DATABASE_URL=postgresql://username:password@localhost:5432/conversai

# ============================================
# OPTIONAL API KEYS (Free Tier)
# ============================================

# OpenWeather (https://openweathermap.org/api)
OPENWEATHER_API_KEY=your_openweather_key

# NewsAPI (https://newsapi.org)
NEWSAPI_KEY=your_newsapi_key

# WeatherAPI (https://www.weatherapi.com)
WEATHERAPI_KEY=your_weatherapi_key

# GNews (https://gnews.io)
GNEWS_API_KEY=your_gnews_key

# API Ninjas (https://api-ninjas.com)
API_NINJAS_KEY=your_api_ninjas_key

# ============================================
# SERVER SETTINGS
# ============================================

APP_NAME=ConversAI
ENVIRONMENT=development
DEBUG=True
HOST=0.0.0.0
PORT=8000

# ============================================
# RATE LIMITING
# ============================================

MAX_REQUESTS_PER_MINUTE=60
MAX_REQUESTS_PER_DAY=1000

# ============================================
# CACHE TTL (seconds)
# ============================================

CACHE_TTL_WEATHER=600
CACHE_TTL_CRYPTO=60
CACHE_TTL_NEWS=1800
CACHE_TTL_DEFAULT=300

# ============================================
# CORS ORIGINS
# ============================================

CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# ============================================
# LOGGING
# ============================================

LOG_LEVEL=INFO
```

#### 3. Generate Encryption Key

**Python Method:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32)[:32])"
```

**OpenSSL Method:**
```bash
openssl rand -base64 32
```

Copy the output and use it as `ENCRYPTION_KEY` in `.env`.

#### 4. Obtain API Keys

##### Groq (Required)
1. Visit https://console.groq.com
2. Sign up for free account
3. Navigate to API Keys section
4. Create new API key
5. Copy and paste into `.env`

##### OpenWeather (Optional)
1. Visit https://openweathermap.org/api
2. Sign up for free account
3. Get API key from dashboard
4. Free tier: 60 calls/minute

##### NewsAPI (Optional)
1. Visit https://newsapi.org
2. Register for free API key
3. Free tier: 100 requests/day

##### Other APIs
Follow similar process for other optional APIs listed above.

### Frontend Configuration

#### 1. Create Environment File (Optional)

```bash
cd frontend
echo "VITE_API_URL=http://localhost:8000" > .env
```

**For production:**
```bash
echo "VITE_API_URL=https://your-api-domain.com" > .env
```

---

## Running the Application

### Development Mode

#### Option 1: Run Manually

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- API Docs (ReDoc): http://localhost:8000/redoc

#### Option 2: Using Scripts (Recommended)

**macOS/Linux - Create startup script:**

`start.sh`:
```bash
#!/bin/bash

# Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Press Ctrl+C to stop"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
```

Make executable and run:
```bash
chmod +x start.sh
./start.sh
```

**Windows - Create startup script:**

`start.ps1`:
```powershell
# Start backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

# Wait 5 seconds
Start-Sleep -Seconds 5

# Start frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
```

Run:
```powershell
.\start.ps1
```

---

## Docker Deployment

### Prerequisites

Install Docker and Docker Compose:
- **Windows/macOS:** [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux:** Follow [official guide](https://docs.docker.com/engine/install/)

### Build and Run

```bash
# Build and start containers
docker-compose up --build

# Run in detached mode (background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Stop and remove volumes (reset database)
docker-compose down -v
```

### Docker Configuration

The `docker-compose.yml` defines two services:

```yaml
services:
  backend:
    - Port: 8000
    - Auto-reload enabled
    - Database persists in volume

  frontend:
    - Port: 3000
    - Hot reload enabled
    - Depends on backend
```

### Environment Variables for Docker

Create `.env` in root directory (same level as `docker-compose.yml`):

```bash
GROQ_API_KEY=your_groq_api_key
ANTHROPIC_API_KEY=your_anthropic_key  # If using
ENCRYPTION_KEY=your_encryption_key
```

Docker Compose will automatically load these.

---

## Production Deployment

### 1. Update Environment

```bash
# backend/.env
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost:5432/conversai
```

### 2. Use Production Database

#### Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

#### Create Database

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE conversai;
CREATE USER conversai_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE conversai TO conversai_user;
\q
```

Update `DATABASE_URL` in `.env`:
```bash
DATABASE_URL=postgresql://conversai_user:your_secure_password@localhost:5432/conversai
```

### 3. Build Frontend for Production

```bash
cd frontend
npm run build
```

This creates optimized files in `frontend/dist/`.

### 4. Serve with Nginx

#### Install Nginx

**Ubuntu/Debian:**
```bash
sudo apt-get install nginx
```

**macOS:**
```bash
brew install nginx
```

#### Configure Nginx

`/etc/nginx/sites-available/conversai`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/conversai/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # API Docs
    location /docs {
        proxy_pass http://localhost:8000/docs;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/conversai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Use Process Manager

#### Install PM2

```bash
npm install -g pm2
```

#### Create PM2 Config

`ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: 'conversai-backend',
    script: 'venv/bin/uvicorn',
    args: 'app.main:app --host 0.0.0.0 --port 8000',
    cwd: './backend',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    }
  }]
};
```

#### Start Application

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### 6. Enable HTTPS (Recommended)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Troubleshooting

### Backend Issues

#### Database Connection Error
```
sqlalchemy.exc.OperationalError: unable to open database file
```

**Solution:**
```bash
# Create data directory
mkdir -p backend/data

# Check permissions
chmod 755 backend/data
```

#### Module Not Found Error
```
ModuleNotFoundError: No module named 'app'
```

**Solution:**
```bash
# Ensure you're in backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt

# Run with module syntax
python -m app.main
```

#### Port Already in Use
```
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
uvicorn app.main:app --port 8001
```

### Frontend Issues

#### CORS Error
```
Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```

**Solution:**
Check `backend/.env`:
```bash
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

Add your frontend URL if different.

#### Build Fails
```
npm ERR! code ELIFECYCLE
```

**Solution:**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm cache clean --force

# Reinstall
npm install

# Try alternative package manager
npm install -g yarn
yarn install
```

### Docker Issues

#### Container Won't Start
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

#### Permission Denied
```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker
```

---

## Getting Help

If you encounter issues not covered here:

1. **Check Logs:**
   - Backend: Look for errors in terminal output
   - Frontend: Check browser console (F12)

2. **GitHub Issues:** [Report a bug](https://github.com/Shamzzz-star/API-To-ChatBot/issues)

3. **Documentation:**
   - [README](README.md)
   - [API Documentation](API_DOCUMENTATION.md)

---

## Next Steps

After successful setup:

1. **Test the application** with example queries
2. **Add custom APIs** via the UI
3. **Configure additional API keys** for more features
4. **Set up production deployment** if needed
5. **Star the repository** if you find it helpful!
