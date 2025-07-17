"""
Test script for Developer Onboarding Bot
Tests various FAQ intents and responses
"""

import requests
import json
import time

def test_rasa_bot():
    """Test the Rasa bot with various FAQ questions"""
    
    rasa_url = 'http://localhost:5005/webhooks/rest/webhook'
    
    test_questions = [
        "Hello",
        "What is Sage Network Connectors?",
        "How do I get started?",
        "Where is the API documentation?",
        "How do I authenticate?",
        "What types of connectors are available?",
        "I'm having issues",
        "How to integrate?",
        "What platforms are supported?",
        "What are the rate limits?",
        "What does error code 400 mean?",
        "How do I contact support?",
        "Are you a bot?",
        "Goodbye"
    ]
    
    print("🤖 Testing Developer Onboarding Bot")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Testing: '{question}'")
        print("-" * 30)
        
        try:
            payload = {
                'sender': 'test_user',
                'message': question
            }
            
            response = requests.post(rasa_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                bot_responses = response.json()
                
                if bot_responses:
                    for bot_response in bot_responses:
                        if 'text' in bot_response:
                            print(f"Bot: {bot_response['text']}")
                        if 'image' in bot_response:
                            print(f"Bot: [Image] {bot_response['image']}")
                else:
                    print("Bot: [No response]")
            else:
                print(f"Error: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            print("Make sure Rasa server is running on localhost:5005")
            break
        except Exception as e:
            print(f"Error: {e}")
        
        # Small delay between requests
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")

def check_rasa_server():
    """Check if Rasa server is running"""
    try:
        response = requests.get('http://localhost:5005/version', timeout=5)
        if response.status_code == 200:
            version_info = response.json()
            print(f"✅ Rasa server is running - Version: {version_info.get('version', 'Unknown')}")
            return True
        else:
            print("❌ Rasa server responded with error")
            return False
    except requests.exceptions.RequestException:
        print("❌ Rasa server is not running")
        print("Start it with: rasa run --enable-api --cors \"*\"")
        return False

if __name__ == "__main__":
    print("🔍 Checking Rasa server status...")
    
    if check_rasa_server():
        print("\n🧪 Starting bot tests...")
        test_rasa_bot()
    else:
        print("\n❌ Cannot run tests - Rasa server is not available")
        print("\nTo start the server:")
        print("1. Open a new terminal")
        print("2. Navigate to your project directory")
        print("3. Run: py -3.9 -m rasa run --enable-api --cors \"*\"") 