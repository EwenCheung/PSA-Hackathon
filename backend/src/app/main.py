"""
Application entrypoint

FastAPI application wiring v1 routers:
- employees, wellbeing, marketplace, sample

The actual route handlers are defined in api/v1/ modules.
This file just creates the app and includes the routers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.v1 import employees, wellbeing, marketplace, sample
from app.core.config import settings

APP_DESCRIPTION = "Future-Ready Workforce Agent Platform API"

# Create FastAPI app
app = FastAPI(
    title="PSA Future-Ready Workforce Platform",
    description=APP_DESCRIPTION,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS to allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from api/v1
app.include_router(employees.router)
app.include_router(wellbeing.router)
app.include_router(marketplace.router)
app.include_router(sample.router)  # Example router showing the pattern


# Health check endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "PSA Future-Ready Workforce Platform API is running",
        "version": "0.1.0",
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "environment": settings.env,
        "anonymous_mode": settings.enable_anonymous_mode,
    }


def start_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """Start the FastAPI server with uvicorn"""
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    # Run the server when executing this file directly
    start_server()

APP_DESCRIPTION = "Future-Ready Workforce Agent Platform API"

app = FastAPI(
  title="PSA Future-Ready Workforce Platform",
  description=APP_DESCRIPTION,
  version="0.1.0",
  docs_url="/docs",
  redoc_url="/redoc",
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(wellbeing.router)


@app.get("/", tags=["Health"])
def root() -> dict:
  return {
    "status": "ok",
    "message": "PSA Future-Ready Workforce Platform API is running",
    "version": "0.1.0",
  }


@app.get("/health", tags=["Health"])
def health_check() -> dict:
  return {"status": "healthy"}
