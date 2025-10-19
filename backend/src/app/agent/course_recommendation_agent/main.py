# main.py
import os
import json
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from .system_prompt import SYSTEM_PROMPT
from .tools import get_employee_context, recommend_courses_tool
# from system_prompt import SYSTEM_PROMPT
# from tools import get_employee_context, recommend_courses_tool
import re
from datetime import datetime

# Load environment variables from .env
load_dotenv()
import getpass

# Load environment
DEPLOYMENT = os.getenv("DEPLOYMENT")
API_VERSION = os.getenv("API_VERSION")
URL = f"https://psacodesprint2025.azure-api.net/openai/deployments/{DEPLOYMENT}/chat/completions?api-version={API_VERSION}"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = URL

# Initialize Azure LLM
llm = AzureChatOpenAI(
    azure_deployment=DEPLOYMENT,
    api_version=API_VERSION,
    temperature=0.3,
    max_tokens=500
)

# ----------------------
# Tool Wrappers
# ----------------------
def recommend_courses_agent_tool(employee_skills: list) -> str:
    """
    Given a list of employee skills, return a formatted string of course recommendations.
    """
    recommendations = recommend_courses_tool(employee_skills)
    if not recommendations:
        return "No course recommendations found."
    
    output = []
    for r in recommendations:
        output.append(f"- {r['title']} ({r['url']})\n  Skills: {', '.join(r['skills'])}\n  Reason: {r['reason']}")
    return "\n\n".join(output)


# ----------------------
# Core Agent Logic
# ----------------------
def get_course_recommendations(employee_id: str) -> dict:
    """
    Given an employee_id, fetch their context and recommend suitable courses.
    Returns both JSON output and a user-friendly natural language summary.
    """
    print(f"=== Fetching Employee {employee_id} Context ===")
    emp_context = get_employee_context(employee_id)
    profile = emp_context["profile"]

    # ---- Print employee info ----
    print("\n--- Employee Profile ---")
    print(f"Name: {profile.get('name')}")
    print(f"Role: {profile.get('role')}")
    print(f"Department: {profile.get('department_id')}")
    print(f"Level: {profile.get('level')}")
    print(f"Points: {profile.get('points_current')}")
    print(f"Hire Date: {profile.get('hire_date')}")

    print("\n--- Employee Skills ---")
    print(", ".join(emp_context["skills"]) or "No skills found")

    print("\n--- Employee Goals ---")
    print(", ".join(emp_context["goals"]) or "No goals found")

    print("\n--- Courses Enrolled ---")
    print(emp_context["courses_enrolled"] or "None")

    # ---- Create the agent ----
    agent = create_agent(
        model=llm,
        tools=[recommend_courses_agent_tool],
        system_prompt=SYSTEM_PROMPT
    )

    prompt = (
        f"Recommend relevant upskilling courses for {profile.get('name')}, "
        f"a {profile.get('level')} {profile.get('role')} in department {profile.get('department_id')}. "
        f"They currently have skills: {emp_context['skills']}, "
        f"and personal or team goals: {emp_context['goals']}. "
        f"Provide course suggestions that align with their role, level, and goals and possible skill gaps with their roles."
    )

    print("\n=== Generating Course Recommendations ===")

    response = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

    # ---- Extract AI message ----
    try:
        ai_message = next(
            (msg for msg in reversed(response["messages"]) if msg.type == "ai"),
            None
        )
        if not ai_message or not ai_message.content:
            raise ValueError("No AI message content found in response")

        # Parse structured JSON
        parsed = json.loads(ai_message.content)

        # --- Generate a human-readable summary ---
        summary_prompt = (
            "Convert the following JSON course recommendations into a friendly, natural summary "
            "for the employee. For each course, include the url, the reason to learn (maybe how it can cover certain skill gaps) and the expected takeaway"
            "Keep it concise and motivating, as if from a personal career coach:\n\n"
            f"{json.dumps(parsed, indent=2)}"
        )
        summary_response = llm.invoke(summary_prompt)
        summary_text = summary_response.content.strip() if hasattr(summary_response, "content") else str(summary_response)

        return {"json": parsed, "text_summary": summary_text}

    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON from LLM output. Returning raw content.")
        return {"raw_output": ai_message.content if ai_message else str(response)}
    except Exception as e:
        print(f"⚠️ Unexpected error while processing response: {e}")
        return {"error": str(e), "raw_output": str(response)}


