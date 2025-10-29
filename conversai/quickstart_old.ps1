# Quick Start Script for ConversAI
# This script helps you set up and test ConversAI quickly

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "  ConversAI - Quick Start Setup" -ForegroundColor Yellow
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Green
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found! Please install Python 3.11+ from python.org" -ForegroundColor Red
    exit 1
}

# Check if in correct directory
Write-Host "`n[2/6] Checking directory structure..." -ForegroundColor Green
if (!(Test-Path "backend")) {
    Write-Host "  ✗ Backend folder not found! Are you in the conversai directory?" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Directory structure looks good" -ForegroundColor Green

# Check for .env file
Write-Host "`n[3/6] Checking environment configuration..." -ForegroundColor Green
if (!(Test-Path ".env")) {
    Write-Host "  ℹ .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "  ✓ Created .env file" -ForegroundColor Green
    Write-Host ""
    Write-Host "  ⚠ IMPORTANT: Edit .env and add your GROQ_API_KEY!" -ForegroundColor Red
    Write-Host "  Get it from: https://console.groq.com" -ForegroundColor Cyan
    Write-Host ""
    $continue = Read-Host "  Have you added your GROQ_API_KEY? (y/n)"
    if ($continue -ne "y") {
        Write-Host "  Please add your API key to .env and run this script again." -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "  ✓ .env file exists" -ForegroundColor Green
    
    # Check if GROQ_API_KEY is set
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "GROQ_API_KEY=gsk_") {
        Write-Host "  ✓ GROQ_API_KEY appears to be configured" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ GROQ_API_KEY may not be configured correctly" -ForegroundColor Yellow
        Write-Host "  Make sure it starts with 'gsk_'" -ForegroundColor Yellow
    }
}

# Create virtual environment
Write-Host "`n[4/6] Setting up Python virtual environment..." -ForegroundColor Green
Set-Location backend

if (!(Test-Path "venv")) {
    Write-Host "  Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "  ✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host "`n[5/6] Installing dependencies..." -ForegroundColor Green
Write-Host "  This may take 2-3 minutes..." -ForegroundColor Cyan

& "venv\Scripts\Activate.ps1"
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "  ✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Test import
Write-Host "`n[6/6] Testing installation..." -ForegroundColor Green
$testPython = @"
try:
    import fastapi
    import groq
    import sqlalchemy
    print('SUCCESS')
except ImportError as e:
    print(f'ERROR: {e}')
"@

$testResult = python -c $testPython
if ($testResult -eq "SUCCESS") {
    Write-Host "  ✓ All dependencies working correctly" -ForegroundColor Green
} else {
    Write-Host "  ✗ Dependency test failed: $testResult" -ForegroundColor Red
    exit 1
}

# Success message
Write-Host ""
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host "  ✓ Setup Complete! ConversAI is ready to run." -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Start the server:" -ForegroundColor White
Write-Host "     uvicorn app.main:app --reload" -ForegroundColor Cyan
Write-Host ""
Write-Host "  2. Open your browser to:" -ForegroundColor White
Write-Host "     http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "  3. Try a test query:" -ForegroundColor White
Write-Host '     {"message": "What is Bitcoin''s price?"}' -ForegroundColor Cyan
Write-Host ""
Write-Host "Would you like to start the server now? (y/n): " -NoNewline -ForegroundColor Yellow
$startNow = Read-Host

if ($startNow -eq "y") {
    Write-Host ""
    Write-Host "Starting ConversAI server..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    uvicorn app.main:app --reload
} else {
    Write-Host ""
    Write-Host "To start the server later, run:" -ForegroundColor Yellow
    Write-Host "  cd backend" -ForegroundColor Cyan
    Write-Host "  venv\Scripts\Activate" -ForegroundColor Cyan
    Write-Host "  uvicorn app.main:app --reload" -ForegroundColor Cyan
}
