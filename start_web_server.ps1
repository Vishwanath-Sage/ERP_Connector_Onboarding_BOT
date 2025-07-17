# Start Web Server for Chat Interface
Write-Host "🌐 STARTING WEB SERVER" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Green

# Check if web_server.py exists
if (-not (Test-Path "web_server.py")) {
    Write-Host "❌ web_server.py not found in current directory" -ForegroundColor Red
    Write-Host "💡 Make sure you're in the FAQ's project directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Found web_server.py" -ForegroundColor Green

# Check if port 3000 is available
Write-Host "🔍 Checking if port 3000 is available..." -ForegroundColor Cyan
try {
    $portTest = Test-NetConnection -ComputerName localhost -Port 3000 -WarningAction SilentlyContinue
    if ($portTest.TcpTestSucceeded) {
        Write-Host "⚠️ Port 3000 is already in use" -ForegroundColor Yellow
        Write-Host "🔄 Attempting to free up port 3000..." -ForegroundColor Yellow
        
        # Try to kill any process using port 3000
        $processes = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($processes) {
            foreach ($pid in $processes) {
                Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            }
            Start-Sleep -Seconds 2
        }
    }
} catch {
    Write-Host "✅ Port 3000 appears to be free" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting Web Server on http://localhost:3000..." -ForegroundColor Blue
Write-Host "This provides the chat interface for your bot" -ForegroundColor Yellow
Write-Host ""
Write-Host "📱 Once started, open your browser to:" -ForegroundColor Cyan
Write-Host "   http://localhost:3000" -ForegroundColor White -BackgroundColor Blue
Write-Host ""
Write-Host "❓ Test these questions:" -ForegroundColor Yellow
Write-Host "   • Hello" -ForegroundColor White
Write-Host "   • How do I authenticate?" -ForegroundColor White
Write-Host "   • How do I get started?" -ForegroundColor White
Write-Host "   • What is Sage Network Connectors?" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop: Press Ctrl+C" -ForegroundColor Red
Write-Host ""

# Activate virtual environment and start web server
try {
    if (Test-Path "venv\Scripts\activate.ps1") {
        Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
        & "venv\Scripts\Activate.ps1"
    }
    
    Write-Host "🌐 Starting Flask web server..." -ForegroundColor Green
    python web_server.py
} catch {
    Write-Host "❌ Failed to start web server" -ForegroundColor Red
    Write-Host "💡 Error details:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Try manual start:" -ForegroundColor Cyan
    Write-Host "   python web_server.py" -ForegroundColor White
} 