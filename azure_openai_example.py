"""
Example: Direct Azure OpenAI integration for FAQ bot
Alternative to Rasa - simpler but less structured approach
Works with your Azure OpenAI key: 7nmb9wlXxOVC1sZlkDTymY4jOn6u4ahkWAGBLcPXWMSPkDqefRQMJQQJ99BGACYeBjFXJ3w3AAABACOGbpXp
"""

import os
from openai import AzureOpenAI
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Initialize Azure OpenAI client with your exact configuration
def get_azure_client():
    return AzureOpenAI(
        api_key="7nmb9wlXxOVC1sZlkDTymY4jOn6u4ahkWAGBLcPXWMSPkDqefRQMJQQJ99BGACYeBjFXJ3w3AAABACOGbpXp",
        api_version="2025-01-01-preview",
        azure_endpoint="https://hackathon-azure-openai-east-us.openai.azure.com/"
    )

# FAQ context for better responses
FAQ_CONTEXT = """
You are a helpful assistant for Sage Network Connectors. Answer questions about:

Key Topics:
- Getting started with Sage Network Connectors
- API documentation and authentication
- Connector types and supported platforms  
- Troubleshooting and integration help
- Rate limits and error codes
- OAuth authentication and API keys
- REST API endpoints and request/response formats
- Sage Intacct, Sage 50, Sage 200 integration
- Invoice/bill processing, payment handling
- Data synchronization and custom fields
- Webhooks and batch processing

Guidelines:
- Provide clear, actionable answers with code examples when relevant
- Include specific API endpoints when applicable
- Suggest checking documentation for detailed guides
- For complex issues, recommend contacting support
- Keep responses concise but comprehensive
- Focus on practical solutions for developers
"""

def get_azure_openai_response(user_message, conversation_history=None):
    """Get response from Azure OpenAI with context"""
    
    client = get_azure_client()
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "o4-mini")
    
    messages = [{"role": "system", "content": FAQ_CONTEXT}]
    
    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            max_tokens=400,
            temperature=0.3,  # Lower temperature for more consistent responses
            presence_penalty=0.1,  # Reduce repetition
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Azure OpenAI API error: {e}")
        return get_fallback_response(user_message)

def get_fallback_response(user_message):
    """Fallback responses when Azure OpenAI is unavailable"""
    
    # Simple keyword matching for fallbacks
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm here to help with Sage Network Connectors questions."
    
    elif any(word in message_lower for word in ['api', 'documentation']):
        return "You can find API documentation at the Sage Developer Portal. For specific endpoints, check the REST API reference."
    
    elif any(word in message_lower for word in ['authentication', 'auth', 'oauth']):
        return "Sage Network Connectors support OAuth 2.0 authentication. You'll need to register your application and obtain API credentials from the developer portal."
    
    elif any(word in message_lower for word in ['error', 'problem', 'issue']):
        return "For troubleshooting, please check the error codes in our documentation or contact support with specific error details and request/response samples."
    
    else:
        return "I'm sorry, I couldn't process your request right now. Please try again or contact support for assistance."

