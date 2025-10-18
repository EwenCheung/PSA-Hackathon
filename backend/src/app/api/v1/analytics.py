"""
API: Analytics

Purpose
- Company-wide KPIs and aggregates for employer dashboard.
"""
from typing import List

from fastapi import APIRouter, Depends

from app.models.pydantic_schemas import (
    AnalyticsDepartment,
    AnalyticsEmployee,
    AnalyticsOverview,
)
from app.services.analytics_service import AnalyticsService


EXPECTED_ROUTES: List[str] = [
    "/api/v1/analytics/overview",
    "/api/v1/analytics/departments",
    "/api/v1/analytics/employees",
]

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


def get_analytics_service() -> AnalyticsService:
    return AnalyticsService()


def overview(service: AnalyticsService | None = None) -> AnalyticsOverview:
    """
    Return top-level KPIs for dashboard tiles.
    """
    service = service or AnalyticsService()
    return service.get_overview_metrics()


def departments(service: AnalyticsService | None = None) -> List[AnalyticsDepartment]:
    """
    Return department aggregates with blended performance scores.
    """
    service = service or AnalyticsService()
    return service.get_department_metrics()


def employees(service: AnalyticsService | None = None) -> List[AnalyticsEmployee]:
    """
    Return employee rows for detailed cards (without sentiment data).
    """
    service = service or AnalyticsService()
    return service.get_employee_metrics()


@router.get("/overview", response_model=AnalyticsOverview)
def overview_endpoint(
    service: AnalyticsService = Depends(get_analytics_service),
) -> AnalyticsOverview:
    return service.get_overview_metrics()


@router.get("/departments", response_model=List[AnalyticsDepartment])
def departments_endpoint(
    service: AnalyticsService = Depends(get_analytics_service),
) -> List[AnalyticsDepartment]:
    return service.get_department_metrics()


@router.get("/employees", response_model=List[AnalyticsEmployee])
def employees_endpoint(
    service: AnalyticsService = Depends(get_analytics_service),
) -> List[AnalyticsEmployee]:
    return service.get_employee_metrics()
