# Mentoring Agent

## Overview
The Mentoring Agent is an AI-powered system designed to facilitate and optimize the mentorship program at PSA International. It helps match employees with suitable mentors, tracks mentorship progress, and provides insights to improve the program.

## Core Responsibilities

### 1. **Mentor-Mentee Matching**
- Analyzes employee profiles, skills, and career goals
- Recommends optimal mentor matches based on:
  - Skill alignment (mentor expertise ↔ mentee needs)
  - Experience level appropriateness
  - Department relevance
  - Mentor availability and capacity
  - Career trajectory alignment
- Provides detailed reasoning for each recommendation

### 2. **Mentorship Goal Setting**
- Helps employees articulate clear development goals
- Breaks down career aspirations into actionable objectives
- Suggests focus areas based on:
  - Current role and career path
  - Identified skill gaps
  - Industry trends
  - Realistic timelines
- Categories: Technical Skills, Leadership, Career Growth, Communication

### 3. **Mentor Profile Management**
- Evaluates mentor qualifications and expertise
- Tracks mentor capacity and availability
- Monitors mentor performance (ratings, success rate, completion rate)
- Identifies gaps where more mentors are needed

### 4. **Progress Tracking & Analytics**
- Monitors active mentorship pairs
- Analyzes session frequency and engagement
- Identifies at-risk mentorships
- Suggests interventions when needed

### 5. **Request Processing**
- Reviews mentorship requests from employees
- Validates request quality
- Suggests improvements to requests
- Prioritizes based on urgency and availability

### 6. **Program Insights**
- Identifies organizational mentorship trends
- Recommends new mentor recruitment
- Suggests program improvements
- Highlights successful patterns

## Tools & Functions

### Core Functions

#### `find_available_mentors(skill_area, department, min_rating)`
Find mentors matching specific criteria.
- **Inputs**: 
  - `skill_area`: Optional skill filter
  - `department`: Optional department filter
  - `min_rating`: Minimum mentor rating
- **Returns**: List of available mentor profiles

#### `recommend_mentors(employee_id, career_goals, desired_skills, max_results)`
Generate mentor recommendations for an employee.
- **Inputs**:
  - `employee_id`: The mentee's ID
  - `career_goals`: List of career aspirations
  - `desired_skills`: Skills to develop
  - `max_results`: Number of recommendations
- **Returns**: Ranked list of mentor matches with scores and reasoning

#### `get_active_mentorship_pairs(mentor_id, mentee_id, department)`
Retrieve active mentorship relationships.
- **Inputs**: Optional filters by mentor, mentee, or department
- **Returns**: List of active mentorship pairs with progress data

#### `analyze_mentorship_progress(pair_id)`
Analyze health and progress of a mentorship.
- **Inputs**: `pair_id`: Unique pair identifier
- **Returns**: Progress metrics, engagement analysis, recommendations

#### `create_mentorship_request(mentee_id, mentor_id, message, goals)`
Create a new mentorship request.
- **Inputs**:
  - `mentee_id`: Requesting employee
  - `mentor_id`: Target mentor
  - `message`: Personal introduction
  - `goals`: List of mentorship goals
- **Returns**: Request ID and status

### Supporting Functions

#### `get_mentor_profile(employee_id)`
Retrieve detailed mentor profile.

#### `get_mentee_profile(employee_id)`
Retrieve detailed employee/mentee profile.

#### `get_mentorship_statistics(department)`
Get program-wide statistics and metrics.

#### `validate_mentorship_goals(goals, employee_profile)`
Validate and improve mentorship goals.

#### `identify_mentor_gaps(department)`
Find skill areas needing more mentors.

## Data Schemas

### MentorProfile
```python
{
    "employee_id": str,
    "name": str,
    "role": str,
    "department": str,
    "expertise": List[str],
    "years_experience": int,
    "mentees_current": int,
    "mentees_capacity": int,
    "rating": float,
    "total_mentees_helped": int,
    "available": bool
}
```

### MenteeProfile
```python
{
    "employee_id": str,
    "name": str,
    "role": str,
    "department": str,
    "current_skills": List[str],
    "career_goals": List[str],
    "desired_skills": List[str],
    "years_experience": int
}
```

### MentorshipMatch
```python
{
    "mentor_id": str,
    "mentor_name": str,
    "mentee_id": str,
    "mentee_name": str,
    "match_score": float,  # 0-100
    "reasons": List[str],
    "focus_areas": List[str]
}
```

### MentorshipPair
```python
{
    "pair_id": str,
    "mentor_id": str,
    "mentee_id": str,
    "start_date": str,  # YYYY-MM-DD
    "focus_areas": List[str],
    "status": str,  # "active", "paused", "completed"
    "progress": int,  # 0-100
    "sessions_completed": int,
    "next_meeting": Optional[str]
}
```

## Integration with Frontend

The agent supports the following frontend features:

### Employee Portal
- **Find Mentors Tab**: Powers mentor recommendations based on selected goals
- **Browse Mentors**: Provides searchable mentor directory
- **Request Mentorship**: Processes and validates mentorship requests
- **My Mentees Tab**: Shows mentors their current mentees and pending requests
- **Progress Tracking**: Monitors mentee development progress

### Employer Dashboard
- **Mentor-Mentee Pairs View**: Displays all active and completed pairs
- **Available Mentors List**: Shows mentor capacity and expertise
- **Seeking Mentors List**: Displays employees looking for guidance
- **Program Statistics**: Provides analytics on mentorship program health

## Matching Algorithm

The agent uses a multi-factor matching algorithm:

1. **Skill Alignment (40%)**: Mentor expertise matches mentee goals
2. **Experience Gap (20%)**: Appropriate seniority difference
3. **Availability (15%)**: Mentor has capacity
4. **Department Relevance (10%)**: Same or complementary domains
5. **Track Record (10%)**: Mentor rating and success rate
6. **Career Path (5%)**: Alignment with mentee's desired trajectory

## Usage Examples

### Example 1: Find Mentor for Technical Leadership
```python
# Employee wants to develop technical leadership skills
recommendations = recommend_mentors(
    employee_id="EMP001",
    career_goals=["Become Tech Lead", "Learn System Design"],
    desired_skills=["Technical Leadership", "System Architecture"],
    max_results=5
)

# Returns ranked list with reasoning
# [{
#   "mentor_name": "David Lee",
#   "match_score": 95,
#   "reasons": [
#     "Expert in System Design and Cloud Architecture",
#     "Successfully mentored 5 engineers to senior roles",
#     "Available with 1 mentee slot open"
#   ]
# }]
```

### Example 2: Monitor Program Health
```python
# Get organization-wide statistics
stats = get_mentorship_statistics()

# Returns metrics
# {
#   "total_active_pairs": 18,
#   "average_match_score": 88.5,
#   "completion_rate": 0.85,
#   "underserved_skills": ["Product Management", "UX Research"]
# }
```

### Example 3: Create Mentorship Request
```python
# Employee requests mentorship
request = create_mentorship_request(
    mentee_id="EMP001",
    mentor_id="EMP005",
    message="I'd love to learn system design from your experience...",
    goals=["System Architecture", "Technical Leadership"]
)

# Returns request details
# {
#   "request_id": "REQ001",
#   "status": "pending",
#   "created_at": "2025-10-18T10:30:00Z"
# }
```

## Best Practices

1. **Match Quality over Quantity**: Focus on high-quality matches rather than maximizing numbers
2. **Respect Capacity**: Don't overload mentors beyond their stated capacity
3. **Regular Check-ins**: Monitor mentorship pairs at regular intervals
4. **Encourage Diversity**: Promote cross-functional and diverse mentorships
5. **Clear Goals**: Ensure all mentorships have well-defined, measurable goals
6. **Feedback Loop**: Use success/failure data to improve matching algorithm

## Development Guidelines

Following `AGENTS.md` rules:
1. ✅ **Follow TDD**: Write tests for all tool functions before implementation
2. ✅ **Avoid try-except blocks**: Use proper validation and return types instead

## Future Enhancements

1. **Personality Matching**: Incorporate personality assessment data
2. **Success Prediction**: ML model to predict mentorship success
3. **Auto-scheduling**: Suggest meeting times based on calendars
4. **Skill Gap Analysis**: Deeper integration with learning paths
5. **Feedback Analysis**: NLP on mentorship session notes
6. **Network Effects**: Consider existing relationships and networks
7. **Cultural Compatibility**: Factor in work styles and communication preferences

## API Endpoints (To Be Implemented)

- `POST /api/mentoring/recommend` - Get mentor recommendations
- `GET /api/mentoring/mentors` - List available mentors
- `GET /api/mentoring/pairs` - Get active mentorship pairs
- `POST /api/mentoring/request` - Create mentorship request
- `GET /api/mentoring/progress/{pair_id}` - Get pair progress
- `GET /api/mentoring/statistics` - Get program statistics
- `POST /api/mentoring/goals/validate` - Validate mentorship goals

## Testing Strategy

1. **Unit Tests**: Test each tool function independently
2. **Integration Tests**: Test agent with full workflow
3. **Mock Data Tests**: Use Employee_Profiles.json for realistic scenarios
4. **Performance Tests**: Ensure matching algorithm scales
5. **Edge Cases**: Test capacity limits, skill mismatches, etc.

## Monitoring & Metrics

Key metrics to track:
- Match quality score distribution
- Mentorship completion rate
- Average time to first meeting
- Mentor utilization (capacity vs actual)
- Skill coverage (supply vs demand)
- Employee satisfaction ratings
- Career progression of mentees

---

**Note**: This agent is designed to support human decision-making, not replace it. Final mentorship decisions should always involve human judgment and employee choice.
