"""
WellbeingMessageRepository: Data access for wellbeing_messages table.
"""
from .base import BaseRepository
from typing import Optional, List

class WellbeingMessageRepository(BaseRepository):
    TABLE = "wellbeing_messages"
    ID_FIELD = "id"

    def get_message(self, message_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, message_id)

    def list_messages(self) -> List[dict]:
        return self.list_all(self.TABLE)
