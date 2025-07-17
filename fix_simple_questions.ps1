# Fix Simple Questions Not Being Answered
# This script will ensure all components are running properly

Write-Host "🔧 FIXING SIMPLE QUESTION RESPONSES" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

# Step 1: Stop all existing processes
Write-Host "🛑 Step 1: Stopping all existing bot processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*rasa*" -or $_.ProcessName -like "*python*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3
Write-Host "✅ All processes stopped" -ForegroundColor Green

# Step 2: Set environment variables
Write-Host "🔧 Step 2: Setting up environment..." -ForegroundColor Cyan
$env:AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_API_KEY_HERE"
$env:AZURE_OPENAI_ENDPOINT="https://hackathon-azure-openai-east-us.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT="o4-mini"
Write-Host "✅ Environment configured" -ForegroundColor Green

# Step 3: Train the model (crucial for intent recognition)
Write-Host "🎯 Step 3: Training model for intent recognition..." -ForegroundColor Magenta
Write-Host "This ensures the bot understands 'How do I authenticate?' questions" -ForegroundColor Yellow
try {
    venv\Scripts\rasa.exe train --force
    Write-Host "✅ Model training complete!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Training had issues, continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 STARTING THREE REQUIRED COMPONENTS:" -ForegroundColor Blue
Write-Host "1. Actions Server (already working)" -ForegroundColor White
Write-Host "2. Rasa Server (for intent recognition)" -ForegroundColor White  
Write-Host "3. Web Server (for chat interface)" -ForegroundColor White
Write-Host ""

# Step 4: Start Actions Server in background
Write-Host "🔧 Step 4: Starting Actions Server..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-Command", "cd '$PWD'; venv\Scripts\rasa.exe run actions" -WindowStyle Minimized
Start-Sleep -Seconds 5

# Step 5: Start Rasa Server in background  
Write-Host "🧠 Step 5: Starting Rasa Server (for intent recognition)..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-Command", "cd '$PWD'; venv\Scripts\rasa.exe run --enable-api --cors '*' --port 5005" -WindowStyle Minimized
Start-Sleep -Seconds 8

# Step 6: Start Web Server
Write-Host "🌐 Step 6: Starting Web Server..." -ForegroundColor Blue
Write-Host ""
Write-Host "🎉 ALL SERVERS STARTING!" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host "📱 Bot will be available at: http://localhost:3000" -ForegroundColor White -BackgroundColor Blue
Write-Host "❓ Test questions:" -ForegroundColor Yellow
Write-Host "   • How do I authenticate?" -ForegroundColor White
Write-Host "   • How do I get started?" -ForegroundColor White
Write-Host "   • What is Sage Network Connectors?" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop all servers: Press Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# Start web server (this will block and show output)
python web_server.py 