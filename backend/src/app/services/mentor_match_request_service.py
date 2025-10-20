"""Service layer for mentor match requests."""
from __future__ import annotations

import json
from contextlib import suppress
from datetime import UTC, datetime, date
from typing import Dict, Iterable, List, Optional

from app.data.repositories.department import DepartmentRepository
from app.data.repositories.employee import EmployeeRepository
from app.data.repositories.mentor_match_request import MentorMatchRequestRepository
from app.data.repositories.mentorship_match import MentorshipMatchRepository
from app.data.repositories.mentorship_profile import MentorshipProfileRepository
from app.data.repositories.skill import SkillRepository


class MentorMatchingService:
    """Co-ordinates mentor matching interactions with the database."""

    def __init__(self, conn):
        self.conn = conn
        self.employee_repo = EmployeeRepository(conn)
        self.profile_repo = MentorshipProfileRepository(conn)
        self.request_repo = MentorMatchRequestRepository(conn)
        self.match_repo = MentorshipMatchRepository(conn)
        self.skill_repo = SkillRepository(conn)
        self.department_repo = DepartmentRepository(conn)

    # --------------------------------------------------------------------- #
    # Mentor discovery
    # --------------------------------------------------------------------- #
    def _resolve_employee_id(self, employee_id: str) -> Optional[str]:
        if not employee_id:
            return None

        profile = self.employee_repo.get_employee_profile(employee_id)
        if profile:
            return employee_id

        normalized = employee_id.upper()
        if normalized.startswith("EP") and normalized[2:].isdigit():
            digits = normalized[2:]
            width = max(len(digits.lstrip("0")) or 1, 3)
            canonical = f"EMP{int(digits):0{width}d}"
            profile = self.employee_repo.get_employee_profile(canonical)
            if profile:
                return canonical

        return employee_id if self.employee_repo.get_employee_profile(employee_id) else None

    def _ensure_employee_profile(self, employee_id: str, role: str) -> dict:
        resolved = self._resolve_employee_id(employee_id)
        if not resolved:
            raise LookupError(f"{role} {employee_id} not found")

        profile = self.employee_repo.get_employee_profile(resolved)
        if not profile:
            raise LookupError(f"{role} {employee_id} not found")
        return profile
    def list_mentors(
        self,
        mentee_id: Optional[str] = None,
        skill_area: Optional[str] = None,
        department: Optional[str] = None,
    ) -> List[Dict]:
        canonical_mentee_id: Optional[str] = None
        mentee_profile = None
        mentee_position = None
        if mentee_id:
            mentee_profile = self._ensure_employee_profile(mentee_id, "Employee")
            mentee_position = mentee_profile.get("position_level")
            canonical_mentee_id = mentee_profile.get("id") or mentee_id

        mentors: List[Dict] = []
        for employee in self.employee_repo.list_employees():
            employee_id = employee.get("id")
            if canonical_mentee_id and employee_id == canonical_mentee_id:
                continue

            mentor_position = employee.get("position_level")
            if mentee_position is not None and (
                mentor_position is None or mentor_position <= mentee_position
            ):
                continue

            if department and employee.get("department_id") != department:
                continue

            raw_employee = self.employee_repo.get_employee_row(employee_id) or {}
            mentor_profile = self.profile_repo.get_profile(employee_id) or {}

            if skill_area:
                skill_area_lower = skill_area.lower()
                skills_map_raw = raw_employee.get("skills_map")
                matches_skill = False
                if skills_map_raw:
                    with suppress(json.JSONDecodeError, TypeError):
                        parsed = json.loads(skills_map_raw)
                        if skill_area in parsed:
                            matches_skill = True
                if not matches_skill:
                    skill_names = [name.lower() for name in self._skills_from_map(raw_employee.get("skills_map"))]
                    matches_skill = any(skill_area_lower in name for name in skill_names)
                if not matches_skill:
                    continue

            combined = {
                **mentor_profile,
                **raw_employee,
                "employee_id": employee_id,
                "name": employee.get("name"),
                "role": employee.get("role"),
                "department_id": employee.get("department_id"),
                "level": employee.get("level"),
                "position_level": employee.get("position_level"),
            }

            combined.setdefault("capacity", mentor_profile.get("capacity", 3))
            combined.setdefault("mentees_count", mentor_profile.get("mentees_count", 0))
            combined.setdefault("rating", mentor_profile.get("rating", 0.0))
            combined.setdefault("personality", mentor_profile.get("personality", ""))

            mentors.append(self._to_mentor_profile(combined))

        mentors.sort(key=lambda mentor: (-mentor.get("rating", 0.0), mentor.get("name", "")))
        return mentors

    def get_mentor(self, mentor_id: str) -> Dict:
        resolved_id = self._resolve_employee_id(mentor_id)
        profile = self.profile_repo.get_profile(resolved_id) if resolved_id else None
        if not profile:
            raise LookupError(f"Mentor {mentor_id} not found")
        employee = self.employee_repo.get_employee_profile(resolved_id)
        if not employee:
            raise LookupError(f"Employee {mentor_id} not found")

        combined = {**profile, **employee}
        # Compose structure similar to rows returned by list_mentors
        combined.update(
            {
                "employee_id": resolved_id,
                "name": employee.get("name"),
                "role": employee.get("role"),
                "department_id": employee.get("department_id"),
                "level": employee.get("level"),
                "position_level": employee.get("position_level"),
            }
        )
        employee_row = self.employee_repo.get_by_id(
            self.employee_repo.TABLE, self.employee_repo.ID_FIELD, resolved_id
        )
        if employee_row:
            combined["skills_map"] = employee_row.get("skills_map")
            combined["hire_date"] = employee_row.get("hire_date")
        return self._to_mentor_profile(combined)

    # --------------------------------------------------------------------- #
    # Mentorship requests
    # --------------------------------------------------------------------- #
    def create_request(
        self,
        mentee_id: str,
        mentor_id: str,
        message: str,
        goals: Iterable[str],
    ) -> Dict:
        mentee_profile = self._ensure_employee_profile(mentee_id, "Employee")
        mentor_profile = self._ensure_employee_profile(mentor_id, "Employee")

        canonical_mentee_id = mentee_profile["id"]
        canonical_mentor_id = mentor_profile["id"]

        mentor_meta = self.profile_repo.get_profile(canonical_mentor_id)
        if mentor_meta and mentor_meta.get("capacity", 0) <= mentor_meta.get("mentees_count", 0):
            raise ValueError("Mentor has reached their capacity")

        existing_requests = self.request_repo.list_requests(mentee_id=canonical_mentee_id)
        for existing in existing_requests:
            status = existing.get("status", "pending")
            mentor_match = existing.get("mentor_id")
            
            # Skip deleted requests
            if status == "deleted":
                continue
            
            # If already has accepted mentorship, cannot request another
            if status == "accepted":
                raise ValueError("You already have an active mentor")
            
            # If has pending request to same mentor, cannot duplicate
            if status == "pending" and mentor_match == canonical_mentor_id:
                raise ValueError("You already have a pending request to this mentor")
            
            # If has pending request to different mentor, cannot request another
            if status == "pending":
                raise ValueError("You already have a pending mentorship request. Please wait for a response or cancel your existing request.")

        mentee_position = mentee_profile.get("position_level") or 0
        mentor_position = mentor_profile.get("position_level") or 0
        if mentor_position <= mentee_position:
            raise ValueError("Mentor must have a higher position level than the mentee")

        goals_list = list(goals)
        payload = {
            "message": message,
            "goals": goals_list,
            "responseMessage": None,
            "respondedAt": None,
        }
        created_at = datetime.now(UTC).isoformat()
        match_score = self.estimate_match_score(canonical_mentor_id, canonical_mentee_id, goals_list)

        record_id = self.request_repo.create_request(
            {
                "mentee_id": canonical_mentee_id,
                "mentor_id": canonical_mentor_id,
                "match_score": match_score,
                "explanation": self.request_repo.encode_payload(payload),
                "status": "pending",
                "created_at": created_at,
            }
        )
        return self._build_request_dict(
            record_id,
            mentee_profile,
            mentor_profile,
            payload,
            status="pending",
            created_at=created_at,
        )

    def list_requests(
        self,
        mentor_id: Optional[str] = None,
        mentee_id: Optional[str] = None,
        include_deleted: bool = False,
    ) -> List[Dict]:
        resolved_mentor = self._resolve_employee_id(mentor_id) if mentor_id else None
        resolved_mentee = self._resolve_employee_id(mentee_id) if mentee_id else None
        rows = self.request_repo.list_requests(mentor_id=resolved_mentor, mentee_id=resolved_mentee)
        results: List[Dict] = []
        for row in rows:
            # Filter out deleted requests unless explicitly requested
            if not include_deleted and row.get("status") == "deleted":
                continue
                
            payload = self.request_repo.decode_payload(row.get("explanation"))
            mentee_profile = self.employee_repo.get_employee_profile(row["mentee_id"]) or {}
            mentor_profile = self.employee_repo.get_employee_profile(row["mentor_id"]) or {}
            results.append(
                self._build_request_dict(
                    row["id"],
                    mentee_profile,
                    mentor_profile,
                    payload,
                    status=row.get("status", "pending"),
                    created_at=row.get("created_at"),
                )
            )
        return results

    def update_request_status(
        self,
        request_id: int,
        status: str,
        response_message: Optional[str] = None,
    ) -> Dict:
        row = self.request_repo.get_request(request_id)
        if not row:
            raise LookupError(f"Request {request_id} not found")

        payload = self.request_repo.decode_payload(row.get("explanation"))
        if status in {"accepted", "declined"}:
            payload["respondedAt"] = datetime.now(UTC).isoformat()
        if response_message:
            payload["responseMessage"] = response_message

        self.request_repo.update_request(
            request_id,
            {
                "status": status,
                "explanation": self.request_repo.encode_payload(payload),
            },
        )

        mentee_profile = self.employee_repo.get_employee_profile(row["mentee_id"]) or {}
        mentor_profile = self.employee_repo.get_employee_profile(row["mentor_id"]) or {}

        if status == "accepted":
            if self.profile_repo.get_profile(row["mentor_id"]):
                self.profile_repo.increment_mentees_count(row["mentor_id"], 1)
            self.match_repo.create_match(
                {
                    "mentor_id": row["mentor_id"],
                    "mentee_id": row["mentee_id"],
                    "score": row.get("match_score", 0.0),
                    "reasons_json": self.request_repo.encode_payload(
                        {"goals": payload.get("goals", [])}
                    ),
                    "status": "active",
                    "created_at": payload.get("respondedAt"),
                }
            )

        return self._build_request_dict(
            row["id"],
            mentee_profile,
            mentor_profile,
            payload,
            status=status,
            created_at=row.get("created_at"),
        )

    def delete_request(self, request_id: int, mentee_id: str) -> None:
        row = self.request_repo.get_request(request_id)
        if not row:
            raise LookupError(f"Request {request_id} not found")

        canonical_mentee = self._resolve_employee_id(mentee_id)
        if not canonical_mentee:
            raise LookupError(f"Employee {mentee_id} not found")

        if row.get("mentee_id") != canonical_mentee:
            raise ValueError("You can only modify your own mentorship requests")

        if row.get("status") == "accepted":
            raise ValueError("Accepted requests cannot be deleted")

        # Soft delete: change status to "deleted" instead of removing the record
        self.request_repo.update_request(request_id, {"status": "deleted"})

    # --------------------------------------------------------------------- #
    # Mentorship pairs and statistics
    # --------------------------------------------------------------------- #
    def list_pairs(
        self,
        mentor_id: Optional[str] = None,
        mentee_id: Optional[str] = None,
    ) -> List[Dict]:
        rows = self.match_repo.list_matches_filtered(
            mentor_id=mentor_id, mentee_id=mentee_id
        )
        pairs: List[Dict] = []
        for row in rows:
            mentor_profile = self.employee_repo.get_employee_profile(row["mentor_id"]) or {}
            mentee_profile = self.employee_repo.get_employee_profile(row["mentee_id"]) or {}
            payload = self.request_repo.decode_payload(row.get("reasons_json"))
            pairs.append(
                {
                    "pairId": f"PAIR{row['id']:03d}",
                    "mentorId": row["mentor_id"],
                    "mentorName": mentor_profile.get("name", row["mentor_id"]),
                    "mentorRole": mentor_profile.get("role", ""),
                    "menteeId": row["mentee_id"],
                    "menteeName": mentee_profile.get("name", row["mentee_id"]),
                    "menteeRole": mentee_profile.get("role", ""),
                    "startDate": row.get("created_at"),
                    "focusAreas": payload.get("goals", []),
                    "status": row.get("status", "active"),
                    "progressPercentage": 0,
                    "sessionsCompleted": 0,
                    "lastMeetingDate": None,
                    "nextMeetingDate": None,
                }
            )
        return pairs

    def statistics(self) -> Dict:
        mentors = self.profile_repo.list_profiles()
        requests = self.request_repo.list_requests()
        matches = self.match_repo.list_matches()

        available = [
            m for m in mentors if m.get("mentees_count", 0) < m.get("capacity", 0)
        ]

        active_matches = [m for m in matches if m.get("status") == "active"]
        scores = [req.get("match_score") for req in requests if req.get("match_score")]
        average_score = sum(scores) / len(scores) if scores else 0.0

        pending_requests = [req for req in requests if req.get("status") == "pending"]

        return {
            "totalActivePairs": len(active_matches),
            "totalMentors": len(mentors),
            "totalMenteesSeeking": len(pending_requests),
            "availableMentors": len(available),
            "averageMatchScore": round(average_score, 2),
            "completionRate": 0.0,
            "underservedSkills": [],
        }

    # --------------------------------------------------------------------- #
    # Helpers
    # --------------------------------------------------------------------- #
    def _to_mentor_profile(self, row: Dict) -> Dict:
        department_row = None
        with suppress(Exception):
            department_row = self.department_repo.get_department(row.get("department_id"))

        skills = self._skills_from_map(row.get("skills_map"))

        return {
            "employeeId": row.get("employee_id"),
            "name": row.get("name"),
            "role": row.get("role"),
            "department": department_row["name"] if department_row else row.get("department_id"),
            "expertiseAreas": skills,
            "rating": float(row.get("rating") or 0.0),
            "menteesCount": row.get("mentees_count", 0),
            "maxMentees": row.get("capacity", 0),
            "isAvailable": row.get("mentees_count", 0) < row.get("capacity", 0),
            "bio": row.get("personality") or "",
            "yearsOfExperience": self._years_of_experience(row.get("hire_date")),
            "achievements": [],
        }

    def _skills_from_map(self, skills_map: Optional[str]) -> List[str]:
        if not skills_map:
            return []
        with suppress(json.JSONDecodeError, TypeError):
            parsed = json.loads(skills_map)
            skill_ids = list(parsed.keys())
            mapping = self.skill_repo.map_skill_ids_to_names(skill_ids)
            return [mapping.get(skill_id, skill_id) for skill_id in skill_ids]
        return []

    def _years_of_experience(self, hire_date: Optional[str]) -> int:
        if not hire_date:
            return 0
        with suppress(ValueError):
            start_date = datetime.fromisoformat(hire_date).date()
            return max(0, (date.today() - start_date).days // 365)
        return 0

    def estimate_match_score(
        self, mentor_id: str, mentee_id: str, goals: Iterable[str]
    ) -> float:
        mentor = self.employee_repo.get_employee(mentor_id) or {}
        mentee = self.employee_repo.get_employee(mentee_id) or {}

        mentor_skills = mentor.get("skills", {})
        mentee_goals = [goal.lower() for goal in goals]

        # Handle case where skills might be a JSON string instead of dict
        if isinstance(mentor_skills, str):
            try:
                import json
                mentor_skills = json.loads(mentor_skills)
            except (ValueError, TypeError, json.JSONDecodeError):
                mentor_skills = {}

        skill_names = self.skill_repo.map_skill_ids_to_names(list(mentor_skills.keys()))
        normalized_skill_terms = {
            skill_id: skill_names.get(skill_id, skill_id).lower()
            for skill_id in mentor_skills.keys()
        }

        overlap = 0
        for goal in mentee_goals:
            if any(goal in name for name in normalized_skill_terms.values()):
                overlap += 1

        base = 40.0
        if mentor.get("department_id") == mentee.get("department_id"):
            base += 10.0

        score = base + overlap * 10.0
        return float(min(score, 100.0))

    def _build_request_dict(
        self,
        request_id: int,
        mentee_profile: Dict,
        mentor_profile: Dict,
        payload: Dict,
        *,
        status: str,
        created_at: Optional[str],
    ) -> Dict:
        return {
            "requestId": f"REQ{request_id:03d}",
            "menteeId": mentee_profile.get("id", ""),
            "menteeName": mentee_profile.get("name", mentee_profile.get("id", "")),
            "menteeRole": mentee_profile.get("role", ""),
            "mentorId": mentor_profile.get("id", mentor_profile.get("employee_id", "")),
            "mentorName": mentor_profile.get("name", mentor_profile.get("id", "")),
            "message": payload.get("message", ""),
            "goals": payload.get("goals", []),
            "status": status,
            "createdAt": created_at,
            "respondedAt": payload.get("respondedAt"),
        }
