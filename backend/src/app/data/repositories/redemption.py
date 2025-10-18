"""
RedemptionRepository: Data access for redemptions table.
"""
from .base import BaseRepository
from typing import Optional, List

class RedemptionRepository(BaseRepository):
    TABLE = "redemptions"
    ID_FIELD = "id"

    def get_redemption(self, redemption_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, redemption_id)

    def list_redemptions(self) -> List[dict]:
        return self.list_all(self.TABLE)
