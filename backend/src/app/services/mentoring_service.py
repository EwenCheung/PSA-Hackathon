"""Mentoring service for matching mentors with mentees."""
import json
from typing import List, Dict, Optional
from app.data.repositories.employee import EmployeeRepository
from app.data.repositories.mentorship_profile import MentorshipProfileRepository


class MentoringService:
    """Service layer for mentoring operations with matching algorithm."""
    
    def __init__(
        self,
        employee_repo: EmployeeRepository,
        mentor_profile_repo: MentorshipProfileRepository
    ):
        self.employee_repo = employee_repo
        self.mentor_profile_repo = mentor_profile_repo
    
    def calculate_match_score(
        self,
        mentor_id: str,
        mentee_id: str,
        desired_skills: List[str]
    ) -> float:
        """
        Calculate match score between mentor and mentee.
        
        Weighted scoring algorithm:
        - Skill alignment: 40% (overlap between mentor expertise and desired skills)
        - Experience gap: 30% (appropriate experience level difference)
        - Department alignment: 15% (same department bonus)
        - Availability: 15% (mentor has capacity)
        
        Args:
            mentor_id: Mentor employee ID
            mentee_id: Mentee employee ID
            desired_skills: Skills mentee wants to learn
        
        Returns:
            Match score from 0-100
        """
        mentor = self.employee_repo.get_employee(mentor_id)
        mentee = self.employee_repo.get_employee(mentee_id)
        mentor_profile = self.mentor_profile_repo.get_profile(mentor_id)
        
        if not mentor or not mentee or not mentor_profile:
            return 0.0
        
        # Parse skills
        mentor_skills = json.loads(mentor.get('skills_map', '{}'))
        mentee_skills = json.loads(mentee.get('skills_map', '{}'))
        
        # 1. Skill alignment score (40%)
        skill_overlap = len(set(desired_skills) & set(mentor_skills.keys()))
        skill_score = (skill_overlap / len(desired_skills)) * 40 if desired_skills else 0
        
        # 2. Experience gap score (30%)
        # Ideal gap is 2-3 levels (Junior->Senior, Mid->Principal)
        level_map = {'Junior': 1, 'Mid': 2, 'Senior': 3, 'Principal': 4}
        mentor_level = level_map.get(mentor.get('level', 'Mid'), 2)
        mentee_level = level_map.get(mentee.get('level', 'Junior'), 1)
        gap = mentor_level - mentee_level
        
        if gap >= 2:
            experience_score = 30.0
        elif gap == 1:
            experience_score = 20.0
        else:
            experience_score = 10.0
        
        # 3. Department alignment score (15%)
        dept_score = 15.0 if mentor.get('department_id') == mentee.get('department_id') else 0.0
        
        # 4. Availability score (15%)
        current_mentees = mentor_profile.get('mentees_count', 0)
        capacity = mentor_profile.get('capacity', 0)
        
        if current_mentees < capacity:
            availability_score = 15.0
        else:
            availability_score = 0.0
        
        total_score = skill_score + experience_score + dept_score + availability_score
        return round(total_score, 2)
    
    def recommend_mentors(
        self,
        employee_id: str,
        career_goals: List[str],
        desired_skills: List[str],
        max_results: int = 5
    ) -> List[Dict]:
        """
        Recommend top mentors for an employee.
        
        Args:
            employee_id: Mentee employee ID
            career_goals: Career aspirations
            desired_skills: Skills to develop
            max_results: Maximum recommendations
        
        Returns:
            List of mentor recommendations with scores and reasons
        """
        if not desired_skills:
            return []
        
        # Get all available mentors
        available_mentors = self.mentor_profile_repo.get_available_mentors()
        
        # Calculate scores for each mentor
        recommendations = []
        for mentor in available_mentors:
            mentor_id = mentor['employee_id']
            score = self.calculate_match_score(mentor_id, employee_id, desired_skills)
            
            if score > 0:
                mentor_emp = self.employee_repo.get_employee(mentor_id)
                mentor_skills = json.loads(mentor_emp.get('skills_map', '{}')) if mentor_emp else {}
                
                # Generate match reasons
                reasons = []
                skill_overlap = set(desired_skills) & set(mentor_skills.keys())
                if skill_overlap:
                    reasons.append(f"Expert in {len(skill_overlap)} of your desired skills")
                
                if mentor.get('rating', 0) >= 4.5:
                    reasons.append(f"Highly rated mentor ({mentor.get('rating', 0)}/5)")
                
                if mentor_emp and mentor_emp.get('department_id') == self.employee_repo.get_employee(employee_id).get('department_id'):
                    reasons.append("Same department - understands your context")
                
                recommendations.append({
                    'mentor_id': mentor_id,
                    'mentor_name': mentor_emp.get('name', 'Unknown') if mentor_emp else 'Unknown',
                    'match_score': score,
                    'reasons': reasons,
                    'focus_areas': list(skill_overlap)
                })
        
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:max_results]
