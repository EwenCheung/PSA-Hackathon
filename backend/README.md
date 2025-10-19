# PSA Hackathon Backend

Future-Ready Workforce Agent Platform (Backend API)

---

## Overview
This backend powers the PSA Future-Ready Workforce platform, providing APIs, business logic, and data storage for employee career development, well-being, mentorship, and analytics. It is designed using a three-layer architecture (Repository → Service → API), with clear separation of concerns and full type safety using Pydantic schemas.

- **Language:** Python 3.11+
- **Framework:** FastAPI (skeleton, to be fully implemented)
- **Database:** SQLite (demo, file-based)
- **AI/ML:** Azure OpenAI API (for chat, recommendations, sentiment)
- **Seed Data:** JSON files for demo/test data
- **Testing:** pytest (TDD-first)

---

## Directory Structure

```
backend/
├── .env, .env.example         # Environment variables (API keys, DB path)
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Project metadata/config
├── uv.lock                    # Package lockfile
├── src/app/
│   ├── main.py                # Entrypoint (FastAPI app skeleton)
│   ├── core/                  # Core utilities (config, db)
│   │   ├── config.py
│   │   └── db.py
│   ├── models/                # Pydantic schemas (API/data validation)
│   │   ├── __init__.py
│   │   ├── pydantic_schemas.py
│   │   └── schemas.py
│   ├── data/                  # Data storage and access
│   │   ├── database/          # SQLite DB file (app.db)
│   │   ├── seeds/             # JSON seed data (departments, employees, etc.)
│   │   ├── seed_data.py       # Seed loader script
│   │   └── repositories/      # Repository pattern (data access layer)
│   ├── services/              # Business logic layer (service classes)
│   ├── api/v1/                # API contracts (type-annotated, versioned)
│   └── agent/                 # AI agent modules (OpenAI, LangChain, etc.)
└── tests/                     # Test scaffolding (pytest, TDD)
```

---

## Folder-by-Folder Guide

### `src/app/core/`
- **config.py**: Centralized configuration (env vars, OpenAI settings)
- **db.py**: SQLite helpers, schema creation, and DB connection logic

### `src/app/models/`
- **pydantic_schemas.py**: Pydantic models for all DB entities (Base/Create/Detail variants)
- **schemas.py**: (Legacy/extra schemas, if any)

### `src/app/data/`
- **database/**: SQLite DB file (`app.db`)
- **seeds/**: JSON files for demo/test data (departments, employees, skills, etc.)
- **seed_data.py**: Script to load all seed data into the DB
- **repositories/**: Repository classes for each entity (CRUD/data access)

### `src/app/services/`
- Service classes for business logic (e.g., `employee_service.py`, `marketplace_service.py`)
- Each service uses repositories for data access and implements domain logic

### `src/app/api/v1/`
- API route contracts (one file per domain: `employees.py`, `wellbeing.py`, etc.)
- Type-annotated, docstring-documented, ready for FastAPI wiring

### `src/app/agent/`
- AI agent modules (e.g., `course_recommendation_agent/`, `well_being_agent/`)
- `sample_azure_openai_usage.py`: Example of raw Azure OpenAI API usage
- `sample_langchain_azure_agent.py`: Example of LangChain agent with Azure OpenAI
- `mentoring_agent/`: Calculates mentor/mentee compatibility scores and explanations

### `tests/`
- Test scaffolding for repositories, services, and API (pytest)
- TDD-first: always write tests before implementation

## Mentoring Agent & Match Requests

- Ensure Azure OpenAI environment variables (`AZURE_OPENAI_*`) are configured; the mentoring agent falls back to heuristic scoring if the LLM is unavailable.
- New endpoints:
  - `POST /api/v1/auth/employee-login` – validate employee ID and return session profile.
  - `GET|POST|DELETE /api/v1/matching/request/{mentee_id}` – manage single active mentor applications per mentee.
  - `GET /api/v1/matching/mentors` and `/mentees` – browse employees sourced from SQLite.
- SQLite now stores `position_level` per employee; run the included migration (automatic via `init_db`) or reload seeds to backfill data.
Frontend -> API -> services -> repositories -> database
---
