#!/usr/bin/env python3
"""
Test script to verify bot responses
"""
import requests
import json
import time

def test_bot_response():
    """Test if the bot responds correctly to 'How do I get started?' question"""
    
    print("🤖 Testing Sage FAQ Bot Response...")
    print("=" * 50)
    
    # Test message
    test_message = "How do I get started?"
    
    # Bot endpoint (assuming web server is running on localhost:3000)
    bot_url = "http://localhost:3000/webhooks/rest/webhook"
    
    try:
        # Send test message
        payload = {
            "sender": "test_user",
            "message": test_message
        }
        
        print(f"📤 Sending: '{test_message}'")
        print("⏳ Waiting for response...")
        
        response = requests.post(bot_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            bot_response = response.json()
            
            if bot_response and len(bot_response) > 0:
                print("✅ Bot Response Received!")
                print("-" * 30)
                for message in bot_response:
                    if 'text' in message:
                        print(f"🤖 Bot: {message['text']}")
                print("-" * 30)
                
                # Check if response contains expected content
                response_text = " ".join([msg.get('text', '') for msg in bot_response])
                if "developer portal" in response_text.lower() or "get started" in response_text.lower():
                    print("✅ SUCCESS: Bot gave expected response!")
                    return True
                else:
                    print("⚠️ WARNING: Response doesn't match expected content")
                    return False
            else:
                print("❌ ERROR: Empty response from bot")
                return False
        else:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to bot")
        print("💡 Make sure web server is running on http://localhost:3000")
        return False
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timeout")
        print("💡 Bot may be processing slowly")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_actions_server():
    """Test if actions server is running"""
    print("\n🔧 Testing Actions Server...")
    try:
        # Try to connect to actions server port
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('localhost', 5055))
        sock.close()
        
        if result == 0:
            print("✅ Actions Server is running on port 5055")
            return True
        else:
            print("❌ Actions Server is not responding on port 5055")
            return False
    except Exception as e:
        print(f"❌ Error checking Actions Server: {e}")
        return False

def test_web_server():
    """Test if web server is running"""
    print("\n🌐 Testing Web Server...")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Web Server is running on port 3000")
            return True
        else:
            print(f"⚠️ Web Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Web Server is not running on port 3000")
        return False
    except Exception as e:
        print(f"❌ Error checking Web Server: {e}")
        return False

if __name__ == "__main__":
    print("🧪 SAGE FAQ BOT DIAGNOSTIC TEST")
    print("=" * 40)
    
    # Test components
    actions_ok = test_actions_server()
    web_ok = test_web_server()
    
    if actions_ok and web_ok:
        # Test bot response
        bot_ok = test_bot_response()
        
        print("\n📊 TEST SUMMARY")
        print("=" * 20)
        print(f"Actions Server: {'✅ OK' if actions_ok else '❌ FAIL'}")
        print(f"Web Server: {'✅ OK' if web_ok else '❌ FAIL'}")
        print(f"Bot Response: {'✅ OK' if bot_ok else '❌ FAIL'}")
        
        if actions_ok and web_ok and bot_ok:
            print("\n🎉 ALL TESTS PASSED! Bot is working correctly!")
        else:
            print("\n⚠️ Some tests failed. Check the issues above.")
    else:
        print("\n❌ Cannot test bot - servers not running")
        print("\n💡 SOLUTION:")
        print("1. Run: .\\start_complete_bot.ps1")
        print("2. Wait for both servers to start")
        print("3. Run this test again") 