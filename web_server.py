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
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
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
    """Provide comprehensive fallback responses when Rasa is not available"""
    message_lower = message.lower()
    
    # Greetings
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greet']):
        return "Hello! Welcome to Sage Network Connectors FAQ Bot. I can help with detailed questions about Sage APIs, invoice models, authentication, and more!"
    
    # Sage Intacct Bills API
    elif any(phrase in message_lower for phrase in ['intacct', 'bill', 'invoice api', 'create bill', 'accounts payable']):
        return """**Sage Intacct Bills API:**

**Key Operations:**
• GET /objects/accounts-payable/bill - List bills
• POST /objects/accounts-payable/bill - Create a bill
• GET /objects/accounts-payable/bill/{key} - Get bill details
• PATCH /objects/accounts-payable/bill/{key} - Update a bill

**Required Fields:**
• vendor (vendor ID)
• dueDate
• createdDate
• lines (bill line items)

Bills move through the AP workflow: creation → approval → payment."""
    
    # Invoice Models
    elif any(phrase in message_lower for phrase in ['invoice model', 'invoice structure', 'invoice schema', 'invoice json']):
        return """**Invoice Model Structure:**

**Core Fields:**
• billNumber - Vendor-assigned identifier
• vendor - {id, key} - Vendor reference
• dueDate - Payment due date
• createdDate - Bill creation date
• totalTxnAmount - Total transaction amount
• currency - {txnCurrency, baseCurrency, exchangeRate}

**Example:**
```json
{
  "billNumber": "INV-001",
  "vendor": {"id": "V001"},
  "dueDate": "2025-01-30",
  "lines": [...]
}
```"""
    
    # Payment Processing
    elif any(phrase in message_lower for phrase in ['payment', 'pay bill', 'payment processing', 'payment workflow']):
        return """**Payment Processing in Sage:**

**Payment Workflow:**
1. Create bills with payment information
2. Set recommendedPaymentDate
3. Use payment priority (urgent/high/normal/low)
4. Process through AP workflow
5. Generate payment requests
6. Execute payments

**Key Fields:**
• paymentInformation.fullyPaidDate
• paymentInformation.totalAmountPaid
• recommendedPaymentDate
• paymentPriority"""
    
    # OAuth Authentication
    elif any(phrase in message_lower for phrase in ['oauth', 'access token', 'refresh token', 'bearer token']):
        return """**OAuth 2.0 Authentication:**

**Setup Process:**
1. Register application in developer portal
2. Obtain client credentials (client_id, client_secret)
3. Implement authorization flow
4. Handle access/refresh tokens

**Authorization Header:**
```
Authorization: Bearer {access_token}
```

**Token expires in 3600 seconds (1 hour)**"""
    
    # API Keys
    elif any(phrase in message_lower for phrase in ['api key', 'api credential', 'developer key']):
        return """**API Key Management:**

**Getting API Keys:**
1. Access Sage Developer Portal
2. Create new application
3. Generate API credentials
4. Configure permissions and scopes
5. Download credentials securely

**Include API key in request headers:**
```
X-API-Key: {your_api_key}
```

**Security: Never expose keys in client-side code!**"""
    
    # Error Codes
    elif any(phrase in message_lower for phrase in ['error', 'error code', 'http error', '400', '401', '403', '404', '500']):
        return """**Common HTTP Error Codes:**

**Client Errors (4xx):**
• 400 Bad Request - Invalid request syntax/parameters
• 401 Unauthorized - Missing or invalid authentication
• 403 Forbidden - Insufficient permissions
• 404 Not Found - Resource doesn't exist
• 429 Too Many Requests - Rate limit exceeded

**Server Errors (5xx):**
• 500 Internal Server Error - Unexpected server error
• 503 Service Unavailable - Service temporarily down"""
    
    # Rate Limits
    elif any(phrase in message_lower for phrase in ['rate limit', 'throttling', 'too many requests', 'quota']):
        return """**Rate Limiting Information:**

**Rate Limits:**
• 1000 requests per hour (standard)
• 10,000 requests per hour (premium)
• Burst allowance for short spikes

**429 Too Many Requests Response:**
```json
{
  "error": "Rate limit exceeded",
  "retry_after": 3600
}
```

**Best Practice: Implement exponential backoff**"""
    
    # REST API Endpoints
    elif any(phrase in message_lower for phrase in ['endpoint', 'rest api', 'api url', 'base url']):
        return """**Main API Endpoints:**

**Bills Management:**
• GET /objects/accounts-payable/bill
• POST /objects/accounts-payable/bill
• GET /objects/accounts-payable/bill/{key}
• PATCH /objects/accounts-payable/bill/{key}

**Vendors:**
• GET /objects/accounts-payable/vendor
• POST /objects/accounts-payable/vendor

**Base URL:** https://api.intacct.com
**All endpoints require authentication**"""
    
    # Currency and Exchange Rates
    elif any(phrase in message_lower for phrase in ['currency', 'exchange rate', 'multi-currency', 'foreign currency']):
        return """**Multi-Currency Support:**

**Currency Structure:**
• txnCurrency - Transaction currency (e.g., USD, EUR)
• baseCurrency - Company base currency
• exchangeRate - Conversion details

**Exchange Rate Object:**
```json
{
  "date": "2025-01-15",
  "rate": 1.0789,
  "typeId": "Daily Rate"
}
```

**Multi-currency bills automatically calculate base amounts using the specified exchange rate.**"""
    
    # Tax Handling
    elif any(phrase in message_lower for phrase in ['tax', 'vat', 'gst', 'tax code', 'tax rate']):
        return """**Tax Management:**

**Tax Configuration:**
• Tax codes (T0-T99)
• Tax rates and calculations
• Tax inclusive vs. exclusive pricing
• VAT/GST processing

**Tax Fields:**
• isTaxInclusive - Boolean flag
• taxCode - Tax code reference
• taxRate - Percentage rate
• taxAmount - Calculated tax

**Tax is calculated automatically based on configured tax codes and rates.**"""
    
    # Webhooks
    elif any(phrase in message_lower for phrase in ['webhook', 'event notification', 'real-time', 'callback']):
        return """**Webhook Configuration:**

**Event Types:**
• Bill created/updated/deleted
• Payment processed
• Vendor changes
• Approval workflow events

**Payload Example:**
```json
{
  "event": "bill.created",
  "data": {
    "key": "123",
    "billNumber": "INV-001"
  },
  "timestamp": "2025-01-15T10:30:00Z"
}
```

**Webhooks enable real-time notifications for system events.**"""
    
    # Batch Processing
    elif any(phrase in message_lower for phrase in ['batch', 'bulk', 'mass', 'multiple']):
        return """**Batch Processing:**

**Bulk Operations:**
• Multiple bill creation
• Batch payments
• Mass data updates
• Bulk imports/exports

**Implementation:**
```json
{
  "requests": [
    {"method": "POST", "url": "/bill", "body": {...}},
    {"method": "POST", "url": "/bill", "body": {...}}
  ]
}
```

**Best Practice: Process in reasonable batch sizes with proper error handling.**"""
    
    # Sage 50 Integration
    elif any(phrase in message_lower for phrase in ['sage 50', 'desktop', 'odbc', 'invoice item']):
        return """**Sage 50 Integration:**

**Desktop Integration:**
• ODBC data access
• SDO (Sage Data Objects)
• File-based import/export

**Invoice Data Structure:**
• INVOICE table - Header information
• INVOICE_ITEM table - Line items
• Fields: STOCK_CODE, QUANTITY, UNIT_PRICE
• Tax codes and calculations

**Key Fields:**
• INVOICE_NUMBER (INTEGER)
• STOCK_CODE (VARCHAR 30)
• NET_AMOUNT, TAX_AMOUNT, GROSS_AMOUNT"""
    
    # General Sage Network Connectors
    elif any(word in message_lower for word in ['what', 'sage', 'network', 'connector']):
        return """**Sage Network Connectors:**

Comprehensive APIs and integration tools for connecting with Sage systems:

• **Data Sync Connectors** - Real-time data synchronization
• **Webhook Connectors** - Event-driven integrations  
• **REST API Connectors** - Standard HTTP-based communication
• **Batch Processing Connectors** - Bulk data operations

**Documentation:** https://internaldeveloper.sage.com/network-connectors"""
    
    # Getting Started
    elif any(word in message_lower for word in ['start', 'begin', 'getting']):
        return """**Getting Started with Sage Network Connectors:**

1. **Visit the developer portal** at https://internaldeveloper.sage.com/network-connectors
2. **Register for API access** and create your application
3. **Review the API documentation** and choose your integration approach
4. **Set up authentication** (API keys or OAuth 2.0)
5. **Start with basic API calls** to test connectivity
6. **Implement error handling** and production-ready code

**Choose from REST APIs, webhooks, or batch processing based on your needs.**"""
    
    # API Documentation
    elif any(word in message_lower for word in ['api', 'documentation', 'docs']):
        return """**API Documentation Resources:**

**Main Documentation:**
• Developer Portal: https://internaldeveloper.sage.com/network-connectors
• Swagger API Reference: https://connector-qa.network-eng.sage.com/swagger/index.html

**What you'll find:**
• Complete endpoint reference
• Request/response examples
• Authentication details
• Error code explanations
• Integration guides
• SDK downloads

**All resources include detailed examples and best practices.**"""
    
    # Authentication
    elif any(word in message_lower for word in ['auth', 'authentication', 'login']):
        return """**Authentication Methods:**

**OAuth 2.0 (Recommended):**
• Access tokens (1-hour expiry)
• Refresh tokens for renewal
• Secure authorization flow

**API Keys:**
• Simple header-based authentication
• Good for server-to-server integration
• Include as: X-API-Key: {your_key}

**Setup:**
1. Register your application in the developer portal
2. Choose authentication method
3. Obtain credentials
4. Implement in your code

**Always store credentials securely!**"""
    
    # Default response
    else:
        return """I'm your enhanced Sage Network Connectors FAQ Bot! I can help with:

**🔧 Technical Topics:**
• Sage Intacct Bills API & Invoice Models
• Payment Processing & Multi-Currency
• OAuth Authentication & API Keys
• Error Handling & Rate Limits

**🚀 Integration Topics:**
• REST API Endpoints & Request Formats
• Webhooks & Batch Processing
• Sage 50/200 Integration
• Data Synchronization

**Ask me anything about Sage APIs, authentication, error codes, or integration!**"""

if __name__ == '__main__':
    print("🚀 Starting Sage Network Connectors FAQ Bot Web Server...")
    print("📖 Visit http://localhost:3000 to use the chatbot")
    print("🤖 The bot will connect to Rasa server when it's ready")
    
    app.run(host='0.0.0.0', port=3000, debug=True) 