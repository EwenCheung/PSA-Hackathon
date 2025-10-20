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
