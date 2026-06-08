# Start ADYAANANT GURUKUL locally on Windows

Write-Host "🔱 Starting ADYAANANT GURUKUL Local Development Server..." -ForegroundColor Cyan
Write-Host ""

# Function to stop processes on port
function StopPort {
    param([int]$Port)
    $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($process in $processes) {
        Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
    }
}

# Stop existing processes
Write-Host "Cleaning up existing processes on ports 8000 and 8001..." -ForegroundColor Yellow
StopPort 8000
StopPort 8001

# Start Backend
Write-Host "Starting Backend API on http://localhost:8000..." -ForegroundColor Green
Push-Location backend
Write-Host "Installing dependencies..." -ForegroundColor Gray
python -m pip install -q -r requirements.txt
Write-Host "Starting uvicorn server..." -ForegroundColor Gray
Start-Process python -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -NoNewWindow -PassThru
Pop-Location

# Wait for backend to start
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "Starting Frontend on http://localhost:8001..." -ForegroundColor Green
Push-Location frontend
Start-Process python -ArgumentList "-m", "http.server", "8001" -NoNewWindow -PassThru
Pop-Location

Write-Host ""
Write-Host "✅ Development servers started!" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend:  http://localhost:8001" -ForegroundColor Cyan
Write-Host "Backend:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs:  http://localhost:8000/api/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in each terminal to stop" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to keep the script running. Close terminals to stop servers."
