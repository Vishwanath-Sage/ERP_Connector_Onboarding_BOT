# 🤖 Complete Bot Startup Fix Guide

## 🔍 **Issue Diagnosis**
Your bot configuration is perfect! The problem is in the startup sequence. You need:
1. ✅ Actions Server (port 5055) - Working
2. ❌ Web Server (port 3000) - Not started 
3. ❌ Trained Model - May need retraining

---

## 🚀 **Step-by-Step Fix**

### **Step 1: Close Everything First**
```powershell
# Close all terminals and PowerShell windows
# Kill any running processes
Get-Process | Where-Object {$_.ProcessName -like "*rasa*" -or $_.ProcessName -like "*python*"} | Stop-Process -Force -ErrorAction SilentlyContinue
```

### **Step 2: Retrain the Model (Important!)**
```powershell
# Open PowerShell in your FAQ's directory
cd "C:\FAQ's"

# Activate virtual environment
venv\Scripts\activate

# Train the model (this is crucial!)
rasa train

# Wait for training to complete (should take 1-2 minutes)
```

### **Step 3: Start Actions Server (Terminal 1)**
```powershell
# Set environment variables
$env:AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_API_KEY_HERE"
$env:AZURE_OPENAI_ENDPOINT="https://hackathon-azure-openai-east-us.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT="o4-mini"

# Start actions server
venv\Scripts\rasa.exe run actions

# Wait for: "Action endpoint is up and running on http://0.0.0.0:5055"
```

### **Step 4: Start Web Server (Terminal 2 - NEW WINDOW)**
```powershell
# Open a NEW PowerShell window
cd "C:\FAQ's"

# Activate virtual environment
venv\Scripts\activate

# Start web server
python web_server.py

# Wait for: "Running on http://localhost:3000"
```

### **Step 5: Test the Bot**
- Open browser: http://localhost:3000
- Type: "How do I get started?"
- Expected response: "To get started with Sage Network Connectors: 1. Visit the developer portal..."

---

## 🔧 **Alternative: All-in-One Script**

If manual steps don't work, use this automated script: 