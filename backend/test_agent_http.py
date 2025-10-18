"""
Test Agent via HTTP API (against running server)

This tests the agent through the actual API endpoint,
which is how the frontend will use it.
"""
import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000"
AGENT_ENDPOINT = f"{API_BASE}/api/v1/mentoring/agent/chat"

print("="*80)
print("🌐 AI MENTORING AGENT - HTTP API OUTPUT TESTER")
print("="*80)
print(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Endpoint: {AGENT_ENDPOINT}\n")

# Check if server is running
try:
    health = requests.get(f"{API_BASE}/health", timeout=2)
    if health.status_code == 200:
        print("✅ Server is running")
        print(f"   Status: {health.json()}\n")
    else:
        print(f"⚠️  Server returned status {health.status_code}\n")
except requests.exceptions.RequestException as e:
    print(f"❌ ERROR: Cannot connect to server!")
    print(f"   {str(e)}")
    print(f"\n💡 Please start the server first:")
    print(f"   cd backend")
    print(f"   uvicorn src.app.main:app --reload --app-dir src\n")
    exit(1)

# Test queries
test_queries = [
    {
        'name': '🔍 Find Python Mentors',
        'message': 'Find me mentors who know Python with rating above 4.5',
        'employee_id': 'EMP020'
    },
    {
        'name': '💡 Get Recommendations',
        'message': 'Recommend mentors for me. I want to learn system design and AWS.',
        'employee_id': 'EMP020'
    },
    {
        'name': '👤 Check Mentor Profile',
        'message': 'Tell me about Dr. Sarah Chen - is she available?',
        'employee_id': 'EMP020'
    },
    {
        'name': '📊 Program Stats',
        'message': 'What are the current mentorship program statistics?',
        'employee_id': 'EMP020'
    },
]

print("="*80)
print("RUNNING AGENT TESTS")
print("="*80 + "\n")

results = []

for i, test in enumerate(test_queries, 1):
    print(f"\n{'─'*80}")
    print(f"TEST {i}/{len(test_queries)}: {test['name']}")
    print(f"{'─'*80}")
    
    print(f"\n📤 REQUEST:")
    print(f"   Message: {test['message']}")
    print(f"   Employee: {test['employee_id']}")
    
    try:
        # Make API request
        response = requests.post(
            AGENT_ENDPOINT,
            json={
                'message': test['message'],
                'employee_id': test['employee_id']
            },
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"\n📥 HTTP RESPONSE:")
        print(f"   Status: {response.status_code} {response.reason}")
        
        if response.status_code == 200:
            data = response.json()
            
            agent_response = data.get('response', '')
            tools_used = data.get('tools_used', [])
            success = data.get('success', False)
            
            print(f"\n✅ AGENT OUTPUT:")
            print(f"{'─'*80}")
            print(agent_response)
            print(f"{'─'*80}")
            
            print(f"\n📊 METRICS:")
            print(f"   • Success: {success}")
            print(f"   • Response length: {len(agent_response)} characters")
            print(f"   • Word count: {len(agent_response.split())} words")
            print(f"   • Tools used: {len(tools_used) if tools_used else 0}")
            
            if tools_used:
                print(f"\n🔧 TOOLS EXECUTED:")
                for tool in tools_used:
                    print(f"   • {tool}")
            
            results.append({
                'test': test['name'],
                'success': success and len(agent_response) > 50,
                'response_length': len(agent_response),
                'tools_count': len(tools_used) if tools_used else 0
            })
            
        else:
            # Error response
            print(f"\n❌ ERROR RESPONSE:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(response.text)
            
            results.append({
                'test': test['name'],
                'success': False,
                'error': f"HTTP {response.status_code}"
            })
    
    except requests.exceptions.Timeout:
        print(f"\n⏱️  TIMEOUT: Request took longer than 30 seconds")
        results.append({
            'test': test['name'],
            'success': False,
            'error': 'Timeout'
        })
    
    except Exception as e:
        print(f"\n❌ EXCEPTION: {type(e).__name__}: {str(e)}")
        results.append({
            'test': test['name'],
            'success': False,
            'error': str(e)
        })

# Summary
print(f"\n\n{'='*80}")
print("📋 TEST SUMMARY")
print(f"{'='*80}\n")

successful = sum(1 for r in results if r.get('success', False))
total = len(results)

print(f"✅ Success Rate: {successful}/{total} ({(successful/total*100):.0f}%)\n")

for result in results:
    status = "✅" if result.get('success') else "❌"
    name = result['test']
    
    if result.get('success'):
        length = result.get('response_length', 0)
        tools = result.get('tools_count', 0)
        print(f"{status} {name}")
        print(f"   {length} chars | {tools} tools")
    else:
        error = result.get('error', 'Unknown')
        print(f"{status} {name} - {error}")

if successful == total:
    print(f"\n🎉 ALL TESTS PASSED! Agent is working perfectly via API!")
elif successful > 0:
    print(f"\n👍 PARTIAL SUCCESS. Some tests passed.")
else:
    print(f"\n⚠️  ALL TESTS FAILED. Check server and configuration.")

print(f"\n{'='*80}\n")
