import sqlite3
import sys
import types

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core import db


@pytest.fixture(autouse=True)
def stub_course_agent_modules(monkeypatch):
    """
    Replace course agent modules that require external services.

    The mentoring router imports seed_data which depends on these modules.
    We stub them so tests can run in isolation without Azure access.
    """
    # Ensure upstream modules are cleared before stubbing
    for module in list(sys.modules):
        if module.startswith("app.agent.course_recommendation_agent."):
            monkeypatch.delitem(sys.modules, module, raising=False)

    tools_stub = types.ModuleType("app.agent.course_recommendation_agent.tools")
    tools_stub.get_employee_context = lambda employee_id: {
        "profile": {
            "id": employee_id,
            "name": "Test User",
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

    main_stub = types.ModuleType("app.agent.course_recommendation_agent.main")
    main_stub.get_leadership_potential_employer = lambda employee_id: {
        "json": {},
        "text_summary": "",
    }
    main_stub.get_career_pathway = lambda employee_id: {
        "json": {},
        "text_summary": "",
    }

    monkeypatch.setitem(
        sys.modules, "app.agent.course_recommendation_agent.tools", tools_stub
    )
    monkeypatch.setitem(
        sys.modules, "app.agent.course_recommendation_agent.main", main_stub
    )


def _make_thread_bound_connection() -> sqlite3.Connection:
    """
    Create an in-memory SQLite connection that enforces same-thread usage.

    FastAPI runs sync dependencies in a thread pool. When the async endpoint
    continues on the event loop, that thread switch triggers the original
    ProgrammingError seen in production.
    """
    conn = sqlite3.connect(":memory:")  # check_same_thread defaults to True
    conn.row_factory = sqlite3.Row
    db.init_db(conn)

    cur = conn.cursor()
    cur.execute("INSERT INTO departments (id, name) VALUES (?, ?)", ("DEPT1", "Engineering"))
    cur.execute(
        """
        INSERT INTO employees (
            id, name, role, department_id, level, position_level,
            points_current, hire_date, skills_map
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "EMP001",
            "Mentor One",
            "Senior Engineer",
            "DEPT1",
            "Senior",
            5,
            1000,
            "2015-01-01",
            '{"python": 3}',
        ),
    )
    cur.execute(
        """
        INSERT INTO mentorship_profiles (
            employee_id, is_mentor, capacity, mentees_count, rating, personality
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        ("EMP001", 1, 3, 0, 4.8, "Helpful mentor"),
    )
    conn.commit()
    return conn


def test_list_mentors_fails_with_default_thread_bound_connection(monkeypatch):
    """
    Reproduce the thread-bound SQLite failure observed in the browser logs.

    The mentoring dependency builds its connection inside a sync dependency,
    then yields control to an async endpoint. Without configuring the
    connection for cross-thread use, FastAPI raises ProgrammingError.
    """
    from app.api.v1 import mentoring

    # Force the dependency to return a thread-bound connection.
    monkeypatch.setattr(
        mentoring,
        "get_connection",
        lambda url=None: _make_thread_bound_connection(),
    )

    app = FastAPI()
    app.include_router(mentoring.router)
    client = TestClient(app)

    response = client.get("/api/v1/mentoring/mentors")
    assert response.status_code == 200
