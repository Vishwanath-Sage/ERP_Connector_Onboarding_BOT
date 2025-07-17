# OpenAI Integration Guide

## Overview

This guide explains how to integrate OpenAI models with your Rasa FAQ bot for enhanced responses and better handling of complex queries.

## Integration Methods

### 1. Hybrid Approach (Recommended)
- **Rasa**: Handles intent classification and simple FAQ responses
- **OpenAI**: Provides enhanced responses for complex queries and fallbacks

### 2. Custom Actions with OpenAI
- Use `action_openai_response` for specific intents
- Use `action_openai_fallback` for unknown/complex queries

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file or set environment variables:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

### 3. Configure Actions Server
The actions are now configured in:
- `actions/actions.py` - Custom OpenAI actions
- `domain.yml` - Action definitions
- `endpoints.yml` - Action server endpoint

### 4. Usage Examples

#### Option A: Replace specific responses with OpenAI
Update your rules in `data/rules.yml`:
```yaml
- rule: Enhanced API documentation response
  steps:
  - intent: api_documentation
  - action: action_openai_response
```

#### Option B: Use as fallback for unknown queries
Update `config.yml`:
```yaml
policies:
  - name: RulePolicy
    core_fallback_threshold: 0.3
    core_fallback_action_name: "action_openai_fallback"
```

## Running with OpenAI Integration

### Start the Action Server
```bash
rasa run actions
```

### Start Rasa Server
```bash
rasa run --enable-api --cors "*"
```

### Start Web Interface
```bash
python web_server.py
```

## Configuration Options

### Available Models
- `gpt-3.5-turbo` (default, cost-effective)
- `gpt-4` (more capable, higher cost)
- `gpt-4-turbo` (latest, balanced performance)

### Customization
Modify the actions in `actions/actions.py`:
- Change model selection
- Adjust max_tokens (response length)
- Modify temperature (creativity level)
- Update system prompts for better context

## Cost Considerations

### Pricing (as of 2024)
- **GPT-3.5-turbo**: ~$0.001/1K tokens
- **GPT-4**: ~$0.03/1K tokens
- **Average response**: 100-300 tokens

### Cost Optimization
1. Use GPT-3.5-turbo for most queries
2. Set appropriate max_tokens limits
3. Cache common responses
4. Use OpenAI only for complex queries

## Alternative Integration Approaches

### Option 1: Complete OpenAI Replacement
Replace entire Rasa NLU/Core with OpenAI:
```python
# Direct API approach in web_server.py
def get_openai_response(user_message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Sage Network Connectors assistant..."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content
```

### Option 2: Vector Database + OpenAI
1. Create embeddings from your FAQ content
2. Use vector search to find relevant context
3. Pass context to OpenAI for response generation

### Option 3: Fine-tuned Models
1. Fine-tune GPT models on your specific FAQ data
2. Use for domain-specific responses
3. Better performance for your use case

## Monitoring and Analytics

### Response Quality
- Log OpenAI responses for quality review
- A/B test against traditional Rasa responses
- Monitor user satisfaction

### Usage Tracking
```python
# Add to actions
import logging
logging.info(f"OpenAI call: {user_message} -> {ai_response}")
```

## Troubleshooting

### Common Issues
1. **API Key Error**: Ensure OPENAI_API_KEY is set correctly
2. **Rate Limits**: Implement retry logic with exponential backoff
3. **Cost Control**: Set monthly spending limits in OpenAI dashboard
4. **Response Quality**: Improve system prompts and context

### Fallback Strategy
The implementation includes fallbacks:
- If OpenAI fails → Use default Rasa response
- If no API key → Skip OpenAI, use traditional flow
- Network issues → Graceful degradation

## Security Considerations

1. **API Key Protection**: Never commit API keys to version control
2. **User Privacy**: Don't log sensitive user information
3. **Content Filtering**: OpenAI has built-in content policies
4. **Rate Limiting**: Implement user-level rate limiting

## Next Steps

1. **Test the Integration**: Try various queries to see OpenAI responses
2. **Customize Prompts**: Tailor system prompts for your specific needs
3. **Monitor Usage**: Track costs and response quality
4. **Optimize Performance**: Fine-tune based on user feedback

## Support

For issues with:
- **Rasa Integration**: Check Rasa documentation
- **OpenAI API**: Review OpenAI documentation
- **Custom Actions**: Debug using rasa shell with --debug flag 