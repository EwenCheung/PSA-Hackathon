"""Quick test to check if tools can access database data."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Testing database and tools...\n")

# Test 1: Database connection
print("1️⃣  Testing database connection...")
from app.core.db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute('SELECT COUNT(*) FROM employees')
emp_count = cur.fetchone()[0]
print(f"   ✅ Database has {emp_count} employees")

cur.execute('SELECT COUNT(*) FROM mentorship_profiles WHERE is_mentor = 1')
mentor_count = cur.fetchone()[0]
print(f"   ✅ Database has {mentor_count} mentors")

# Test 2: Tool functions directly
print("\n2️⃣  Testing tool functions directly...")

from app.agent.mentoring_agent.tools import find_available_mentors, get_mentor_profile

try:
    # Test find_available_mentors (use .invoke() for LangChain tools)
    result = find_available_mentors.invoke({"skill_area": "Python", "min_rating": 4.5})
    print(f"   ✅ find_available_mentors returned {len(result)} mentors")
    if result:
        print(f"      First mentor: {result[0].get('name', 'Unknown')}")
except Exception as e:
    print(f"   ❌ find_available_mentors error: {e}")

try:
    # Test get_mentor_profile (use .invoke() for LangChain tools)
    profile = get_mentor_profile.invoke({"employee_id": "EMP001"})
    if profile:
        print(f"   ✅ get_mentor_profile returned: {profile.get('name', 'Unknown')}")
    else:
        print(f"   ⚠️  get_mentor_profile returned None")
except Exception as e:
    print(f"   ❌ get_mentor_profile error: {e}")

print("\n✨ Database and tools test complete!")
