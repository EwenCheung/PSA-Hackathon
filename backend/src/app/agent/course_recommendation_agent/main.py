# main.py
import os
import json
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from system_prompt import SYSTEM_PROMPT
from tools import get_employee_context, recommend_courses_tool

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
# def get_course_recommendations(employee_id: str) -> dict:
#     """
#     Given an employee_id, fetch their context and recommend suitable courses.
#     """
#     print(f"=== Fetching Employee {employee_id} Context ===")
#     emp_context = get_employee_context(employee_id)
#     profile = emp_context["profile"]

#     # ---- Pretty print employee info ----
#     print("\n--- Employee Profile ---")
#     print(f"Name: {profile.get('name')}")
#     print(f"Role: {profile.get('role')}")
#     print(f"Department: {profile.get('department_id')}")
#     print(f"Level: {profile.get('level')}")
#     print(f"Points: {profile.get('points_current')}")
#     print(f"Hire Date: {profile.get('hire_date')}")

#     print("\n--- Employee Skills ---")
#     print(", ".join(emp_context["skills"]) or "No skills found")

#     print("\n--- Employee Goals ---")
#     print(", ".join(emp_context["goals"]) or "No goals found")

#     print("\n--- Courses Enrolled ---")
#     print(emp_context["courses_enrolled"] or "None")

#     # ---- Build the LangChain agent ----
#     agent = create_agent(
#         model=llm,
#         tools=[recommend_courses_agent_tool],
#         system_prompt=SYSTEM_PROMPT
#     )

#     # ---- Construct dynamic prompt ----
#     prompt = (
#         f"Recommend relevant upskilling courses for {profile.get('name')}, "
#         f"a {profile.get('level')} {profile.get('role')} in department {profile.get('department_id')}. "
#         f"They currently have skills: {emp_context['skills']}, "
#         f"and personal or team goals: {emp_context['goals']}. "
#         f"Provide course suggestions that align with their role, level, and goals."
#     )

#     print("\n=== Generating Course Recommendations ===")

#     response = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

#     # ---- Extract AI message ----
#     try:
#         ai_message = next(
#             (msg for msg in reversed(response["messages"]) if msg.type == "ai"),
#             None
#         )
#         if not ai_message or not ai_message.content:
#             raise ValueError("No AI message content found in response")

#         parsed = json.loads(ai_message.content)
#         return parsed

#     except json.JSONDecodeError:
#         print("⚠️ Could not parse JSON from LLM output. Returning raw content.")
#         return {"raw_output": ai_message.content if ai_message else str(response)}
#     except Exception as e:
#         print(f"⚠️ Unexpected error while processing response: {e}")
#         return {"error": str(e), "raw_output": str(response)}


# # ----------------------
# # Entry Point (Test Case)
# # ----------------------
# if __name__ == "__main__":
#     employee_id = "EMP004"  # Change this to test other employees
#     result = get_course_recommendations(employee_id)

#     # ---- Pretty print structured result ----
#     print("\n=== Final Recommendations ===")
#     if "recommended_courses" in result:
#         print("\nAnalysis:")
#         print(result["analysis"])
#         print("\nRecommended Courses:")
#         for c in result["recommended_courses"]:
#             print(f"  Course: {c['title']}")
#             print(f"  Link: {c['url']}")
#             print(f"  Reason: {c['reason']}")
#             # print(f"  Matched Skills: {', '.join(c['matched_skills'])}")
#             print(f"  Expected Outcome: {c['expected_outcome']}\n")
#     else:
#         print("Raw result:", result)

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

# ----------------------
# Entry Point (Career Pathway Test Case)
# ----------------------
if __name__ == "__main__":
    employee_id = "EMP004"
    result = get_career_pathway(employee_id)

    print("\n=== Final Structured JSON ===")
    print(json.dumps(result.get("json", {}), indent=2))

    print("\n=== Natural Language Career Pathway Summary ===")
    print(result.get("text_summary", "No summary generated."))


# ----------------------
# Entry Point (Course Recco Test Case)
# ----------------------
# if __name__ == "__main__":
#     employee_id = "EMP004"
#     result = get_course_recommendations(employee_id)

#     print("\n=== Final Structured JSON ===")
#     print(json.dumps(result.get("json", {}), indent=2))

#     print("\n=== Natural Language Summary ===")
#     print(result.get("text_summary", "No summary generated."))