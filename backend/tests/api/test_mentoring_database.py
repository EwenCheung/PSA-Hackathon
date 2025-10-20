import json
import os
from pathlib import Path
from typing import Tuple

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1 import mentoring
from app.core.db import get_connection, init_db


def _seed_basic_data(db_path: Path) -> None:
    conn = get_connection(str(db_path))
    init_db(conn)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO departments (id, name) VALUES (?, ?)",
        ("DEPT777", "Innovation"),
    )

    cursor.execute(
        """
        INSERT INTO employees (
            id, name, role, department_id, level,
            position_level, points_current, hire_date,
            skills_map, courses_enrolled_map, goals_set
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "MENTOR123",
            "Dana Mentor",
            "Staff Engineer",
            "DEPT777",
            "Principal",
            4,
            500,
            "2018-01-15",
            json.dumps({"SKILL_A": 5, "SKILL_B": 4}),
            json.dumps({}),
            json.dumps(["Host architecture guild"]),
        ),
    )

    cursor.execute(
        """
        INSERT INTO employees (
            id, name, role, department_id, level,
            position_level, points_current, hire_date,
            skills_map, courses_enrolled_map, goals_set
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "SENIOR789",
            "Morgan Architect",
            "Principal Engineer",
            "DEPT777",
            "Senior",
            3,
            420,
            "2019-05-20",
            json.dumps({"SKILL_B": 5}),
            json.dumps({}),
            json.dumps(["Grow engineering leadership"]),
        ),
    )

    cursor.execute(
        """
        INSERT INTO employees (
            id, name, role, department_id, level,
            position_level, points_current, hire_date,
            skills_map, courses_enrolled_map, goals_set
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "MENTEE456",
            "Riley Learner",
            "Software Engineer",
            "DEPT777",
            "Mid",
            2,
            120,
            "2022-09-01",
            json.dumps({"SKILL_B": 2}),
            json.dumps({}),
            json.dumps(["Grow in system design"]),
        ),
    )

    cursor.executemany(
        "INSERT INTO skills (id, name, category) VALUES (?, ?, ?)",
        [
            ("SKILL_A", "System Design", "Architecture"),
            ("SKILL_B", "Technical Leadership", "Leadership"),
        ],
    )

    cursor.execute(
        """
        INSERT INTO mentorship_profiles (
            employee_id, is_mentor, capacity, mentees_count, rating, personality
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        ("MENTOR123", 1, 3, 1, 4.9, "Analytical"),
    )

    conn.commit()
    conn.close()


@pytest.fixture()
def client_with_db(tmp_path: Path) -> Tuple[TestClient, Path]:
    db_path = tmp_path / "mentoring_test.db"
    os.environ["DATABASE_URL"] = str(db_path)
    _seed_basic_data(db_path)

    app = FastAPI()
    app.include_router(mentoring.router)
    client = TestClient(app)

    yield client, db_path

    os.environ.pop("DATABASE_URL", None)


def test_list_mentors_reads_from_database(client_with_db: Tuple[TestClient, Path]) -> None:
    client, _ = client_with_db
    response = client.get(
        "/api/v1/mentoring/mentors",
        params={"mentee_id": "MENTEE456"},
    )

    assert response.status_code == 200
    payload = response.json()
    ids = {mentor["employeeId"] for mentor in payload}

    assert ids == {"MENTOR123", "SENIOR789"}


def test_create_request_persists_record(client_with_db: Tuple[TestClient, Path]) -> None:
    client, db_path = client_with_db
    payload = {
        "menteeId": "MENTEE456",
        "mentorId": "SENIOR789",
        "message": "I'd love guidance on system design.",
        "goals": ["System Design"],
    }

    create_response = client.post("/api/v1/mentoring/request", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["menteeId"] == "MENTEE456"
    assert created["mentorId"] == "SENIOR789"

    conn = get_connection(str(db_path))
    row = conn.execute(
        "SELECT mentee_id, mentor_id, status FROM mentor_match_requests"
    ).fetchone()
    conn.close()

    assert row is not None
    assert row["mentee_id"] == "MENTEE456"
    assert row["mentor_id"] == "SENIOR789"
    assert row["status"] == "pending"

    # Attempting a duplicate pending request should fail
    duplicate_response = client.post("/api/v1/mentoring/request", json=payload)
    assert duplicate_response.status_code == 400


def test_list_requests_filtered_by_mentor(client_with_db: Tuple[TestClient, Path]) -> None:
    client, _ = client_with_db

    payload = {
        "menteeId": "MENTEE456",
        "mentorId": "SENIOR789",
        "message": "Looking forward to learning more.",
        "goals": ["System Design"],
    }
    client.post("/api/v1/mentoring/request", json=payload)

    response = client.get(
        "/api/v1/mentoring/requests",
        params={"mentor_id": "SENIOR789"},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["menteeId"] == "MENTEE456"


def test_declined_requests_stay_in_history_and_allow_new_application(
    client_with_db: Tuple[TestClient, Path]
) -> None:
    client, _ = client_with_db

    initial_payload = {
        "menteeId": "MENTEE456",
        "mentorId": "MENTOR123",
        "message": "First attempt",
        "goals": ["System Design"],
    }
    first_response = client.post("/api/v1/mentoring/request", json=initial_payload)
    assert first_response.status_code == 201
    first_request_id = first_response.json()["requestId"]

    decline_response = client.put(
        f"/api/v1/mentoring/requests/{first_request_id}",
        json={"status": "declined", "responseMessage": "No capacity"},
    )
    assert decline_response.status_code == 200

    second_payload = {
        "menteeId": "MENTEE456",
        "mentorId": "SENIOR789",
        "message": "Second attempt",
        "goals": ["Leadership"],
    }
    second_response = client.post("/api/v1/mentoring/request", json=second_payload)
    assert second_response.status_code == 201

    history_response = client.get(
        "/api/v1/mentoring/requests",
        params={"mentee_id": "MENTEE456"},
    )
    assert history_response.status_code == 200
    history = history_response.json()

    assert len(history) == 2
    statuses = {entry["status"] for entry in history}
    assert statuses == {"declined", "pending"}
    mentor_ids = {entry["mentorId"] for entry in history}
    assert mentor_ids == {"MENTOR123", "SENIOR789"}


def test_accept_request_creates_pair(client_with_db: Tuple[TestClient, Path]) -> None:
    client, db_path = client_with_db
    payload = {
        "menteeId": "MENTEE456",
        "mentorId": "MENTOR123",
        "message": "Looking forward to learning more.",
        "goals": ["System Design"],
    }
    create_response = client.post("/api/v1/mentoring/request", json=payload)
    request_id = create_response.json()["requestId"]

    update_response = client.put(
        f"/api/v1/mentoring/requests/{request_id}",
        json={"status": "accepted"},
    )
    assert update_response.status_code == 200

    conn = get_connection(str(db_path))
    request_row = conn.execute(
        "SELECT status FROM mentor_match_requests"
    ).fetchone()
    match_row = conn.execute(
        "SELECT mentor_id, mentee_id FROM mentorship_matches"
    ).fetchone()
    mentor_profile = conn.execute(
        "SELECT mentees_count FROM mentorship_profiles WHERE employee_id = ?",
        ("MENTOR123",),
    ).fetchone()
    conn.close()

    assert request_row is not None
    assert request_row["status"] == "accepted"
    assert match_row is not None
    assert match_row["mentor_id"] == "MENTOR123"
    assert match_row["mentee_id"] == "MENTEE456"
    assert mentor_profile is not None
    assert mentor_profile["mentees_count"] == 2


def test_delete_request_allows_new_application(client_with_db: Tuple[TestClient, Path]) -> None:
    client, db_path = client_with_db
    payload = {
        "menteeId": "MENTEE456",
        "mentorId": "MENTOR123",
        "message": "First attempt.",
        "goals": ["System Design"],
    }
    create_response = client.post("/api/v1/mentoring/request", json=payload)
    request_id = create_response.json()["requestId"]

    delete_response = client.delete(
        f"/api/v1/mentoring/requests/{request_id}", params={"mentee_id": "MENTEE456"}
    )
    assert delete_response.status_code == 204

    conn = get_connection(str(db_path))
    row = conn.execute(
        "SELECT * FROM mentor_match_requests WHERE mentee_id = ?", ("MENTEE456",)
    ).fetchone()
    conn.close()
    assert row is None

    second_response = client.post("/api/v1/mentoring/request", json=payload)
    assert second_response.status_code == 201


def test_create_request_accepts_alias_ids(client_with_db: Tuple[TestClient, Path]) -> None:
    client, db_path = client_with_db
    conn = get_connection(str(db_path))
    init_db(conn)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO employees (
            id, name, role, department_id, level, position_level,
            points_current, hire_date, skills_map, courses_enrolled_map, goals_set
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "EMP001",
            "Alice Mentor",
            "Principal Engineer",
            "DEPT777",
            "Principal",
            4,
            500,
            "2015-01-01",
            json.dumps({"SKILL_A": 5}),
            json.dumps({}),
            json.dumps(["Grow leaders"]),
        ),
    )
    cursor.execute(
        """
        INSERT OR REPLACE INTO employees (
            id, name, role, department_id, level, position_level,
            points_current, hire_date, skills_map, courses_enrolled_map, goals_set
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "EMP010",
            "Casey Learner",
            "Software Engineer",
            "DEPT777",
            "Mid",
            2,
            150,
            "2022-05-05",
            json.dumps({"SKILL_B": 2}),
            json.dumps({}),
            json.dumps(["Improve leadership"]),
        ),
    )
    cursor.execute(
        """
        INSERT OR REPLACE INTO mentorship_profiles (
            employee_id, is_mentor, capacity, mentees_count, rating, personality
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        ("EMP001", 1, 3, 0, 4.9, "Supportive"),
    )
    conn.commit()
    conn.close()

    payload = {
        "menteeId": "EP010",
        "mentorId": "EP001",
        "message": "Alias request.",
        "goals": ["Leadership"],
    }

    create_response = client.post("/api/v1/mentoring/request", json=payload)
    assert create_response.status_code == 201
    body = create_response.json()
    assert body["menteeId"] == "EMP010"
    assert body["mentorId"] == "EMP001"

    list_response = client.get(
        "/api/v1/mentoring/requests",
        params={"mentee_id": "EP010"},
    )
    assert list_response.status_code == 200
    assert list_response.json()
