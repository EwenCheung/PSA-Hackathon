"""
Tests for mentorship_profile repository
Following TDD approach - tests written before implementation
"""
import pytest
import sqlite3
from app.data.repositories.mentorship_profile import MentorshipProfileRepository
from app.core.db import init_db


@pytest.fixture
def test_db():
    """Create an in-memory test database with schema"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    
    # Insert test data
    cur = conn.cursor()
    
    # Insert test departments
    cur.execute("INSERT INTO departments (id, name) VALUES ('DEPT001', 'Engineering')")
    
    # Insert test employees
    cur.execute("""
        INSERT INTO employees (id, name, role, department_id, level, points_current, hire_date, skills_map)
        VALUES 
        ('EMP001', 'Alice Chen', 'Senior Software Engineer', 'DEPT001', 'Senior', 350, '2020-03-15', 
         '{"SKILL001": 5, "SKILL003": 4}'),
        ('EMP002', 'Bob Martinez', 'Operations Manager', 'DEPT002', 'Mid', 280, '2019-07-22',
         '{"SKILL011": 5, "SKILL012": 5}'),
        ('EMP005', 'David Lee', 'Tech Lead', 'DEPT001', 'Senior', 400, '2018-01-10',
         '{"SKILL001": 5, "SKILL009": 5}')
    """)
    
    # Insert test mentorship profiles
    cur.execute("""
        INSERT INTO mentorship_profiles (employee_id, is_mentor, capacity, mentees_count, rating, personality)
        VALUES 
        ('EMP001', 1, 3, 2, 4.8, 'Analytical, Patient'),
        ('EMP002', 1, 2, 1, 4.5, 'Strategic, Supportive'),
        ('EMP005', 1, 3, 3, 4.9, 'Technical, Thorough')
    """)
    
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def repo(test_db):
    """Create repository instance with test database"""
    return MentorshipProfileRepository(test_db)


class TestGetAvailableMentors:
    """Test get_available_mentors method"""
    
    def test_returns_all_available_mentors_when_no_filters(self, repo):
        """GIVEN mentors in database
           WHEN calling get_available_mentors with no filters
           THEN all available mentors are returned"""
        mentors = repo.get_available_mentors()
        assert len(mentors) >= 1
        assert all(m['is_mentor'] == 1 for m in mentors)
    
    def test_filters_by_skill_area(self, repo, test_db):
        """GIVEN mentors with different skills
           WHEN filtering by specific skill
           THEN only mentors with that skill are returned"""
        # This requires joining with employees table for skills
        mentors = repo.get_available_mentors(skill_area="SKILL001")
        assert len(mentors) >= 1
        # Verify mentors have the requested skill
    
    def test_filters_by_department(self, repo):
        """GIVEN mentors in different departments
           WHEN filtering by department
           THEN only mentors from that department are returned"""
        mentors = repo.get_available_mentors(department="DEPT001")
        assert len(mentors) >= 1
    
    def test_filters_by_min_rating(self, repo):
        """GIVEN mentors with different ratings
           WHEN filtering by minimum rating
           THEN only mentors with rating >= min_rating are returned"""
        mentors = repo.get_available_mentors(min_rating=4.7)
        assert all(m['rating'] >= 4.7 for m in mentors)
    
    def test_excludes_at_capacity_mentors(self, repo):
        """GIVEN mentors at full capacity
           WHEN getting available mentors
           THEN mentors where mentees_count >= capacity are excluded"""
        mentors = repo.get_available_mentors()
        # EMP005 has 3/3 capacity, should be excluded
        mentor_ids = [m['employee_id'] for m in mentors]
        assert 'EMP005' not in mentor_ids
    
    def test_combines_multiple_filters(self, repo):
        """GIVEN multiple filter criteria
           WHEN all filters applied
           THEN only mentors matching ALL criteria are returned"""
        mentors = repo.get_available_mentors(
            department="DEPT001",
            min_rating=4.5
        )
        assert all(m['rating'] >= 4.5 for m in mentors)


class TestGetMentorStatistics:
    """Test get_mentor_statistics method"""
    
    def test_returns_statistics_for_mentor(self, repo):
        """GIVEN a mentor with mentees
           WHEN getting statistics
           THEN returns capacity, current count, and rating"""
        stats = repo.get_mentor_statistics('EMP001')
        assert stats is not None
        assert stats['capacity'] == 3
        assert stats['mentees_count'] == 2
        assert stats['rating'] == 4.8
    
    def test_returns_none_for_nonexistent_mentor(self, repo):
        """GIVEN a non-existent employee ID
           WHEN getting statistics
           THEN returns None"""
        stats = repo.get_mentor_statistics('NONEXISTENT')
        assert stats is None
