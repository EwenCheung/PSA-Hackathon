from fastapi import APIRouter, HTTPException, status

from app.models.pydantic_schemas import (
    EmployeeLoginRequest,
    EmployeeLoginResponse,
)
from app.services.auth_service import auth_service


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)


@router.post(
    "/employee-login",
    response_model=EmployeeLoginResponse,
    status_code=status.HTTP_200_OK,
)
async def employee_login(payload: EmployeeLoginRequest) -> EmployeeLoginResponse:
    """
    Validate employee ID login and return profile plus session timestamp.
    """
    profile = auth_service.validate_employee(payload.employee_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee {payload.employee_id} not found",
        )

    issued_at = auth_service.issue_session_timestamp()
    return EmployeeLoginResponse(employee=profile, session={"issued_at": issued_at})
