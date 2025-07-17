# Developer Onboarding Bot

A comprehensive onboarding chatbot built with Rasa and Flask for helping developers get started with Sage Network Connectors.

## 🚀 Features

- **Interactive Web Interface**: Modern, responsive chat interface accessible via web browser
- **Comprehensive FAQ Coverage**: Handles questions about:
  - Getting started with Sage Network Connectors
  - API documentation and authentication
  - Connector types and supported platforms
  - Troubleshooting and integration help
  - Rate limits and error codes
  - Contact support information

## 📋 Prerequisites

- Python 3.8+
- Git

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Vishwanath-Sage/ERP_Connector_Onboarding_BOT.git
   cd ERP_Connector_Onboarding_BOT
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```powershell
     .\venv\Scripts\activate.bat
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Bot

### Method 1: Web Interface Only (Recommended for quick start)

1. **Start the web server**:
   ```bash
   python web_server.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:3000
   ```

The bot includes a fallback system that provides helpful responses even without the full Rasa backend.

### Method 2: Full Rasa Integration

1. **Train the Rasa model** (if needed):
   ```bash
   rasa train
   ```

2. **Start the Rasa server** (in one terminal):
   ```bash
   rasa run --enable-api --cors "*"
   ```

3. **Start the web server** (in another terminal):
   ```bash
   python web_server.py
   ```

4. **Access the bot** at:
   ```
   http://localhost:3000
   ```

## 📁 Project Structure

```
ERP_Connector_Onboarding_BOT/
├── actions/                 # Custom Rasa actions
├── data/                   # Training data
│   ├── nlu.yml            # Natural language understanding data
│   ├── rules.yml          # Conversation rules
│   └── stories.yml        # Conversation stories
├── models/                # Trained Rasa models
├── tests/                 # Test files
├── config.yml             # Rasa configuration
├── domain.yml             # Rasa domain file
├── endpoints.yml          # Rasa endpoints configuration
├── credentials.yml        # Channel credentials
├── web_server.py          # Flask web server
├── web_chat.html          # Chat interface (embedded in web_server.py)
└── requirements.txt       # Python dependencies
```

## 🎯 Supported FAQ Topics

- **What is Sage Network Connectors**
- **Getting Started Guide**
- **API Documentation**
- **Authentication Help**
- **Connector Types**
- **Troubleshooting**
- **Integration Assistance**
- **Supported Platforms**
- **Rate Limits**
- **Error Codes**
- **Contact Support**

## 🔧 Customization

### Adding New FAQ Topics

1. **Update NLU data** in `data/nlu.yml`:
   ```yaml
   - intent: new_topic
     examples: |
       - How do I do X?
       - Tell me about X
   ```

2. **Add responses** in `domain.yml`:
   ```yaml
   responses:
     utter_new_topic:
       - text: "Here's information about X..."
   ```

3. **Create rules** in `data/rules.yml`:
   ```yaml
   - rule: Answer FAQ about new topic
     steps:
     - intent: new_topic
     - action: utter_new_topic
   ```

4. **Retrain the model**:
   ```bash
   rasa train
   ```

### Customizing the Web Interface

Modify the HTML template in `web_server.py` to change the appearance, colors, or layout of the chat interface.

## 🧪 Testing

Run the test stories:
```bash
rasa test
```

## 📱 Accessing the Bot

- **Local Development**: http://localhost:3000
- **Network Access**: http://[your-ip]:3000 (accessible to other devices on your network)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For technical support or questions about the bot, please contact the development team or create an issue in this repository.

## 📄 License

This project is proprietary to Sage and intended for internal use.

---

**Built with ❤️ by the Sage Development Team** 