"""
MentorshipProfileRepository: Data access for mentorship_profiles table.
"""
from .base import BaseRepository
from typing import Optional, List

class MentorshipProfileRepository(BaseRepository):
    TABLE = "mentorship_profiles"
    ID_FIELD = "employee_id"

    def get_profile(self, employee_id: str) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, employee_id)

    def list_profiles(self) -> List[dict]:
        return self.list_all(self.TABLE)
    
    def get_available_mentors(
        self,
        skill_area: Optional[str] = None,
        department: Optional[str] = None,
        min_rating: float = 0.0
    ) -> List[dict]:
        """
        Get available mentors matching specified criteria.
        
        Args:
            skill_area: Filter by specific skill ID in employee skills_map
            department: Filter by department ID
            min_rating: Minimum mentor rating required
        
        Returns:
            List of mentor profiles with employee details
        """
        cur = self.conn.cursor()
        
        query = """
            SELECT 
                mp.*,
                e.name,
                e.role,
                e.department_id,
                e.level,
                e.position_level,
                e.skills_map,
                e.hire_date
            FROM mentorship_profiles mp
            JOIN employees e ON mp.employee_id = e.id
            WHERE mp.is_mentor = 1
              AND mp.mentees_count < mp.capacity
              AND mp.rating >= ?
        """
        
        params = [min_rating]
        
        if department:
            query += " AND e.department_id = ?"
            params.append(department)
        
        if skill_area:
            query += " AND e.skills_map LIKE ?"
            params.append(f'%"{skill_area}"%')
        
        query += " ORDER BY mp.rating DESC"
        
        cur.execute(query, params)
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    
    def get_mentor_statistics(self, mentor_id: str) -> Optional[dict]:
        """
        Get statistics for a specific mentor.
        
        Args:
            mentor_id: The mentor's employee ID
        
        Returns:
            Dictionary with capacity, mentees_count, rating, or None if not found
        """
        return self.get_profile(mentor_id)

    def increment_mentees_count(self, mentor_id: str, delta: int = 1) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE mentorship_profiles
            SET mentees_count = mentees_count + ?
            WHERE employee_id = ?
            """,
            (delta, mentor_id),
        )
        self.conn.commit()
