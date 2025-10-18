"""
GoalRepository: Data access for goals table.
"""
from .base import BaseRepository
from typing import Optional, List


class GoalRepository(BaseRepository):
    TABLE = "goals"
    ID_FIELD = "id"

    def get_goal(self, goal_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, goal_id)

    def list_goals(self) -> List[dict]:
        return self.list_all(self.TABLE)

    def get_average_progress_by_employee(self) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT 
                employee_id,
                AVG(progress_percent) AS average_progress
            FROM goals
            GROUP BY employee_id
            """
        )
        return [dict(row) for row in cur.fetchall()]
