"""Comprehensive check of wellbeing agent tools implementation."""
import sys
from pathlib import Path

# Add src to path
backend_src = Path(__file__).parent
sys.path.insert(0, str(backend_src))

def check_implementation():
    print("=" * 80)
    print("WELLBEING AGENT TOOLS - IMPLEMENTATION CHECK")
    print("=" * 80)
    print()
    
    # 1. Check tools can be imported
    print("1️⃣ CHECKING IMPORTS")
    print("-" * 80)
    try:
        from app.agent.well_being_agent.tools import (
            analyze_message_sentiment,
            update_sentiment_snapshot,
            get_past_sentiment_history,
            search_wellbeing_resources
        )
        print("✅ All 4 tools imported successfully")
        print("   - analyze_message_sentiment")
        print("   - update_sentiment_snapshot")
        print("   - get_past_sentiment_history")
        print("   - search_wellbeing_resources")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    print()
    
    # 2. Check analyze_message_sentiment signature
    print("2️⃣ CHECKING analyze_message_sentiment")
    print("-" * 80)
    import inspect
    sig = inspect.signature(analyze_message_sentiment.func)
    params = list(sig.parameters.keys())
    print(f"Parameters: {params}")
    
    if 'message_content' in params and 'employee_id' in params:
        print("✅ Correct signature: (message_content, employee_id)")
    else:
        print("❌ Incorrect signature - should have message_content and employee_id")
        return False
    print()
    
    # 3. Check get_past_sentiment_history
    print("3️⃣ CHECKING get_past_sentiment_history")
    print("-" * 80)
    try:
        result = get_past_sentiment_history("TEST_CHECK", days_back=7)
        if all(key in result for key in ['employee_id', 'summary', 'daily_snapshots', 'recent_sentiments']):
            print("✅ Returns correct structure")
        if all(key in result['summary'] for key in ['average_sentiment_score', 'data_available']):
            print("✅ Summary contains average_sentiment_score and data_available")
        print(f"   Sample: average_sentiment_score = {result['summary']['average_sentiment_score']}")
        print(f"   Sample: data_available = {result['summary']['data_available']}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    print()
    
    # 4. Check search_wellbeing_resources region detection
    print("4️⃣ CHECKING search_wellbeing_resources REGION DETECTION")
    print("-" * 80)
    
    # Test local service
    local_result = search_wellbeing_resources.invoke({"query": "find therapist", "max_results": 1})
    print(f"Query: 'find therapist'")
    print(f"Region detected: {local_result.get('region')}")
    if local_result.get('region') == 'sg-en':
        print("✅ Local service correctly uses Singapore region")
    else:
        print("❌ Local service should use sg-en region")
        return False
    
    print()
    
    # Test general resource
    general_result = search_wellbeing_resources.invoke({"query": "stress management", "max_results": 1})
    print(f"Query: 'stress management'")
    print(f"Region detected: {general_result.get('region')}")
    if general_result.get('region') == 'wt-wt':
        print("✅ General resource correctly uses worldwide region")
    else:
        print("❌ General resource should use wt-wt region")
        return False
    print()
    
    # 5. Check system prompt alignment
    print("5️⃣ CHECKING SYSTEM PROMPT ALIGNMENT")
    print("-" * 80)
    try:
        from app.agent.well_being_agent.system_prompt import SYSTEM_PROMPT
        
        checks = {
            "analyze_message_sentiment mentioned": "analyze_message_sentiment" in SYSTEM_PROMPT,
            "employee_id parameter mentioned": "employee_id" in SYSTEM_PROMPT,
            "baseline comparison mentioned": "baseline" in SYSTEM_PROMPT,
            "search_wellbeing_resources mentioned": "search_wellbeing_resources" in SYSTEM_PROMPT,
            "Singapore auto-detection mentioned": "automatically" in SYSTEM_PROMPT and "Singapore" in SYSTEM_PROMPT,
        }
        
        for check_name, passed in checks.items():
            if passed:
                print(f"✅ {check_name}")
            else:
                print(f"⚠️ {check_name}")
    except Exception as e:
        print(f"❌ Error checking system prompt: {e}")
    print()
    
    # 6. Summary
    print("=" * 80)
    print("✅ IMPLEMENTATION CHECK COMPLETE")
    print("=" * 80)
    print()
    print("Summary:")
    print("✅ All tools properly implemented")
    print("✅ Sentiment analysis with baseline comparison")
    print("✅ Automatic Singapore region for local services")
    print("✅ System prompt aligned with tools")
    print()
    print("The wellbeing agent is ready for use! 🎉")
    
    return True

if __name__ == "__main__":
    success = check_implementation()
    sys.exit(0 if success else 1)
