import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.analytics import router, get_analytics_service
from app.core.db import get_connection, init_db
from app.services.analytics_service import AnalyticsService


@pytest.fixture()
def conn():
    connection = get_connection(":memory:")
    init_db(connection)
    seed_test_data(connection)
    yield connection
    connection.close()


def seed_test_data(connection):
    cursor = connection.cursor()
    # Departments
    cursor.execute("INSERT INTO departments (id, name) VALUES (?, ?)", ("DEPT001", "Engineering"))
    cursor.execute("INSERT INTO departments (id, name) VALUES (?, ?)", ("DEPT002", "Product"))

    # Employees
    employees = [
        ("EMP001", "Alice Chen", "Senior Engineer", "DEPT001", "Senior", 400, "2020-03-15"),
        ("EMP002", "Bob Lee", "Engineer", "DEPT001", "Mid", 200, "2021-05-20"),
        ("EMP003", "Cara Diaz", "Product Manager", "DEPT002", "Mid", 100, "2022-01-10"),
    ]
    for employee in employees:
        cursor.execute(
            """
            INSERT INTO employees (
                id, name, role, department_id, level, points_current, hire_date,
                skills_map, courses_enrolled_map, goals_set
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (*employee, "{}", "{}", "[]"),
        )

    # Courses
    courses = [
        ("COURSE001", "Advanced Python", "Desc", "Advanced", 8, 5, 100, "High", 1),
        ("COURSE002", "Leadership", "Desc", "Intermediate", 6, 3, 80, "High", 1),
        ("COURSE003", "Product Strategy", "Desc", "Intermediate", 6, 3, 80, "Medium", 1),
    ]
    for course in courses:
        cursor.execute(
            """
            INSERT INTO courses (
                id, title, description, difficulty, duration_weeks,
                effort_hours_week, points_reward, roi, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            course,
        )

    # Enrollments
    enrollments = [
        ("EMP001", "COURSE001", "completed", 100, "2024-01-10", "2024-03-15", 100),
        ("EMP001", "COURSE002", "in-progress", 50, "2024-05-01", None, None),
        ("EMP002", "COURSE001", "completed", 100, "2024-02-05", "2024-04-20", 100),
        ("EMP003", "COURSE003", "in-progress", 40, "2024-03-11", None, None),
    ]
    for enrollment in enrollments:
        cursor.execute(
            """
            INSERT INTO enrollments (
                employee_id, course_id, status, progress_percent,
                started_at, completed_at, points_awarded
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            enrollment,
        )

    # Goals
    goals = [
        ("EMP001", "Goal 1", "2025-01-01", 80),
        ("EMP001", "Goal 2", "2025-06-01", 60),
        ("EMP002", "Goal 1", "2025-04-01", 50),
        ("EMP003", "Goal 1", "2025-07-01", 30),
    ]
    for goal in goals:
        cursor.execute(
            """
            INSERT INTO goals (employee_id, title, target_date, progress_percent)
            VALUES (?, ?, ?, ?)
            """,
            goal,
        )

    connection.commit()


@pytest.fixture()
def analytics_client(conn):
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_analytics_service] = lambda: AnalyticsService(conn)
    return TestClient(app)


def test_overview_metrics(conn):
    service = AnalyticsService(conn)

    overview = service.get_overview_metrics()

    assert overview.total_employees == 3
    assert overview.total_completed_courses == 2
    assert overview.average_career_progress == 50.0


def test_department_metrics(conn):
    service = AnalyticsService(conn)

    departments = service.get_department_metrics()
    metrics = {dept.department_id: dept for dept in departments}

    assert metrics["DEPT001"].employee_count == 2
    assert metrics["DEPT001"].average_performance == 67.5
    assert metrics["DEPT002"].average_performance == 27.5


def test_employee_metrics(conn):
    service = AnalyticsService(conn)

    employees = service.get_employee_metrics()
    metrics = {emp.id: emp for emp in employees}

    assert metrics["EMP001"].courses_completed == 1
    assert metrics["EMP001"].courses_in_progress == 1
    assert metrics["EMP001"].career_progress_percent == 70.0
    assert metrics["EMP001"].points == 400

    assert metrics["EMP003"].courses_completed == 0
    assert metrics["EMP003"].courses_in_progress == 1
    assert metrics["EMP003"].career_progress_percent == 30.0


def test_overview_endpoint(analytics_client):
    response = analytics_client.get("/api/v1/analytics/overview")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total_employees"] == 3
    assert payload["total_completed_courses"] == 2
    assert payload["average_career_progress"] == 50.0


def test_departments_endpoint(analytics_client):
    response = analytics_client.get("/api/v1/analytics/departments")
    assert response.status_code == 200
    payload = {dept["department_id"]: dept for dept in response.json()}
    assert payload["DEPT001"]["employee_count"] == 2
    assert payload["DEPT001"]["average_performance"] == 67.5


def test_employees_endpoint(analytics_client):
    response = analytics_client.get("/api/v1/analytics/employees")
    assert response.status_code == 200
    payload = {emp["id"]: emp for emp in response.json()}
    assert "sentiment" not in payload["EMP001"]
    assert payload["EMP001"]["courses_completed"] == 1
