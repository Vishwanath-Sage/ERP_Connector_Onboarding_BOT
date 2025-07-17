Write-Host "===============================================" -ForegroundColor Green
Write-Host " Starting Developer Onboarding Bot" -ForegroundColor Green
Write-Host " with Azure OpenAI Integration" -ForegroundColor Green  
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Check if Azure OpenAI configuration is set
if (-not $env:AZURE_OPENAI_API_KEY) {
    Write-Host "⚠️  Azure OpenAI API key not found!" -ForegroundColor Yellow
    Write-Host "Please run .\setup_openai.ps1 first to configure your Azure OpenAI credentials" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not $env:AZURE_OPENAI_ENDPOINT) {
    Write-Host "⚠️  Azure OpenAI endpoint not found!" -ForegroundColor Yellow
    Write-Host "Please run .\setup_openai.ps1 first to configure your Azure OpenAI endpoint" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$deployment = $env:AZURE_OPENAI_DEPLOYMENT
if (-not $deployment) {
    $deployment = "gpt-35-turbo"
    Write-Host "ℹ️  Using default deployment: $deployment" -ForegroundColor Blue
}

Write-Host "✅ Azure OpenAI Configuration Found:" -ForegroundColor Green
Write-Host "   Endpoint: $env:AZURE_OPENAI_ENDPOINT" -ForegroundColor Gray
Write-Host "   Deployment: $deployment" -ForegroundColor Gray
Write-Host "   API Key: $($env:AZURE_OPENAI_API_KEY.Substring(0, 8))..." -ForegroundColor Gray

# Activate virtual environment
Write-Host ""
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Please run .\setup_openai.ps1 first" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting services..." -ForegroundColor Cyan
Write-Host ""

# Function to start a service in a new window
function Start-Service {
    param($Title, $Command, $Color)
    Write-Host "Starting $Title..." -ForegroundColor $Color
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; $Command; Read-Host 'Press Enter to close'"
    Start-Sleep -Seconds 2
}

# Start Rasa Actions Server
Start-Service "Rasa Actions Server" "rasa run actions" "Yellow"

# Start Rasa Server  
Start-Service "Rasa Core Server" "rasa run --enable-api --cors '*'" "Blue"

# Start Web Server
Start-Service "Web Interface" "python web_server.py" "Magenta"

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host " All Services Started Successfully!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Bot Interface: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Rasa API: http://localhost:5005" -ForegroundColor Gray
Write-Host "⚙️  Actions Server: http://localhost:5055" -ForegroundColor Gray
Write-Host ""
Write-Host "✨ Features enabled:" -ForegroundColor Green
Write-Host "   • Traditional Rasa responses for structured FAQs" -ForegroundColor White
Write-Host "   • Azure OpenAI-powered responses for complex queries" -ForegroundColor White
Write-Host "   • Intelligent fallback system" -ForegroundColor White
Write-Host "   • Enhanced conversation capabilities" -ForegroundColor White
Write-Host ""
Write-Host "💡 Try asking:" -ForegroundColor Yellow
Write-Host "   • 'What is Sage Network Connectors?'" -ForegroundColor Gray
Write-Host "   • 'How do I authenticate with OAuth 2.0?'" -ForegroundColor Gray
Write-Host "   • 'Explain rate limiting best practices'" -ForegroundColor Gray
Write-Host "   • 'What are common integration patterns?'" -ForegroundColor Gray
Write-Host "   • 'How do I handle API errors gracefully?'" -ForegroundColor Gray
Write-Host ""
Write-Host "🛑 To stop all services:" -ForegroundColor Red
Write-Host "   Close all PowerShell windows or press Ctrl+C in each" -ForegroundColor Gray
Write-Host ""
Write-Host "📊 Monitor Azure OpenAI usage in Azure Portal" -ForegroundColor Cyan
Write-Host "🌐 Azure Portal: https://portal.azure.com" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to open the bot in your browser"

# Open browser
Start-Process "http://localhost:3000" 