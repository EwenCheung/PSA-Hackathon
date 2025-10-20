<<<<<<< HEAD
1. Use TDD Driven Development.
2. Minimise try and except blocks.

3. /Users/ewencheung/Documents/GitHub/PSA-Hackathon/backend/src/app/agent/well_being_agent/agent.py
/Users/ewencheung/Documents/GitHub/PSA-Hackathon/backend/src/app/api/v1/wellbeing.py

4. Connnect the frontend with the api call in the file listed in 3. 
@router.get("/{employee_id}/messages_past_10_history")
async def get_messages(employee_id: str):
    return well_being_agent.get_messages(employee_id)


@router.post("/{employee_id}/messages")
async def post_message(employee_id: str, req: WellbeingMessageRequest):
    return well_being_agent.post_message(employee_id, req)

=======
<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->
>>>>>>> Daerenbranch