def get_career_pathway(employee_id: str) -> dict:
    """
    Given an employee_id, analyze their context and recommend a personalized career pathway.
    Returns both structured JSON and a natural language summary.
    """
    print(f"=== Fetching Employee {employee_id} Context ===")
    emp_context = get_employee_context(employee_id)
    profile = emp_context["profile"]

    print("\n--- Employee Profile ---")
    print(f"Name: {profile.get('name')}")
    print(f"Role: {profile.get('role')}")
    print(f"Level: {profile.get('level')}")
    print(f"Department: {profile.get('department_id')}")
    print(f"Goals: {', '.join(emp_context['goals']) or 'None'}")

    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=SYSTEM_PROMPT
    )

    # ---- Force a structured JSON output ----
    prompt = f"""
    Create a personalized career development pathway for {profile.get('name')}, 
    a {profile.get('level')} {profile.get('role')} in the {profile.get('department_id')} department.
    Current skills: {emp_context['skills']}.
    Career goals: {emp_context['goals']}.
    
    Return your response STRICTLY in this JSON format (no extra text):

    {{
        "analysis": "Brief analysis of current situation",
        "career_pathway": {{
            "short_term": {{
                "duration": "0-6 months",
                "focus": ["skill1", "skill2"],
                "suggested_actions": ["action1", "action2"],
                "expected_outcomes": "what they’ll achieve"
            }},
            "mid_term": {{
                "duration": "6-18 months",
                "focus": ["skill3"],
                "suggested_actions": ["action3"],
                "expected_outcomes": "expected progress"
            }},
            "long_term": {{
                "duration": "18+ months",
                "focus": ["advanced skills", "leadership"],
                "suggested_actions": ["action4"],
                "expected_outcomes": "long-term growth outcome"
            }}
        }},
        "role_transition": "Target future role and rationale"
    }}
    """

    print("\n=== Generating Career Pathway ===")
    response = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

    try:
        ai_message = next(
            (msg for msg in reversed(response["messages"]) if msg.type == "ai"),
            None
        )
        if not ai_message or not ai_message.content:
            raise ValueError("No AI message content found in response")

        parsed = json.loads(ai_message.content)

        # --- Generate natural summary for display ---
        summary_prompt = (
            f"Write a clear, motivational summary based on this career pathway JSON. "
            f"Describe the employee’s growth journey across short, mid, and long-term stages, "
            f"highlighting skill growth, milestones, and how it supports their goals."
            f"Reply as if you're talking to the employee directly\n\n"
            f"{json.dumps(parsed, indent=2)}"
        )

        summary_response = llm.invoke(summary_prompt)
        summary_text = (
            summary_response.content.strip()
            if hasattr(summary_response, "content")
            else str(summary_response)
        )

        return {"json": parsed, "text_summary": summary_text}

    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON. Returning raw content.")
        return {"raw_output": ai_message.content if ai_message else str(response)}
    except Exception as e:
        print(f"⚠️ Unexpected error while processing response: {e}")
        return {"error": str(e), "raw_output": str(response)}


