# 🚀 IMMEDIATE SETUP: Your Azure OpenAI Integration

## ✅ Your API Key is Configured!
Your Azure OpenAI key is already set: `7nmb9wlXxOVC1sZlkDTymY4jOn6u4ahkWAGBLcPXWMSPkDqefRQMJQQJ99BGACYeBjFXJ3w3AAABACOGbpXp`

## 🎯 Next Steps (2 minutes)

### Step 1: Set Your Azure OpenAI Endpoint
You need your Azure OpenAI endpoint URL. Run this command with YOUR endpoint:

```powershell
$env:AZURE_OPENAI_ENDPOINT = "https://YOUR-RESOURCE-NAME.openai.azure.com/"
```

**Where to find your endpoint:**
1. Go to https://portal.azure.com
2. Find your OpenAI resource
3. Go to "Keys and Endpoint"
4. Copy the endpoint URL

### Step 2: Test the Configuration
```powershell
python test_openai.py
```

### Step 3: Install Dependencies (if needed)
```powershell
pip install openai flask rasa rasa-sdk
```

### Step 4: Start the Bot!

**Option A: Simple Azure OpenAI Bot (No Rasa)**
```powershell
python azure_openai_example.py
```
Then visit: http://localhost:3001

**Option B: Full Rasa + Azure OpenAI Integration**
Open 3 PowerShell windows and run:
```powershell
# Window 1:
rasa run actions

# Window 2: 
rasa run --enable-api --cors "*"

# Window 3:
python web_server.py
```
Then visit: http://localhost:3000

## 🔧 Quick Manual Setup
If you want to set everything at once:

```powershell
# Your configuration
$env:AZURE_OPENAI_API_KEY = "YOUR_AZURE_OPENAI_API_KEY_HERE"
$env:AZURE_OPENAI_ENDPOINT = "https://YOUR-RESOURCE-NAME.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT = "gpt-35-turbo"

# Make permanent (optional)
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "YOUR_AZURE_OPENAI_API_KEY_HERE", [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "https://YOUR-RESOURCE-NAME.openai.azure.com/", [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo", [System.EnvironmentVariableTarget]::User)
```

## 💡 What You'll Get

### Traditional FAQ Response:
```
User: "How do I handle API errors?"
Bot: "Check our documentation for error handling guides."
```

### Azure OpenAI Enhanced Response:
```
User: "How do I handle API errors?"
Bot: "Here's a comprehensive approach to API error handling:

1. **Implement Retry Logic**:
   - Use exponential backoff for transient failures
   - Maximum 3-5 retry attempts
   
2. **Parse Error Codes**:
   - 401: Authentication issues
   - 429: Rate limit exceeded
   - 500: Server errors
   
3. **Code Example**:
   ```python
   import time
   import requests
   
   def api_call_with_retry(url, headers, max_retries=3):
       for attempt in range(max_retries):
           try:
               response = requests.get(url, headers=headers)
               if response.status_code == 429:
                   time.sleep(2 ** attempt)  # Exponential backoff
                   continue
               return response
           except requests.exceptions.RequestException as e:
               print(f"Attempt {attempt + 1} failed: {e}")
               if attempt == max_retries - 1:
                   raise
   ```

Would you like me to explain any specific error scenario?"
```

## 🎉 You're Ready!
Your Azure OpenAI integration is configured and ready to provide intelligent, contextual responses about Sage Network Connectors!

---

**Need your endpoint?** Check Azure Portal → Your OpenAI Resource → Keys and Endpoint 