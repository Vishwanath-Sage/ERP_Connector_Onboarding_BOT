# MCP Integration Setup Guide

## Model Context Protocol (MCP) for Sage Network Connectors Bot

This guide explains how to set up and use the Model Context Protocol features in your Sage Network Connectors FAQ bot to assist external developers.

## What is MCP Integration?

The MCP integration allows your bot to:
- **Live API Testing**: Test Sage API endpoints directly through chat
- **Dynamic Schema Retrieval**: Fetch current API documentation and schemas
- **Code Generation**: Generate connector code examples in multiple languages
- **System Status Monitoring**: Check API health and availability
- **Interactive Development Support**: Provide real-time assistance to developers

## Environment Variables Setup

Set these environment variables for full MCP functionality:

```bash
# Sage API Configuration
SAGE_API_BASE_URL=https://api.sage.com
SAGE_API_KEY=your_sage_api_key_here

# GitHub Integration (optional)
GITHUB_TOKEN=your_github_token_here

# OpenAI Configuration (existing)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Azure OpenAI (alternative)
AZURE_OPENAI_API_KEY=your_azure_openai_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-35-turbo
```

## New Bot Capabilities

### 1. API Schema Retrieval
**User says:** "Show me the API schema for bills"
**Bot does:** Fetches live API documentation and structure

### 2. Live API Testing
**User says:** "Can I test the vendors API?"
**Bot does:** Makes actual API calls and shows results

### 3. Code Generation
**User says:** "Show me a Python example for authentication"
**Bot does:** Generates working code snippets

### 4. System Status Checks
**User says:** "Are the Sage APIs up?"
**Bot does:** Checks API health and reports status

## Example Conversations

### API Schema Request
```
Developer: "What's the structure of the invoices API?"
Bot: "Here's the current API schema for invoices:
{
  "fields": {
    "invoice_id": "string",
    "amount": "decimal",
    "currency": "string",
    "vendor_id": "string"
  }
}
Based on this schema, you'll need to include..."
```

### Code Example Generation
```
Developer: "How do I implement authentication in Python?"
Bot: "Here's a Python example for OAuth2 authentication:

```python
import requests

def get_access_token(client_id, client_secret):
    url = "https://api.sage.com/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, data=payload)
    return response.json()["access_token"]
```

This implementation handles the OAuth2 flow..."
```

## Advanced Features

### Multi-Language Support
The bot can generate code examples in:
- Python
- JavaScript/Node.js
- C#
- Java

### Real-Time API Validation
- Tests API endpoints with actual data
- Validates request formats
- Shows response structures
- Identifies authentication issues

### Dynamic Documentation
- Always uses latest API schemas
- Reflects current field requirements
- Shows available endpoints
- Includes deprecation notices

## Installation and Setup

1. **Update Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables:**
   Set the required environment variables in your system or `.env` file

3. **Train the Bot:**
   ```bash
   rasa train
   ```

4. **Start the Bot:**
   ```bash
   rasa run actions & rasa shell
   ```

## Security Considerations

- **API Keys**: Never expose real API keys in examples
- **Rate Limiting**: Respect API rate limits during testing
- **Permissions**: Use read-only tokens where possible
- **Logging**: Be careful about logging sensitive data

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   - Ensure environment variables are set correctly
   - Check API key permissions

2. **Connection Errors**
   - Verify SAGE_API_BASE_URL is correct
   - Check network connectivity

3. **Schema Fetch Failures**
   - Confirm API endpoint exists
   - Verify authentication

## Benefits for External Developers

1. **Faster Development**: Get immediate answers and examples
2. **Reduced Support Load**: Self-service troubleshooting
3. **Current Information**: Always up-to-date API details
4. **Interactive Testing**: Test ideas without writing code
5. **Multi-Language Support**: Examples in preferred languages

## Next Steps

- Add more sophisticated NLP for parameter extraction
- Implement webhook testing capabilities
- Add support for batch operations
- Include performance monitoring
- Add integration with CI/CD pipelines 