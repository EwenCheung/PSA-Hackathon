"""
EnrollmentRepository: Data access for enrollments table.
"""
from .base import BaseRepository
from typing import List


class EnrollmentRepository(BaseRepository):
    TABLE = "enrollments"

    def list_enrollments(self) -> List[dict]:
        return self.list_all(self.TABLE)

    def count_completed_courses(self) -> int:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT COUNT(*) AS total_completed
            FROM enrollments
            WHERE status = 'completed'
            """
        )
        row = cur.fetchone()
        return row["total_completed"] if row else 0

    def get_employee_course_stats(self) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT 
                employee_id,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS courses_completed,
                SUM(CASE WHEN status = 'in-progress' THEN 1 ELSE 0 END) AS courses_in_progress,
                AVG(progress_percent) AS average_course_progress
            FROM enrollments
            GROUP BY employee_id
            """
        )
        return [dict(row) for row in cur.fetchall()]
