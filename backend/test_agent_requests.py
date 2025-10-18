#!/usr/bin/env python3
"""Test the agent chat endpoint with Python requests."""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1/mentoring/agent/chat"

def test_agent_chat(message, employee_id="EMP002", chat_history=None):
    """Test a single agent chat request."""
    payload = {
        "message": message,
        "employee_id": employee_id
    }
    if chat_history:
        payload["chat_history"] = chat_history
    
    print(f"🔄 Sending: {message[:50]}...")
    start_time = time.time()
    
    try:
        response = requests.post(BASE_URL, json=payload, timeout=30)
        elapsed = time.time() - start_time
        
        print(f"⏱️  Response time: {elapsed:.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data.get('success', False)}")
            print(f"🔧 Tools used: {data.get('tools_used', [])}")
            print(f"💬 Response: {data.get('response', 'No response')[:100]}...")
        else:
            print(f"❌ Error: {response.text}")
            
        print("-" * 60)
        return response.json() if response.status_code == 200 else None
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the server running on port 8000?")
        return None
    except requests.exceptions.Timeout:
        print("❌ Request timed out - server may be slow or unresponsive")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def main():
    print("🧪 Testing PSA Agent Chat API\n")
    print("Server should be running at: http://localhost:8000")
    print("="*60 + "\n")
    
    # Test 1: Health check (non-agent endpoint)
    try:
        health = requests.get("http://localhost:8000/health", timeout=5)
        if health.status_code == 200:
            print("✅ Server is running and healthy")
        else:
            print("⚠️  Server responding but health check failed")
    except:
        print("❌ Server not responding - start with: uvicorn app.main:app --reload --port 8000")
        return
    
    print()
    
    # Test 2: Find available mentors
    print("Test 1: Find available mentors")
    test_agent_chat(
        "Show me available mentors who can help with leadership and strategic planning"
    )
    
    # Test 3: Get personalized recommendations  
    print("Test 2: Get personalized recommendations")
    test_agent_chat(
        "I want to develop my leadership skills and learn strategic planning. Who would be the best mentor match for me?"
    )
    
    # Test 4: Program statistics
    print("Test 3: Get program statistics")
    test_agent_chat(
        "What are the current mentorship program statistics? How many mentors are available?"
    )
    
    # Test 5: Multi-turn conversation
    print("Test 4: Multi-turn conversation")
    test_agent_chat(
        "Tell me more about Sarah Chen's background and mentoring style",
        chat_history=[
            {"role": "user", "content": "Who are good mentors for leadership?"},
            {"role": "assistant", "content": "I found several excellent mentors including Sarah Chen and Michael Rodriguez..."}
        ]
    )
    
    # Test 6: Error handling - empty message
    print("Test 5: Error handling (empty message)")
    test_agent_chat("")
    
    print("🎉 Testing complete!")
    print("\n💡 Tips:")
    print("- Successful responses should have 'success': true")
    print("- Check 'tools_used' to see which AI tools were called")
    print("- Response times should be under 10 seconds")
    print("- If you get 503 errors, check your Azure OpenAI configuration")

if __name__ == "__main__":
    main()