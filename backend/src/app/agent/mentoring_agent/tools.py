"""Tools for the Mentoring Agent with LangChain integration."""
import json
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from langchain.tools import tool
from app.core.db import get_connection
from app.data.repositories.employee import EmployeeRepository
from app.data.repositories.mentorship_profile import MentorshipProfileRepository
from app.services.mentoring_service import MentoringService


class MentorProfile(BaseModel):
    """Schema for mentor profile data"""
    employee_id: str = Field(description="Unique employee identifier")
    name: str = Field(description="Mentor's full name")
    role: str = Field(description="Current job title")
    department: str = Field(description="Department/unit")
    expertise: List[str] = Field(description="Areas of expertise and skills")
    years_experience: int = Field(description="Years of professional experience")
    mentees_current: int = Field(description="Current number of mentees")
    mentees_capacity: int = Field(description="Maximum mentees they can handle")
    rating: float = Field(description="Mentor rating (0-5)")
    total_mentees_helped: int = Field(description="Total mentees mentored over time")
    available: bool = Field(description="Currently accepting new mentees")


class MenteeProfile(BaseModel):
    """Schema for mentee profile data"""
    employee_id: str = Field(description="Unique employee identifier")
    name: str = Field(description="Employee's full name")
    role: str = Field(description="Current job title")
    department: str = Field(description="Department/unit")
    current_skills: List[str] = Field(description="Current skills and competencies")
    career_goals: List[str] = Field(description="Career aspirations and goals")
    desired_skills: List[str] = Field(description="Skills they want to develop")
    years_experience: int = Field(description="Years of professional experience")


class MentorshipMatch(BaseModel):
    """Schema for a mentor-mentee match recommendation"""
    mentor_id: str = Field(description="Mentor's employee ID")
    mentor_name: str = Field(description="Mentor's name")
    mentee_id: str = Field(description="Mentee's employee ID")
    mentee_name: str = Field(description="Mentee's name")
    match_score: float = Field(description="Match quality score (0-100)")
    reasons: List[str] = Field(description="Specific reasons for the match")
    focus_areas: List[str] = Field(description="Recommended focus areas for mentorship")


class MentorshipPair(BaseModel):
    """Schema for an active mentorship pair"""
    pair_id: str = Field(description="Unique pair identifier")
    mentor_id: str = Field(description="Mentor's employee ID")
    mentee_id: str = Field(description="Mentee's employee ID")
    start_date: str = Field(description="Mentorship start date (YYYY-MM-DD)")
    focus_areas: List[str] = Field(description="Current focus areas")
    status: str = Field(description="active, paused, or completed")
    progress: int = Field(description="Progress percentage (0-100)")
    sessions_completed: int = Field(description="Number of mentoring sessions held")
    next_meeting: Optional[str] = Field(description="Next scheduled meeting date")


@tool
def find_available_mentors(
    skill_area: Optional[str] = None,
    department: Optional[str] = None,
    min_rating: float = 0.0
) -> List[Dict]:
    """
    Find available mentors matching specified criteria.
    
    Use this tool when employees want to search for mentors by skill, department, or rating.
    Returns mentors who are currently available (not at full capacity).
    
    Args:
        skill_area: Filter by specific skill or expertise area (e.g., 'Python', 'Leadership')
        department: Filter by department ID (e.g., 'DEPT001')
        min_rating: Minimum mentor rating required (0.0-5.0)
    
    Returns:
        List of mentor profiles matching the criteria with availability status
    """
    conn = get_connection()
    mentor_repo = MentorshipProfileRepository(conn)
    
    mentors = mentor_repo.get_available_mentors(
        skill_area=skill_area,
        department=department,
        min_rating=min_rating
    )
    
    # Transform to simpler dict format
    result = []
    for mentor in mentors:
        result.append({
            'employee_id': mentor['employee_id'],
            'name': mentor.get('name', 'Unknown'),
            'role': mentor.get('role', ''),
            'department': mentor.get('department_id', ''),
            'rating': mentor.get('rating', 0.0),
            'capacity': mentor.get('capacity', 0),
            'current_mentees': mentor.get('mentees_count', 0),
            'available': mentor.get('mentees_count', 0) < mentor.get('capacity', 0)
        })
    
    return result


