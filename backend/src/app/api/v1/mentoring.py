"""
API v1: Mentoring Router

Purpose:
- Mentor discovery and matching
- Mentorship request management
- Active mentorship pair tracking
- Program statistics and insights
- AI-powered mentoring assistant

Routes:
- GET /api/v1/mentoring/mentors
- GET /api/v1/mentoring/mentors/{employee_id}
- POST /api/v1/mentoring/recommend
- POST /api/v1/mentoring/request
- GET /api/v1/mentoring/requests
- PUT /api/v1/mentoring/requests/{request_id}
- GET /api/v1/mentoring/pairs
- GET /api/v1/mentoring/statistics
- POST /api/v1/mentoring/agent/chat (AI Assistant)
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
import os

from app.core.db import get_connection, init_db
from app.data.seed_data import load_all_seeds
from app.services.mentor_match_request_service import MentorMatchingService

# Create router
router = APIRouter(
    prefix="/api/v1/mentoring",
    tags=["Mentoring"],
)


def get_matching_service() -> MentorMatchingService:
    conn = get_connection()
    try:
        init_db(conn)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM employees")
        count = cur.fetchone()[0]
        if count == 0:
            load_all_seeds(conn)
        yield MentorMatchingService(conn)
    finally:
        conn.close()


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class MentorProfile(BaseModel):
    """Mentor profile information"""
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


class MentorRecommendation(BaseModel):
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


class MentorshipRequest(BaseModel):
    """Mentorship request information"""
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


class MentorshipPair(BaseModel):
    """Active mentorship pair information"""
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
    """Mentorship program statistics"""
    totalActivePairs: int
    totalMentors: int
    totalMenteesSeeking: int
    availableMentors: int
    averageMatchScore: float
    completionRate: float
    underservedSkills: List[str]


class AgentChatRequest(BaseModel):
    """Request for AI agent chat"""
    message: str = Field(..., description="User's question or request", min_length=1)
    employee_id: Optional[str] = Field(None, description="Optional employee ID for context")
    chat_history: Optional[List[Dict[str, str]]] = Field(None, description="Previous conversation history")
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Ensure message is not just whitespace"""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty or whitespace only")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Find me a mentor for cloud architecture",
                "employee_id": "EMP005",
                "chat_history": []
            }
        }


class AgentChatResponse(BaseModel):
    """Response from AI agent"""
    response: str = Field(..., description="Agent's response message")
    tools_used: Optional[List[str]] = Field(None, description="Tools the agent called")
    success: bool = Field(True, description="Whether the request was successful")
    error: Optional[str] = Field(None, description="Error message if any")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "I found 3 mentors with cloud architecture expertise...",
                "tools_used": ["find_available_mentors"],
                "success": True,
                "error": None
            }
        }


