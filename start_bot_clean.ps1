# Clean Bot Startup Script
# This will properly start your Sage FAQ Bot

Write-Host "🤖 Starting Developer Onboarding Bot..." -ForegroundColor Green

# Kill any existing Rasa processes
Write-Host "🧹 Cleaning up existing processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*rasa*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

# Set environment variables
Write-Host "🔧 Setting up Azure OpenAI connection..." -ForegroundColor Cyan
$env:AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_API_KEY_HERE"
$env:AZURE_OPENAI_ENDPOINT="https://hackathon-azure-openai-east-us.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT="o4-mini"

Write-Host "✅ Environment configured successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Starting Rasa actions server..." -ForegroundColor Green
Write-Host "💡 Wait for 'Action endpoint is up and running' message" -ForegroundColor Yellow
Write-Host "💡 Then open another terminal and run: python web_server.py" -ForegroundColor Yellow
Write-Host "💡 Finally visit: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""

# Start actions server
venv\Scripts\rasa.exe run actions --port 5055 --debug 