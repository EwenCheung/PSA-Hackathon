"""
Pydantic Schemas for all database entities (Phase 2)

- Each entity has Base, Create, and Detail variants as needed
- Used for API request/response validation and serialization
- All fields are type-annotated and documented

Note: This file is auto-generated for Phase 2. Please review and adjust as needed.
"""
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

# --- Department ---
class DepartmentBase(BaseModel):
    id: str = Field(..., description="Department ID")
    name: str

class DepartmentCreate(BaseModel):
    id: str
    name: str

class DepartmentDetail(DepartmentBase):
    pass

# --- Employee ---
class EmployeeBase(BaseModel):
    id: str
    name: str
    role: str
    department_id: str
    level: str
    points_current: int
    hire_date: Optional[str]
    skills_map: Optional[str]
    courses_enrolled_map: Optional[str]
    goals_set: Optional[str]

class EmployeeCreate(BaseModel):
    name: str
    role: str
    department_id: str
    level: str
    points_current: int = 0
    hire_date: Optional[str] = None
    skills_map: Optional[str] = None
    courses_enrolled_map: Optional[str] = None
    goals_set: Optional[str] = None

class EmployeeDetail(EmployeeBase):
    pass

# --- Skill ---
class SkillBase(BaseModel):
    id: str
    name: str
    category: str

class SkillCreate(BaseModel):
    id: str
    name: str
    category: str

class SkillDetail(SkillBase):
    pass

# --- Course ---
class CourseBase(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str
    duration_weeks: int
    effort_hours_week: int
    points_reward: int
    roi: str
    active: int

class CourseCreate(BaseModel):
    title: str
    description: str
    difficulty: str
    duration_weeks: int
    effort_hours_week: int
    points_reward: int
    roi: str
    active: int = 1

class CourseDetail(CourseBase):
    pass

# --- CourseSkill ---
class CourseSkillBase(BaseModel):
    course_id: str
    skill_id: str
    weight: int

class CourseSkillCreate(CourseSkillBase):
    pass

class CourseSkillDetail(CourseSkillBase):
    pass

# --- Enrollment ---
class EnrollmentBase(BaseModel):
    employee_id: str
    course_id: str
    status: str
    progress_percent: int
    started_at: Optional[str]
    completed_at: Optional[str]
    points_awarded: Optional[int]

class EnrollmentCreate(BaseModel):
    employee_id: str
    course_id: str
    status: str
    progress_percent: int = 0
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    points_awarded: Optional[int] = None

class EnrollmentDetail(EnrollmentBase):
    pass

# --- Goal ---
class GoalBase(BaseModel):
    id: Optional[int]
    employee_id: str
    title: str
    target_date: str
    progress_percent: int

class GoalCreate(BaseModel):
    employee_id: str
    title: str
    target_date: str
    progress_percent: int = 0

class GoalDetail(GoalBase):
    pass

# --- WellbeingMessage ---
class WellbeingMessageBase(BaseModel):
    id: Optional[int]
    employee_id: str
    anon_session_id: Optional[str]
    sender: str
    content: str
    timestamp: str
    is_anonymous: int = 0

class WellbeingMessageCreate(BaseModel):
    """Request payload for wellbeing chat messages."""

    content: str = Field(..., description="Message content from the employee")
    is_anonymous: bool = Field(default=False, description="Flag indicating anonymous mode")
    anon_session_id: Optional[str] = Field(default=None, description="Existing anonymous session identifier")

class WellbeingMessageDetail(WellbeingMessageBase):
    pass

# --- SentimentMessage ---
class SentimentMessageBase(BaseModel):
    id: Optional[int]
    message_id: int
    label: str
    score: float
    confidence: float
    created_at: str

class SentimentMessageCreate(BaseModel):
    message_id: int
    label: str
    score: float
    confidence: float
    created_at: str

class SentimentMessageDetail(SentimentMessageBase):
    pass

# --- SentimentSnapshot ---
class SentimentSnapshotBase(BaseModel):
    id: Optional[int]
    employee_id: str
    anon_session_id: Optional[str]
    day: str
    label: str
    average_score: float
    messages_count: int
    created_at: str

class SentimentSnapshotCreate(BaseModel):
    employee_id: str
    anon_session_id: Optional[str] = None
    day: str
    label: str
    average_score: float
    messages_count: int
    created_at: str

class SentimentSnapshotDetail(SentimentSnapshotBase):
    pass

# --- MentorshipProfile ---
class MentorshipProfileBase(BaseModel):
    employee_id: str
    is_mentor: int = 0
    capacity: int
    mentees_count: int
    rating: float
    personality: str

class MentorshipProfileCreate(BaseModel):
    employee_id: str
    is_mentor: int = 0
    capacity: int
    mentees_count: int = 0
    rating: float = 0.0
    personality: str

class MentorshipProfileDetail(MentorshipProfileBase):
    pass

# --- MentorshipMatch ---
class MentorshipMatchBase(BaseModel):
    id: Optional[int]
    mentor_id: str
    mentee_id: str
    score: float
    reasons_json: Optional[str]
    status: str
    created_at: str

class MentorshipMatchCreate(BaseModel):
    mentor_id: str
    mentee_id: str
    score: float
    reasons_json: Optional[str] = None
    status: str
    created_at: str

class MentorshipMatchDetail(MentorshipMatchBase):
    pass

# --- MentorSession ---
class MentorSessionBase(BaseModel):
    id: Optional[int]
    mentor_id: str
    mentee_id: str
    session_date: str
    notes: Optional[str]
    points_awarded: Optional[int]

class MentorSessionCreate(BaseModel):
    mentor_id: str
    mentee_id: str
    session_date: str
    notes: Optional[str] = None
    points_awarded: Optional[int] = None

class MentorSessionDetail(MentorSessionBase):
    pass

# --- MarketplaceItem ---
class MarketplaceItemBase(BaseModel):
    id: int
    name: str
    description: str
    points_cost: int
    category: str
    in_stock: int = 1

class MarketplaceItemCreate(BaseModel):
    name: str
    description: str
    points_cost: int
    category: str
    in_stock: int = 1

class MarketplaceItemDetail(MarketplaceItemBase):
    pass

# --- Redemption ---
class RedemptionBase(BaseModel):
    id: Optional[int]
    employee_id: str
    item_id: int
    points_cost: int
    created_at: str

class RedemptionCreate(BaseModel):
    employee_id: str
    item_id: int
    points_cost: int
    created_at: str

class RedemptionDetail(RedemptionBase):
    pass

# --- PointsLedger ---
class PointsLedgerBase(BaseModel):
    id: Optional[int]
    employee_id: str
    delta: int
    source: str
    reference_id: Optional[str]
    created_at: str

class PointsLedgerCreate(BaseModel):
    employee_id: str
    delta: int
    source: str
    reference_id: Optional[str] = None
    created_at: str

class PointsLedgerDetail(PointsLedgerBase):
    pass

# --- LeadershipPotentialPrediction ---
class LeadershipPotentialPredictionBase(BaseModel):
    id: Optional[int]
    employee_id: str
    model_version: str
    score: float
    label: str
    factors_json: Optional[str]
    created_at: str

class LeadershipPotentialPredictionCreate(BaseModel):
    employee_id: str
    model_version: str
    score: float
    label: str
    factors_json: Optional[str] = None
    created_at: str

class LeadershipPotentialPredictionDetail(LeadershipPotentialPredictionBase):
    pass
