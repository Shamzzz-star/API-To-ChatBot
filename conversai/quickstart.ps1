# ConversAI Quick Start Script
# Run this to set up and start the backend server

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ConversAI - Quick Start Setup" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  OK: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Python not found!" -ForegroundColor Red
    exit 1
}

# Check directory
Write-Host "`n[2/5] Checking directory..." -ForegroundColor Green
if (!(Test-Path "backend")) {
    Write-Host "  ERROR: backend folder not found!" -ForegroundColor Red
    Write-Host "  Make sure you're in the conversai directory" -ForegroundColor Yellow
    exit 1
}
Write-Host "  OK: Directory structure found" -ForegroundColor Green

# Check .env
Write-Host "`n[3/5] Checking .env file..." -ForegroundColor Green
if (!(Test-Path "backend\.env")) {
    Write-Host "  WARNING: backend\.env not found!" -ForegroundColor Yellow
    Write-Host "  You'll need to add GROQ_API_KEY to backend\.env" -ForegroundColor Yellow
    Write-Host "  Get it from: https://console.groq.com" -ForegroundColor Cyan
} else {
    Write-Host "  OK: .env file exists" -ForegroundColor Green
}

# Setup venv
Write-Host "`n[4/5] Setting up virtual environment..." -ForegroundColor Green
Set-Location backend

if (!(Test-Path "venv")) {
    Write-Host "  Creating venv..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "  OK: Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "  OK: Virtual environment exists" -ForegroundColor Green
}

# Install dependencies
Write-Host "`n[5/5] Installing dependencies..." -ForegroundColor Green
Write-Host "  This may take 2-3 minutes..." -ForegroundColor Cyan

& "venv\Scripts\Activate.ps1"
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK: Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Success
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Make sure GROQ_API_KEY is in backend\.env" -ForegroundColor White
Write-Host "  2. Start backend:" -ForegroundColor White
Write-Host "     uvicorn app.main:app --reload" -ForegroundColor Cyan
Write-Host "  3. Start frontend in another terminal:" -ForegroundColor White
Write-Host "     cd frontend" -ForegroundColor Cyan
Write-Host "     npm run dev" -ForegroundColor Cyan
Write-Host "  4. Open: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Start backend now? (y/n): " -NoNewline -ForegroundColor Yellow
$startNow = Read-Host

if ($startNow -eq "y") {
    Write-Host ""
    Write-Host "Starting backend server..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    uvicorn app.main:app --reload
} else {
    Write-Host ""
    Write-Host "To start later:" -ForegroundColor Yellow
    Write-Host "  cd backend" -ForegroundColor Cyan
    Write-Host "  venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "  uvicorn app.main:app --reload" -ForegroundColor Cyan
}
