"""
Core: config

Purpose
- Centralize environment configuration and feature flags.

Usage
- Import settings to configure services (e.g., LLM keys, toggles).
"""
import os
from dataclasses import dataclass


@dataclass
class Settings:
    env: str = os.getenv("APP_ENV", "dev")
    enable_anonymous_mode: bool = os.getenv("ENABLE_ANON", "true").lower() not in {"0", "false", "no"}
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")


settings = Settings()

