"""
EmployeeService: Business logic for employee domain.
"""
from app.data.repositories.employee import EmployeeRepository
from app.data.repositories.goal import GoalRepository
from app.models.pydantic_schemas import EmployeeDetail, GoalDetail
from app.core.db import get_connection
from typing import List

class EmployeeService:
    def __init__(self):
        conn = get_connection()
        self.employee_repo = EmployeeRepository(conn)
        self.goal_repo = GoalRepository(conn)

    def get_employee_profile(self, employee_id: str) -> EmployeeDetail:
        employee = self.employee_repo.get_employee(employee_id)
        if not employee:
            raise ValueError(f"Employee {employee_id} not found")
        return EmployeeDetail(**employee)

    def get_employee_goals(self, employee_id: str) -> List[GoalDetail]:
        goals = self.goal_repo.list_goals()
        # Filter by employee_id
        filtered = [GoalDetail(**g) for g in goals if g.get("employee_id") == employee_id]
        return filtered

    def create_goal(self, employee_id: str, goal_data: dict) -> GoalDetail:
        goal_data["employee_id"] = employee_id
        goal_id = self.goal_repo.create(self.goal_repo.TABLE, goal_data)
        goal = self.goal_repo.get_goal(goal_id)
        return GoalDetail(**goal)

    def update_goal_progress(self, goal_id: int, progress: int) -> GoalDetail:
        self.goal_repo.update(self.goal_repo.TABLE, self.goal_repo.ID_FIELD, goal_id, {"progress_percent": progress})
        goal = self.goal_repo.get_goal(goal_id)
        return GoalDetail(**goal)

    def get_employee_points(self, employee_id: str) -> int:
        employee = self.employee_repo.get_employee(employee_id)
        if not employee:
            raise ValueError(f"Employee {employee_id} not found")
        return employee.get("points_current", 0)

    def validate_employee_exists(self, employee_id: str) -> bool:
        return self.employee_repo.get_employee(employee_id) is not None