def get_leadership_potential_employee(employee_id: str) -> dict:
    """
    Analyze the employee's context and estimate their leadership potential
    based on PSA's leadership values and employee attributes.
    Returns both structured JSON and a natural-language explanation.
    """

    print(f"=== Fetching Employee {employee_id} Context ===")
    emp_context = get_employee_context(employee_id)
    profile = emp_context["profile"]
    skills = emp_context["skills"]
    goals = emp_context["goals"]
    courses_enrolled = emp_context["courses_enrolled"]

    # ------------------------------
    # Compute derived metrics
    # ------------------------------
    hire_date_str = profile.get("hire_date")
    hire_date = datetime.strptime(hire_date_str, "%Y-%m-%d") if hire_date_str else None
    years_with_company = (
        (datetime.now() - hire_date).days / 365 if hire_date else 0
    )

    num_courses_completed = sum(
        1 for status in courses_enrolled.values() if status.lower() == "completed"
    )

    # ------------------------------
    # Build AI reasoning prompt
    # ------------------------------
    prompt = f"""
    You are a talent intelligence assistant for PSA, evaluating leadership potential.

    PSA's Vision:
    "To be a leading supply chain ecosystem orchestrator powered by innovation, technology and sustainable practices."

    PSA's Mission:
    "To be the port operator of choice in the world’s gateway hubs, renowned for best-in-class services and successful partnerships."

    PSA's Values:
    - Committed to Excellence: continuous improvement and innovation
    - Dedicated to Customers: anticipating and meeting needs
    - Focused on People: teamwork, respect, and support
    - Integrated Globally: diversity and local optimization
    - Responsible Corporate Citizenship: sustainability and ethics

    Leadership Qualities to Evaluate:
    - Communication, integrity, empathy, accountability
    - Strategic abilities: vision, problem-solving, delegation
    - Personal traits: resilience, adaptability, self-awareness
    - Alignment with PSA values
    - Growth mindset (shown through upskilling and goals)
    - Seniority and tenure (longer experience = more maturity)
    - Learning engagement (courses completed, skill-building)

    Employee Profile:
    - Name: {profile.get('name')}
    - Role: {profile.get('role')}
    - Level: {profile.get('level')}
    - Department: {profile.get('department_id')}
    - Years with company: {years_with_company:.1f}
    - Completed courses: {num_courses_completed}
    - Skills: {', '.join(skills) or 'None'}
    - Goals: {', '.join(goals) or 'None'}

    Based on this profile and PSA's leadership framework,
    assess the employee’s leadership potential and return STRICTLY in this JSON format:

    {{
        "leadership_analysis": "brief reasoning considering PSA's values and the employee's data",
        "leadership_score": {{
            "experience_weight": 0-10,
            "learning_engagement_weight": 0-10,
            "soft_skills_alignment_weight": 0-10,
            "overall_score": 0-10
        }},
        "potential_level": "Low | Mid | High",
        "recommendations": [
            "specific improvement or action item",
            "another recommendation"
        ]
    }}
    """

    print("\n=== Predicting Leadership Potential ===")
    response = llm.invoke(prompt)

    # ------------------------------
    # Parse and postprocess
    # ------------------------------
    try:
        parsed = json.loads(response.content)

        # --- Generate a motivational summary for UI ---
        summary_prompt = f"""
        You are a career coach speaking directly to {profile['name']}.
        Summarize this leadership evaluation in a positive, constructive way.
        Encourage them to grow their leadership potential by highlighting their strengths and next steps.
        Use a professional yet motivating tone.

        JSON:
        {json.dumps(parsed, indent=2)}
        """

        summary_response = llm.invoke(summary_prompt)
        summary_text = summary_response.content.strip() if hasattr(summary_response, "content") else str(summary_response)

        return {"json": parsed, "text_summary": summary_text}

    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON. Returning raw output.")
        return {"raw_output": response.content}
    except Exception as e:
        print(f"⚠️ Error evaluating leadership potential: {e}")
        return {"error": str(e), "raw_output": str(response)}

