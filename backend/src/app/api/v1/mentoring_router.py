"""
Mentoring API Router

FastAPI router for mentoring endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from .mentoring import (
    # Models
    MentorProfileResponse,
    MentorRecommendationRequest,
    MentorRecommendationResponse,
    MentorshipRequestCreate,
    MentorshipRequestResponse,
    MentorshipRequestUpdate,
    MentorshipPairResponse,
    MentorshipStatistics,
    # Functions
    get_available_mentors,
    get_mentor_by_id,
    recommend_mentors,
    create_mentorship_request,
    get_mentorship_requests,
    update_mentorship_request,
    get_mentorship_pairs,
    get_mentorship_statistics,
)

router = APIRouter(prefix="/api/v1/mentoring", tags=["Mentoring"])


@router.get("/mentors", response_model=List[MentorProfileResponse])
async def list_mentors(
    skill_area: Optional[str] = Query(None, description="Filter by skill area"),
    department: Optional[str] = Query(None, description="Filter by department")
):
    """
    Get list of available mentors.
    
    Optionally filter by skill area or department.
    """
    return get_available_mentors(skill_area, department)


@router.get("/mentors/{employee_id}", response_model=MentorProfileResponse)
async def get_mentor(employee_id: str):
    """
    Get a specific mentor's profile by employee ID.
    """
    mentor = get_mentor_by_id(employee_id)
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    return mentor


@router.post("/recommend", response_model=List[MentorRecommendationResponse])
async def get_recommendations(request: MentorRecommendationRequest):
    """
    Get personalized mentor recommendations based on career goals and desired skills.
    
    Uses AI-powered matching algorithm to find the best mentors for your needs.
    """
    return recommend_mentors(
        request.employeeId,
        request.careerGoals,
        request.desiredSkills,
        request.maxResults
    )


@router.post("/request", response_model=MentorshipRequestResponse)
async def create_request(request: MentorshipRequestCreate):
    """
    Create a new mentorship request.
    
    The mentor will be notified and can accept or decline the request.
    """
    try:
        return create_mentorship_request(
            request.menteeId,
            request.mentorId,
            request.message,
            request.goals
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/requests", response_model=List[MentorshipRequestResponse])
async def list_requests(
    mentor_id: Optional[str] = Query(None, description="Filter by mentor ID"),
    mentee_id: Optional[str] = Query(None, description="Filter by mentee ID")
):
    """
    Get mentorship requests.
    
    Can be filtered by mentor_id (requests you received) or mentee_id (requests you sent).
    """
    return get_mentorship_requests(mentor_id, mentee_id)


@router.put("/requests/{request_id}", response_model=MentorshipRequestResponse)
async def update_request(request_id: str, update: MentorshipRequestUpdate):
    """
    Update a mentorship request status (accept or decline).
    
    When accepted, this creates an active mentorship pair.
    """
    try:
        return update_mentorship_request(
            request_id,
            update.status,
            update.responseMessage
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/pairs", response_model=List[MentorshipPairResponse])
async def list_pairs(
    mentor_id: Optional[str] = Query(None, description="Filter by mentor ID"),
    mentee_id: Optional[str] = Query(None, description="Filter by mentee ID")
):
    """
    Get active mentorship pairs.
    
    Can be filtered by mentor_id or mentee_id to see specific relationships.
    """
    return get_mentorship_pairs(mentor_id, mentee_id)


@router.get("/statistics", response_model=MentorshipStatistics)
async def get_statistics():
    """
    Get overall mentorship program statistics.
    
    Useful for employer dashboard and program monitoring.
    """
    return get_mentorship_statistics()
