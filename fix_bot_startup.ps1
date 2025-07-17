# Fix Bot Startup Issues
# This script will kill any existing processes on port 5055 and restart the bot

Write-Host "🤖 Fixing Sage FAQ Bot Startup Issues..." -ForegroundColor Green

# Step 1: Kill any process using port 5055
Write-Host "📍 Checking for processes using port 5055..." -ForegroundColor Yellow
try {
    $processes = Get-NetTCPConnection -LocalPort 5055 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
    if ($processes) {
        foreach ($pid in $processes) {
            Write-Host "🔄 Killing process $pid using port 5055..." -ForegroundColor Yellow
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
        Start-Sleep -Seconds 2
    } else {
        Write-Host "✅ Port 5055 is free" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ Could not check port 5055 status" -ForegroundColor Yellow
}

# Step 2: Set environment variables
Write-Host "🔧 Setting up environment variables..." -ForegroundColor Cyan
$env:AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_API_KEY_HERE"
$env:AZURE_OPENAI_ENDPOINT="https://hackathon-azure-openai-east-us.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT="o4-mini"

# Step 3: Start Rasa actions server
Write-Host "🚀 Starting Rasa actions server..." -ForegroundColor Green
Write-Host "📌 If you see 'Action endpoint is up and running on http://0.0.0.0:5055', the bot is ready!" -ForegroundColor Green
Write-Host "📌 In another terminal, run: python web_server.py" -ForegroundColor Cyan
Write-Host "📌 Then visit: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""

# Start the actions server
venv\Scripts\rasa.exe run actions --port 5055 