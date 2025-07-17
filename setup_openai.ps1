Write-Host "===============================================" -ForegroundColor Green
Write-Host " Sage Network Connectors - Azure OpenAI Setup" -ForegroundColor Green  
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Azure OpenAI Configuration
Write-Host ""
Write-Host "AZURE OPENAI CONFIGURATION" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You'll need the following from your Azure OpenAI resource:" -ForegroundColor White
Write-Host "1. API Key (from Keys and Endpoint section)" -ForegroundColor White
Write-Host "2. Endpoint URL (e.g., https://your-resource.openai.azure.com/)" -ForegroundColor White
Write-Host "3. Deployment name (e.g., gpt-35-turbo, gpt-4)" -ForegroundColor White
Write-Host ""

# Get Azure OpenAI API Key
$apiKey = Read-Host "Enter your Azure OpenAI API Key"

# Get Azure OpenAI Endpoint
Write-Host ""
Write-Host "Enter your Azure OpenAI endpoint URL:" -ForegroundColor White
Write-Host "Example: https://your-resource.openai.azure.com/" -ForegroundColor Gray
$endpoint = Read-Host "Endpoint URL"

# Ensure endpoint ends with /
if (-not $endpoint.EndsWith("/")) {
    $endpoint = $endpoint + "/"
}

# Get Deployment Name
Write-Host ""
Write-Host "Enter your deployment name:" -ForegroundColor White
Write-Host "Common names: gpt-35-turbo, gpt-4, gpt-4-turbo" -ForegroundColor Gray
$deployment = Read-Host "Deployment name"

# Set environment variables for current session
$env:AZURE_OPENAI_API_KEY = $apiKey
$env:AZURE_OPENAI_ENDPOINT = $endpoint
$env:AZURE_OPENAI_DEPLOYMENT = $deployment

# Set permanent environment variables
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", $apiKey, [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", $endpoint, [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT", $deployment, [System.EnvironmentVariableTarget]::User)

Write-Host ""
Write-Host "✅ Configuration saved:" -ForegroundColor Green
Write-Host "   API Key: $($apiKey.Substring(0, 8))..." -ForegroundColor Gray
Write-Host "   Endpoint: $endpoint" -ForegroundColor Gray
Write-Host "   Deployment: $deployment" -ForegroundColor Gray

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host " Azure OpenAI Setup Complete!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 To run the bot with Azure OpenAI integration:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Option 1: Automatic startup (recommended)" -ForegroundColor Yellow
Write-Host "   Run: .\start_bot.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Option 2: Test your configuration first" -ForegroundColor Yellow
Write-Host "   Run: python test_openai.py" -ForegroundColor White
Write-Host ""
Write-Host "Option 3: Manual startup" -ForegroundColor Yellow
Write-Host "   1. Open 3 separate PowerShell windows in this folder" -ForegroundColor White
Write-Host "   2. In each one, run: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   3. Then run these commands (one in each window):" -ForegroundColor White
Write-Host "      Terminal 1: rasa run actions" -ForegroundColor Gray
Write-Host "      Terminal 2: rasa run --enable-api --cors '*'" -ForegroundColor Gray
Write-Host "      Terminal 3: python web_server.py" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 Access your bot at: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Your provided API key has been configured for Azure OpenAI!" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to continue" 