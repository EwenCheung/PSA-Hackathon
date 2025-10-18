"""
MentorshipService: Business logic for mentorship domain.
"""
import json
from app.data.repositories.mentorship_profile import MentorshipProfileRepository
from app.data.repositories.mentorship_match import MentorshipMatchRepository
from app.data.repositories.mentor_session import MentorSessionRepository
from app.data.repositories.employee import EmployeeRepository
from app.models.pydantic_schemas import MentorshipProfileDetail, MentorshipMatchDetail
from app.core.db import get_connection
from typing import List, Dict, Optional

class MentoringService:
    def __init__(self, employee_repo=None, mentor_repo=None):
        """Initialize with optional repos (for testing)"""
        if employee_repo and mentor_repo:
            self.employee_repo = employee_repo
            self.mentor_repo = mentor_repo
        else:
            conn = get_connection()
            self.employee_repo = EmployeeRepository(conn)
            self.mentor_repo = MentorshipProfileRepository(conn)
    
    def calculate_match_score(self, mentee: Dict, mentor: Dict) -> float:
        """
        Calculate match score between mentee and mentor.
        
        Weighted scoring:
        - Skill Alignment: 40%
        - Experience Gap: 30%
        - Department Relevance: 15%
        - Availability & Rating: 15%
        """
        # Skill alignment (40%)
        skill_score = self._calculate_skill_score(
            mentee.get('desired_skills', []),
            mentor.get('skills_map', '{}')
        )
        
        # Experience gap (30%)
        experience_score = self._calculate_experience_score(
            mentee.get('level', 'Junior'),
            mentor.get('level', 'Senior')
        )
        
        # Department relevance (15%)
        dept_score = self._calculate_department_score(
            mentee.get('department_id'),
            mentor.get('department_id')
        )
        
        # Availability & rating (15%)
        availability_score = self._calculate_availability_score(mentor)
        
        # Weighted total
        total = (
            skill_score * 0.4 +
            experience_score * 0.3 +
            dept_score * 0.15 +
            availability_score * 0.15
        )
        
        return min(total, 100.0)
    
    def _calculate_skill_score(self, desired_skills: List[str], mentor_skills_map: str) -> float:
        """Calculate skill alignment score"""
        if not desired_skills:
            return 50.0
        
        mentor_skills = json.loads(mentor_skills_map) if mentor_skills_map else {}
        mentor_skill_ids = set(mentor_skills.keys())
        
        exact_matches = len(set(desired_skills) & mentor_skill_ids)
        score = exact_matches * 15
        return min(score, 100.0)
    
    def _calculate_experience_score(self, mentee_level: str, mentor_level: str) -> float:
        """Calculate experience gap score"""
        level_values = {'Junior': 1, 'Mid': 2, 'Senior': 3, 'Lead': 4}
        
        mentee_val = level_values.get(mentee_level, 1)
        mentor_val = level_values.get(mentor_level, 3)
        
        gap = mentor_val - mentee_val
        
        if gap >= 2:
            return 100.0
        elif gap == 1:
            return 80.0
        else:
            return 50.0
    
    def _calculate_department_score(self, mentee_dept: Optional[str], mentor_dept: Optional[str]) -> float:
        """Calculate department relevance score"""
        if not mentee_dept or not mentor_dept:
            return 70.0
        
        if mentee_dept == mentor_dept:
            return 70.0
        else:
            return 100.0  # Cross-dept bonus
    
    def _calculate_availability_score(self, mentor: Dict) -> float:
        """Calculate availability and rating score"""
        rating = mentor.get('rating', 0.0)
        mentees_count = mentor.get('mentees_count', 0)
        capacity = mentor.get('capacity', 3)
        
        if mentees_count >= capacity:
            return 0.0
        
        capacity_pct = mentees_count / capacity if capacity > 0 else 1.0
        capacity_score = (1 - capacity_pct) * 50
        rating_score = (rating / 5.0) * 50
        
        return capacity_score + rating_score
    
    def recommend_mentors(
        self,
        employee_id: str,
        career_goals: List[str],
        desired_skills: List[str],
        max_results: int = 5
    ) -> List[Dict]:
        """Recommend mentors for an employee"""
        mentee = self.employee_repo.get_employee(employee_id)
        if not mentee:
            return []
        
        mentors = self.mentor_repo.get_available_mentors()
        
        recommendations = []
        for mentor in mentors:
            mentee_profile = {
                'desired_skills': desired_skills,
                'level': mentee.get('level'),
                'department_id': mentee.get('department_id')
            }
            
            score = self.calculate_match_score(mentee_profile, mentor)
            
            reasons = self._generate_match_reasons(mentee_profile, mentor, score)
            
            recommendations.append({
                'mentor_id': mentor['employee_id'],
                'mentor_name': mentor.get('name', 'Unknown'),
                'mentee_id': employee_id,
                'mentee_name': mentee.get('name', 'Unknown'),
                'match_score': round(score, 1),
                'reasons': reasons,
                'focus_areas': desired_skills[:3]
            })
        
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:max_results]
    
    def _generate_match_reasons(self, mentee: Dict, mentor: Dict, score: float) -> List[str]:
        """Generate human-readable reasons for the match"""
        reasons = []
        
        desired_skills = mentee.get('desired_skills', [])
        mentor_skills = json.loads(mentor.get('skills_map', '{}'))
        matching_skills = set(desired_skills) & set(mentor_skills.keys())
        
        if matching_skills:
            reasons.append(f"Expertise in {len(matching_skills)} desired skills")
        
        rating = mentor.get('rating', 0)
        if rating >= 4.5:
            reasons.append(f"High rating: {rating}★")
        
        capacity = mentor.get('capacity', 0)
        current = mentor.get('mentees_count', 0)
        if current < capacity:
            reasons.append(f"Available ({current}/{capacity} mentees)")
        
        return reasons if reasons else ["General mentoring available"]


