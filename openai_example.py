"""
Example: Direct OpenAI integration for FAQ bot
Alternative to Rasa - simpler but less structured approach
"""

import os
from openai import OpenAI
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FAQ context for better responses
FAQ_CONTEXT = """
You are a helpful assistant for Sage Network Connectors. Answer questions about:

Key Topics:
- Getting started with Sage Network Connectors
- API documentation and authentication
- Connector types and supported platforms  
- Troubleshooting and integration help
- Rate limits and error codes
- OAuth authentication
- REST API endpoints
- Sage Intacct, Sage 50, Sage 200 integration
- Invoice/bill processing, payment handling
- Data synchronization and custom fields

Guidelines:
- Provide clear, actionable answers
- Include relevant API endpoints when applicable
- Suggest checking documentation for detailed guides
- For complex issues, recommend contacting support
- Keep responses concise but helpful
"""

def get_openai_response(user_message, conversation_history=None):
    """Get response from OpenAI with context"""
    
    messages = [{"role": "system", "content": FAQ_CONTEXT}]
    
    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=400,
            temperature=0.3,  # Lower temperature for more consistent responses
            presence_penalty=0.1,  # Reduce repetition
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return get_fallback_response(user_message)

def get_fallback_response(user_message):
    """Fallback responses when OpenAI is unavailable"""
    
    # Simple keyword matching for fallbacks
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm here to help with Sage Network Connectors questions."
    
    elif any(word in message_lower for word in ['api', 'documentation']):
        return "You can find API documentation at the Sage Developer Portal. For specific endpoints, check the REST API reference."
    
    elif any(word in message_lower for word in ['authentication', 'auth', 'oauth']):
        return "Sage Network Connectors support OAuth 2.0 authentication. You'll need to register your application and obtain API credentials."
    
    elif any(word in message_lower for word in ['error', 'problem', 'issue']):
        return "For troubleshooting, please check the error codes in our documentation or contact support with specific error details."
    
    else:
        return "I'm sorry, I couldn't process your request right now. Please try again or contact support for assistance."

# Simple chat interface (similar to existing web_server.py structure)
SIMPLE_CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>OpenAI-Powered FAQ Bot</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .chat-container { border: 1px solid #ddd; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        .message { margin-bottom: 10px; }
        .user { text-align: right; color: blue; }
        .bot { text-align: left; color: green; }
        input[type="text"] { width: 70%; padding: 10px; }
        button { width: 25%; padding: 10px; }
    </style>
</head>
<body>
    <h1>Sage Network Connectors FAQ Bot (OpenAI)</h1>
    <div id="chat" class="chat-container"></div>
    <input type="text" id="userInput" placeholder="Ask about Sage Network Connectors..." />
    <button onclick="sendMessage()">Send</button>

    <script>
        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value;
            if (!message) return;

            // Add user message to chat
            addMessage('You: ' + message, 'user');
            input.value = '';

            // Send to server
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                addMessage('Bot: ' + data.response, 'bot');
            });
        }

        function addMessage(text, className) {
            const chat = document.getElementById('chat');
            const div = document.createElement('div');
            div.className = 'message ' + className;
            div.textContent = text;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        // Send message on Enter key
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Serve the chat interface"""
    return render_template_string(SIMPLE_CHAT_HTML)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Please enter a message.'})
    
    # Get response from OpenAI
    response = get_openai_response(user_message)
    
    return jsonify({'response': response})

@app.route('/status')
def status():
    """Check if OpenAI is configured"""
    api_key = os.getenv("OPENAI_API_KEY")
    return jsonify({
        'openai_configured': bool(api_key),
        'model': 'gpt-3.5-turbo',
        'status': 'ready' if api_key else 'needs_api_key'
    })

if __name__ == '__main__':
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set!")
        print("   Set it with: export OPENAI_API_KEY='your-api-key-here'")
        print("   The bot will use fallback responses without OpenAI.")
    else:
        print("✅ OpenAI API key found - enhanced responses enabled!")
    
    print(f"🚀 Starting FAQ bot at http://localhost:3001")
    print(f"📚 Using OpenAI integration example")
    
    app.run(host='0.0.0.0', port=3001, debug=True) 