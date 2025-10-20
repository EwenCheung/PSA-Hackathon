# PSA Hackathon (PathForger)
Monorepo containing a FastAPI backend and a Vite/React frontend for the PSA Hackathon prototype. Use the automation in `Prototype_ThreeMusketeer/` to spin up both services consistently.

## Quick start
- `Prototype_ThreeMusketeer/start_server.sh` orchestrates the full stack. Run with `--dry-run` first if you want to preview the commands.
- The launcher performs:
  1. Navigate to `backend/`, run `uv sync`, activate `.venv`, and launch `uvicorn app.main:app --reload` on port 8000.
  2. Navigate to `frontend/`, run `npm install`, and start `npm run dev` (Vite on port 5173).
- On errors the script reminds you to shut down conflicting servers (FastAPI or Vite) before retrying.

```bash
cd Prototype_ThreeMusketeer
bash start_server.sh             # start both servers (Ctrl+C stops them)
bash start_server.sh --dry-run   # preview commands only
```

### Manual startup (alternative workflow)
If you prefer to launch services manually, follow the flow many teammates use:

1. Backend terminal
   ```bash
   cd backend
   uv sync
   source .venv/bin/activate
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir src
   ```
   Wait for the backend to finish initial sync and boot (typically 5–10 minutes on first run) before starting the frontend.

2. Frontend terminal (new shell window/tab)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

This path mirrors what the launcher automates, but gives you granular control over each process.

## Architecture Overview
- **Platform vision**: PathForger is an AI-powered growth platform helping employees build leadership potential while giving employers a real-time picture of workforce readiness.
- **Modular AI agents**: The backend hosts dedicated agents for course recommendations, wellbeing analysis, leadership evaluation, and mentor matching. Each agent encapsulates prompts, policies, and data pipelines for its domain.
- **Vector intelligence**: Skill, role, and goal data are embedded into a vector index so the recommendation agent can surface the top courses for each employee with explanations.
- **Central data hub**: A secure SQL database stores employee profiles, skill taxonomies, engagement telemetry, and mentorship activity. Repositories in `backend/src/app/data/` abstract reads/writes.
- **Extensibility**: The service layer is designed to plug into enterprise systems (e.g., SAP, Workday) by swapping repository adapters without touching the agent logic.
- **Front-end shell**: React + Vite provide a responsive experience, with view modules composed so that Employee and Employer dashboards share UI primitives while presenting role-specific insights.

## Employee View Experience
- **Personalised course intelligence**: Employees sign in, trigger the embeddings pipeline, and receive the top three course matches with rationale anchored to their skills, aspirations, and current role.
- **Career path navigator**: A roadmap breaks growth into short-term (0–6 months), mid-term (6–18 months), and long-term (18+ months) stages with focus areas, actions, and likely future roles.
- **Leadership readiness scoring**: Agents evaluate proactive learning, skill velocity, and emotional steadiness to flag leadership potential and highlight improvement levers.
- **Mentorship orchestration**: Requests go through an AI matcher that pairs mentees with mentors based on expertise, goals, and compatibility. The agent keeps sessions on track, nudging both sides if progress stalls.
- **Wellbeing agent**: Sentiment analysis monitors mood shifts, suggests interventions, routes to resources, and coordinates schedules to prevent burnout while respecting privacy.
- **Gamification layer**: Employees earn redeemable points by completing courses, mentoring colleagues, reaching milestones, and maintaining wellbeing streaks—turning growth into a rewarding loop.

## Employer Insights Dashboard
- **Real-time workforce intelligence**: Dashboards surface top performers, leadership candidates, and emerging skill gaps so managers can prioritise interventions.
- **Single-load analytics**: Insights hydrate once from the database, then stream updates, tracking course adoption, skill trends, and engagement momentum without reloading the full view.
- **Mentorship oversight**: Employers observe mentor capacity, request queues, and programme health, receiving alerts when pairings need support.
- **Strategic planning**: Aggregated analytics spotlight future leaders, critical skill shortages, and training ROI, enabling data-driven promotion and reskilling decisions.

## Vision and Roadmap
- **Holistic growth**: PathForger unites learning, leadership development, wellbeing, and gamification so employees see a full 360° view of their career trajectory.
- **Actionable employer value**: Organisations translate platform telemetry into targeted training, balanced mentorship programmes, and early identification of leadership pipelines.
- **Future-ready evolution**: The modular architecture keeps the platform adaptable, paving the way for deeper enterprise integrations, additional agents, and region-specific content.
- **Where growth meets opportunity**: By aligning engagement, insight, and development, PathForger forges leaders while keeping teams energised for what’s next.

## Backend notes
- Code lives in `backend/src/app/` (agents, repositories, and data files under `data/`).
- Requires Python 3.10+ and the [`uv`](https://github.com/astral-sh/uv) tool for dependency syncing. After activation, the FastAPI app is served at `http://localhost:8000`.
- Seed JSON and the SQLite database reside under `backend/src/app/data/` (check `database/app.db`).

## Frontend notes
- Vite + React (TypeScript) lives in `frontend/` with shared UI primitives under `src/components/`.
- `npm run dev` serves the UI on `http://localhost:5173` with hot reload.

## Testing & validation
- Shell smoke tests live under `tests/`. Run `tests/test_start_server.sh` to ensure the launcher script keeps its contract intact.
- Add Python tests under `backend/tests/` (pytest) and frontend tests under `frontend/src/__tests__/` (Vitest) as features grow.

## Troubleshooting
- `uv sync` failures: ensure the `.venv` folder exists and no other Python process is locking dependencies.
- Port conflicts: stop existing FastAPI or Vite instances (`lsof -i :8000` / `lsof -i :5173`) before re-running the launcher.
- `npm install` permission errors often stem from global cache issues; clear `~/.npm` or retry after closing other Node processes.

## Contributing guidelines
- Keep backend and frontend changes in separate commits when practical.
- Document new automation or setup steps in `Prototype_ThreeMusketeer/README.md` so the whole team stays aligned.
