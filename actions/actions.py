import os
import json
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

try:
    from openai import OpenAI, AzureOpenAI
except ImportError:
    print("OpenAI package not found. Please install with: pip install openai")
    OpenAI = None
    AzureOpenAI = None

class MCPToolsManager:
    """Manager for MCP (Model Context Protocol) tools to assist external developers"""
    
    def __init__(self):
        self.sage_api_base = os.getenv("SAGE_API_BASE_URL", "https://api.sage.com")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.api_key = os.getenv("SAGE_API_KEY")
        self.mcp_enabled = bool(self.api_key)  # Only enable if API key is available
    
    def get_api_schema(self, endpoint: str) -> Dict:
        """Fetch live API schema for a specific endpoint"""
        if not self.mcp_enabled:
            return {"error": "MCP features require SAGE_API_KEY environment variable", "mock_data": True}
        
        try:
            response = requests.get(f"{self.sage_api_base}/v1/schema/{endpoint}", timeout=10)
            return response.json() if response.status_code == 200 else {"error": "Schema not found"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}", "fallback": "Using mock data"}
        except Exception as e:
            return {"error": f"Failed to fetch schema: {str(e)}"}
    
    def test_api_endpoint(self, endpoint: str, method: str, payload: Dict = None) -> Dict:
        """Test an API endpoint with provided parameters"""
        if not self.mcp_enabled:
            return {"error": "API testing requires SAGE_API_KEY environment variable", "mock_data": True}
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            url = f"{self.sage_api_base}/{endpoint}"
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=payload, headers=headers, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, json=payload, headers=headers, timeout=10)
            else:
                return {"error": "Unsupported HTTP method"}
            
            return {
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "headers": dict(response.headers)
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"error": f"API test failed: {str(e)}"}
    
    def get_code_examples(self, api_type: str, language: str = "python") -> str:
        """Generate code examples for specific API integrations"""
        examples = {
            "python": {
                "sage_intacct_bills": '''
import requests

# Create a bill in Sage Intacct
def create_bill(vendor_id, amount, description):
    url = "https://api.sage.com/v1/intacct/bills"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    payload = {
        "vendor_id": vendor_id,
        "amount": amount,
        "description": description,
        "currency": "USD"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
                ''',
                "authentication": '''
import requests

# OAuth2 Authentication Flow
def get_access_token(client_id, client_secret):
    url = "https://api.sage.com/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, data=payload)
    return response.json()["access_token"]
                ''',
                "general": '''
import requests

# Basic API request example
def make_api_request(endpoint, method="GET", data=None):
    url = f"https://api.sage.com/{endpoint}"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=data, headers=headers)
    
    return response.json()
                '''
            },
            "javascript": {
                "authentication": '''
// OAuth2 Authentication in JavaScript
async function getAccessToken(clientId, clientSecret) {
    const response = await fetch('https://api.sage.com/oauth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            grant_type: 'client_credentials',
            client_id: clientId,
            client_secret: clientSecret
        })
    });
    const data = await response.json();
    return data.access_token;
}
                ''',
                "general": '''
// Basic API request in JavaScript
async function makeApiRequest(endpoint, method = 'GET', data = null) {
    const url = `https://api.sage.com/${endpoint}`;
    const options = {
        method: method,
        headers: {
            'Authorization': 'Bearer YOUR_API_KEY',
            'Content-Type': 'application/json'
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    const response = await fetch(url, options);
    return await response.json();
}
                '''
            }
        }
        return examples.get(language, {}).get(api_type, examples.get(language, {}).get("general", "No example available for this combination"))
    
    def check_system_status(self) -> Dict:
        """Check Sage API system status and health"""
        if not self.mcp_enabled:
            return {"status": "unknown", "message": "Status check requires SAGE_API_KEY"}
        
        try:
            response = requests.get(f"{self.sage_api_base}/health", timeout=5)
            return response.json() if response.status_code == 200 else {"status": "unknown"}
        except requests.exceptions.RequestException:
            return {"status": "unreachable", "message": "Could not connect to API"}
        except Exception as e:
            return {"status": "error", "message": f"Status check failed: {str(e)}"}

