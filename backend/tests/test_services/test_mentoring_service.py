"""
Mentoring Service: Business logic for mentor-mentee matching and analytics
Following TDD approach
"""
import pytest
import sqlite3
import json
from app.services.mentoring_service import MentoringService
from app.data.repositories.employee import EmployeeRepository
from app.data.repositories.mentorship_profile import MentorshipProfileRepository
from app.core.db import init_db


@pytest.fixture
def test_db():
    """Create test database with realistic data"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    
    cur = conn.cursor()
    
    # Departments
    cur.execute("INSERT INTO departments (id, name) VALUES ('DEPT001', 'Engineering'), ('DEPT002', 'Operations')")
    
    # Skills
    cur.execute("""
        INSERT INTO skills (id, name, category)
        VALUES 
        ('SKILL001', 'Python', 'Technical'),
        ('SKILL003', 'SQL', 'Technical'),
        ('SKILL009', 'System Design', 'Technical'),
        ('SKILL012', 'Leadership', 'Soft')
    """)
    
    # Employees
    cur.execute("""
        INSERT INTO employees (id, name, role, department_id, level, skills_map, hire_date, goals_set)
        VALUES 
        ('EMP001', 'Alice Chen', 'Senior Software Engineer', 'DEPT001', 'Senior',
         '{"SKILL001": 5, "SKILL003": 4, "SKILL009": 4}', '2015-03-15', '["Mentoring"]'),
        ('EMP003', 'Carol Johnson', 'Junior Developer', 'DEPT001', 'Junior',
         '{"SKILL001": 2}', '2023-01-10', '["Learn System Design", "Python Mastery"]')
    """)
    
    # Mentorship profiles
    cur.execute("""
        INSERT INTO mentorship_profiles (employee_id, is_mentor, capacity, mentees_count, rating, personality)
        VALUES 
        ('EMP001', 1, 3, 1, 4.8, 'Analytical, Patient')
    """)
    
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def service(test_db):
    """Create service with repositories"""
    employee_repo = EmployeeRepository(test_db)
    mentor_repo = MentorshipProfileRepository(test_db)
    return MentoringService(employee_repo, mentor_repo)


class TestCalculateMatchScore:
    """Test matching algorithm"""
    
    def test_calculates_skill_alignment_score(self, service):
        """GIVEN mentee wants Python and System Design
           AND mentor has both skills
           THEN skill score should be high"""
        mentee = {
            'desired_skills': ['SKILL001', 'SKILL009'],
            'level': 'Junior',
            'department_id': 'DEPT001'
        }
        mentor = {
            'skills_map': '{"SKILL001": 5, "SKILL009": 4}',
            'level': 'Senior',
            'department_id': 'DEPT001',
            'rating': 4.8,
            'mentees_count': 1,
            'capacity': 3
        }
        
        score = service.calculate_match_score(mentee, mentor)
        assert score > 70  # Should be high match
    
    def test_lower_score_for_skill_mismatch(self, service):
        """GIVEN mentee wants skills mentor doesn't have
           THEN score should be lower"""
        mentee = {
            'desired_skills': ['SKILL999'],
            'level': 'Junior',
            'department_id': 'DEPT001'
        }
        mentor = {
            'skills_map': '{"SKILL001": 5}',
            'level': 'Senior',
            'department_id': 'DEPT001',
            'rating': 4.8,
            'mentees_count': 1,
            'capacity': 3
        }
        
        score = service.calculate_match_score(mentee, mentor)
        assert score < 50  # Should be low match


class TestRecommendMentors:
    """Test end-to-end mentor recommendation"""
    
    def test_returns_ranked_mentors(self, service):
        """GIVEN a mentee profile
           WHEN requesting recommendations
           THEN returns mentors ranked by score"""
        recommendations = service.recommend_mentors(
            employee_id='EMP003',
            career_goals=['Learn System Design'],
            desired_skills=['SKILL001', 'SKILL009'],
            max_results=5
        )
        
        assert len(recommendations) > 0
        assert 'mentor_id' in recommendations[0]
        assert 'match_score' in recommendations[0]
        assert 'reasons' in recommendations[0]
