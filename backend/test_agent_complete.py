"""
Test the mentoring agent with seeded database.

This script:
1. Seeds the database with test data
2. Tests the agent with various queries
3. Verifies tool execution and responses
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("="*70)
print("🧪 MENTORING AGENT TEST SUITE")
print("="*70)

# Step 1: Seed the database
print("\n📊 Step 1: Seeding database...")
print("-"*70)

from app.core.seed_data import seed_test_data

try:
    seed_test_data()
except Exception as e:
    print(f"⚠️  Seed error (might already be seeded): {e}")

# Step 2: Test the agent
print("\n🤖 Step 2: Testing AI Agent...")
print("-"*70)

from app.agent.mentoring_agent.agent import run_agent_query

# Test queries
test_cases = [
    {
        'name': 'Find Python Mentors',
        'query': 'Find me mentors who know Python with rating above 4.5'
    },
    {
        'name': 'Get Recommendations',
        'query': 'Recommend mentors for employee EMP020 who wants to learn system design and AWS'
    },
    {
        'name': 'Program Statistics',
        'query': 'What are the mentorship program statistics?'
    },
    {
        'name': 'Check Mentor Profile',
        'query': 'Tell me about mentor EMP001'
    }
]

print("\nRunning test queries...\n")

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*70}")
    print(f"Test {i}/{len(test_cases)}: {test['name']}")
    print(f"{'='*70}")
    print(f"Query: {test['query']}")
    print(f"{'-'*70}")
    
    try:
        result = run_agent_query(test['query'])
        
        output = result.get('output', '')
        steps = result.get('intermediate_steps', [])
        
        # Check if we got a response
        if output and len(output) > 10:
            print(f"✅ SUCCESS - Got response ({len(output)} chars)")
            print(f"\nResponse Preview:")
            print(f"{output[:300]}{'...' if len(output) > 300 else ''}")
        else:
            print(f"❌ FAILED - Empty or very short response")
            print(f"Response: '{output}'")
        
        # Check tool usage
        if steps:
            print(f"\n🔧 Tools Used: {len(steps)}")
            for step in steps:
                tool_name = step.get('tool', 'unknown')
                result_status = step.get('result', 'unknown')
                print(f"   - {tool_name}: {result_status}")
        else:
            print(f"\n⚠️  No tools were used")
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {str(e)}")

# Summary
print("\n" + "="*70)
print("📋 TEST SUMMARY")
print("="*70)

print("\n✨ If you see responses with tool usage above, the agent is working!")
print("💡 If responses are empty, check:")
print("   1. Environment variables (.env file)")
print("   2. Azure OpenAI endpoint access")
print("   3. Database has data (should be seeded now)")

print("\n" + "="*70)
print("🎉 TEST COMPLETE")
print("="*70 + "\n")
