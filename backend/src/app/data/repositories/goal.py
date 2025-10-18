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
