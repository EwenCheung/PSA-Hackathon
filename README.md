# PSA-Hackathon (PathForger)
Short repo README to onboard developers quickly. Contains frontend and backend run instructions, data locations, and agent/embeddings notes.

## Project overview
- Monorepo with two main areas:
  - `frontend/` — Vite + React + TypeScript UI (components under `components/`).
  - `backend/` — Python services and data layer under `backend/src/app/` (agents, repositories, seeds, DB).

This project prototypes a course-recommendation agent that uses repository-backed seed data, embeddings, and a small LangChain-based agent.

## Quick start (developer)

Prerequisites
- Node 18+ / npm or pnpm for frontend
- Python 3.10+ (3.11 recommended) and virtualenv/venv for backend

1) Start the frontend

```bash
cd frontend
npm install
npm run dev
```

The UI runs on Vite (default port 5173). `frontend-sample/` is a duplicate/reference app — confirm which to modify before sweeping changes.

2) Backend setup

Create and activate a Python virtual environment, install dependencies (if `requirements.txt` exists), and set `PYTHONPATH` so `backend/src` is importable:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # if present
export PYTHONPATH=$(pwd)/src
```

3) Environment variables

Create a `.env` in `backend/` with at least the following for Azure OpenAI usage (if you use embeddings/LLM):

```env
AZURE_OPENAI_API_KEY=sk-...
DEPLOYMENT=text-embedding-3-small
API_VERSION=2023-05-15
AZURE_OPENAI_ENDPOINT=https://psacodesprint2025.azure-api.net
```

Note: some modules set `AZURE_OPENAI_ENDPOINT` or `AZURE_OPENAI_API_KEY` into `os.environ` at runtime; ensure your `.env` values are present before importing agent modules.

## Database & seed data
- SQLite DB (expected path): `backend/src/app/data/database/app.db`
- Seed JSON files: `backend/src/app/data/seeds/*.json` (examples: `courses.json`, `skills.json`, `course_skills.json`, `employees.json`)
- Repositories (read/write and sync logic) live under `backend/src/app/data/repositories/`.

To sync `course_skills.json` into the DB (script provided):

```bash
export PYTHONPATH=$(pwd)/src
python backend/src/app/data/repositories/sync_course_skills.py
```

The sync script will look for the DB at `backend/src/app/data/database/app.db` and the JSON at `backend/src/app/data/seeds/course_skills.json`.

## Agent & embeddings (where things live)
- Agent entrypoint: `backend/src/app/agent/course_recommendation_agent/main.py` — responsible for loading `.env`, instantiating the LLM (`AzureChatOpenAI`), creating the agent, and invoking it.
- Tooling: `backend/src/app/agent/course_recommendation_agent/tools.py` — exposes `recommend_courses_tool` and `get_employee_context`. This module reads data from the repository layer and builds documents for embedding.
- Embeddings & vectorstore: currently built in `tools.py` during initialization in this tree. For production or larger data sets, prefer extracting this logic into a lazy provider (e.g., `embeddings_store.py`) that builds/persists the FAISS index on first use.

Important runtime notes
- Building FAISS/embeddings at import time may block or fail if environment variables or packages are missing. Tests and CLI scripts in this repo add defensive fallbacks; if you see import errors, ensure `PYTHONPATH` and `.env` are set before running.
- If `langchain` / `faiss` imports fail, the tools include keyword-overlap fallbacks so the service can still return recommendations (less accurate than embeddings).

## Useful quick commands
- Run agent main (example):

```bash
export PYTHONPATH=$(pwd)/backend/src
python backend/src/app/agent/course_recommendation_agent/main.py
```

- Run the tools self-test to print sample courses/employees/skills:

```bash
export PYTHONPATH=$(pwd)/backend/src
python backend/src/app/agent/course_recommendation_agent/tools.py
```

## Project structure (high level)
- backend/
  - src/app/agent/course_recommendation_agent/  (agent main, tools, system prompts)
  - src/app/data/repositories/  (CourseRepository, CourseSkillRepository, EmployeeRepository, SkillRepository, sync scripts)
  - src/app/data/seeds/  (seed JSONs)
  - src/app/data/database/  (SQLite DB: app.db)
- frontend/  (Vite + React UI)

## Troubleshooting
- If imports for `langchain`, `langchain_openai`, or `faiss` fail, either install the required packages (see `requirements.txt`) or run the backend self-test which uses fallbacks.
- If the sync script reports the DB not found, confirm `backend/src/app/data/database/app.db` exists and that you ran it with `PYTHONPATH` set to `backend/src`.
- If the agent prints unexpected response objects, run `main.py` and paste the printed repr; the codebase already includes tolerant response printers that can be extended.

## Contributing
- Add small, focused PRs. When adding backend services, include a `README`, `.env.example`, and tests.
- Keep UI changes in `frontend/` and reuse `components/ui/` primitives.

If you'd like, I can scaffold `embeddings_store.py` (lazy vectorstore provider) and a `db.py` connection helper and update `tools.py`/`main.py` to use them — say the word and I will implement it.
