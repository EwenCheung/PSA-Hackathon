"""
Application entrypoint

FastAPI application wiring v1 routers:
- employees, wellbeing, marketplace, analytics, matching, mentoring
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.mentoring_router import router as mentoring_router

APP_DESCRIPTION = "Future-Ready Workforce Agent Platform API"

# Create FastAPI application
app = FastAPI(
    title="PSA Hackathon - Future Ready Workforce API",
    description=APP_DESCRIPTION,
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(mentoring_router)

# Health check endpoints
@app.get("/")
async def root():
    return {
        "message": "PSA Hackathon API - Future Ready Workforce",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