@tool
def get_mentor_profile(employee_id: str) -> Optional[Dict]:
    """
    Retrieve detailed profile for a specific mentor.
    
    Use this tool to get complete information about a mentor including their expertise,
    rating, capacity, and current mentees.
    
    Args:
        employee_id: The mentor's employee ID (e.g., 'EMP001')
    
    Returns:
        Mentor profile dictionary if found, None otherwise
    """
    if not employee_id:
        return None
    
    conn = get_connection()
    mentor_repo = MentorshipProfileRepository(conn)
    employee_repo = EmployeeRepository(conn)
    
    mentor_profile = mentor_repo.get_profile(employee_id)
    if not mentor_profile:
        return None
    
    employee = employee_repo.get_employee(employee_id)
    
    # Combine mentor and employee data
    return {
        'employee_id': employee_id,
        'name': employee.get('name', 'Unknown') if employee else 'Unknown',
        'role': employee.get('role', '') if employee else '',
        'department': employee.get('department_id', '') if employee else '',
        'rating': mentor_profile.get('rating', 0.0),
        'capacity': mentor_profile.get('capacity', 0),
        'current_mentees': mentor_profile.get('mentees_count', 0),
        'available': mentor_profile.get('mentees_count', 0) < mentor_profile.get('capacity', 0),
        'personality': mentor_profile.get('personality', '')
    }


@tool
def get_mentee_profile(employee_id: str) -> Optional[Dict]:
    """
    Retrieve detailed profile for a specific mentee/employee.
    
    Use this tool to get employee information including their skills, goals, and career level.
    
    Args:
        employee_id: The employee's ID (e.g., 'EMP003')
    
    Returns:
        Mentee profile dictionary if found, None otherwise
    """
    if not employee_id:
        return None
    
    conn = get_connection()
    employee_repo = EmployeeRepository(conn)
    
    employee = employee_repo.get_employee(employee_id)
    if not employee:
        return None
    
    # Parse JSON fields
    skills_map = json.loads(employee.get('skills_map', '{}')) if employee.get('skills_map') else {}
    goals = json.loads(employee.get('goals_set', '[]')) if employee.get('goals_set') else []
    
    return {
        'employee_id': employee_id,
        'name': employee.get('name', 'Unknown'),
        'role': employee.get('role', ''),
        'department': employee.get('department_id', ''),
        'level': employee.get('level', 'Junior'),
        'current_skills': list(skills_map.keys()),
        'career_goals': goals
    }


@tool
def recommend_mentors(
    employee_id: str,
    career_goals: List[str],
    desired_skills: List[str],
    max_results: int = 5
) -> List[Dict]:
    """
    Recommend mentors for an employee based on their goals and desired skills.
    
    Use this tool when employees need personalized mentor recommendations. 
    Returns top matches ranked by compatibility score with detailed reasoning.
    
    Args:
        employee_id: The mentee's employee ID (e.g., 'EMP003')
        career_goals: List of career aspirations (e.g., ['Technical Leadership', 'System Design'])
        desired_skills: Skills the employee wants to develop (e.g., ['SKILL001', 'SKILL009'])
        max_results: Maximum number of recommendations to return (default: 5)
    
    Returns:
        List of mentor recommendations with match scores, reasons, and focus areas
    """
    if not employee_id or not desired_skills:
        return []
    
    conn = get_connection()
    employee_repo = EmployeeRepository(conn)
    mentor_repo = MentorshipProfileRepository(conn)
    service = MentoringService(employee_repo, mentor_repo)
    
    recommendations = service.recommend_mentors(
        employee_id=employee_id,
        career_goals=career_goals,
        desired_skills=desired_skills,
        max_results=max_results
    )
    
    return recommendations


@tool
def analyze_mentorship_progress(pair_id: str) -> Dict:
    """
    Analyze the progress and health of a mentorship relationship.
    
    Use this tool to check if a mentorship pair is on track, identify issues,
    and get recommendations for intervention.
    
    Args:
        pair_id: The mentorship pair ID (e.g., 'PAIR_001')
    
    Returns:
        Dictionary with progress score, engagement level, alerts, and recommendations
    """
    if not pair_id:
        return {
            "progress_score": 0,
            "engagement_level": "unknown",
            "sessions_on_track": False,
            "recommendations": ["Invalid pair ID provided"]
        }
    
    # TODO: Implement with mentor_sessions repository
    # For now, return placeholder analysis
    return {
        "progress_score": 75,
        "engagement_level": "medium",
        "sessions_on_track": True,
        "recommendations": ["Continue bi-weekly meetings", "Review goal progress next session"]
    }


@tool
def get_mentorship_statistics(department: Optional[str] = None) -> Dict:
    """
    Get organization-wide mentorship program statistics.
    
    Use this tool for employer dashboards to show program health metrics,
    active pairs, available mentors, and completion rates.
    
    Args:
        department: Optional filter by department ID (e.g., 'DEPT001')
    
    Returns:
        Dictionary with total active pairs, available mentors, average scores, and trends
    """
    conn = get_connection()
    mentor_repo = MentorshipProfileRepository(conn)
    
    # Get all mentors
    all_mentors = mentor_repo.list_profiles()
    
    if department:
        # Filter would require join with employees - simplified for now
        mentors = [m for m in all_mentors if m.get('is_mentor') == 1]
    else:
        mentors = [m for m in all_mentors if m.get('is_mentor') == 1]
    
    # Calculate statistics
    total_mentors = len(mentors)
    available_mentors = len([m for m in mentors if m.get('mentees_count', 0) < m.get('capacity', 0)])
    total_active_pairs = sum(m.get('mentees_count', 0) for m in mentors)
    avg_rating = sum(m.get('rating', 0.0) for m in mentors) / total_mentors if total_mentors > 0 else 0.0
    
    return {
        "total_active_pairs": total_active_pairs,
        "total_mentors": total_mentors,
        "available_mentors": available_mentors,
        "total_mentees_seeking": 0,  # Would need mentorship_matches table
        "average_rating": round(avg_rating, 2),
        "completion_rate": 85.0,  # Placeholder
        "underserved_skills": []  # Would need skill gap analysis
    }


