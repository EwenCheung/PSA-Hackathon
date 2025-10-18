"""
Mentoring API - Business Logic Layer

This module contains the business logic and data models for the mentoring system.
Currently uses mock data, but can be replaced with database queries.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class MentorProfileResponse(BaseModel):
    """Response model for mentor profile"""
    employeeId: str
    name: str
    role: str
    department: str
    expertiseAreas: List[str]
    rating: float
    menteesCount: int
    maxMentees: int
    isAvailable: bool
    bio: str
    yearsOfExperience: int
    achievements: List[str] = []


class MentorRecommendationRequest(BaseModel):
    """Request for mentor recommendations"""
    employeeId: str
    careerGoals: List[str]
    desiredSkills: List[str]
    maxResults: int = 5


class MentorRecommendationResponse(BaseModel):
    """Individual mentor recommendation"""
    mentorId: str
    mentorName: str
    role: str
    matchScore: int
    reason: str
    focusAreas: List[str]


class MentorshipRequestCreate(BaseModel):
    """Request to create a mentorship request"""
    menteeId: str
    mentorId: str
    message: str
    goals: List[str]


class MentorshipRequestResponse(BaseModel):
    """Response model for mentorship request"""
    requestId: str
    menteeId: str
    menteeName: str
    menteeRole: str
    mentorId: str
    mentorName: str
    message: str
    goals: List[str]
    status: str  # pending, accepted, declined
    createdAt: str
    respondedAt: Optional[str] = None


class MentorshipRequestUpdate(BaseModel):
    """Update mentorship request status"""
    status: str  # accepted or declined
    responseMessage: Optional[str] = None


class MentorshipPairResponse(BaseModel):
    """Response model for active mentorship pair"""
    pairId: str
    mentorId: str
    mentorName: str
    mentorRole: str
    menteeId: str
    menteeName: str
    menteeRole: str
    startDate: str
    focusAreas: List[str]
    status: str
    progressPercentage: int
    sessionsCompleted: int
    lastMeetingDate: Optional[str] = None
    nextMeetingDate: Optional[str] = None


class MentorshipStatistics(BaseModel):
    """Statistics for mentorship program"""
    totalActivePairs: int
    totalMentors: int
    totalMenteesSeeking: int
    availableMentors: int
    averageMatchScore: float
    completionRate: float
    underservedSkills: List[str]


# ============================================================================
# MOCK DATA
# ============================================================================

MOCK_MENTORS = [
    {
        "employeeId": "EMP001",
        "name": "Sarah Chen",
        "role": "Senior Operations Manager",
        "department": "Operations",
        "expertiseAreas": ["Leadership", "Strategic Planning", "Operations Management"],
        "rating": 4.8,
        "menteesCount": 3,
        "maxMentees": 5,
        "isAvailable": True,
        "bio": "15+ years in operations with focus on leadership development",
        "yearsOfExperience": 15,
        "achievements": ["Leadership Excellence Award 2023", "Mentor of the Year 2022"]
    },
    {
        "employeeId": "EMP002",
        "name": "Michael Rodriguez",
        "role": "Technology Director",
        "department": "IT",
        "expertiseAreas": ["Technical Skills", "Innovation", "Digital Transformation"],
        "rating": 4.9,
        "menteesCount": 2,
        "maxMentees": 4,
        "isAvailable": True,
        "bio": "Tech leader with expertise in digital transformation",
        "yearsOfExperience": 12,
        "achievements": ["Innovation Award 2024"]
    },
    {
        "employeeId": "EMP003",
        "name": "Jennifer Park",
        "role": "HR Business Partner",
        "department": "Human Resources",
        "expertiseAreas": ["HR Management", "Team Building", "Communication"],
        "rating": 4.7,
        "menteesCount": 4,
        "maxMentees": 4,
        "isAvailable": False,
        "bio": "Passionate about employee development and team dynamics",
        "yearsOfExperience": 10,
        "achievements": []
    },
    {
        "employeeId": "EMP004",
        "name": "David Kumar",
        "role": "Senior Business Analyst",
        "department": "Analytics",
        "expertiseAreas": ["Analytics", "Process Optimization", "Data-Driven Decision Making"],
        "rating": 4.6,
        "menteesCount": 2,
        "maxMentees": 5,
        "isAvailable": True,
        "bio": "Expert in leveraging data for business insights",
        "yearsOfExperience": 8,
        "achievements": ["Analytics Excellence 2023"]
    }
]

MOCK_REQUESTS = {}  # Will be populated as requests are created
MOCK_PAIRS = {}  # Will be populated as requests are accepted


# ============================================================================
# BUSINESS LOGIC FUNCTIONS
# ============================================================================

def get_available_mentors(skill_area: Optional[str] = None, department: Optional[str] = None) -> List[MentorProfileResponse]:
    """
    Get list of available mentors, optionally filtered by skill area or department.
    """
    mentors = MOCK_MENTORS.copy()
    
    if skill_area:
        mentors = [m for m in mentors if skill_area.lower() in [area.lower() for area in m["expertiseAreas"]]]
    
    if department:
        mentors = [m for m in mentors if m["department"].lower() == department.lower()]
    
    return [MentorProfileResponse(**mentor) for mentor in mentors]


def get_mentor_by_id(employee_id: str) -> Optional[MentorProfileResponse]:
    """
    Get a specific mentor by employee ID.
    """
    mentor = next((m for m in MOCK_MENTORS if m["employeeId"] == employee_id), None)
    return MentorProfileResponse(**mentor) if mentor else None


def recommend_mentors(
    employee_id: str,
    career_goals: List[str],
    desired_skills: List[str],
    max_results: int = 5
) -> List[MentorRecommendationResponse]:
    """
    Get personalized mentor recommendations based on career goals and desired skills.
    Uses a simple matching algorithm based on expertise overlap.
    """
    recommendations = []
    
    for mentor in MOCK_MENTORS:
        if not mentor["isAvailable"]:
            continue
            
        # Calculate match score based on expertise overlap
        expertise_set = set(area.lower() for area in mentor["expertiseAreas"])
        goals_set = set(goal.lower() for goal in career_goals + desired_skills)
        
        # Find overlapping areas
        overlap = expertise_set.intersection(goals_set)
        match_score = int((len(overlap) / len(goals_set)) * 100) if goals_set else 0
        
        # Boost score based on rating and availability
        if mentor["menteesCount"] < mentor["maxMentees"]:
            match_score = min(100, match_score + 10)
        match_score = min(100, int(match_score * (mentor["rating"] / 5.0)))
        
        if match_score > 30:  # Only include decent matches
            recommendations.append(
                MentorRecommendationResponse(
                    mentorId=mentor["employeeId"],
                    mentorName=mentor["name"],
                    role=mentor["role"],
                    matchScore=match_score,
                    reason=f"Strong expertise in {', '.join(list(overlap)[:2]) if overlap else 'relevant areas'}",
                    focusAreas=mentor["expertiseAreas"][:3]
                )
            )
    
    # Sort by match score and return top results
    recommendations.sort(key=lambda x: x.matchScore, reverse=True)
    return recommendations[:max_results]


def create_mentorship_request(
    mentee_id: str,
    mentor_id: str,
    message: str,
    goals: List[str]
) -> MentorshipRequestResponse:
    """
    Create a new mentorship request.
    """
    request_id = f"REQ{len(MOCK_REQUESTS) + 1:03d}"
    
    # Find mentor details
    mentor = next((m for m in MOCK_MENTORS if m["employeeId"] == mentor_id), None)
    if not mentor:
        raise ValueError(f"Mentor {mentor_id} not found")
    
    request = {
        "requestId": request_id,
        "menteeId": mentee_id,
        "menteeName": "John Doe",  # In real app, fetch from employee data
        "menteeRole": "Software Developer",
        "mentorId": mentor_id,
        "mentorName": mentor["name"],
        "message": message,
        "goals": goals,
        "status": "pending",
        "createdAt": datetime.now().isoformat(),
        "respondedAt": None
    }
    
    MOCK_REQUESTS[request_id] = request
    return MentorshipRequestResponse(**request)


def get_mentorship_requests(
    mentor_id: Optional[str] = None,
    mentee_id: Optional[str] = None
) -> List[MentorshipRequestResponse]:
    """
    Get mentorship requests, optionally filtered by mentor or mentee.
    """
    requests = list(MOCK_REQUESTS.values())
    
    if mentor_id:
        requests = [r for r in requests if r["mentorId"] == mentor_id]
    
    if mentee_id:
        requests = [r for r in requests if r["menteeId"] == mentee_id]
    
    return [MentorshipRequestResponse(**req) for req in requests]


def update_mentorship_request(
    request_id: str,
    status: str,
    response_message: Optional[str] = None
) -> MentorshipRequestResponse:
    """
    Update a mentorship request status (accept or decline).
    If accepted, creates a mentorship pair.
    """
    if request_id not in MOCK_REQUESTS:
        raise ValueError(f"Request {request_id} not found")
    
    request = MOCK_REQUESTS[request_id]
    request["status"] = status
    request["respondedAt"] = datetime.now().isoformat()
    
    # If accepted, create a mentorship pair
    if status == "accepted":
        pair_id = f"PAIR{len(MOCK_PAIRS) + 1:03d}"
        mentor = next((m for m in MOCK_MENTORS if m["employeeId"] == request["mentorId"]), None)
        
        pair = {
            "pairId": pair_id,
            "mentorId": request["mentorId"],
            "mentorName": request["mentorName"],
            "mentorRole": mentor["role"] if mentor else "Unknown",
            "menteeId": request["menteeId"],
            "menteeName": request["menteeName"],
            "menteeRole": request["menteeRole"],
            "startDate": datetime.now().isoformat(),
            "focusAreas": request["goals"],
            "status": "active",
            "progressPercentage": 0,
            "sessionsCompleted": 0,
            "lastMeetingDate": None,
            "nextMeetingDate": None
        }
        MOCK_PAIRS[pair_id] = pair
    
    return MentorshipRequestResponse(**request)


def get_mentorship_pairs(
    mentor_id: Optional[str] = None,
    mentee_id: Optional[str] = None
) -> List[MentorshipPairResponse]:
    """
    Get active mentorship pairs, optionally filtered by mentor or mentee.
    """
    pairs = list(MOCK_PAIRS.values())
    
    if mentor_id:
        pairs = [p for p in pairs if p["mentorId"] == mentor_id]
    
    if mentee_id:
        pairs = [p for p in pairs if p["menteeId"] == mentee_id]
    
    return [MentorshipPairResponse(**pair) for pair in pairs]


def get_mentorship_statistics() -> MentorshipStatistics:
    """
    Get overall mentorship program statistics.
    """
    total_mentors = len(MOCK_MENTORS)
    available_mentors = len([m for m in MOCK_MENTORS if m["isAvailable"]])
    active_pairs = len([p for p in MOCK_PAIRS.values() if p["status"] == "active"])
    
    return MentorshipStatistics(
        totalActivePairs=active_pairs,
        totalMentors=total_mentors,
        totalMenteesSeeking=len([r for r in MOCK_REQUESTS.values() if r["status"] == "pending"]),
        availableMentors=available_mentors,
        averageMatchScore=85.0,
        completionRate=0.78,
        underservedSkills=["Data Science", "Change Management", "Public Speaking"]
    )
