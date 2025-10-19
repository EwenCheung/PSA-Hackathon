## Project overview

PSA Future-Ready Workforce (PSA Hackathon) is an AI-assisted platform for employee career development, wellbeing, mentorship, and skills/learning management. The repository is a monorepo with a TypeScript/React frontend (Vite) and a Python FastAPI backend (src/app). The backend exposes versioned REST APIs and integrates with AI services (OpenAI/Azure OpenAI and LangChain).

This document captures the project's tech stack, conventions, run/test instructions, and contributor guidance so maintainers and new contributors can onboard quickly.

## Tech stack

- Backend
	- Language: Python 3.11+ (pyproject.toml target)
	- Web framework: FastAPI
	- ASGI server: Uvicorn (recommended with [standard] extras)
	- Data validation/settings: Pydantic v2 + pydantic-settings
	- DB (development/demo): SQLite (file-based under src/app/data/database)
	- AI integrations: openai, langchain (langchain-openai)
	- Testing: pytest, pytest-asyncio, httpx, pytest-cov (configured in pyproject)
	- Tooling: black, ruff, mypy (optional), python-dotenv

- Frontend
	- Framework: React 18 + TypeScript
	- Bundler: Vite
	- Styling: Tailwind CSS
	- UI primitives: Radix UI components
	- Utilities: react-hook-form, recharts, sonner, lucide-react

- Dev / CI
	- Recommend GitHub Actions for test/format/lint pipeline
	- Local development via virtualenv (Python) and pnpm/npm for frontend

## Architecture & conventions

- Layering: Frontend -> API (versioned) -> Services -> Repositories -> Database
	- API layer (src/app/api/v1/) contains FastAPI routers and request/response models.
	- Services (src/app/services/) contain business logic, orchestrate repositories and agents.
	- Repositories (src/app/data/repositories/) encapsulate raw SQL/data access.
	- Core helpers (src/app/core/) include DB connection and app configuration.

- API versioning: routes live under `/api/v1/` — when breaking changes are needed, add `/api/v2/` and keep v1 stable.

- Error handling: routes should return appropriate HTTP status codes and structured errors (`{"detail": "..."}`).

- Type safety: use Pydantic models from `src/app/models/pydantic_schemas.py` for all request/response and internal DTOs.

- Formatting and linting:
	- Format Python with `black` (configured in pyproject.toml)
	- Lint with `ruff`
	- Prefer type annotations on public functions and service/repository boundaries.

- Database migrations: currently SQLite is used for demo. If migrating to Postgres, add Alembic or use SQLModel migrations.

## Tests

- Backend tests: located in `backend/tests/` and use pytest. Tests expect the Python package root as `src/`.

- Running tests locally (recommended)

	- Create and activate virtualenv (macOS / zsh):

	```bash
	cd backend
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -U pip setuptools wheel
	pip install -r requirements.txt
	```

	- Run a single test file (ignore project-wide pytest addopts coverage flags when debugging):

	```bash
	# ensure src is on PYTHONPATH so `app` package resolves
	PYTHONPATH=src PYTEST_ADDOPTS= python -m pytest tests/test_dev_api.py -v
	```

## Run & dev commands

- Backend (run locally):

```bash
cd backend
# activate venv
source .venv/bin/activate
# start server
uvicorn src.app.main:app --reload --port 8000
# Open API docs: http://localhost:8000/docs
```

- Frontend (dev):

```bash
cd frontend
pnpm install # or npm install
pnpm dev
# open http://localhost:5173
```

## Environment variables

- Keep secrets in `.env` and never commit them. Include `.env.example` with placeholders.
- Common variables:
	- OPENAI_API_KEY or AZURE_OPENAI_*
	- DATABASE_URL (for production DB)
	- SENTRY_DSN (optional)

## CI / Quality gates (recommended)

- Basic GitHub Actions workflow should run on push/PR and include:
	1. Python job: install dependencies, run `ruff`, `black --check`, `mypy` (optional), and `pytest`.
	2. Node job: install dependencies and run `pnpm build` to ensure frontend builds.

- Example quick PR checks:
	- black --check
	- ruff check
	- python -m pytest

## Git & contribution conventions

- Branching:
	- Feature branches: `feature/<short-desc>`
	- Bugfix branches: `fix/<short-desc>`
	- Release branches/tags follow semver

- Commits:
	- Use concise commit messages. Prefer Conventional Commits if you want automated changelogs (e.g., `feat:`, `fix:`, `chore:`).

- PR requirements:
	- At least one approving review
	- CI passing (lint + tests)
	- Descriptive PR body with motivation and testing notes

## Security & secrets

- Do not commit `.env` or any credentials. Keep secrets in GitHub Actions secrets for CI and use a secrets manager for production.

## Developer ergonomics & troubleshooting

- If you see PEP 668 `externally-managed-environment` errors when installing, ensure a virtualenv is active (recommended) or pass `--break-system-packages` if you understand the implications.

- If Python in `.venv` fails with `ModuleNotFoundError: No module named 'encodings'`, recreate the venv using the system Python: `python3 -m venv .venv`.

## Suggested next steps

- Add `CONTRIBUTING.md` with step-by-step onboarding and PR checklist.
- Add a minimal GitHub Actions workflow for backend tests and frontend build.
- Add migrations (Alembic) if you plan to move from SQLite to Postgres.

## Contacts

- PSA Hackathon Team / repository contributors (see Git history for names and GitHub handles).

---

Last updated: 2025-10-19
