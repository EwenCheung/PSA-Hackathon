"""
Application entrypoint

Hosts the FastAPI application and wires v1 routers as they come online.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.analytics import router as analytics_router
from app.core.db import get_connection, init_db
from app.data.seed_data import load_all_seeds

APP_DESCRIPTION = "Future-Ready Workforce Agent Platform API"

app = FastAPI(
    title="PSA Hackathon API",
    description=APP_DESCRIPTION,
    version="0.1.0",
)

# Allow the Vite dev server and other origins during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wire up available routes.
app.include_router(analytics_router)


@app.on_event("startup")
def startup() -> None:
    """
    Ensure the SQLite schema exists and demo data is loaded for local runs.
    """
    conn = get_connection()
    try:
        init_db(conn)
        load_all_seeds(conn)
    finally:
        conn.close()


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Health check endpoint for uptime monitoring."""
    return {"status": "ok"}
