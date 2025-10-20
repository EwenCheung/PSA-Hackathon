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

from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
import os

# Create router
router = APIRouter(
    prefix="/api/v1/mentoring",
    tags=["Mentoring"],
)


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


# ============================================================================
# MOCK DATA (Replace with database queries in production)
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
# ROUTE HANDLERS
# ============================================================================

@router.get("/mentors", response_model=List[MentorProfile])
async def list_mentors(
    skill_area: Optional[str] = Query(None, description="Filter by skill area"),
    department: Optional[str] = Query(None, description="Filter by department")
):
    """
    Get list of available mentors.
    
    Optionally filter by skill area or department.
    
    Args:
        skill_area: Filter mentors by specific expertise area
        department: Filter mentors by department
        
    Returns:
        List[MentorProfile]: List of mentor profiles
    """
    try:
        mentors = MOCK_MENTORS.copy()
        
        if skill_area:
            mentors = [m for m in mentors if skill_area.lower() in [area.lower() for area in m["expertiseAreas"]]]
        
        if department:
            mentors = [m for m in mentors if m["department"].lower() == department.lower()]
        
        return [MentorProfile(**mentor) for mentor in mentors]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )


@router.get("/mentors/{employee_id}", response_model=MentorProfile)
async def get_mentor(employee_id: str):
    """
    Get a specific mentor's profile by employee ID.

    Args:
        employee_id: The mentor's employee identifier

    Returns:
        MentorProfile: Mentor profile information

    Raises:
        HTTPException: 404 if mentor not found
    """
    mentor = next((m for m in MOCK_MENTORS if m["employeeId"] == employee_id), None)
    if mentor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mentor {employee_id} not found",
        )
    return MentorProfile(**mentor)


@router.post("/recommend", response_model=List[MentorRecommendation])
async def get_recommendations(request: MentorRecommendationRequest):
    """
    Get personalized mentor recommendations based on career goals and desired skills.
    
    Uses AI-powered matching algorithm to find the best mentors for your needs.
    
    Args:
        request: Recommendation request with employee ID, goals, and desired skills
        
    Returns:
        List[MentorRecommendation]: Ranked list of mentor recommendations
    """
    try:
        recommendations = []
        
        for mentor in MOCK_MENTORS:
            if not mentor["isAvailable"]:
                continue
                
            # Calculate match score based on expertise overlap
            expertise_set = set(area.lower() for area in mentor["expertiseAreas"])
            goals_set = set(goal.lower() for goal in request.careerGoals + request.desiredSkills)
            
            # Find overlapping areas
            overlap = expertise_set.intersection(goals_set)
            match_score = int((len(overlap) / len(goals_set)) * 100) if goals_set else 0
            
            # Boost score based on rating and availability
            if mentor["menteesCount"] < mentor["maxMentees"]:
                match_score = min(100, match_score + 10)
            match_score = min(100, int(match_score * (mentor["rating"] / 5.0)))
            
            if match_score > 30:  # Only include decent matches
                recommendations.append(
                    MentorRecommendation(
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
        return recommendations[:request.maxResults]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )


@router.post("/request", response_model=MentorshipRequest, status_code=status.HTTP_201_CREATED)
async def create_request(request: MentorshipRequestCreate):
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
        # Find mentor details
        mentor = next((m for m in MOCK_MENTORS if m["employeeId"] == request.mentorId), None)
        if not mentor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mentor {request.mentorId} not found"
            )
        
        request_id = f"REQ{len(MOCK_REQUESTS) + 1:03d}"
        
        new_request = {
            "requestId": request_id,
            "menteeId": request.menteeId,
            "menteeName": "John Doe",  # In real app, fetch from employee data
            "menteeRole": "Software Developer",
            "mentorId": request.mentorId,
            "mentorName": mentor["name"],
            "message": request.message,
            "goals": request.goals,
            "status": "pending",
            "createdAt": datetime.now().isoformat(),
            "respondedAt": None
        }
        
        MOCK_REQUESTS[request_id] = new_request
        return MentorshipRequest(**new_request)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )


@router.get("/requests", response_model=List[MentorshipRequest])
async def list_requests(
    mentor_id: Optional[str] = Query(None, description="Filter by mentor ID"),
    mentee_id: Optional[str] = Query(None, description="Filter by mentee ID")
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
    try:
        requests = list(MOCK_REQUESTS.values())
        
        if mentor_id:
            requests = [r for r in requests if r["mentorId"] == mentor_id]
        
        if mentee_id:
            requests = [r for r in requests if r["menteeId"] == mentee_id]
        
        return [MentorshipRequest(**req) for req in requests]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )


@router.put("/requests/{request_id}", response_model=MentorshipRequest)
async def update_request(request_id: str, update: MentorshipRequestUpdate):
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
        if request_id not in MOCK_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Request {request_id} not found"
            )
        
        request = MOCK_REQUESTS[request_id]
        request["status"] = update.status
        request["respondedAt"] = datetime.now().isoformat()
        
        # If accepted, create a mentorship pair
        if update.status == "accepted":
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
        
        return MentorshipRequest(**request)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )


@router.get("/pairs", response_model=List[MentorshipPair])
async def list_pairs(
    mentor_id: Optional[str] = Query(None, description="Filter by mentor ID"),
    mentee_id: Optional[str] = Query(None, description="Filter by mentee ID")
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
    try:
        pairs = list(MOCK_PAIRS.values())
        
        if mentor_id:
            pairs = [p for p in pairs if p["mentorId"] == mentor_id]
        
        if mentee_id:
            pairs = [p for p in pairs if p["menteeId"] == mentee_id]
        
        return [MentorshipPair(**pair) for pair in pairs]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )


@router.get("/statistics", response_model=MentorshipStatistics)
async def get_statistics():
    """
    Get overall mentorship program statistics.
    
    Useful for employer dashboard and program monitoring.
    
    Returns:
        MentorshipStatistics: Program-wide statistics
    """
    try:
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
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )


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
