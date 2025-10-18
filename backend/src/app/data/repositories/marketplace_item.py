"""
MarketplaceItemRepository: Data access for marketplace_items table.
"""
from .base import BaseRepository
from typing import Optional, List

class MarketplaceItemRepository(BaseRepository):
    TABLE = "marketplace_items"
    ID_FIELD = "id"

    def get_item(self, item_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, item_id)

    def list_items(self) -> List[dict]:
        return self.list_all(self.TABLE)