@tool
def validate_mentorship_goals(goals: List[str], employee_profile: Dict) -> Dict:
    """
    Validate and provide feedback on mentorship goals.
    
    Use this tool to check if an employee's mentorship goals are specific,
    measurable, and appropriate. Provides suggestions for improvement.
    
    Args:
        goals: List of proposed mentorship goals
        employee_profile: Employee's profile data including role and level
    
    Returns:
        Dictionary with validation status, feedback, and suggested improvements
    """
    if not goals:
        return {
            "valid": False,
            "feedback": ["No goals provided"],
            "suggested_goals": ["Define specific skills to develop", "Set measurable objectives"]
        }
    
    feedback = []
    valid = True
    
    # Check for vague goals
    vague_terms = ['learn', 'improve', 'better', 'understand']
    for goal in goals:
        goal_lower = goal.lower()
        if any(term in goal_lower for term in vague_terms) and len(goal.split()) < 4:
            feedback.append(f"Goal '{goal}' is too vague - be more specific")
            valid = False
    
    # Check for measurable criteria
    measurable_terms = ['certification', 'project', 'proficiency', 'master', 'build']
    has_measurable = any(any(term in goal.lower() for term in measurable_terms) for goal in goals)
    
    if not has_measurable:
        feedback.append("Consider adding measurable outcomes (e.g., 'Earn AWS certification', 'Build portfolio project')")
    
    if valid and feedback == []:
        feedback = ["✓ Goals are specific and measurable", "✓ Well-defined objectives"]
    
    return {
        "valid": valid and len(feedback) < 2,
        "feedback": feedback,
        "suggested_goals": [
            "Master [specific technology] for [specific use case]",
            "Complete [certification/project] by [timeframe]",
            "Develop [skill] to [proficiency level]"
        ] if not valid else []
    }


@tool
def identify_mentor_gaps(department: Optional[str] = None) -> List[Dict]:
    """
    Identify areas where more mentors are needed.
    
    Use this tool for workforce planning to find skill areas with high mentee demand
    but insufficient mentor supply.
    
    Args:
        department: Optional filter by department ID
    
    Returns:
        List of skill areas with demand/supply gap information
    """
    conn = get_connection()
    employee_repo = EmployeeRepository(conn)
    mentor_repo = MentorshipProfileRepository(conn)
    
    # Get all employees and mentors
    employees = employee_repo.list_employees()
    mentors = mentor_repo.list_profiles()
    
    # Analyze skill demand vs supply
    # This is a simplified version - full implementation would analyze goals_set
    skill_demand = {}
    skill_supply = {}
    
    # Count mentor supply by skill
    for mentor in mentors:
        if mentor.get('is_mentor') != 1:
            continue
        mentor_emp = employee_repo.get_employee(mentor['employee_id'])
        if mentor_emp and mentor_emp.get('skills_map'):
            skills = json.loads(mentor_emp['skills_map'])
            for skill in skills.keys():
                skill_supply[skill] = skill_supply.get(skill, 0) + 1
    
    # Count mentee demand (simplified - would parse goals for actual demand)
    for emp in employees:
        if emp.get('level') in ['Junior', 'Mid'] and emp.get('skills_map'):
            skills = json.loads(emp.get('skills_map', '{}'))
            for skill in skills.keys():
                skill_demand[skill] = skill_demand.get(skill, 0) + 1
    
    # Identify gaps
    gaps = []
    for skill, demand in skill_demand.items():
        supply = skill_supply.get(skill, 0)
        if demand > supply * 2:  # High demand, low supply
            gaps.append({
                'skill': skill,
                'demand': demand,
                'supply': supply,
                'gap_severity': 'high' if demand > supply * 3 else 'medium'
            })
    
    return sorted(gaps, key=lambda x: x['demand'] - x['supply'], reverse=True)[:5]


# Tool list for agent integration
MENTORING_TOOLS = [
    find_available_mentors,
    get_mentor_profile,
    get_mentee_profile,
    recommend_mentors,
    analyze_mentorship_progress,
    get_mentorship_statistics,
    validate_mentorship_goals,
    identify_mentor_gaps,
]
