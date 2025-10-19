"""
API v1: Employees Router

Purpose
- Employee profile, goals, points and career course lifecycle.

Routes:
- GET /api/v1/employees/{employee_id}
- GET /api/v1/employees/{employee_id}/career/recommendations
- POST /api/v1/employees/{employee_id}/career/courses/{course_id}/start
- POST /api/v1/employees/{employee_id}/career/courses/{course_id}/complete
- GET /api/v1/employees/{employee_id}/goals
- PATCH /api/v1/employees/{employee_id}/points
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List

from app.models.pydantic_schemas import EmployeeDetail, CourseDetail, GoalDetail
from app.services.employee_service import EmployeeService
from app.core.db import get_connection

# Create router
router = APIRouter(
    prefix="/api/v1/employees",
    tags=["Employees"],
)


@router.get("/{employee_id}", response_model=EmployeeDetail)
async def get_employee_profile(employee_id: str):
    """
    Get employee profile with points and metadata.
    
    Args:
        employee_id: The employee's unique identifier
        
    Returns:
        EmployeeDetail: Employee profile with points and metadata
        
    Raises:
        HTTPException: 404 if employee not found
        HTTPException: 500 for internal errors
    """
    try:
        service = EmployeeService()
        return service.get_employee_profile(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal error: {str(e)}")


@router.get("/{employee_id}/career/recommendations", response_model=List[CourseDetail])
async def get_career_recommendations(employee_id: str):
    """
    Get ranked course recommendations for employee.
    
    Args:
        employee_id: The employee's unique identifier
        
    Returns:
        List[CourseDetail]: Ranked list of recommended courses
        
    Raises:
        HTTPException: 501 Not Implemented
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Career recommendations not yet implemented"
    )


@router.post("/{employee_id}/career/courses/{course_id}/start", response_model=CourseDetail)
async def start_course(employee_id: str, course_id: str):
    """
    Mark a course as in-progress for employee.
    
    Args:
        employee_id: The employee's unique identifier
        course_id: The course's unique identifier
        
    Returns:
        CourseDetail: Updated course information
        
    Raises:
        HTTPException: 501 Not Implemented
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Start course not yet implemented"
    )


@router.post("/{employee_id}/career/courses/{course_id}/complete", response_model=CourseDetail)
async def complete_course(employee_id: str, course_id: str):
    """
    Mark a course as completed and add points.
    
    Args:
        employee_id: The employee's unique identifier
        course_id: The course's unique identifier
        
    Returns:
        CourseDetail: Updated course information with points awarded
        
    Raises:
        HTTPException: 501 Not Implemented
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Complete course not yet implemented"
    )


@router.get("/{employee_id}/goals", response_model=List[GoalDetail])
async def get_goals(employee_id: str):
    """
    Get employee career goals with progress and targets.
    
    Args:
        employee_id: The employee's unique identifier
        
    Returns:
        List[GoalDetail]: List of employee goals with progress
        
    Raises:
        HTTPException: 501 Not Implemented
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Goals not yet implemented"
    )


@router.patch("/{employee_id}/points", response_model=EmployeeDetail)
async def adjust_points(employee_id: str, delta: int = Query(..., description="Points to add (positive) or deduct (negative)")):
    """
    Adjust employee points (earn/redeem).
    
    Args:
        employee_id: The employee's unique identifier
        delta: Points to add (positive) or deduct (negative)
        
    Returns:
        EmployeeDetail: Updated employee profile with new points
        
    Raises:
        HTTPException: 501 Not Implemented
    """
    try:
        service = EmployeeService()
        updated = service.adjust_points_transactional(employee_id, delta, source="api_points_adjust")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal error: {str(e)}")