# Legacy class for backward compatibility
class MentorshipService(MentoringService):
    def __init__(self):
        conn = get_connection()
        super().__init__(
            employee_repo=EmployeeRepository(conn),
            mentor_repo=MentorshipProfileRepository(conn)
        )
        self.profile_repo = self.mentor_repo
        self.match_repo = MentorshipMatchRepository(conn)
        self.session_repo = MentorSessionRepository(conn)

    def get_available_mentors(self, available_only: bool = True) -> List[MentorshipProfileDetail]:
        profiles = self.profile_repo.list_profiles()
        filtered = [MentorshipProfileDetail(**p) for p in profiles if not available_only or p.get("capacity", 0) > p.get("mentees_count", 0)]
        return filtered

    def get_mentee_candidates(self) -> List[dict]:
        employees = self.employee_repo.list_employees()
        return [e for e in employees if e.get("role") == "mentee"]

    def generate_match_suggestions(self, limit: int = 5) -> List[MentorshipMatchDetail]:
        matches = self.match_repo.list_matches()[:limit]
        return [MentorshipMatchDetail(**m) for m in matches]

    def confirm_match(self, match_id: int) -> MentorshipMatchDetail:
        self.match_repo.update(self.match_repo.TABLE, self.match_repo.ID_FIELD, match_id, {"status": "confirmed"})
        match = self.match_repo.get_match(match_id)
        return MentorshipMatchDetail(**match)

    def record_session(self, mentor_id: str, mentee_id: str, session_data: dict) -> dict:
        session_data["mentor_id"] = mentor_id
        session_data["mentee_id"] = mentee_id
        session_id = self.session_repo.create(self.session_repo.TABLE, session_data)
        return self.session_repo.get_session(session_id)

    def award_mentor_points(self, mentor_id: str, points: int) -> dict:
        return {"mentor_id": mentor_id, "points": points}
