# Prototype Three Musketeer
Helper utilities for orchestrating the PSA Hackathon prototype from a single entrypoint.

## start_server.sh
- Ensures the FastAPI backend and Vite frontend run together with predictable steps.
- Accepts `--dry-run` to print the commands without executing them.
- Prints guidance to shut down existing servers if a step fails (e.g., port already in use).

### Prerequisites
- Bash 5+, `uv` installed and on PATH.
- Python 3.10+ virtual environment available at `backend/.venv/` (created automatically by `uv sync`).
- Node 18+ with npm available for frontend dependencies.

### Usage
```bash
cd Prototype_ThreeMusketeer
bash start_server.sh --dry-run  # optional: preview
bash start_server.sh            # launches backend + frontend
```

The script will:
1. Change into `../backend`, run `uv sync`, activate `.venv`, and start `uvicorn app.main:app --reload` on port 8000.
2. Return to the repo root, move into `../frontend`, run `npm install`, and start `npm run dev` on port 5173.

Back-end and front-end processes run in the background; pressing `Ctrl+C` in the terminal stops both.

### Testing
- `tests/test_start_server.sh` verifies the dry-run output so README instructions stay accurate. Update the test if you change the command sequence or messaging.

### Troubleshooting
- Backend step fails immediately: confirm no existing uvicorn process is using port 8000 and that `.venv` exists.
- Frontend step fails with permission issues: close other Node processes and clear `~/.npm` if necessary before rerunning.
