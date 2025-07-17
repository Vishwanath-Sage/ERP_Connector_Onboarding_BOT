# 🚀 Quick Start: Rasa + Azure OpenAI Integration

## ⚡ Fastest Setup (3 Minutes)

### Step 1: ✅ Your Azure OpenAI Key is Ready!
Perfect! I can see you have an Azure OpenAI API key. Azure OpenAI keys are longer and have a different format than regular OpenAI keys.

**Your key:** `7nmb9wlXxOVC1sZlkDTymY4jOn6u4ahkWAGBLcPXWMSPkDqefRQMJQQJ99BGACYeBjFXJ3w3AAABACOGbpXp`

### Step 2: Run Setup
Open PowerShell in your project folder and run:
```powershell
.\setup_openai.ps1
```
When prompted, provide:
1. **API Key**: `7nmb9wlXxOVC1sZlkDTymY4jOn6u4ahkWAGBLcPXWMSPkDqefRQMJQQJ99BGACYeBjFXJ3w3AAABACOGbpXp`
2. **Endpoint**: Your Azure OpenAI endpoint (e.g., `https://your-resource.openai.azure.com/`)
3. **Deployment**: Your model deployment name (e.g., `gpt-35-turbo`, `gpt-4`)

### Step 3: Test Configuration
```powershell
python test_openai.py
```
This validates your Azure OpenAI setup.

### Step 4: Start the Bot
```powershell
.\start_bot.ps1
```
This automatically starts all three services and opens your browser.

### Step 5: Test It!
Visit http://localhost:3000 and try asking:
- "What is Sage Network Connectors?"
- "How do I authenticate with OAuth 2.0?"
- "Explain rate limiting best practices"
- "Show me error handling patterns"

---

## 🔧 Manual Setup (If Scripts Don't Work)

### 1. Set Environment Variables
```powershell
$env:AZURE_OPENAI_API_KEY = "YOUR_AZURE_OPENAI_API_KEY_HERE"
$env:AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT = "gpt-35-turbo"

# Make them permanent
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "YOUR_AZURE_OPENAI_API_KEY_HERE", [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com/", [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo", [System.EnvironmentVariableTarget]::User)
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Start Services (3 separate terminals)
```powershell
# Terminal 1: Actions Server
rasa run actions

# Terminal 2: Rasa Server  
rasa run --enable-api --cors "*"

# Terminal 3: Web Interface
python web_server.py
```

---

## 🧪 Test Your Setup
```powershell
python test_openai.py
```

---

## ✨ What You Get

### Enhanced Capabilities
- **Intelligent Responses**: Azure OpenAI handles complex technical questions
- **Fallback System**: Unknown queries get smart responses instead of "I don't understand"
- **Context Awareness**: Better understanding of developer questions
- **Natural Conversations**: More human-like interaction

### Cost Efficiency (Azure OpenAI Pricing)
- **Hybrid Approach**: Simple FAQs use free Rasa responses
- **Smart Routing**: Only complex queries use Azure OpenAI (saves money)
- **Token Optimization**: Responses limited to 300 tokens
- **Pay-per-use**: Only pay for actual API calls

### Example Interactions

**Traditional Rasa Response:**
```
User: "What is Sage Network Connectors?"
Bot: [Pre-defined response from training data]
```

**Enhanced Azure OpenAI Response:**
```
User: "How do I implement exponential backoff for API rate limiting?"
Bot: [Intelligent, contextual response explaining rate limiting, backoff strategies, 
     code examples, and best practices specific to Sage APIs with Azure OpenAI's 
     enhanced understanding]
```

---

## 🚨 Troubleshooting

### Common Issues

1. **"Azure OpenAI API key not found"**
   - Run `.\setup_openai.ps1` again
   - Your key is ready: `7nmb9wlXxOVC1sZlkDTymY4jOn6u4ahkWAGBLcPXWMSPkDqefRQMJQQJ99BGACYeBjFXJ3w3AAABACOGbpXp`

2. **"Invalid API key"**
   - Verify your key in Azure Portal > Your OpenAI Resource > Keys and Endpoint
   - Check for extra spaces or characters

3. **"Deployment not found"**
   - Check your deployment name in Azure Portal
   - Common names: `gpt-35-turbo`, `gpt-4`, `gpt-4-turbo`

4. **"Endpoint error"**
   - Verify endpoint format: `https://your-resource.openai.azure.com/`
   - Must end with `/`

5. **"Python not found"**
   - Install Python 3.8+ from https://python.org
   - Make sure "Add to PATH" is checked during installation

6. **"Cannot load PowerShell script"**
   - Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Azure OpenAI Specific

1. **Find Your Endpoint**: Azure Portal > Your OpenAI Resource > Keys and Endpoint
2. **Find Your Deployment**: Azure Portal > Your OpenAI Resource > Model deployments
3. **Check Quota**: Azure Portal > Your OpenAI Resource > Quotas

### Need Help?
- 📖 Full documentation: `OPENAI_INTEGRATION.md`
- 🧪 Test your setup: `python test_openai.py`
- 🌐 Azure Portal: https://portal.azure.com
- 📊 Monitor usage: Azure Portal > Your OpenAI Resource > Metrics

---

## 🎯 Next Steps

1. **Customize Prompts**: Edit system prompts in `actions/actions.py`
2. **Add More Actions**: Create new Azure OpenAI-powered actions for specific use cases
3. **Monitor Costs**: Track usage in Azure Portal
4. **Scale Up**: Deploy to Azure for production use

## 🔐 Security Note
Your API key is now safely stored as an environment variable and won't be exposed in your code files.

Happy coding with Azure OpenAI! 🚀🤖 