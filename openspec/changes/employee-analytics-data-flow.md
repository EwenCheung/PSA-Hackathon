# Change Proposal: Employee Analytics Data Flow Integration

- **Status:** Proposed
- **Author:** Codex (AI assistant)
- **Created:** 2024-11-24
- **Impacted Areas:** `frontend/components/employer/EmployeeAnalytics.tsx`, `backend/src/app/api/v1/analytics.py`, `backend/src/app/services/*`, `backend/src/app/data/repositories/*`, `backend/src/app/models/pydantic_schemas.py`, `backend/src/app/data/seed_data.py`

## Background

The Employer Dashboard currently renders hand-crafted analytics cards with static placeholder data (`frontend/components/employer/EmployeeAnalytics.tsx`). On the backend, the analytics API module (`backend/src/app/api/v1/analytics.py`) only documents intended routes and raises `NotImplementedError`. Repository and service layers do not yet expose aggregate queries that surface organization-wide KPIs, and the SQLite seed data lacks enrollment samples required for course-completion metrics. As a result, there is no end-to-end data flow from the database through repositories, services, API handlers, and up to the frontend.

## Goals

- Implement a full-stack data flow (Frontend → API → Service → Repository → Database) that powers the analytics tiles and tables on the Employer Dashboard.
- Deliver organization-wide KPIs: total employees, total completed courses, and average career-progress percent across employees.
- Provide department aggregates showing employee counts and blended performance scores (goal progress plus points) without exposing per-employee sentiment.
- Supply an employee detail dataset for the dashboard devoid of sentiment metadata to preserve privacy.
- Reuse and extend the existing project skeleton; avoid introducing new frameworks or replacing foundational modules.

## Non-Goals

- Rebuild the FastAPI application or change routing structure beyond implementing the analytics contract.
- Introduce real-time streaming or background jobs; analytics remain request/response over the existing SQLite demo dataset.
- Expose per-employee sentiment, wellbeing content, or privacy-sensitive telemetry.
- Redesign the Employer Dashboard layout outside of what is necessary to bind dynamic data and remove sentiment badges.

## Functional Overview

### Data Flow Overview

1. Frontend `EmployeeAnalytics` mounts and requests:
   - `GET /api/v1/analytics/overview`
   - `GET /api/v1/analytics/departments`
   - `GET /api/v1/analytics/employees`
2. FastAPI handlers in `backend/src/app/api/v1/analytics.py` delegate to an `AnalyticsService`.
3. `AnalyticsService` orchestrates repository calls:
   - `EmployeeRepository` for counts, base employee metadata, and points normalization data.
   - `EnrollmentRepository` for completion and progress stats.
   - `GoalRepository` for career-progress inputs used in blended performance scoring.
   - `DepartmentRepository` for department labels.
4. Repositories execute aggregate SQL over the SQLite database and return normalized dicts.
5. Service composes Pydantic response models for transport back to the frontend.
6. UI renders KPI tiles, department progress bars, and employee tables using fetched data with sentiment removed.

### Backend Changes

- **API Layer (`backend/src/app/api/v1/analytics.py`):**
  - Replace placeholder functions with FastAPI router definitions that call the service and return typed responses.
  - Ensure module exports a router for future wiring inside `main.py` without altering other API modules.

- **Service Layer (`backend/src/app/services/analytics_service.py`):**
  - Create a new `AnalyticsService` responsible for:
    - Aggregating totals (`get_overview_metrics`).
    - Computing department rollups (`get_department_metrics`).
    - Preparing employee-facing stats (`get_employee_metrics`), omitting sentiment fields.
  - Inject repositories via constructor (connections from `get_connection()`).
  - Normalise calculations (e.g., default zero totals when no rows, guard against division by zero).
  - Define blended performance scoring:
    - Normalise each employee's `points_current` to a 0-100 scale by dividing by the global maximum (fall back to 0 when max is zero).
    - Use average goal progress percent per employee as the second component.
    - Compute `performance_score = 0.5 * goal_progress_percent + 0.5 * points_normalised` and average by department.