# Enhanced chat interface optimized for Azure OpenAI
AZURE_CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Sage Network Connectors FAQ Bot (Azure OpenAI)</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            max-width: 900px; 
            margin: 0 auto; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 { 
            color: #333; 
            text-align: center; 
            margin-bottom: 10px;
            font-size: 24px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .chat-container { 
            border: 2px solid #e0e0e0; 
            height: 450px; 
            overflow-y: auto; 
            padding: 15px; 
            margin-bottom: 15px; 
            border-radius: 8px;
            background: #fafafa;
        }
        .message { 
            margin-bottom: 15px; 
            padding: 10px 15px;
            border-radius: 8px;
            max-width: 80%;
        }
        .user { 
            text-align: right; 
            background: #007bff;
            color: white;
            margin-left: auto;
        }
        .bot { 
            text-align: left; 
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            color: #333;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        input[type="text"] { 
            flex: 1;
            padding: 12px; 
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 14px;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #007bff;
        }
        button { 
            padding: 12px 20px; 
            background: #007bff;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
        }
        button:hover {
            background: #0056b3;
        }
        .status {
            text-align: center;
            font-size: 12px;
            color: #666;
            margin-top: 10px;
        }
        .examples {
            margin-top: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #007bff;
        }
        .examples h3 {
            margin: 0 0 10px 0;
            color: #333;
            font-size: 14px;
        }
        .example {
            cursor: pointer;
            padding: 5px;
            border-radius: 4px;
            margin: 2px 0;
            font-size: 13px;
            color: #555;
        }
        .example:hover {
            background: #e9ecef;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Sage Network Connectors FAQ Bot</h1>
        <div class="subtitle">Powered by Azure OpenAI</div>
        
        <div id="chat" class="chat-container">
            <div class="message bot">
                <strong>Bot:</strong> Hello! I'm your Sage Network Connectors assistant powered by Azure OpenAI. 
                I can help you with API documentation, authentication, troubleshooting, and integration guidance. 
                What would you like to know?
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="userInput" placeholder="Ask about Sage Network Connectors..." />
            <button onclick="sendMessage()">Send</button>
        </div>
        
        <div class="status" id="status">Ready to help! Powered by Azure OpenAI</div>
        
        <div class="examples">
            <h3>💡 Try these questions:</h3>
            <div class="example" onclick="askExample('What is Sage Network Connectors?')">• What is Sage Network Connectors?</div>
            <div class="example" onclick="askExample('How do I authenticate with OAuth 2.0?')">• How do I authenticate with OAuth 2.0?</div>
            <div class="example" onclick="askExample('What are the API rate limits?')">• What are the API rate limits?</div>
            <div class="example" onclick="askExample('How do I handle API errors gracefully?')">• How do I handle API errors gracefully?</div>
            <div class="example" onclick="askExample('Show me integration patterns for Sage Intacct')">• Show me integration patterns for Sage Intacct</div>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;

            // Add user message to chat
            addMessage('You: ' + message, 'user');
            input.value = '';
            
            // Show loading status
            document.getElementById('status').textContent = 'Azure OpenAI is thinking...';

            // Send to server
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                addMessage('Bot: ' + data.response, 'bot');
                document.getElementById('status').textContent = 'Ready to help! Powered by Azure OpenAI';
            })
            .catch(error => {
                addMessage('Bot: Sorry, I encountered an error. Please try again.', 'bot');
                document.getElementById('status').textContent = 'Error - Please try again';
            });
        }

        function addMessage(text, className) {
            const chat = document.getElementById('chat');
            const div = document.createElement('div');
            div.className = 'message ' + className;
            div.innerHTML = text.replace(/\n/g, '<br>');
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }
        
        function askExample(question) {
            document.getElementById('userInput').value = question;
            sendMessage();
        }

        // Send message on Enter key
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
        
        // Auto-focus input
        document.getElementById('userInput').focus();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Serve the chat interface"""
    return render_template_string(AZURE_CHAT_HTML)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Please enter a message.'})
    
    # Get response from Azure OpenAI
    response = get_azure_openai_response(user_message)
    
    return jsonify({'response': response})

@app.route('/status')
def status():
    """Check if Azure OpenAI is configured"""
    api_key = "7nmb9wlXxOVC1sZlkDTymY4jOn6u4ahkWAGBLcPXWMSPkDqefRQMJQQJ99BGACYeBjFXJ3w3AAABACOGbpXp"
    endpoint = "https://hackathon-azure-openai-east-us.openai.azure.com/"
    deployment = "o4-mini"
    
    return jsonify({
        'azure_openai_configured': bool(api_key and endpoint),
        'api_key_present': bool(api_key),
        'endpoint_present': bool(endpoint),
        'deployment': deployment,
        'status': 'ready' if (api_key and endpoint) else 'needs_configuration'
    })

if __name__ == '__main__':
    # Check if Azure OpenAI is configured
    api_key = "7nmb9wlXxOVC1sZlkDTymY4jOn6u4ahkWAGBLcPXWMSPkDqefRQMJQQJ99BGACYeBjFXJ3w3AAABACOGbpXp"
    endpoint = "https://hackathon-azure-openai-east-us.openai.azure.com/"
    deployment = "o4-mini"
    
    print("🤖 Azure OpenAI FAQ Bot")
    print("=" * 50)
    print("✅ Azure OpenAI API key configured!")
    print(f"✅ Azure OpenAI endpoint: {endpoint}")
    print(f"✅ Using deployment: {deployment}")
    print("")
    print(f"🚀 Starting Azure OpenAI FAQ bot at http://localhost:3001")
    print(f"📚 Direct Azure OpenAI integration (no Rasa)")
    print(f"💡 Ready to answer questions about Sage Network Connectors!")
    
    app.run(host='0.0.0.0', port=3001, debug=True) 