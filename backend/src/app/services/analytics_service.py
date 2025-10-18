"""
AnalyticsService: Aggregates organization metrics for employer analytics.
"""
from __future__ import annotations

from typing import List, Optional

from app.core.db import get_connection
from app.data.repositories.employee import EmployeeRepository
from app.data.repositories.enrollment import EnrollmentRepository
from app.data.repositories.goal import GoalRepository
from app.models.pydantic_schemas import (
    AnalyticsDepartment,
    AnalyticsEmployee,
    AnalyticsOverview,
)


class AnalyticsService:
    def __init__(self, conn=None) -> None:
        self.conn = conn or get_connection()
        self.employee_repo = EmployeeRepository(self.conn)
        self.enrollment_repo = EnrollmentRepository(self.conn)
        self.goal_repo = GoalRepository(self.conn)

    def get_overview_metrics(self) -> AnalyticsOverview:
        employees = self.employee_repo.list_employees()
        total_employees = len(employees)
        total_completed_courses = self.enrollment_repo.count_completed_courses()

        goal_progress_map = {
            row["employee_id"]: float(row["average_progress"])
            for row in self.goal_repo.get_average_progress_by_employee()
            if row["average_progress"] is not None
        }

        cumulative_progress = 0.0
        if total_employees:
            for employee in employees:
                cumulative_progress += goal_progress_map.get(employee["id"], 0.0)
            average_career_progress = cumulative_progress / total_employees
        else:
            average_career_progress = 0.0

        return AnalyticsOverview(
            total_employees=total_employees,
            total_completed_courses=total_completed_courses,
            average_career_progress=round(average_career_progress, 2),
        )

    def get_department_metrics(self) -> List[AnalyticsDepartment]:
        employees = self.employee_repo.list_with_department()
        if not employees:
            return []

        goal_progress_map = {
            row["employee_id"]: float(row["average_progress"])
            for row in self.goal_repo.get_average_progress_by_employee()
            if row["average_progress"] is not None
        }
        max_points = self.employee_repo.get_max_points()
        department_totals: dict[str, dict[str, Optional[float]]] = {}

        for employee in employees:
            department_id = employee["department_id"]
            department_name = employee.get("department_name") or "Unknown"
            goal_progress = goal_progress_map.get(employee["id"], 0.0)
            normalized_points = (
                (float(employee["points_current"]) / float(max_points)) * 100
                if max_points
                else 0.0
            )
            performance_score = 0.5 * goal_progress + 0.5 * normalized_points

            if department_id not in department_totals:
                department_totals[department_id] = {
                    "department_name": department_name,
                    "employee_count": 0,
                    "performance_sum": 0.0,
                }

            department_totals[department_id]["employee_count"] += 1
            department_totals[department_id]["performance_sum"] += performance_score

        department_metrics: List[AnalyticsDepartment] = []
        for dept_id, values in department_totals.items():
            employee_count = values["employee_count"] or 0
            avg_performance = (
                values["performance_sum"] / employee_count if employee_count else 0.0
            )
            department_metrics.append(
                AnalyticsDepartment(
                    department_id=dept_id or "UNKNOWN",
                    department_name=values["department_name"] or "Unknown",
                    employee_count=employee_count,
                    average_performance=round(avg_performance, 2),
                )
            )

        department_metrics.sort(key=lambda dept: dept.department_name)
        return department_metrics

    def get_employee_metrics(self) -> List[AnalyticsEmployee]:
        employees = self.employee_repo.list_with_department()
        if not employees:
            return []

        goal_progress_map = {
            row["employee_id"]: float(row["average_progress"])
            for row in self.goal_repo.get_average_progress_by_employee()
            if row["average_progress"] is not None
        }
        course_stats_map = {
            row["employee_id"]: row
            for row in self.enrollment_repo.get_employee_course_stats()
        }

        employee_metrics: List[AnalyticsEmployee] = []
        for employee in employees:
            stats = course_stats_map.get(employee["id"], {})
            employee_metrics.append(
                AnalyticsEmployee(
                    id=employee["id"],
                    name=employee["name"],
                    role=employee["role"],
                    department=employee.get("department_name") or "Unknown",
                    courses_completed=int(stats.get("courses_completed", 0) or 0),
                    courses_in_progress=int(stats.get("courses_in_progress", 0) or 0),
                    career_progress_percent=round(
                        goal_progress_map.get(employee["id"], 0.0), 2
                    ),
                    points=int(employee.get("points_current", 0) or 0),
                )
            )

        employee_metrics.sort(key=lambda emp: emp.name)
        return employee_metrics
