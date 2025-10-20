# PathForger - PSA Hackathon Solution

## Problem Statement
**Future-Ready Workforce – AI for Employee Growth and Engagement**

PSA faces challenges in managing employee career development amid rapid technological transformation. The need for personalized growth support, mental well-being resources, and equitable opportunities across diverse employee groups requires an AI-driven solution.

## Objective
Develop an AI-powered platform that:
- **Personalizes Career Development**: Recommends career pathways, internal mobility, and upskilling plans
- **Provides Intelligent Support**: Conversational AI for engagement, well-being, and continuous development
- **Predicts Leadership Potential**: Uses behavioral, performance, and engagement data analytics
- **Enables Inclusive Growth**: Targeted mentorship, accessibility, and recognition systems for multi-generational workforce

## Solution Overview
PathForger is an AI-powered growth platform that helps employees build leadership potential while providing employers real-time workforce readiness insights through modular AI agents and vector-based intelligence.

## Quick Start
```bash
cd Prototype_ThreeMusketeer
bash start_server.sh             # Start both servers (Ctrl+C to stop)
bash start_server.sh --dry-run   # Preview commands only
```

The launcher automatically:
1. Sets up FastAPI backend (Python 3.10+, uv tool) on port 8000
2. Starts React/Vite frontend on port 5173

### Manual startup (alternative workflow)
If you prefer to launch services manually, follow the flow many teammates use:

1. Backend terminal
   ```bash
   cd backend
   uv sync
   source .venv/bin/activate
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir src
   ```
   Wait for the backend to finish initial sync and boot (typically 5–10 minutes on first run) before starting the frontend.

2. Frontend terminal (new shell window/tab)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

This path mirrors what the launcher automates, but gives you granular control over each process.

## Key Features

### For Employees
- **Personalized Course Recommendations**: AI-powered course matching based on skills, goals, and career aspirations
- **Career Path Navigation**: Short-term (0-6 months), mid-term (6-18 months), and long-term (18+ months) development roadmaps
- **Leadership Scoring**: AI evaluation of leadership potential using learning velocity and engagement data
- **Smart Mentorship Matching**: AI-driven mentor pairing based on expertise and compatibility
- **Wellbeing Support**: Sentiment analysis and proactive mental health interventions
- **Gamification**: Points system for courses, mentoring, and milestone achievements

### For Employers
- **Workforce Analytics**: Real-time insights on top performers, leadership candidates, and skill gaps
- **Mentorship Program Management**: Oversight of mentor capacity and program effectiveness
- **Strategic Planning Tools**: Data-driven promotion and reskilling decision support

## Technology Stack
- **Backend**: FastAPI (Python 3.10+) with modular AI agents and vector embeddings
- **Frontend**: React + TypeScript with Vite
- **Database**: SQLite for employee profiles and engagement data
- **AI/ML**: Vector intelligence for recommendations and sentiment analysis

## Employee View Experience
- **Personalised course intelligence**: Employees sign in, trigger the embeddings pipeline, and receive the top three course matches with rationale anchored to their skills, aspirations, and current role.
- **Career path navigator**: A roadmap breaks growth into short-term (0–6 months), mid-term (6–18 months), and long-term (18+ months) stages with focus areas, actions, and likely future roles.
- **Leadership readiness scoring**: Agents evaluate proactive learning, skill velocity, and emotional steadiness to flag leadership potential and highlight improvement levers.
- **Mentorship orchestration**: Requests go through an AI matcher that pairs mentees with mentors based on expertise, goals, and compatibility. The agent keeps sessions on track, nudging both sides if progress stalls.
- **Wellbeing agent**: Sentiment analysis monitors mood shifts, suggests interventions, routes to resources, and coordinates schedules to prevent burnout while respecting privacy.
- **Gamification layer**: Employees earn redeemable points by completing courses, mentoring colleagues, reaching milestones, and maintaining wellbeing streaks—turning growth into a rewarding loop.

## Employer Insights Dashboard
- **Real-time workforce intelligence**: Dashboards surface top performers, leadership candidates, and emerging skill gaps so managers can prioritise interventions.
- **Single-load analytics**: Insights hydrate once from the database, then stream updates, tracking course adoption, skill trends, and engagement momentum without reloading the full view.
- **Mentorship oversight**: Employers observe mentor capacity, request queues, and programme health, receiving alerts when pairings need support.
- **Strategic planning**: Aggregated analytics spotlight future leaders, critical skill shortages, and training ROI, enabling data-driven promotion and reskilling decisions.

## Vision and Roadmap
- **Holistic growth**: PathForger unites learning, leadership development, wellbeing, and gamification so employees see a full 360° view of their career trajectory.
- **Actionable employer value**: Organisations translate platform telemetry into targeted training, balanced mentorship programmes, and early identification of leadership pipelines.
- **Future-ready evolution**: The modular architecture keeps the platform adaptable, paving the way for deeper enterprise integrations, additional agents, and region-specific content.
- **Where growth meets opportunity**: By aligning engagement, insight, and development, PathForger forges leaders while keeping teams energised for what’s next.

## Project Structure
```
├── backend/               # FastAPI backend with AI agents
├── frontend/             # React + Vite frontend
└── Prototype_ThreeMusketeer/  # Launch automation scripts
```

## Development Setup
**Requirements**: Python 3.10+, Node.js, [`uv`](https://github.com/astral-sh/uv) tool

**Ports**: Backend (8000), Frontend (5173)

## Team
Three Musketeers - PSA Hackathon 2025
