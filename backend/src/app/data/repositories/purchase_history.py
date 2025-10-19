# repositories/purchase_history.py
import sqlite3, json
from pathlib import Path
from typing import List, Dict, Any, Optional

JSON_FILE = Path(__file__).parent.parent / "seeds" / "purchase_history.json"

class PurchaseHistoryRepository:
    TABLE = "purchase_history"
    ID_FIELD = "id"

    def __init__(self, conn: sqlite3.Connection, auto_sync: bool = True):
        self.conn = conn
        self.conn.row_factory = sqlite3.Row
        if auto_sync:
            self.sync_from_json()

    def sync_from_json(self):
        if not JSON_FILE.exists():
            print(f"Warning: {JSON_FILE} does not exist.")
            return

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        cur = self.conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {self.TABLE}")
        cur.execute(f"""
            CREATE TABLE {self.TABLE} (
                id TEXT PRIMARY KEY,
                points INTEGER DEFAULT 0,
                bought_items TEXT DEFAULT '[]'
            )
        """)
        self.conn.commit()

        insert_data = [
            (emp["id"], emp.get("points", 0), json.dumps(emp.get("bought_items", [])))
            for emp in data
        ]
        cur.executemany(f"INSERT INTO {self.TABLE} VALUES (?, ?, ?)", insert_data)
        self.conn.commit()
        print(f"Synced {len(insert_data)} employees into purchase_history.")

    # Redeem marketplace item
    def redeem_item(self, employee_id: str, item: Dict[str, Any]) -> bool:
        """Deduct points and record purchased item if enough points."""
        points = self.get_points(employee_id)
        if points < item["points"]:
            return False

        # Deduct points
        cur = self.conn.cursor()
        cur.execute(
            f"UPDATE {self.TABLE} SET points = points - ? WHERE {self.ID_FIELD} = ?",
            (item["points"], employee_id)
        )

        # Add item to bought_items
        bought_items = self.get_bought_items(employee_id)
        bought_items.append(item["name"])
        cur.execute(
            f"UPDATE {self.TABLE} SET bought_items = ? WHERE {self.ID_FIELD} = ?",
            (json.dumps(bought_items), employee_id)
        )
        self.conn.commit()
        return True

    def get_points(self, employee_id: str) -> int:
        cur = self.conn.cursor()
        cur.execute(f"SELECT points FROM {self.TABLE} WHERE id = ?", (employee_id,))
        row = cur.fetchone()
        return row["points"] if row else 0

    def get_bought_items(self, employee_id: str) -> List[str]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT bought_items FROM {self.TABLE} WHERE id = ?", (employee_id,))
        row = cur.fetchone()
        return json.loads(row["bought_items"]) if row else []

    def list_all(self) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.TABLE}")
        return [
            dict(row, bought_items=json.loads(row["bought_items"]))
            for row in cur.fetchall()
        ]
