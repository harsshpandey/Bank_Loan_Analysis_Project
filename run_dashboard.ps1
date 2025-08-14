# Bank Loan Analytics Dashboard - PowerShell Launcher
Write-Host "🏦 Bank Loan Analytics Dashboard" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.7+ first." -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if requirements are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import dash, plotly, pandas" 2>$null
    Write-Host "✅ Dependencies are installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Some dependencies missing. Installing..." -ForegroundColor Yellow
    try {
        python -m pip install -r requirements.txt
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "🚀 Starting the dashboard..." -ForegroundColor Green
Write-Host "   If a browser doesn't open automatically, go to: http://127.0.0.1:8050/" -ForegroundColor Yellow
Write-Host "   Press Ctrl+C to stop the dashboard" -ForegroundColor Yellow
Write-Host ""

try {
    python bank_loan_dashboard.py
} catch {
    Write-Host "❌ Error running dashboard: $_" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
