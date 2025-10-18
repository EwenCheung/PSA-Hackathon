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

