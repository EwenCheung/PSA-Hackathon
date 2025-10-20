# repositories/marketplace_item.py
from .base import BaseRepository
from typing import Optional, List, Dict, Any

class MarketplaceItemRepository(BaseRepository):
    TABLE = "marketplace_items"
    ID_FIELD = "id"

    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, item_id)

    def list_items(self) -> List[Dict[str, Any]]:
        return self.list_all(self.TABLE)

    def sync_from_json(self, json_file: str):
        """Sync marketplace items from JSON file into SQLite."""
        import sqlite3, json
        from pathlib import Path

        json_path = Path(json_file)
        if not json_path.exists():
            print(f"Warning: {json_file} does not exist.")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        cur = self.conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {self.TABLE}")
        cur.execute(f"""
            CREATE TABLE {self.TABLE} (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                points INTEGER,
                category TEXT,
                in_stock INTEGER DEFAULT 1
            )
        """)
        self.conn.commit()

        insert_data = [
            (i["id"], i["name"], i["description"], i["points"], i["category"], 1)
            for i in items
        ]
        cur.executemany(f"INSERT INTO {self.TABLE} VALUES (?, ?, ?, ?, ?, ?)", insert_data)
        self.conn.commit()
        print(f"Synced {len(insert_data)} marketplace items.")
