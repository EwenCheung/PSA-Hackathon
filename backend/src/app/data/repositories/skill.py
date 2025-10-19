"""
SkillRepository: Data access and management for skills table.
"""
from typing import Optional, List, Dict
from .base import BaseRepository

class SkillRepository(BaseRepository):
    TABLE = "skills"
    ID_FIELD = "id"

    def get_skill(self, skill_id: str) -> Optional[dict]:
        """Retrieve a skill by its ID."""
        return self.get_by_id(self.TABLE, self.ID_FIELD, skill_id)

    def list_skills(self) -> List[dict]:
        """Return all skills."""
        return self.list_all(self.TABLE)

    def list_by_category(self, category: str) -> List[dict]:
        """List skills filtered by category."""
        query = f"SELECT * FROM {self.TABLE} WHERE category = ?"
        return self.fetchall(query, (category,))

    def search_skills(self, keyword: str) -> List[dict]:
        """Search skills by keyword in skill name."""
        query = f"SELECT * FROM {self.TABLE} WHERE name LIKE ?"
        return self.fetchall(query, (f"%{keyword}%",))

    def add_skill(self, skill: Dict[str, str]) -> None:
        """Insert a new skill record."""
        query = f"INSERT INTO {self.TABLE} (id, name, category) VALUES (?, ?, ?)"
        self.execute(query, (skill["id"], skill["name"], skill["category"]))

    def bulk_insert(self, skills: List[Dict[str, str]]) -> None:
        """Batch insert multiple skills (used for seeding from skills.json)."""
        query = f"INSERT INTO {self.TABLE} (id, name, category) VALUES (?, ?, ?)"
        data = [(s["id"], s["name"], s["category"]) for s in skills]
        self.executemany(query, data)

    def delete_skill(self, skill_id: str) -> None:
        """Delete a skill by ID."""
        query = f"DELETE FROM {self.TABLE} WHERE {self.ID_FIELD} = ?"
        self.execute(query, (skill_id,))
