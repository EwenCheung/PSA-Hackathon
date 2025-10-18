"""
LeadershipPotentialPredictionRepository: Data access for leadership_potential_predictions table.
"""
from .base import BaseRepository
from typing import Optional, List

class LeadershipPotentialPredictionRepository(BaseRepository):
    TABLE = "leadership_potential_predictions"
    ID_FIELD = "id"

    def get_prediction(self, prediction_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, prediction_id)

    def list_predictions(self) -> List[dict]:
        return self.list_all(self.TABLE)
