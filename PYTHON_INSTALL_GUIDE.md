# 🐍 Python Installation & Azure OpenAI Bot Setup

## 🎯 Your Configuration is Ready!
- ✅ **Endpoint**: `https://hackathon-azure-openai-east-us.openai.azure.com/`
- ✅ **Deployment**: `o4-mini`
- ✅ **API Key**: Configured
- ⚠️ **Need**: Python installation

---

## 📥 Step 1: Install Python

### Option A: Download from Python.org (Recommended)
1. **Go to**: https://python.org/downloads/
2. **Download**: Python 3.8 or newer (latest recommended)
3. **CRITICAL**: During installation, check ✅ **"Add Python to PATH"**
4. **Install**: Follow the installer

### Option B: Microsoft Store (Windows 10/11)
1. Open **Microsoft Store**
2. Search **"Python"**
3. Install **Python 3.12** (or latest)

### Option C: Chocolatey (If you have it)
```powershell
choco install python
```

---

## 🔄 Step 2: Verify Installation
**Restart PowerShell**, then test:
```powershell
python --version
pip --version
```

**Expected output:**
```
Python 3.12.x
pip 24.x
```

---

## 📦 Step 3: Install Dependencies
```powershell
pip install openai flask
```

---

## ⚙️ Step 4: Configure Azure OpenAI
**Your configuration** (already set in session):
```powershell
$env:AZURE_OPENAI_API_KEY = "YOUR_AZURE_OPENAI_API_KEY_HERE"
$env:AZURE_OPENAI_ENDPOINT = "https://hackathon-azure-openai-east-us.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT = "o4-mini"
```

**Make it permanent** (optional):
```powershell
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "YOUR_AZURE_OPENAI_API_KEY_HERE", [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "https://hackathon-azure-openai-east-us.openai.azure.com/", [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT", "o4-mini", [System.EnvironmentVariableTarget]::User)
```

---

## 🚀 Step 5: Launch Your Bot!

### Simple Azure OpenAI Bot:
```powershell
python azure_openai_example.py
```
**Access**: http://localhost:3001

### Full Rasa + Azure OpenAI Integration:
```powershell
# Install Rasa (if needed)
pip install rasa rasa-sdk

# Train model
rasa train

# Start services (3 terminals)
rasa run actions                    # Terminal 1
rasa run --enable-api --cors "*"   # Terminal 2
python web_server.py               # Terminal 3
```
**Access**: http://localhost:3000

---

## 🧪 Step 6: Test Azure OpenAI Connection
```powershell
python test_openai.py
```

**Success looks like:**
```
🤖 Sage Network Connectors - Azure OpenAI Integration Test
======================================================================

🧪 Testing Azure OpenAI Integration...
==================================================
✅ API key found: 7nmb9wlX...bpXp
✅ Endpoint: https://hackathon-azure-openai-east-us.openai.azure.com/
✅ Deployment: o4-mini
✅ Azure OpenAI client initialized successfully

🔍 Testing API call...
✅ API call successful!
📝 Sample response: Sage Network Connectors are enterprise-grade APIs...
🔢 Tokens used: 87

🎉 ALL TESTS PASSED!
✅ Azure OpenAI integration is ready
✅ Rasa integration is ready

🚀 You can now run: .\start_bot.ps1
```

---

## 🎯 What You'll Experience

Once running, ask questions like:

### 🤖 **Basic FAQ**:
- "What is Sage Network Connectors?"
- "How do I get started?"

### 🧠 **AI-Enhanced Responses**:
- "Show me OAuth 2.0 implementation with code examples"
- "Explain error handling patterns for API integration"
- "How do I implement rate limiting with exponential backoff?"
- "What are the best practices for webhook security?"

### 🔧 **Technical Deep Dives**:
- "Generate a Python script for Sage Intacct bill creation"
- "Explain multi-currency handling in invoice processing"
- "Show me integration patterns for Sage 200"

---

## 🚨 Troubleshooting

### "Python still not found after installation"
1. **Restart PowerShell** (important!)
2. Try: `py --version` (alternative command)
3. **Reinstall Python** with "Add to PATH" checked

### "pip not found"
```powershell
python -m pip --version
```

### "Module not found errors"
```powershell
pip install openai flask rasa rasa-sdk
```

### "Azure OpenAI connection fails"
- ✅ Your endpoint is correct: `hackathon-azure-openai-east-us.openai.azure.com`
- ✅ Your deployment is: `o4-mini`  
- ✅ Your API key is set
- Check firewall/network restrictions

---

## 🎉 Next Steps After Installation

1. **Install Python** → **Test** → **Run Bot**
2. **Experience AI-powered FAQ responses**
3. **Customize prompts** in `actions/actions.py`
4. **Add more FAQ content** in `data/nlu.yml`
5. **Deploy to Azure** for production use

---

## 📞 Need Help?

**Files to check:**
- `YOUR_AZURE_CONFIG.txt` - Your exact configuration
- `test_openai.py` - Test your setup
- `azure_openai_example.py` - Simple bot
- `QUICK_START_SIMPLE.md` - Alternative instructions

**Your Azure OpenAI is configured and ready - just need Python! 🐍✨** 