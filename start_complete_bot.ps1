# Complete Sage FAQ Bot Startup Script
# This script will train the model and start both servers automatically

param(
    [switch]$SkipTraining = $false
)

Write-Host "🤖 DEVELOPER ONBOARDING BOT STARTUP" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

# Step 1: Cleanup
Write-Host "🧹 Step 1: Cleaning up existing processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*rasa*" -or $_.ProcessName -like "*python*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "✅ Cleanup complete" -ForegroundColor Green
Write-Host ""

# Step 2: Check environment
Write-Host "🔧 Step 2: Setting up environment..." -ForegroundColor Cyan
if (-not (Test-Path "venv\Scripts\activate.ps1")) {
    Write-Host "❌ Virtual environment not found! Please run: python -m venv venv" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
& "venv\Scripts\Activate.ps1"
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Set Azure OpenAI environment variables
$env:AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_API_KEY_HERE"
$env:AZURE_OPENAI_ENDPOINT="https://hackathon-azure-openai-east-us.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT="o4-mini"
Write-Host "✅ Azure OpenAI configured" -ForegroundColor Green
Write-Host ""

# Step 3: Train model (if needed)
if (-not $SkipTraining) {
    Write-Host "🎯 Step 3: Training Rasa model..." -ForegroundColor Magenta
    Write-Host "This may take 1-2 minutes..." -ForegroundColor Yellow
    
    try {
        & "venv\Scripts\rasa.exe" train
        Write-Host "✅ Model training complete!" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️ Training failed, but continuing..." -ForegroundColor Yellow
    }
} else {
    Write-Host "⏭️ Step 3: Skipping model training" -ForegroundColor Yellow
}
Write-Host ""

# Step 4: Start Actions Server in background
Write-Host "🚀 Step 4: Starting Actions Server..." -ForegroundColor Blue
$actionsJob = Start-Job -ScriptBlock {
    param($apiKey, $endpoint, $deployment)
    Set-Location $args[3]
    $env:AZURE_OPENAI_API_KEY = $apiKey
    $env:AZURE_OPENAI_ENDPOINT = $endpoint
    $env:AZURE_OPENAI_DEPLOYMENT = $deployment
    & "venv\Scripts\rasa.exe" run actions --port 5055
} -ArgumentList $env:AZURE_OPENAI_API_KEY, $env:AZURE_OPENAI_ENDPOINT, $env:AZURE_OPENAI_DEPLOYMENT, (Get-Location).Path

Write-Host "⏳ Waiting for Actions Server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if actions server is running
$actionsRunning = $false
try {
    $connection = Test-NetConnection -ComputerName localhost -Port 5055 -WarningAction SilentlyContinue
    if ($connection.TcpTestSucceeded) {
        $actionsRunning = $true
        Write-Host "✅ Actions Server is running on port 5055" -ForegroundColor Green
    }
}
catch {
    Write-Host "⚠️ Cannot verify Actions Server status" -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Start Web Server
Write-Host "🌐 Step 5: Starting Web Server..." -ForegroundColor Blue
Write-Host "📍 Starting web server on http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎉 BOT STARTUP COMPLETE!" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host "📱 Open your browser to: http://localhost:3000" -ForegroundColor White -BackgroundColor Blue
Write-Host "❓ Try asking: 'How do I get started?'" -ForegroundColor White -BackgroundColor Blue
Write-Host ""
Write-Host "🛑 To stop: Press Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# Start web server (this will block)
try {
    python web_server.py
}
catch {
    Write-Host "❌ Web server failed to start" -ForegroundColor Red
    Write-Host "💡 Try: python web_server.py manually" -ForegroundColor Yellow
}

# Cleanup on exit
Write-Host "🧹 Cleaning up..." -ForegroundColor Yellow
Stop-Job $actionsJob -ErrorAction SilentlyContinue
Remove-Job $actionsJob -ErrorAction SilentlyContinue 