class ActionMCPDeveloperAssist(Action):
    """MCP-enabled action to assist external developers with Sage connector development"""

    def name(self) -> Text:
        return "action_mcp_developer_assist"

    def __init__(self):
        self.mcp_tools = MCPToolsManager()
        # Initialize OpenAI client for enhanced responses
        self.client = None
        self.model_name = "gpt-3.5-turbo"
        
        if OpenAI is None:
            print("Warning: OpenAI package not available")
            return
            
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if azure_api_key and azure_endpoint:
            self.client = AzureOpenAI(
                api_key=azure_api_key,
                api_version="2024-02-15-preview",
                azure_endpoint=azure_endpoint
            )
            self.model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")
        else:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if openai_api_key:
                self.client = OpenAI(api_key=openai_api_key)
                self.model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '')
        intent = tracker.latest_message.get('intent', {}).get('name', '')
        
        # Determine what MCP tools to use based on intent and message content
        response_data = {}
        
        if any(keyword in user_message.lower() for keyword in ['api schema', 'endpoint documentation', 'api structure']):
            # Extract endpoint from message or use default
            endpoint = self._extract_endpoint_from_message(user_message)
            schema_data = self.mcp_tools.get_api_schema(endpoint)
            response_data['schema'] = schema_data
            
        elif any(keyword in user_message.lower() for keyword in ['test api', 'try endpoint', 'api test']):
            # For API testing requests
            endpoint, method, payload = self._extract_test_params_from_message(user_message)
            test_result = self.mcp_tools.test_api_endpoint(endpoint, method, payload)
            response_data['test_result'] = test_result
            
        elif any(keyword in user_message.lower() for keyword in ['code example', 'sample code', 'how to implement']):
            # Generate code examples
            api_type = self._determine_api_type_from_intent(intent)
            language = self._extract_language_from_message(user_message)
            code_example = self.mcp_tools.get_code_examples(api_type, language)
            response_data['code_example'] = code_example
            
        elif any(keyword in user_message.lower() for keyword in ['status', 'health', 'api down']):
            # Check system status
            status = self.mcp_tools.check_system_status()
            response_data['system_status'] = status

        # Generate enhanced response using OpenAI with MCP data
        enhanced_response = self._generate_enhanced_response(user_message, intent, response_data)
        
        dispatcher.utter_message(text=enhanced_response)
        
        return []

    def _extract_endpoint_from_message(self, message: str) -> str:
        """Extract API endpoint from user message"""
        # Simple extraction logic - can be enhanced with NLP
        if 'bills' in message.lower():
            return 'bills'
        elif 'invoices' in message.lower():
            return 'invoices'
        elif 'vendors' in message.lower():
            return 'vendors'
        return 'general'
    
    def _extract_test_params_from_message(self, message: str) -> tuple:
        """Extract API test parameters from message"""
        # Default values - in production, use more sophisticated NLP
        endpoint = "bills"
        method = "GET"
        payload = {}
        return endpoint, method, payload
    
    def _determine_api_type_from_intent(self, intent: str) -> str:
        """Map intent to API type for code examples"""
        mapping = {
            'sage_intacct_bills': 'sage_intacct_bills',
            'oauth_authentication': 'authentication',
            'api_keys': 'authentication',
            'payment_processing': 'payments',
            'vendor_management': 'vendors'
        }
        return mapping.get(intent, 'general')
    
    def _extract_language_from_message(self, message: str) -> str:
        """Extract programming language preference from message"""
        if 'javascript' in message.lower() or 'js' in message.lower():
            return 'javascript'
        elif 'c#' in message.lower() or 'csharp' in message.lower():
            return 'csharp'
        elif 'java' in message.lower():
            return 'java'
        return 'python'  # default
    
    def _generate_enhanced_response(self, user_message: str, intent: str, mcp_data: Dict) -> str:
        """Generate enhanced response using OpenAI with MCP data context"""
        if not self.client:
            return self._fallback_response(intent, mcp_data)
        
        # Create context for OpenAI including MCP data
        context = f"""
        User is a developer building Sage Network Connectors. 
        User message: {user_message}
        Intent: {intent}
        Live API data: {json.dumps(mcp_data, indent=2)}
        
        Provide a helpful, technical response that assists with connector development.
        Include specific API details, code examples, and actionable guidance.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a Sage Network Connectors expert assistant helping external developers build integrations. Use the provided live API data to give accurate, current information."},
                    {"role": "user", "content": context}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_response(intent, mcp_data)
    
    def _fallback_response(self, intent: str, mcp_data: Dict) -> str:
        """Fallback response when OpenAI is not available"""
        if mcp_data.get('schema'):
            return f"Here's the current API schema information: {json.dumps(mcp_data['schema'], indent=2)}"
        elif mcp_data.get('test_result'):
            return f"API test result: {json.dumps(mcp_data['test_result'], indent=2)}"
        elif mcp_data.get('code_example'):
            return f"Here's a code example:\n\n```\n{mcp_data['code_example']}\n```"
        elif mcp_data.get('system_status'):
            return f"System status: {json.dumps(mcp_data['system_status'], indent=2)}"
        
        return "I'm here to help with Sage Network Connectors development. What would you like to know?"

class ActionOpenAIResponse(Action):
    """Custom action that uses OpenAI (regular or Azure) for enhanced responses"""

    def name(self) -> Text:
        return "action_openai_response"

    def __init__(self):
        # Initialize OpenAI client - supports both regular OpenAI and Azure OpenAI
        self.client = None
        self.model_name = "gpt-3.5-turbo"
        
        if OpenAI is None:
            print("Warning: OpenAI package not available")
            return
            
        # Check if Azure OpenAI is configured
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if azure_api_key and azure_endpoint:
            # Use Azure OpenAI
            self.client = AzureOpenAI(
                api_key=azure_api_key,
                api_version="2024-02-15-preview",
                azure_endpoint=azure_endpoint
            )
            self.model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")
            print("Using Azure OpenAI")
        else:
            # Use regular OpenAI
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if openai_api_key:
                self.client = OpenAI(api_key=openai_api_key)
                self.model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
                print("Using regular OpenAI")
            else:
                print("Warning: No OpenAI API key found. Set OPENAI_API_KEY or AZURE_OPENAI_API_KEY environment variable.")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the user's message
        user_message = tracker.latest_message.get("text", "")
        intent = tracker.latest_message.get("intent", {}).get("name", "")
        
        # Create context for Azure OpenAI
        context = f"""
                    You are a helpful assistant for Developer Onboarding Bot.
        The user asked: "{user_message}"
        The detected intent is: "{intent}"
        
        Please provide a helpful, accurate response about Sage Network Connectors, APIs, or related topics.
        Keep your response concise and helpful for developers.
        Focus on practical solutions and code examples when relevant.
        """

        # Check if OpenAI client is available
        if self.client is None:
            fallback_message = "I'm sorry, the enhanced AI features are not configured. Please check our documentation or contact support for help."
            dispatcher.utter_message(text=fallback_message)
            return []

        try:
            # Call OpenAI API (works for both regular and Azure OpenAI)
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            dispatcher.utter_message(text=ai_response)
            
        except Exception as e:
            # Fallback to default response if OpenAI fails
            fallback_message = "I'm sorry, I'm having trouble accessing enhanced responses right now. Please check our documentation or contact support for help."
            dispatcher.utter_message(text=fallback_message)
            print(f"OpenAI API error: {e}")

        return []

class ActionOpenAIFallback(Action):
    """Fallback action using OpenAI (regular or Azure) for unknown queries"""

    def name(self) -> Text:
        return "action_openai_fallback"

    def __init__(self):
        # Initialize OpenAI client - supports both regular OpenAI and Azure OpenAI
        self.client = None
        self.model_name = "gpt-3.5-turbo"
        
        if OpenAI is None:
            print("Warning: OpenAI package not available")
            return
            
        # Check if Azure OpenAI is configured
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if azure_api_key and azure_endpoint:
            # Use Azure OpenAI
            self.client = AzureOpenAI(
                api_key=azure_api_key,
                api_version="2024-02-15-preview",
                azure_endpoint=azure_endpoint
            )
            self.model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")
        else:
            # Use regular OpenAI
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if openai_api_key:
                self.client = OpenAI(api_key=openai_api_key)
                self.model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text", "")
        
        context = f"""
                    You are a Developer Onboarding Bot assistant. The user asked something that our trained model couldn't understand.
        User message: "{user_message}"
        
        Try to help with:
        - Sage Network Connectors
        - API integration
        - Authentication
        - Troubleshooting
        - Development guidance
        
        If the question is not related to these topics, politely redirect them to contact support.
        Provide practical, actionable advice.
        """

        # Check if OpenAI client is available
        if self.client is None:
            dispatcher.utter_message(
                text="I'm sorry, I didn't understand that. Please contact our support team for assistance."
            )
            return []

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content
            dispatcher.utter_message(text=ai_response)
            
        except Exception as e:
            dispatcher.utter_message(
                text="I'm sorry, I didn't understand that. Please contact our support team for assistance."
            )
            print(f"OpenAI API error: {e}")

        return []
