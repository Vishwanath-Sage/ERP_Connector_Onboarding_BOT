# Quick Status Check for Sage FAQ Bot
Write-Host "🔍 CHECKING BOT STATUS" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Green

# Check Actions Server (port 5055)
Write-Host "🔧 Checking Actions Server (port 5055)..." -ForegroundColor Cyan
try {
    $actionsTest = Test-NetConnection -ComputerName localhost -Port 5055 -WarningAction SilentlyContinue
    if ($actionsTest.TcpTestSucceeded) {
        Write-Host "✅ Actions Server: RUNNING" -ForegroundColor Green
    } else {
        Write-Host "❌ Actions Server: NOT RUNNING" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Actions Server: CANNOT CHECK" -ForegroundColor Red
}

# Check Rasa Server (port 5005)
Write-Host "🧠 Checking Rasa Server (port 5005)..." -ForegroundColor Cyan
try {
    $rasaTest = Test-NetConnection -ComputerName localhost -Port 5005 -WarningAction SilentlyContinue
    if ($rasaTest.TcpTestSucceeded) {
        Write-Host "✅ Rasa Server: RUNNING" -ForegroundColor Green
    } else {
        Write-Host "❌ Rasa Server: NOT RUNNING" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Rasa Server: CANNOT CHECK" -ForegroundColor Red
}

# Check Web Server (port 3000)
Write-Host "🌐 Checking Web Server (port 3000)..." -ForegroundColor Cyan
try {
    $webTest = Test-NetConnection -ComputerName localhost -Port 3000 -WarningAction SilentlyContinue
    if ($webTest.TcpTestSucceeded) {
        Write-Host "✅ Web Server: RUNNING" -ForegroundColor Green
    } else {
        Write-Host "❌ Web Server: NOT RUNNING" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Web Server: CANNOT CHECK" -ForegroundColor Red
}

Write-Host ""
Write-Host "📝 SUMMARY:" -ForegroundColor Yellow
Write-Host "For the bot to work, you need ALL THREE servers running:"
Write-Host "1. Actions Server (port 5055) - For AI responses"
Write-Host "2. Rasa Server (port 5005) - For understanding questions"  
Write-Host "3. Web Server (port 3000) - For chat interface"
Write-Host ""

# Check if model exists
if (Test-Path "models\*.tar.gz") {
    Write-Host "✅ Trained model found" -ForegroundColor Green
} else {
    Write-Host "❌ No trained model found - run 'rasa train'" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 NEXT STEPS:" -ForegroundColor Blue
Write-Host "If any servers are missing, run: .\fix_simple_questions.ps1"
Write-Host "Then test at: http://localhost:3000" 