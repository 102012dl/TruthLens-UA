Param(
    [string]$Mode = "local"  # local | render
)

Write-Host "=== TruthLens-UA MVP Demo ===" -ForegroundColor Cyan
Write-Host "Mode: $Mode" -ForegroundColor Yellow

$ErrorActionPreference = "Stop"

Set-Location -Path (Split-Path $MyInvocation.MyCommand.Path -Parent) | Out-Null
Set-Location ..  # go to repo root

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\activate.ps1

Write-Host "Ensuring dependencies are installed..." -ForegroundColor Yellow
pip install -r requirements.txt | Out-Null

if ($Mode -eq "local") {
    Write-Host "Starting local API (uvicorn) on http://127.0.0.1:8000 ..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\.venv\Scripts\activate.ps1; uvicorn src.api.main:app --reload"
    $env:TRUTHLENS_API_URL = "http://127.0.0.1:8000"
} else {
    Write-Host "Using Render API https://truthlens-ua.onrender.com" -ForegroundColor Yellow
    $env:TRUTHLENS_API_URL = "https://truthlens-ua.onrender.com"
}

Write-Host "Starting Streamlit dashboard on http://localhost:8501 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\.venv\Scripts\activate.ps1; streamlit run scripts/truthlens_dashboard.py"

Write-Host ""
Write-Host "Dashboard URL: http://localhost:8501" -ForegroundColor Green
Write-Host "Swagger (if using Render or local API): http://localhost:8000/docs or https://truthlens-ua.onrender.com/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Tip: pin this script and run:" -ForegroundColor Cyan
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\run_mvp_demo.ps1" -ForegroundColor Cyan

