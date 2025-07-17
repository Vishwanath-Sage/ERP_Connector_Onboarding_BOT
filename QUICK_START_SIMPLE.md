# 🚀 Quick Start: Simple Azure OpenAI Bot

## Option 1: Install Python (Recommended)

### 1. Download Python
- Go to https://python.org/downloads/
- Download Python 3.8 or newer
- **IMPORTANT**: Check "Add Python to PATH" during installation

### 2. Verify Installation
```powershell
python --version
pip --version
```

### 3. Install Dependencies
```powershell
pip install openai flask
```

### 4. Configure Azure OpenAI
Replace `YOUR-RESOURCE-NAME` with your actual Azure resource name:

```powershell
$env:AZURE_OPENAI_API_KEY = "YOUR_AZURE_OPENAI_API_KEY_HERE"
$env:AZURE_OPENAI_ENDPOINT = "https://YOUR-RESOURCE-NAME.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT = "gpt-35-turbo"
```

### 5. Start the Bot
```powershell
python azure_openai_example.py
```

### 6. Access Your Bot
Open your browser to: **http://localhost:3001**

---

## Option 2: Using Virtual Environment

If you prefer to use the existing virtual environment:

### 1. Create/Recreate Virtual Environment
```powershell
# Remove existing venv if problematic
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue

# Create new virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install openai flask
```

### 3. Set Configuration & Run
```powershell
# Set your Azure OpenAI configuration
$env:AZURE_OPENAI_API_KEY = "YOUR_AZURE_OPENAI_API_KEY_HERE"
$env:AZURE_OPENAI_ENDPOINT = "https://YOUR-RESOURCE-NAME.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT = "gpt-35-turbo"

# Run the bot
python azure_openai_example.py
```

---

## 🔍 Finding Your Azure OpenAI Endpoint

1. Go to https://portal.azure.com
2. Search for "OpenAI" or find your OpenAI resource
3. Click on your OpenAI resource
4. Go to "Keys and Endpoint" in the left menu
5. Copy the "Endpoint" URL (looks like: `https://your-resource.openai.azure.com/`)

**Example endpoints:**
- `https://my-openai-resource.openai.azure.com/`
- `https://company-gpt.openai.azure.com/`
- `https://sage-ai.openai.azure.com/`

---

## 💬 What You'll Experience

Once running, you can ask questions like:

**🤖 Enhanced AI Responses:**
- "What is Sage Network Connectors?"
- "How do I authenticate with OAuth 2.0?"
- "Show me API rate limiting best practices"
- "Explain error handling patterns with code examples"
- "What are the integration steps for Sage Intacct?"

**🎯 Smart Features:**
- ✅ Contextual understanding
- ✅ Code examples
- ✅ Step-by-step guides
- ✅ Best practices
- ✅ Troubleshooting help

---

## 🚨 Troubleshooting

### "Python not found"
- Install Python from https://python.org
- Make sure to check "Add to PATH" during installation
- Restart PowerShell after installation

### "Module not found"
```powershell
pip install openai flask
```

### "Invalid endpoint"
- Check your endpoint URL in Azure Portal
- Make sure it ends with `/`
- Example: `https://your-resource.openai.azure.com/`

### "API Key issues"
- Your key is already set: `YOUR_AZURE_OPENAI_API_KEY_HERE`
- Verify it matches your Azure Portal key

---

## 🎉 Success!

When working, you'll see:
```
🤖 Azure OpenAI FAQ Bot
==================================================
✅ Azure OpenAI API key found!
✅ Azure OpenAI endpoint: https://your-resource.openai.azure.com/
✅ Using deployment: gpt-35-turbo

🚀 Starting Azure OpenAI FAQ bot at http://localhost:3001
📚 Direct Azure OpenAI integration (no Rasa)
💡 Your Azure OpenAI key is ready to use!
```

**Your intelligent FAQ bot will be live at http://localhost:3001! 🚀** 