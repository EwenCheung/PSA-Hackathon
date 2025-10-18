"""
Tests for employee repository skill matching queries
Following TDD approach
"""
import pytest
import sqlite3
from app.data.repositories.employee import EmployeeRepository
from app.core.db import init_db


@pytest.fixture
def test_db():
    """Create an in-memory test database with schema"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    
    cur = conn.cursor()
    
    # Insert test departments
    cur.execute("INSERT INTO departments (id, name) VALUES ('DEPT001', 'Engineering'), ('DEPT002', 'Operations')")
    
    # Insert test skills
    cur.execute("""
        INSERT INTO skills (id, name, category)
        VALUES 
        ('SKILL001', 'Python', 'Technical'),
        ('SKILL002', 'JavaScript', 'Technical'),
        ('SKILL003', 'SQL', 'Technical'),
        ('SKILL009', 'System Design', 'Technical')
    """)
    
    # Insert test employees with skills
    cur.execute("""
        INSERT INTO employees (id, name, role, department_id, level, skills_map, hire_date)
        VALUES 
        ('EMP001', 'Alice Chen', 'Senior Software Engineer', 'DEPT001', 'Senior',
         '{"SKILL001": 5, "SKILL003": 4, "SKILL009": 4}', '2020-03-15'),
        ('EMP002', 'Bob Martinez', 'Operations Manager', 'DEPT002', 'Mid',
         '{"SKILL002": 3}', '2019-07-22'),
        ('EMP003', 'Carol Johnson', 'Data Analyst', 'DEPT001', 'Mid',
         '{"SKILL001": 3, "SKILL003": 5}', '2021-01-10'),
        ('EMP004', 'David Lee', 'Junior Developer', 'DEPT001', 'Junior',
         '{"SKILL002": 3, "SKILL003": 3}', '2023-05-01')
    """)
    
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def repo(test_db):
    """Create repository instance with test database"""
    return EmployeeRepository(test_db)


class TestFindEmployeesBySkills:
    """Test find_employees_by_skills method"""
    
    def test_finds_employees_with_single_skill(self, repo):
        """GIVEN employees with various skills
           WHEN searching for single skill
           THEN returns all employees with that skill"""
        employees = repo.find_employees_by_skills(['SKILL001'])
        assert len(employees) >= 2  # Alice and Carol have Python
        employee_ids = [e['id'] for e in employees]
        assert 'EMP001' in employee_ids
        assert 'EMP003' in employee_ids
    
    def test_finds_employees_with_multiple_skills(self, repo):
        """GIVEN employees with skill combinations
           WHEN searching for multiple skills
           THEN returns employees matching ANY of the skills"""
        employees = repo.find_employees_by_skills(['SKILL001', 'SKILL009'])
        assert len(employees) >= 1
        # At least Alice should match (has both)
        employee_ids = [e['id'] for e in employees]
        assert 'EMP001' in employee_ids
    
    def test_returns_empty_for_nonexistent_skill(self, repo):
        """GIVEN a skill that no employee has
           WHEN searching for that skill
           THEN returns empty list"""
        employees = repo.find_employees_by_skills(['SKILL999'])
        assert len(employees) == 0
    
    def test_returns_empty_for_empty_skill_list(self, repo):
        """GIVEN empty skill list
           WHEN searching
           THEN returns empty list"""
        employees = repo.find_employees_by_skills([])
        assert len(employees) == 0


class TestGetEmployeeByDepartment:
    """Test getting employees by department"""
    
    def test_filters_by_department(self, repo):
        """GIVEN employees in different departments
           WHEN filtering by department
           THEN only employees from that department are returned"""
        employees = repo.get_employees_by_department('DEPT001')
        assert len(employees) >= 3
        assert all(e['department_id'] == 'DEPT001' for e in employees)
    
    def test_returns_empty_for_nonexistent_department(self, repo):
        """GIVEN a non-existent department
           WHEN getting employees
           THEN returns empty list"""
        employees = repo.get_employees_by_department('NONEXISTENT')
        assert len(employees) == 0
