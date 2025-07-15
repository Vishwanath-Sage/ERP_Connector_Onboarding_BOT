"""
Flask Web Server for Sage Network Connectors FAQ Bot
Serves the chatbot interface and handles API requests to Rasa
"""

from flask import Flask, render_template_string, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# HTML template for the chatbot interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sage Network Connectors FAQ Bot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .chat-container {
            width: 800px;
            height: 600px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-header {
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }

        .chat-header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }

        .chat-header p {
            opacity: 0.8;
            font-size: 14px;
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }

        .message {
            margin-bottom: 15px;
            display: flex;
        }

        .message.bot {
            justify-content: flex-start;
        }

        .message.user {
            justify-content: flex-end;
        }

        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
            white-space: pre-wrap;
        }

        .message.bot .message-content {
            background: #e3f2fd;
            color: #1976d2;
            border-bottom-left-radius: 4px;
        }

        .message.user .message-content {
            background: #2c3e50;
            color: white;
            border-bottom-right-radius: 4px;
        }

        .chat-input {
            display: flex;
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
        }

        .input-field {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            outline: none;
            font-size: 16px;
        }

        .input-field:focus {
            border-color: #2c3e50;
        }

        .send-button {
            margin-left: 10px;
            padding: 12px 24px;
            background: #2c3e50;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }

        .send-button:hover {
            background: #34495e;
        }

        .quick-questions {
            padding: 10px 20px;
            background: #f8f9fa;
            border-top: 1px solid #eee;
        }

        .quick-questions h4 {
            margin-bottom: 10px;
            color: #2c3e50;
            font-size: 14px;
        }

        .quick-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .quick-button {
            padding: 6px 12px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 15px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s;
        }

        .quick-button:hover {
            background: #2c3e50;
            color: white;
        }

        .status-indicator {
            padding: 10px 20px;
            background: #f8f9fa;
            border-top: 1px solid #eee;
            text-align: center;
            font-size: 12px;
            color: #666;
        }

        .status-indicator.connected {
            background: #d4edda;
            color: #155724;
        }

        .status-indicator.disconnected {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🤖 Sage Network Connectors FAQ Bot</h1>
            <p>Get instant answers about APIs, authentication, integration, and more!</p>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                <div class="message-content">
                    Hello! Welcome to Sage Network Connectors FAQ Bot. I'm here to help you with questions about our APIs, authentication, integration guides, and troubleshooting. What would you like to know?
                </div>
            </div>
        </div>

        <div class="quick-questions">
            <h4>Quick Questions:</h4>
            <div class="quick-buttons">
                <button class="quick-button" onclick="sendQuickMessage('What is Sage Network Connectors?')">What are Network Connectors?</button>
                <button class="quick-button" onclick="sendQuickMessage('How do I get started?')">Getting Started</button>
                <button class="quick-button" onclick="sendQuickMessage('Where is the API documentation?')">API Documentation</button>
                <button class="quick-button" onclick="sendQuickMessage('How do I authenticate?')">Authentication</button>
                <button class="quick-button" onclick="sendQuickMessage('I am having issues')">Troubleshooting</button>
            </div>
        </div>

        <div class="status-indicator" id="statusIndicator">
            Checking connection to bot...
        </div>
        
        <div class="chat-input">
            <input type="text" class="input-field" id="messageInput" placeholder="Type your question about Sage Network Connectors..." onkeypress="handleKeyPress(event)">
            <button class="send-button" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const statusIndicator = document.getElementById('statusIndicator');

        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            addMessage(message, true);
            messageInput.value = '';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message
                    })
                });

                const data = await response.json();
                
                if (data.responses && data.responses.length > 0) {
                    data.responses.forEach(botResponse => {
                        if (botResponse.text) {
                            addMessage(botResponse.text);
                        }
                    });
                } else {
                    addMessage(data.error || "I'm sorry, I couldn't understand that. Please try asking about Sage Network Connectors topics.");
                }
            } catch (error) {
                addMessage("Sorry, I'm having trouble processing your request. Please try again.");
                console.error('Error:', error);
            }
        }

        function sendQuickMessage(message) {
            messageInput.value = message;
            sendMessage();
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // Check bot status
        async function checkBotStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                if (data.status === 'ready') {
                    statusIndicator.textContent = '🟢 Bot is ready to answer your questions!';
                    statusIndicator.className = 'status-indicator connected';
                } else {
                    statusIndicator.textContent = '🟡 Bot is starting up...';
                    statusIndicator.className = 'status-indicator';
                }
            } catch (error) {
                statusIndicator.textContent = '🔴 Bot is not available';
                statusIndicator.className = 'status-indicator disconnected';
            }
        }

        // Check status on load and periodically
        checkBotStatus();
        setInterval(checkBotStatus, 10000); // Check every 10 seconds

        // Focus on input field
        messageInput.focus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main chatbot interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and forward to Rasa"""
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Try to send message to Rasa
        rasa_url = 'http://localhost:5005/webhooks/rest/webhook'
        rasa_payload = {
            'sender': 'web_user',
            'message': message
        }
        
        response = requests.post(rasa_url, json=rasa_payload, timeout=10)
        
        if response.status_code == 200:
            bot_responses = response.json()
            return jsonify({'responses': bot_responses})
        else:
            return jsonify({'error': 'Bot is not available right now'}), 503
            
    except requests.exceptions.RequestException:
        # If Rasa is not running, provide fallback responses
        fallback_responses = get_fallback_response(message)
        return jsonify({'responses': [{'text': fallback_responses}]})
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/status')
def status():
    """Check if the bot is ready"""
    try:
        # Try to ping Rasa server
        response = requests.get('http://localhost:5005/version', timeout=5)
        if response.status_code == 200:
            return jsonify({'status': 'ready'})
        else:
            return jsonify({'status': 'not_ready'})
    except:
        return jsonify({'status': 'not_ready'})

def get_fallback_response(message):
    """Provide basic fallback responses when Rasa is not available"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greet']):
        return "Hello! Welcome to Sage Network Connectors FAQ Bot. The main bot is starting up, but I can help with basic information."
    
    elif any(word in message_lower for word in ['what', 'sage', 'network', 'connector']):
        return "Sage Network Connectors are APIs and integration tools for connecting with Sage systems. Visit https://internaldeveloper.sage.com/network-connectors for documentation."
    
    elif any(word in message_lower for word in ['start', 'begin', 'getting']):
        return "To get started: 1) Visit the developer portal, 2) Register for API access, 3) Review documentation, 4) Set up authentication. The full bot will provide more detailed guidance once it's ready."
    
    elif any(word in message_lower for word in ['api', 'documentation', 'docs']):
        return "API documentation is available at:\n• Developer Portal: https://internaldeveloper.sage.com/network-connectors\n• Swagger API: https://connector-qa.network-eng.sage.com/swagger/index.html"
    
    elif any(word in message_lower for word in ['auth', 'authentication', 'login']):
        return "Authentication typically uses API keys or OAuth 2.0. Register your application in the developer portal to get credentials."
    
    else:
        return "I'm a basic fallback while the main FAQ bot is starting up. For detailed help, please wait for the full bot to be ready, or visit the developer documentation."

if __name__ == '__main__':
    print("🚀 Starting Sage Network Connectors FAQ Bot Web Server...")
    print("📖 Visit http://localhost:3000 to use the chatbot")
    print("🤖 The bot will connect to Rasa server when it's ready")
    
    app.run(host='0.0.0.0', port=3000, debug=True) 