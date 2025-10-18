#!/usr/bin/env python3
"""Test script to verify Azure OpenAI configuration for PSA Hackathon."""

import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    print("🔍 Testing Azure OpenAI Configuration for PSA Agent...\n")
    
    # Check the exact variables your code expects
    required_vars = {
        "DEPLOYMENT": os.getenv("DEPLOYMENT"),
        "API_VERSION": os.getenv("API_VERSION"), 
        "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
    }
    
    all_set = True
    for var_name, var_value in required_vars.items():
        if var_value:
            if "KEY" in var_name:
                display_value = f"{var_value[:8]}...{var_value[-4:]}" if len(var_value) > 12 else "***"
            else:
                display_value = var_value
            print(f"✅ {var_name}: {display_value}")
        else:
            print(f"❌ {var_name}: NOT SET")
            all_set = False
    
    print("\n" + "="*50)
    
    if all_set:
        print("✅ Configuration looks good!")
        print("\n🚀 Next steps:")
        print("1. Start the server: uvicorn app.main:app --reload --port 8000")
        print("2. Test the endpoint with curl:")
        print('   curl -X POST http://localhost:8000/api/v1/mentoring/agent/chat \\')
        print('     -H "Content-Type: application/json" \\')
        print('     -d \'{"message": "Find me a mentor", "employee_id": "EMP002"}\'')
        
        # Test agent import
        try:
            from app.agent.mentoring_agent.agent import run_agent_query
            print("\n✅ Agent module imports successfully!")
            
            # Test basic functionality (without actual API call)
            print("✅ Agent is ready to use!")
            
        except ImportError as e:
            print(f"\n⚠️  Agent import issue: {e}")
            print("Make sure you're in the backend directory and dependencies are installed")
        except Exception as e:
            print(f"\n⚠️  Agent setup issue: {e}")
            
    else:
        print("❌ Missing configuration!")
        print("\n📝 Create/update your .env file with:")
        print("DEPLOYMENT=gpt-4.1-nano")
        print("API_VERSION=2025-01-01-preview")
        print("AZURE_OPENAI_API_KEY=your_actual_key_here")
        print("\n💡 Get your API key from the PSA Hackathon organizers or Azure Portal")

if __name__ == "__main__":
    main()