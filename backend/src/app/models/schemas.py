"""
Models: schemas (contracts)

Purpose
- Define data contracts exchanged with frontend. Using TypedDict for zero-dep tests.
  Replace with Pydantic BaseModel when wiring FastAPI.
"""
from typing import List, Literal, Optional, TypedDict


class Employee(TypedDict, total=False):
    id: str
    name: str
    role: str
    department: str
    level: str
    points: int
    goals: List[str]
    skills: List[str]
    courses: dict


class Course(TypedDict, total=False):
    id: str | int
    title: str
    description: str
    difficulty: Literal["Beginner", "Intermediate", "Advanced"]
    duration: str
    effort: str
    points: int
    roi: Literal["Medium", "High", "Very High"]
    progress: int
    status: Literal["not-started", "in-progress", "completed"]
    skills: List[str]


class Message(TypedDict, total=False):
    id: int
    sender: Literal["user", "ai"]
    content: str
    timestamp: str
    isAnonymous: bool


class MarketplaceItem(TypedDict, total=False):
    id: str | int
    name: str
    description: str
    points: int
    category: str
    inStock: bool


class Mentor(TypedDict, total=False):
    id: str
    name: str
    role: str
    expertise: List[str]
    capacity: int
    mentees: int
    points: int
    rating: float
    personality: str


class Mentee(TypedDict, total=False):
    id: str
    name: str
    role: str
    goals: List[str]
    personality: str
    matchedWith: Optional[str]

