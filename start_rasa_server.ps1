# Start Rasa Server for Intent Recognition
Write-Host "🧠 STARTING RASA SERVER" -ForegroundColor Blue
Write-Host "=======================" -ForegroundColor Blue

# Check if model exists
if (-not (Test-Path "models\*.tar.gz")) {
    Write-Host "⚠️ No trained model found. Training now..." -ForegroundColor Yellow
    Write-Host "This may take 1-2 minutes..." -ForegroundColor Yellow
    
    try {
        venv\Scripts\rasa.exe train --force
        Write-Host "✅ Model training complete!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Training failed. Check for errors above." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Trained model found" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting Rasa Server on port 5005..." -ForegroundColor Cyan
Write-Host "This server handles intent recognition (understanding questions)" -ForegroundColor Yellow
Write-Host ""
Write-Host "⏳ Starting... (this may take 10-15 seconds)" -ForegroundColor Yellow
Write-Host "🎯 Look for: 'Rasa server is up and running'" -ForegroundColor Green
Write-Host ""

# Start Rasa server
try {
    venv\Scripts\rasa.exe run --enable-api --cors "*" --port 5005
} catch {
    Write-Host "❌ Failed to start Rasa server" -ForegroundColor Red
    Write-Host "💡 Make sure you're in the FAQ's directory and virtual environment is set up" -ForegroundColor Yellow
} 