"""
Interactive Agent Output Tester

Run various queries and see detailed agent outputs including:
- Full response text
- Tools called
- Tool results
- Response quality metrics
"""
import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("="*80)
print("🤖 AI MENTORING AGENT - OUTPUT TESTER")
print("="*80)
print(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

from app.agent.mentoring_agent.agent import run_agent_query

# Test queries with expected behaviors
test_cases = [
    {
        'name': '🔍 Search: Python Mentors',
        'query': 'Find me mentors who know Python with rating above 4.5',
        'expected_tools': ['find_available_mentors'],
        'expected_content': ['mentor', 'Python', 'rating']
    },
    {
        'name': '💡 Recommendation: Specific Employee',
        'query': 'Recommend mentors for employee EMP020 who wants to learn system design and cloud architecture',
        'expected_tools': ['recommend_mentors', 'get_mentee_profile'],
        'expected_content': ['recommend', 'system design', 'match']
    },
    {
        'name': '👤 Profile: Get Mentor Details',
        'query': 'Tell me about mentor EMP001 - what are their skills and availability?',
        'expected_tools': ['get_mentor_profile'],
        'expected_content': ['mentor', 'skill', 'available']
    },
    {
        'name': '📊 Analytics: Program Statistics',
        'query': 'What are the current mentorship program statistics?',
        'expected_tools': ['get_mentorship_statistics'],
        'expected_content': ['mentor', 'pair', 'statistic']
    },
    {
        'name': '✅ Validation: Goal Quality',
        'query': 'I want to set mentorship goals: "Learn Python", "Get better at coding", "Become a senior engineer". Are these good goals?',
        'expected_tools': ['validate_mentorship_goals'],
        'expected_content': ['goal', 'specific', 'measurable']
    },
    {
        'name': '🎯 Analysis: Skill Gaps',
        'query': 'What skills are we lacking mentors for in our organization?',
        'expected_tools': ['identify_mentor_gaps'],
        'expected_content': ['skill', 'gap', 'demand']
    },
]

def analyze_response(response_text, expected_content):
    """Analyze response quality"""
    metrics = {
        'length': len(response_text),
        'word_count': len(response_text.split()),
        'has_data': len(response_text) > 50,
        'content_match': sum(1 for term in expected_content if term.lower() in response_text.lower()),
        'is_helpful': len(response_text) > 100 and any(term.lower() in response_text.lower() for term in expected_content)
    }
    return metrics

def print_separator(char='─', length=80):
    print(char * length)

# Run tests
results = []

for i, test in enumerate(test_cases, 1):
    print(f"\n{'═'*80}")
    print(f"TEST {i}/{len(test_cases)}: {test['name']}")
    print(f"{'═'*80}")
    
    print(f"\n📝 Query:")
    print(f"   {test['query']}")
    print_separator()
    
    try:
        # Run the agent
        print("\n⚙️  Running agent...")
        result = run_agent_query(test['query'])
        
        output = result.get('output', '')
        steps = result.get('intermediate_steps', [])
        error = result.get('error')
        
        # Extract tool information
        tools_used = [step.get('tool') for step in steps if 'tool' in step]
        
        # Analyze response
        metrics = analyze_response(output, test['expected_content'])
        
        # Display results
        print(f"\n✅ AGENT RESPONSE:")
        print_separator('─')
        print(output)
        print_separator('─')
        
        print(f"\n📊 RESPONSE METRICS:")
        print(f"   • Length: {metrics['length']} characters")
        print(f"   • Words: {metrics['word_count']} words")
        print(f"   • Has meaningful data: {'✓' if metrics['has_data'] else '✗'}")
        print(f"   • Content relevance: {metrics['content_match']}/{len(test['expected_content'])} expected terms found")
        print(f"   • Overall quality: {'🟢 GOOD' if metrics['is_helpful'] else '🟡 NEEDS IMPROVEMENT'}")
        
        if tools_used:
            print(f"\n🔧 TOOLS EXECUTED ({len(tools_used)}):")
            for j, tool in enumerate(tools_used, 1):
                step = steps[j-1]
                status = step.get('result', 'unknown')
                status_icon = '✓' if status == 'success' else '✗' if status == 'error' else '?'
                print(f"   {j}. {status_icon} {tool} ({status})")
                
                # Show tool result preview if available
                if 'result_preview' in step:
                    preview = step['result_preview']
                    print(f"      Preview: {preview}...")
                elif 'error' in step:
                    print(f"      Error: {step['error']}")
        else:
            print(f"\n⚠️  NO TOOLS EXECUTED")
        
        # Check against expectations
        print(f"\n🎯 EXPECTATION CHECK:")
        expected_tool_set = set(test['expected_tools'])
        actual_tool_set = set(tools_used)
        
        if expected_tool_set.issubset(actual_tool_set):
            print(f"   ✓ Tools: Expected tools called")
        else:
            missing = expected_tool_set - actual_tool_set
            print(f"   ✗ Tools: Missing {missing}")
        
        # Record result
        results.append({
            'test': test['name'],
            'success': metrics['is_helpful'] and len(tools_used) > 0,
            'metrics': metrics,
            'tools_used': len(tools_used),
            'output_length': metrics['length']
        })
        
        if error:
            print(f"\n⚠️  ERROR DETAILS:")
            print(f"   {error}")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED:")
        print(f"   Error: {type(e).__name__}: {str(e)}")
        
        results.append({
            'test': test['name'],
            'success': False,
            'error': str(e)
        })
    
    print()  # Extra spacing

# Summary Report
print("\n" + "="*80)
print("📋 TEST SUMMARY REPORT")
print("="*80)

successful = sum(1 for r in results if r.get('success', False))
total = len(results)

print(f"\n✅ Success Rate: {successful}/{total} ({(successful/total*100):.0f}%)")

print(f"\n📊 Detailed Results:")
for i, result in enumerate(results, 1):
    status = "✓" if result.get('success') else "✗"
    test_name = result['test']
    
    if result.get('success'):
        metrics = result['metrics']
        tools = result['tools_used']
        length = result['output_length']
        print(f"   {status} {test_name}")
        print(f"      {length} chars | {tools} tools | Quality: {'🟢' if metrics['is_helpful'] else '🟡'}")
    else:
        error = result.get('error', 'Unknown error')
        print(f"   {status} {test_name}")
        print(f"      Error: {error[:60]}...")

# Quality Assessment
print(f"\n🎯 QUALITY ASSESSMENT:")
avg_length = sum(r.get('output_length', 0) for r in results if r.get('success')) / max(successful, 1)
total_tools = sum(r.get('tools_used', 0) for r in results if r.get('success'))

print(f"   • Average response length: {avg_length:.0f} characters")
print(f"   • Total tools executed: {total_tools}")
print(f"   • Agent is generating responses: {'✓ YES' if avg_length > 100 else '✗ NO'}")
print(f"   • Agent is using tools: {'✓ YES' if total_tools > 0 else '✗ NO'}")

if successful == total and avg_length > 150:
    print(f"\n🎉 EXCELLENT! Agent is working perfectly!")
elif successful > total / 2:
    print(f"\n👍 GOOD! Agent is mostly working. Some improvements possible.")
else:
    print(f"\n⚠️  NEEDS ATTENTION! Agent may have issues.")

print("\n" + "="*80)
print("🏁 Testing Complete")
print("="*80 + "\n")

# Save detailed results to file
output_file = 'agent_test_results.json'
with open(output_file, 'w') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_tests': total,
            'successful': successful,
            'success_rate': successful/total*100,
            'avg_response_length': avg_length,
            'total_tools_used': total_tools
        },
        'results': results
    }, f, indent=2)

print(f"💾 Detailed results saved to: {output_file}\n")
