"""
API v1: Employees Router

Purpose:
- Employee profile, goals, points, and career course lifecycle.

Routes:
- GET /api/v1/employees/{employee_id}
- GET /api/v1/employees/{employee_id}/career/recommendations
- GET /api/v1/employees/{employee_id}/leadership/potential
- POST /api/v1/employees/{employee_id}/career/courses/{course_id}/start
- POST /api/v1/employees/{employee_id}/career/courses/{course_id}/complete
- GET /api/v1/employees/{employee_id}/goals
- PATCH /api/v1/employees/{employee_id}/points
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List

from app.models.pydantic_schemas import EmployeeDetail, CourseDetail, GoalDetail
<<<<<<< HEAD
from ...agent.course_recommendation_agent.main import get_course_recommendations, get_leadership_potential_employee, get_career_pathway, get_leadership_potential_employer
from ...agent.course_recommendation_agent.tools import get_employee_context
=======
from app.services.employee_service import EmployeeService
from app.core.db import get_connection
>>>>>>> origin/WenyiBranch

# --------------------------
# Router
# --------------------------
router = APIRouter(
    prefix="/api/v1/employees",
    tags=["Employees"],
)

# --------------------------
# Employee Profile
# --------------------------
@router.get("/{employee_id}")
async def get_employee_profile(employee_id: str):
    """
    Get the full employee profile including skills, goals, and courses.
    """
    try:
<<<<<<< HEAD
        emp_context = get_employee_context(employee_id)
        if not emp_context or "profile" not in emp_context:
            raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
        
        profile = emp_context["profile"]
        # Merge profile with nested fields
        profile_full = {
            **profile,
            "skills": emp_context.get("skills", []),
            "goals": emp_context.get("goals", []),
            "courses_enrolled": emp_context.get("courses_enrolled", {})
        }

        return profile_full

    except ValueError:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------
# Career Recommendations
# --------------------------
@router.get("/{employee_id}/career/recommendations")
async def career_recommendations(employee_id: str):
    try:
        result = get_course_recommendations(employee_id)
        # Ensure JSON is returned, fallback to empty dict
        recommendations = result.get("json", {})
        return {
            "employee_id": employee_id,
            "recommendations": recommendations,
            "summary": result.get("text_summary", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
=======
        service = EmployeeService()
        return service.get_employee_profile(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal error: {str(e)}")
>>>>>>> origin/WenyiBranch



# --------------------------
# Career Pathway (full growth plan)
# --------------------------
@router.get("/{employee_id}/career/pathway")
async def career_pathway(employee_id: str):
    try:
        result = get_career_pathway(employee_id)
        pathway_json = result.get("json", {})
        return {
            "employee_id": employee_id,
            "career_pathway": pathway_json,
            "summary": result.get("text_summary", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# --------------------------
# Leadership Potential (Employee View)
# --------------------------
@router.get("/{employee_id}/leadership/potential")
async def leadership_potential_employee(employee_id: str):
    """
    Evaluate leadership potential for the employee.
    """
    try:
        result = get_leadership_potential_employee(employee_id)
        return {
            "employee_id": employee_id,
            "evaluation": result.get("json"),
            "summary": result.get("text_summary")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------
# Leadership Potential (Employer View)
# --------------------------
@router.get("/{employee_id}/leadership/employer")
async def leadership_potential_employer(employee_id: str):
    """
    Evaluate leadership potential from the employer's perspective.
    """
    try:
        result = get_leadership_potential_employer(employee_id)
        return {
            "employee_id": employee_id,
            "evaluation": result.get("json"),
            "summary": result.get("text_summary")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------
# Start Course
# --------------------------
@router.post("/{employee_id}/career/courses/{course_id}/start", response_model=CourseDetail)
async def start_course(employee_id: str, course_id: str):
    """
    Start a course for the employee.
    """
    try:
        # TODO: Implement DB persistence
        # Currently just a placeholder to update in-memory
        emp_context = get_employee_context(employee_id)
        courses = emp_context.get("profile", {}).get("courses_enrolled", {})
        courses[course_id] = "in-progress"
        return CourseDetail(course_id=course_id, status="in-progress")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------
# Complete Course
# --------------------------
@router.post("/{employee_id}/career/courses/{course_id}/complete", response_model=CourseDetail)
async def complete_course(employee_id: str, course_id: str):
    """
    Mark a course as completed.
    """
    try:
        # TODO: Implement DB persistence
        emp_context = get_employee_context(employee_id)
        courses = emp_context.get("profile", {}).get("courses_enrolled", {})
        courses[course_id] = "completed"
        return CourseDetail(course_id=course_id, status="completed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------
# Employee Goals
# --------------------------
@router.get("/{employee_id}/goals", response_model=List[GoalDetail])
async def get_employee_goals(employee_id: str):
    try:
        emp_context = get_employee_context(employee_id)
        goals = emp_context.get("goals", [])

        print("EMP CONTEXT:", emp_context)
        print("GOALS PATH:", emp_context.get("profile", {}).get("goals"))

        unpacked_goals = [
            GoalDetail(name=g) if isinstance(g, str) else GoalDetail(**g)
            for g in goals
        ]
        return unpacked_goals
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# --------------------------
# Adjust Points
# --------------------------
@router.patch("/{employee_id}/points", response_model=EmployeeDetail)
async def adjust_points(employee_id: str, delta: int = Query(..., description="Points to add/deduct")):
    """
    Adjust employee points by delta (add or subtract).
    """
    try:
<<<<<<< HEAD
        emp_context = get_employee_context(employee_id)
        profile = emp_context.get("profile")
        if not profile:
            raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
        
        profile["points_current"] = (profile.get("points_current", 0) or 0) + delta
        # TODO: persist points in DB
        return EmployeeDetail(**profile)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
=======
        service = EmployeeService()
        updated = service.adjust_points_transactional(employee_id, delta, source="api_points_adjust")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal error: {str(e)}")

>>>>>>> origin/WenyiBranch
