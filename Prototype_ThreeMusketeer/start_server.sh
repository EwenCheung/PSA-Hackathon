#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: start_server.sh [--dry-run]

Bootstraps the backend (FastAPI) and frontend (Vite) development servers
for the PSA Hackathon prototype.

Options:
  --dry-run   Print the commands that would be executed without running them.
  -h, --help  Show this help message.
USAGE
}

DRY_RUN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

BACKEND_PID=""
FRONTEND_PID=""

handle_failure() {
  echo "Error while setting up the environment. Please shut down any running FastAPI or Vite instances and retry." >&2
  exit 1
}

run_command() {
  local label=$1
  shift
  echo "Running: $label"
  if [[ $DRY_RUN -eq 1 ]]; then
    return
  fi

  if ! "$@"; then
    handle_failure
  fi
}

run_command_bg() {
  local label=$1
  shift
  echo "Running: $label"
  if [[ $DRY_RUN -eq 1 ]]; then
    return
  fi

  "$@" &
  local pid=$!
  if [[ -z $BACKEND_PID ]]; then
    BACKEND_PID=$pid
  else
    FRONTEND_PID=$pid
  fi
}

cleanup() {
  if [[ -n $BACKEND_PID ]]; then
    kill "$BACKEND_PID" >/dev/null 2>&1 || true
  fi
  if [[ -n $FRONTEND_PID ]]; then
    kill "$FRONTEND_PID" >/dev/null 2>&1 || true
  fi
}

trap cleanup EXIT

echo "Switching to backend directory: $BACKEND_DIR"
if [[ $DRY_RUN -eq 0 ]]; then
  cd "$BACKEND_DIR"
fi
run_command "uv sync" uv sync
run_command "source .venv/bin/activate" bash -c "source .venv/bin/activate"
run_command_bg "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir src" \
  bash -c "source .venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir src"

if [[ $DRY_RUN -eq 0 ]]; then
  cd "$ROOT_DIR"
fi

echo "Switching to frontend directory: $FRONTEND_DIR"
if [[ $DRY_RUN -eq 0 ]]; then
  cd "$FRONTEND_DIR"
fi
run_command "npm install" npm install
run_command_bg "npm run dev" npm run dev

if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry run complete."
  exit 0
fi

echo "Backend and frontend servers are starting. Press Ctrl+C to stop both."

wait
