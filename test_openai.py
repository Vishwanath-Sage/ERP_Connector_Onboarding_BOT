"""
Test script to verify Azure OpenAI integration with Rasa bot
Run this to check if your Azure OpenAI configuration is working correctly
"""

import os
from openai import AzureOpenAI

def test_azure_openai_connection():
    """Test basic Azure OpenAI API connection"""
    print("🧪 Testing Azure OpenAI Integration...")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if not api_key:
        print("❌ FAILED: AZURE_OPENAI_API_KEY environment variable not set")
        print("   Run setup_openai.ps1 to configure your Azure OpenAI credentials")
        return False
    
    # Check if endpoint is set
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not endpoint:
        print("❌ FAILED: AZURE_OPENAI_ENDPOINT environment variable not set")
        print("   Run setup_openai.ps1 to configure your Azure OpenAI endpoint")
        return False
    
    # Check if deployment is set
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")
    
    print(f"✅ API key found: {api_key[:8]}...{api_key[-8:]}")
    print(f"✅ Endpoint: {endpoint}")
    print(f"✅ Deployment: {deployment}")
    
    # Initialize Azure OpenAI client
    try:
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-02-15-preview",
            azure_endpoint=endpoint
        )
        print("✅ Azure OpenAI client initialized successfully")
    except Exception as e:
        print(f"❌ FAILED to initialize Azure OpenAI client: {e}")
        return False
    
    # Test API call
    print("\n🔍 Testing API call...")
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for Sage Network Connectors."},
                {"role": "user", "content": "What is Sage Network Connectors?"}
            ],
            max_tokens=100
        )
        
        ai_response = response.choices[0].message.content
        print("✅ API call successful!")
        print(f"📝 Sample response: {ai_response[:100]}...")
        
        # Check token usage
        if hasattr(response, 'usage'):
            print(f"🔢 Tokens used: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED API call: {e}")
        if "invalid_api_key" in str(e).lower():
            print("💡 This usually means your API key is incorrect")
            print("   Please verify your key in Azure Portal > Your OpenAI Resource > Keys and Endpoint")
        elif "rate_limit" in str(e).lower():
            print("💡 Rate limit exceeded - please wait a moment and try again")
        elif "insufficient_quota" in str(e).lower():
            print("💡 Insufficient quota - please check your Azure OpenAI quota")
        elif "deployment" in str(e).lower():
            print("💡 Deployment not found - check your deployment name in Azure Portal")
        elif "endpoint" in str(e).lower():
            print("💡 Endpoint issue - verify your endpoint URL format")
        return False

def test_rasa_integration():
    """Test if Rasa dependencies are available"""
    print("\n🔧 Testing Rasa Integration...")
    print("=" * 50)
    
    try:
        import rasa_sdk
        print("✅ rasa-sdk is installed")
    except ImportError:
        print("❌ rasa-sdk not found - run: pip install rasa-sdk")
        return False
    
    try:
        import rasa
        print("✅ rasa is installed")
    except ImportError:
        print("❌ rasa not found - run: pip install rasa")
        return False
    
    # Check if actions file is valid
    try:
        from actions.actions import ActionOpenAIResponse, ActionOpenAIFallback
        print("✅ Custom Azure OpenAI actions found")
        return True
    except Exception as e:
        print(f"❌ Error importing custom actions: {e}")
        return False

def main():
    print("🤖 Sage Network Connectors - Azure OpenAI Integration Test")
    print("=" * 70)
    print()
    
    azure_openai_ok = test_azure_openai_connection()
    rasa_ok = test_rasa_integration()
    
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    if azure_openai_ok and rasa_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Azure OpenAI integration is ready")
        print("✅ Rasa integration is ready") 
        print("\n🚀 You can now run: .\\start_bot.ps1")
        print("\n💡 Sample queries to try:")
        print("   • 'What is Sage Network Connectors?'")
        print("   • 'How do I authenticate with OAuth 2.0?'")
        print("   • 'Explain API rate limiting best practices'")
        print("   • 'Show me error handling patterns'")
    else:
        print("⚠️  SOME TESTS FAILED")
        if not azure_openai_ok:
            print("❌ Azure OpenAI integration needs attention")
            print("   Make sure you have:")
            print("   1. Valid Azure OpenAI API key")
            print("   2. Correct endpoint URL")
            print("   3. Valid deployment name")
        if not rasa_ok:
            print("❌ Rasa integration needs attention")
        print("\n🔧 Please fix the issues above before running the bot")
    
    print("\n📖 For help, check: OPENAI_INTEGRATION.md")
    print("🌐 Azure Portal: https://portal.azure.com")

if __name__ == "__main__":
    main() 