def get_leadership_potential_employer(employee_id: str) -> dict:
    """
    Evaluate an employee's leadership potential from an employer's perspective.
    Focuses on next-generation leadership readiness, alignment with PSA values,
    and organizational fit. Returns both structured JSON and a concise summary
    suitable for management dashboards.
    """
    print(f"=== Fetching Employee {employee_id} Context ===")
    emp_context = get_employee_context(employee_id)
    profile = emp_context["profile"]
    skills = emp_context["skills"]
    goals = emp_context["goals"]
    courses_enrolled = emp_context["courses_enrolled"]

    # ------------------------------
    # Compute derived metrics
    # ------------------------------
    hire_date_str = profile.get("hire_date")
    hire_date = datetime.strptime(hire_date_str, "%Y-%m-%d") if hire_date_str else None
    years_with_company = (datetime.now() - hire_date).days / 365 if hire_date else 0

    num_courses_completed = sum(
        1 for status in courses_enrolled.values() if status.lower() == "completed"
    )

    # ------------------------------
    # Build AI reasoning prompt
    # ------------------------------
    prompt = f"""
You are an HR analytics assistant evaluating leadership potential for PSA.

Evaluate the employee’s next-generation leadership potential in alignment
with PSA’s strategic leadership qualities and values.

PSA Leadership Competencies:
- Communication & Empathy
- Strategic Thinking & Systems Vision
- Accountability & Integrity
- Innovation & Growth Mindset
- Team Collaboration & People Development
- Alignment with PSA’s mission and corporate responsibility

Consider:
- Role seniority and tenure (experience)
- Skill depth and relevance to leadership
- Learning engagement (courses completed, skill-building)
- Goal alignment with organizational growth
- Growth mindset and continuous learning

Employee Profile:
- Name: {profile.get('name')}
- Role: {profile.get('role')}
- Level: {profile.get('level')}
- Department: {profile.get('department_id')}
- Years with company: {years_with_company:.1f}
- Completed courses: {num_courses_completed}
- Skills: {', '.join(skills) or 'None'}
- Goals: {', '.join(goals) or 'None'}

Return STRICTLY in JSON format:

{{
    "leadership_summary": "Concise reasoning about leadership readiness and qualities shown",
    "leadership_factors": {{
        "experience": "short note and score 0-10",
        "learning_engagement": "short note and score 0-10",
        "soft_skills_alignment": "short note and score 0-10",
        "strategic_outlook": "short note and score 0-10"
    }},
    "overall_potential_score": 0-10,
    "potential_category": "Low | Mid | High",
    "recommendations_for_employer": [
        "development or mentorship recommendation",
        "rotation, leadership program, or targeted training suggestion"
    ]
}}
"""

    print("\n=== Evaluating Leadership Potential (Employer View) ===")
    response = llm.invoke(prompt)
    content = response.content.strip() if hasattr(response, "content") else str(response)

    # ------------------------------
    # Try to extract JSON safely
    # ------------------------------
    json_str_match = re.search(r"\{.*\}", content, re.DOTALL)
    json_str = json_str_match.group(0) if json_str_match else content

    try:
        parsed = json.loads(json_str)

        # --- Generate executive summary ---
        summary_prompt = f"""
You are summarizing leadership potential for HR executives.
Write a concise, professional summary (3–5 sentences) highlighting:
- Leadership readiness level (Low/Mid/High)
- Key observed strengths
- Potential areas to develop
- Recommended employer actions
Keep tone analytical and suitable for a dashboard.

JSON data:
{json.dumps(parsed, indent=2)}
"""

        summary_response = llm.invoke(summary_prompt)
        summary_text = summary_response.content.strip() if hasattr(summary_response, "content") else str(summary_response)

        return {"json": parsed, "text_summary": summary_text}

    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON. Returning raw output.")
        return {"raw_output": content}
    except Exception as e:
        print(f"⚠️ Error evaluating leadership potential (employer view): {e}")
        return {"error": str(e), "raw_output": str(response)}



# ------------------------------
# Entry Point (Leadership Potential (Employee) Test Case)
# ------------------------------
# if __name__ == "__main__":
#     employee_id = "EMP005"  
#     result = get_leadership_potential_employer(employee_id)

#     print("\n=== Leadership Potential (Structured JSON) ===")
#     print(json.dumps(result.get("json", {}), indent=2))

#     print("\n=== Employer Summary (Dashboard View) ===")
#     print(result.get("text_summary", "No summary generated."))

# ------------------------------
# Entry Point (Leadership Potential (Employee) Test Case)
# ------------------------------
# if __name__ == "__main__":
#     employee_id = "EMP002"  # Example: Bob Martinez
#     result = get_leadership_potential_employee(employee_id)

#     print("\n=== Final Structured JSON ===")
#     print(json.dumps(result.get("json", result.get("raw_output", {})), indent=2))

#     print("\n=== Leadership Summary ===")
#     print(result.get("text_summary", "No summary generated."))


# ----------------------
# Entry Point (Career Pathway Test Case)
# ----------------------
# if __name__ == "__main__":
#     employee_id = "EMP004"
#     result = get_career_pathway(employee_id)

#     print("\n=== Final Structured JSON ===")
#     print(json.dumps(result.get("json", {}), indent=2))

#     print("\n=== Natural Language Career Pathway Summary ===")
#     print(result.get("text_summary", "No summary generated."))


# ----------------------
# Entry Point (Course Recco Test Case)
# ----------------------
if __name__ == "__main__":
    employee_id = "EMP004"
    result = get_course_recommendations(employee_id)

    print("\n=== Final Structured JSON ===")
    print(json.dumps(result.get("json", {}), indent=2))

    print("\n=== Natural Language Summary ===")
    print(result.get("text_summary", "No summary generated."))