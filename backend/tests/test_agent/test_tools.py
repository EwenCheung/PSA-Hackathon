"""Tests for mentoring agent tools."""
import json
import pytest
from app.agent.mentoring_agent.tools import (
    find_available_mentors,
    get_mentor_profile,
    get_mentee_profile,
    recommend_mentors,
    analyze_mentorship_progress,
    get_mentorship_statistics,
    validate_mentorship_goals,
    identify_mentor_gaps,
    MENTORING_TOOLS
)
from app.core.db import get_connection
from app.data.repositories.employee import EmployeeRepository
from app.data.repositories.mentorship_profile import MentorshipProfileRepository


@pytest.fixture
def setup_test_data():
    """Setup test database with sample data."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Initialize schema
    from app.core.db import init_db
    init_db(conn)
    
    # Create test employees (note: schema uses 'id' not 'employee_id')
    cursor.execute("""
        INSERT INTO employees (id, name, role, department_id, level, skills_map, goals_set)
        VALUES 
        ('MENTOR1', 'Alice Expert', 'Senior Engineer', 'DEPT001', 'Senior', 
         '{"SKILL001": 5, "SKILL002": 4}', '[]'),
        ('MENTOR2', 'Bob Guru', 'Lead Architect', 'DEPT001', 'Senior',
         '{"SKILL001": 5, "SKILL009": 5}', '[]'),
        ('MENTEE1', 'Charlie Junior', 'Junior Dev', 'DEPT001', 'Junior',
         '{"SKILL001": 2}', '["Learn cloud architecture", "Get certified"]')
    """)
    
    # Create mentorship profiles
    cursor.execute("""
        INSERT INTO mentorship_profiles (employee_id, is_mentor, capacity, mentees_count, rating, personality)
        VALUES 
        ('MENTOR1', 1, 3, 1, 4.5, 'Supportive'),
        ('MENTOR2', 1, 5, 2, 4.8, 'Analytical')
    """)
    
    conn.commit()
    yield conn
    
    # Cleanup
    cursor.execute("DELETE FROM mentorship_profiles WHERE employee_id IN ('MENTOR1', 'MENTOR2')")
    cursor.execute("DELETE FROM employees WHERE id IN ('MENTOR1', 'MENTOR2', 'MENTEE1')")
    conn.commit()


def test_find_available_mentors_no_filters(setup_test_data):
    """Test finding all available mentors."""
    result = find_available_mentors.invoke({})
    
    assert isinstance(result, list)
    assert len(result) >= 2
    assert all('employee_id' in m for m in result)
    assert all('available' in m for m in result)


def test_find_available_mentors_by_skill(setup_test_data):
    """Test finding mentors by specific skill."""
    result = find_available_mentors.invoke({"skill_area": "SKILL009"})
    
    assert isinstance(result, list)
    mentor_ids = [m['employee_id'] for m in result]
    assert 'MENTOR2' in mentor_ids


def test_find_available_mentors_by_rating(setup_test_data):
    """Test finding mentors with minimum rating."""
    result = find_available_mentors.invoke({"min_rating": 4.7})
    
    assert isinstance(result, list)
    assert all(m['rating'] >= 4.7 for m in result)


def test_find_available_mentors_excludes_full_capacity(setup_test_data):
    """Test that mentors at capacity are marked unavailable."""
    # Update MENTOR1 to full capacity
    conn = setup_test_data
    cursor = conn.cursor()
    cursor.execute("UPDATE mentorship_profiles SET mentees_count = 3 WHERE employee_id = 'MENTOR1'")
    conn.commit()
    
    result = find_available_mentors.invoke({})
    
    mentor1 = next((m for m in result if m['employee_id'] == 'MENTOR1'), None)
    if mentor1:
        assert not mentor1['available']


def test_get_mentor_profile_valid(setup_test_data):
    """Test retrieving a valid mentor profile."""
    result = get_mentor_profile.invoke({"employee_id": "MENTOR1"})
    
    assert result is not None
    assert result['employee_id'] == 'MENTOR1'
    assert result['name'] == 'Alice Expert'
    assert result['rating'] == 4.5
    assert 'available' in result


def test_get_mentor_profile_invalid(setup_test_data):
    """Test retrieving non-existent mentor."""
    result = get_mentor_profile.invoke({"employee_id": "INVALID"})
    assert result is None


def test_get_mentor_profile_empty_id(setup_test_data):
    """Test retrieving mentor with empty ID."""
    result = get_mentor_profile.invoke({"employee_id": ""})
    assert result is None


def test_get_mentee_profile_valid(setup_test_data):
    """Test retrieving a valid mentee profile."""
    result = get_mentee_profile.invoke({"employee_id": "MENTEE1"})
    
    assert result is not None
    assert result['employee_id'] == 'MENTEE1'
    assert result['name'] == 'Charlie Junior'
    assert result['level'] == 'Junior'
    assert 'current_skills' in result
    assert 'career_goals' in result


def test_get_mentee_profile_invalid(setup_test_data):
    """Test retrieving non-existent mentee."""
    result = get_mentee_profile.invoke({"employee_id": "INVALID"})
    assert result is None


def test_recommend_mentors_basic(setup_test_data):
    """Test basic mentor recommendation."""
    result = recommend_mentors.invoke({
        "employee_id": "MENTEE1",
        "career_goals": ["Cloud Architecture"],
        "desired_skills": ["SKILL001", "SKILL009"],
        "max_results": 3
    })
    
    assert isinstance(result, list)
    assert len(result) <= 3
    if len(result) > 0:
        assert all('match_score' in r for r in result)
        assert all('reasons' in r for r in result)


def test_recommend_mentors_empty_skills(setup_test_data):
    """Test recommendation with no skills returns empty."""
    result = recommend_mentors.invoke({
        "employee_id": "MENTEE1",
        "career_goals": [],
        "desired_skills": [],
        "max_results": 5
    })
    
    assert isinstance(result, list)
    assert len(result) == 0


def test_analyze_mentorship_progress_valid_pair(setup_test_data):
    """Test progress analysis for a valid pair."""
    result = analyze_mentorship_progress.invoke({"pair_id": "PAIR_001"})
    
    assert isinstance(result, dict)
    assert 'progress_score' in result
    assert 'engagement_level' in result
    assert 'recommendations' in result


def test_analyze_mentorship_progress_invalid_pair(setup_test_data):
    """Test progress analysis with invalid pair ID."""
    result = analyze_mentorship_progress.invoke({"pair_id": ""})
    
    assert isinstance(result, dict)
    assert result['progress_score'] == 0
    assert result['engagement_level'] == 'unknown'


def test_get_mentorship_statistics(setup_test_data):
    """Test getting overall mentorship statistics."""
    result = get_mentorship_statistics.invoke({})
    
    assert isinstance(result, dict)
    assert 'total_active_pairs' in result
    assert 'total_mentors' in result
    assert 'available_mentors' in result
    assert 'average_rating' in result
    assert result['total_mentors'] >= 2


def test_get_mentorship_statistics_by_department(setup_test_data):
    """Test statistics filtered by department."""
    result = get_mentorship_statistics.invoke({"department": "DEPT001"})
    
    assert isinstance(result, dict)
    assert 'total_mentors' in result


def test_validate_mentorship_goals_valid(setup_test_data):
    """Test validation of good mentorship goals."""
    result = validate_mentorship_goals.invoke({
        "goals": [
            "Master AWS certification by Q2",
            "Build production microservices project"
        ],
        "employee_profile": {"role": "Junior Dev", "level": "Junior"}
    })
    
    assert isinstance(result, dict)
    assert 'valid' in result
    assert 'feedback' in result


def test_validate_mentorship_goals_vague(setup_test_data):
    """Test validation catches vague goals."""
    result = validate_mentorship_goals.invoke({
        "goals": ["Learn Python"],
        "employee_profile": {"role": "Junior Dev", "level": "Junior"}
    })
    
    assert isinstance(result, dict)
    assert not result['valid']
    assert len(result['feedback']) > 0


def test_validate_mentorship_goals_empty(setup_test_data):
    """Test validation with no goals."""
    result = validate_mentorship_goals.invoke({
        "goals": [],
        "employee_profile": {"role": "Junior Dev", "level": "Junior"}
    })
    
    assert isinstance(result, dict)
    assert not result['valid']
    assert "No goals provided" in result['feedback']


def test_identify_mentor_gaps(setup_test_data):
    """Test identifying mentor skill gaps."""
    result = identify_mentor_gaps.invoke({})
    
    assert isinstance(result, list)
    if len(result) > 0:
        assert all('skill' in gap for gap in result)
        assert all('demand' in gap for gap in result)
        assert all('supply' in gap for gap in result)
        assert all('gap_severity' in gap for gap in result)


def test_identify_mentor_gaps_by_department(setup_test_data):
    """Test gap analysis for specific department."""
    result = identify_mentor_gaps.invoke({"department": "DEPT001"})
    
    assert isinstance(result, list)


def test_all_tools_have_decorator():
    """Verify all tools in MENTORING_TOOLS have @tool decorator."""
    assert len(MENTORING_TOOLS) == 8
    
    # Check that each tool is properly decorated (has required attributes)
    for tool in MENTORING_TOOLS:
        assert hasattr(tool, 'name'), f"{tool} missing 'name' attribute from @tool decorator"
        assert hasattr(tool, 'description'), f"{tool} missing 'description' attribute from @tool decorator"
        assert hasattr(tool, 'invoke'), f"{tool} missing 'invoke' method from @tool decorator"


def test_tool_names_are_unique():
    """Verify all tools have unique names."""
    names = [tool.name for tool in MENTORING_TOOLS]
    assert len(names) == len(set(names)), "Duplicate tool names found"


def test_all_tools_have_descriptions():
    """Verify all tools have non-empty descriptions."""
    for tool in MENTORING_TOOLS:
        assert tool.description, f"{tool.name} has empty description"
        assert len(tool.description) > 10, f"{tool.name} description too short"