@router.get("/mentors", response_model=List[MentorProfile])
async def list_mentors(
    skill_area: Optional[str] = Query(None, description="Filter by skill area"),
    department: Optional[str] = Query(None, description="Filter by department"),
    mentee_id: Optional[str] = Query(
        None,
        description="Only return mentors senior to this employee",
        alias="mentee_id",
    ),
    service: MentorMatchingService = Depends(get_matching_service),
):
    try:
        mentors = service.list_mentors(
            mentee_id=mentee_id,
            skill_area=skill_area,
            department=department,
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return [MentorProfile(**mentor) for mentor in mentors]


@router.get("/mentors/{employee_id}", response_model=MentorProfile)
async def get_mentor(
    employee_id: str,
    service: MentorMatchingService = Depends(get_matching_service),
):
    try:
        mentor = service.get_mentor(employee_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return MentorProfile(**mentor)


@router.post("/recommend", response_model=List[MentorRecommendation])
async def get_recommendations(
    request: MentorRecommendationRequest,
    service: MentorMatchingService = Depends(get_matching_service),
):
    try:
        mentors = service.list_mentors(mentee_id=request.employeeId)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    recommendations: List[MentorRecommendation] = []
    goals_set = set(goal.lower() for goal in request.careerGoals + request.desiredSkills)

    for mentor in mentors:
        score = service.estimate_match_score(
            mentor["employeeId"],
            request.employeeId,
            request.desiredSkills or request.careerGoals,
        )
        if score <= 0:
            continue
        expertise_set = set(area.lower() for area in mentor["expertiseAreas"])
        overlap = expertise_set.intersection(goals_set)
        reason = (
            f"Strong expertise in {', '.join(list(overlap)[:2])}"
            if overlap
            else "Relevant experience for your goals"
        )
        recommendations.append(
            MentorRecommendation(
                mentorId=mentor["employeeId"],
                mentorName=mentor["name"],
                role=mentor["role"],
                matchScore=int(score),
                reason=reason,
                focusAreas=mentor["expertiseAreas"][:3],
            )
        )

    recommendations.sort(key=lambda item: item.matchScore, reverse=True)
    return recommendations[: request.maxResults]


@router.post("/request", response_model=MentorshipRequest, status_code=status.HTTP_201_CREATED)
async def create_request(
    request: MentorshipRequestCreate,
    service: MentorMatchingService = Depends(get_matching_service),
):
    """
    Create a new mentorship request.
    
    The mentor will be notified and can accept or decline the request.
    
    Args:
        request: Mentorship request details
        
    Returns:
        MentorshipRequest: The created mentorship request
        
    Raises:
        HTTPException: 404 if mentor not found
    """
    try:
        created = service.create_request(
            request.menteeId, request.mentorId, request.message, request.goals
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return MentorshipRequest(**created)


@router.get("/requests", response_model=List[MentorshipRequest])
async def list_requests(
    mentor_id: Optional[str] = Query(None, description="Filter by mentor ID"),
    mentee_id: Optional[str] = Query(None, description="Filter by mentee ID"),
    service: MentorMatchingService = Depends(get_matching_service),
):
    """
    Get mentorship requests.
    
    Can be filtered by mentor_id (requests you received) or mentee_id (requests you sent).
    
    Args:
        mentor_id: Filter by mentor employee ID
        mentee_id: Filter by mentee employee ID
        
    Returns:
        List[MentorshipRequest]: List of mentorship requests
    """
    requests = service.list_requests(mentor_id=mentor_id, mentee_id=mentee_id)
    return [MentorshipRequest(**req) for req in requests]


@router.put("/requests/{request_id}", response_model=MentorshipRequest)
async def update_request(
    request_id: str,
    update: MentorshipRequestUpdate,
    service: MentorMatchingService = Depends(get_matching_service),
):
    """
    Update a mentorship request status (accept or decline).
    
    When accepted, this creates an active mentorship pair.
    
    Args:
        request_id: The request identifier
        update: Status update details
        
    Returns:
        MentorshipRequest: Updated mentorship request
        
    Raises:
        HTTPException: 404 if request not found
    """
    try:
        numeric_id = int(request_id.replace("REQ", "")) if request_id.startswith("REQ") else int(request_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request id") from exc

    try:
        updated = service.update_request_status(
            numeric_id, update.status, update.responseMessage
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return MentorshipRequest(**updated)


@router.delete("/requests/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_request(
    request_id: str,
    mentee_id: str = Query(..., description="Employee ID of the mentee withdrawing the request"),
    service: MentorMatchingService = Depends(get_matching_service),
) -> Response:
    """
    Cancel/withdraw a mentorship request.
    
    This marks the request as deleted (soft delete) rather than removing it from the database.
    Only pending requests can be canceled. Accepted requests cannot be deleted.
    
    Args:
        request_id: The request identifier (e.g., "REQ001" or "1")
        mentee_id: Employee ID of the mentee who made the request
        
    Returns:
        204 No Content on successful cancellation
        
    Raises:
        HTTPException: 404 if request not found
        HTTPException: 400 if request cannot be deleted or invalid parameters
    """
    try:
        numeric_id = int(request_id.replace("REQ", "")) if request_id.startswith("REQ") else int(request_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request id") from exc

    try:
        service.delete_request(numeric_id, mentee_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/pairs", response_model=List[MentorshipPair])
async def list_pairs(
    mentor_id: Optional[str] = Query(None, description="Filter by mentor ID"),
    mentee_id: Optional[str] = Query(None, description="Filter by mentee ID"),
    service: MentorMatchingService = Depends(get_matching_service),
):
    """
    Get active mentorship pairs.
    
    Can be filtered by mentor_id or mentee_id to see specific relationships.
    
    Args:
        mentor_id: Filter by mentor employee ID
        mentee_id: Filter by mentee employee ID
        
    Returns:
        List[MentorshipPair]: List of mentorship pairs
    """
    pairs = service.list_pairs(mentor_id=mentor_id, mentee_id=mentee_id)
    return [MentorshipPair(**pair) for pair in pairs]


@router.get("/statistics", response_model=MentorshipStatistics)
async def get_statistics(
    service: MentorMatchingService = Depends(get_matching_service),
):
    """
    Get overall mentorship program statistics.
    
    Useful for employer dashboard and program monitoring.
    
    Returns:
        MentorshipStatistics: Program-wide statistics
    """
    stats = service.statistics()
    return MentorshipStatistics(**stats)


@router.post("/agent/chat", response_model=AgentChatResponse)
async def agent_chat(request: AgentChatRequest):
    """
    Chat with the AI mentoring assistant.
    
    The AI agent can help with:
    - Finding mentors by skill, department, or rating
    - Getting personalized mentor recommendations
    - Analyzing mentorship progress
    - Providing program statistics and insights
    - Validating mentorship goals
    - Identifying skill gaps in the mentoring program
    
    Args:
        request: AgentChatRequest with message and optional context
        
    Returns:
        AgentChatResponse: AI agent's response with tool usage information
        
    Raises:
        HTTPException: 400 for invalid input
        HTTPException: 503 if AI service is unavailable
        HTTPException: 500 for internal errors
        
    Example:
        POST /api/v1/mentoring/agent/chat
        {
            "message": "Find me a mentor for Python and machine learning",
            "employee_id": "EMP005"
        }
    """
    # Validate environment variables are set (matching what agent.py expects)
    required_env_vars = [
        'AZURE_OPENAI_API_KEY',
        'DEPLOYMENT',
        'API_VERSION'
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "AI agent not configured",
                "message": f"Missing environment variables: {', '.join(missing_vars)}. Please configure Azure OpenAI credentials.",
                "missing_variables": missing_vars
            }
        )
    
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    try:
        # Import agent here to avoid import errors if dependencies not installed
        from app.agent.mentoring_agent.agent import run_agent_query
        
        # Prepare input for agent
        agent_result = run_agent_query(
            query=request.message,
            chat_history=request.chat_history
        )
        
        # Extract response and tool information
        response_text = agent_result.get('output', 'Sorry, I could not process that request.')
        
        # Extract tools used if intermediate_steps available
        tools_used = []
        if 'intermediate_steps' in agent_result:
            for step in agent_result['intermediate_steps']:
                if isinstance(step, tuple) and len(step) > 0:
                    action = step[0]
                    if hasattr(action, 'tool'):
                        tools_used.append(action.tool)
        
        return AgentChatResponse(
            response=response_text,
            tools_used=tools_used if tools_used else None,
            success=True,
            error=None
        )
    
    except ImportError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "AI dependencies not installed",
                "message": f"Required packages not available: {str(e)}",
                "suggestion": "Install langchain and langchain-openai packages"
            }
        )
    
    except ValueError as e:
        # Handle configuration errors from agent
        error_msg = str(e)
        if "Missing required environment variables" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "error": "AI agent configuration error",
                    "message": error_msg
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid request: {error_msg}"
            )
    
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Agent error: {type(e).__name__}: {str(e)}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Agent execution failed",
                "message": "An unexpected error occurred while processing your request.",
                "type": type(e).__name__
            }
        )
