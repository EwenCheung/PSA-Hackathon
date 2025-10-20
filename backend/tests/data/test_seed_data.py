import sqlite3
import sys
import types

# Stub heavy course agent dependencies before importing seed_data
tools_module = "app.agent.course_recommendation_agent.tools"
if tools_module not in sys.modules:
    tools_stub = types.ModuleType(tools_module)
    tools_stub.get_employee_context = lambda employee_id: {
        "profile": {
            "id": employee_id,
            "name": "Seed Test User",
            "department_id": "DEPT1",
            "role": "Role",
            "level": "Senior",
            "hire_date": "2015-01-01",
            "points_current": 0,
        },
        "skills": ["python"],
        "goals": [],
        "courses_enrolled": {},
    }
    tools_stub.recommend_courses_tool = lambda skills, top_k=3: []

    class _EmployeeRepoStub:
        def list_employees(self):
            return []

    tools_stub.employee_repo = _EmployeeRepoStub()
    sys.modules[tools_module] = tools_stub

main_module = "app.agent.course_recommendation_agent.main"
if main_module not in sys.modules:
    main_stub = types.ModuleType(main_module)
    main_stub.get_leadership_potential_employer = lambda employee_id: {
        "json": {},
        "text_summary": "",
    }
    main_stub.get_career_pathway = lambda employee_id: {
        "json": {},
        "text_summary": "",
    }
    sys.modules[main_module] = main_stub

from app.core.db import init_db
from app.data import seed_data


def test_load_all_seeds_can_skip_insights(monkeypatch):
    """
    When load_all_seeds is asked to skip insights generation it should not
    trigger the expensive analytics workflow.
    """
    called = False

    def _fake_generate(conn):
        nonlocal called
        called = True

    monkeypatch.setattr(seed_data, "generate_employee_insights", _fake_generate)

    conn = sqlite3.connect(":memory:")
    init_db(conn)

    seed_data.load_all_seeds(conn, generate_insights=False)

    assert called is False
    conn.close()


def test_load_mentorship_profiles_skips_missing_employee(monkeypatch):
    """Mentorship profile loader should skip rows whose employee is absent."""
    conn = sqlite3.connect(":memory:")
    init_db(conn)

    sample_profiles = [
        {
            "employee_id": "EMP999",
            "is_mentor": 1,
            "capacity": 2,
            "mentees_count": 0,
            "rating": 4.5,
            "personality": "Supportive mentor",
        }
    ]

    def fake_load_json(path):
        if path.name == "mentorship_profiles.json":
            return sample_profiles
        raise AssertionError(f"Unexpected file load: {path}")

    monkeypatch.setattr(seed_data, "load_json_file", fake_load_json)

    # Should not raise even though employee EMP999 does not exist
    seed_data.load_mentorship_profiles(conn)

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM mentorship_profiles")
    assert cur.fetchone()[0] == 0
    conn.close()


def test_load_goals_skips_missing_employee(monkeypatch):
    """Goal loader should ignore rows for employees that do not exist."""
    conn = sqlite3.connect(":memory:")
    init_db(conn)

    sample_goals = [
        {
            "employee_id": "EMP123",
            "title": "Build mentorship culture",
            "target_date": "2025-06-01",
            "progress_percent": 50,
        }
    ]

    def fake_load_json(path):
        if path.name == "goals.json":
            return sample_goals
        raise AssertionError(f"Unexpected file load: {path}")

    monkeypatch.setattr(seed_data, "load_json_file", fake_load_json)

    seed_data.load_goals(conn)

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM goals")
    assert cur.fetchone()[0] == 0
    conn.close()