- **Repository Layer:**
  - Extend `EmployeeRepository` with `count_employees()`, `list_with_department()` to fetch joined department names, `get_department_counts()`, and a helper to read the global max of `points_current`.
  - Extend `EnrollmentRepository` with methods that calculate:
    - Total completed courses filtered by `status='completed'`.
    - Per-employee course completion counts and progress averages.
  - Extend `GoalRepository` with helper to compute average `progress_percent` per employee and network-wide for performance scoring.
  - Add targeted SQL queries that leverage `GROUP BY` aggregations instead of loading all rows client-side.

- **Pydantic Schemas (`backend/src/app/models/pydantic_schemas.py`):**
  - Introduce dedicated response models:
    - `AnalyticsOverview` with `total_employees`, `total_completed_courses`, `average_career_progress`.
    - `AnalyticsDepartment` with `department_id`, `department_name`, `employee_count`, `average_performance` (0-100 blended score).
    - `AnalyticsEmployee` with `id`, `name`, `role`, `department`, `courses_completed`, `courses_in_progress`, `career_progress_percent`, `points`.
  - Update `__all__` exports if present (confirm file structure).

- **Database Seeding (`backend/src/app/data/seed_data.py` + JSON):**
  - Add enrollment seed records with realistic `status` (`completed`, `in-progress`) and `progress_percent`.
  - Ensure goals data covers multiple employees to support averaging logic (extend `goals.json` if necessary).
  - Re-run seed loader sequence to populate new tables while maintaining existing data shape.

### Frontend Changes

- **Data Fetching (`frontend/components/employer/EmployeeAnalytics.tsx`):**
  - Replace static arrays with API calls using `useEffect` plus `useState`.
  - Introduce TypeScript interfaces mirroring backend response schemas.
  - Provide loading and empty states; surface errors unobtrusively (e.g., toast or inline message).

- **UI Adjustments:**
  - Bind KPI cards to `overview` metrics.
  - Render department progress from `analytics/departments`.
  - Populate employee details table from `analytics/employees` data.
  - Remove sentiment badges and icons; ensure privacy mandate by limiting fields to role, department, course, points, and progress.

- **Config:**
  - Define `BACKEND_BASE_URL` in environment configuration:
    - Local development: `http://localhost:8000`.
    - Deployed environments: deployment-specific HTTPS endpoint (e.g., `https://api.companydomain.com`).
  - Surface the value to the frontend via Vite (mirror into `VITE_BACKEND_BASE_URL`) and default API clients to this setting.

### Privacy & Compliance

- Strip sentiment data at the service layer and ensure repositories used for analytics never join sentiment tables.
- Confirm frontend type definitions exclude `sentiment`, `wellbeing`, or `anon_session_id`.
- Add automated/unit tests that assert sentiment fields are absent from responses.

## Testing & Validation

- **Backend Unit Tests (`backend/tests`):**
  - Add tests for `AnalyticsService` methods using in-memory SQLite seeded with fixtures.
  - Cover edge cases: no enrollments, employees missing goals, division-by-zero protections.
  - Assert blended performance scoring matches expected values when points or goals dominate.

- **API Contract Tests:**
  - Use FastAPI test client to assert response payload shape and HTTP status codes for each analytics endpoint.

- **Frontend Testing:**
  - Add component-level tests (e.g., React Testing Library) that mock fetch responses and verify rendering without sentiment badges.

- **Manual QA:**
  - Seed database, run FastAPI app, load Employer Dashboard, confirm dynamic data matches DB counts.

## Risks & Mitigations

- **Inconsistent Seed Data:** Ensure new enrollment/goal seeds remain in sync with departments and employees; write helper to validate foreign keys during seeding.
- **Performance of Aggregations:** Queries rely on simple aggregates over small tables in SQLite; document possibility of indexing when scaling.
- **API Backward Compatibility:** Analytics endpoints were unimplemented, so adding JSON structures will not break existing consumers; document the contract.
- **Frontend Error Handling:** Provide fallback UI to avoid blank dashboard on API failure.

## Open Questions

- None.
