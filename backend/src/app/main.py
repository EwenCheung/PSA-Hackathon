"""
Application entrypoint for the PSA Future-Ready Workforce API.

Exposes FastAPI routing for employees, wellbeing, marketplace, analytics,
and mentorship capabilities.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import wellbeing

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
