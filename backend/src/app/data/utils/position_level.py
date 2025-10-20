"""
Utilities for deriving numeric position levels from textual descriptors.
"""
from __future__ import annotations

LEVEL_MAP: dict[str, int] = {
    "intern": 1,
    "apprentice": 1,
    "trainee": 1,
    "junior": 2,
    "associate": 2,
    "specialist": 3,
    "mid": 3,
    "mid-level": 3,
    "mid level": 3,
    "consultant": 3,
    "senior": 4,
    "lead": 5,
    "principal": 6,
    "manager": 5,
    "director": 6,
    "head": 6,
    "vp": 7,
    "executive": 7,
    "chief": 8,
}

DEFAULT_LEVEL = 1


def derive_position_level(level_text: str | None = None, explicit: int | None = None) -> int:
    """
    Determine numeric position level.

    Args:
        level_text: Textual descriptor (e.g., \"Senior\", \"Mid-Level\")
        explicit: Provided numeric level which takes precedence

    Returns:
        Integer level suitable for mentor/mentee comparisons.
    """
    if explicit is not None:
        return explicit

    if not level_text:
        return DEFAULT_LEVEL

    normalized = level_text.strip().lower()
    return LEVEL_MAP.get(normalized, DEFAULT_LEVEL)
