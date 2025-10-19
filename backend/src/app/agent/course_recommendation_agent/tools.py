# tools.py
import os
import sys
import sqlite3
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict
import json

# LangChain imports
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings

# Add src to path
src_root = Path(__file__).parents[3]
sys.path.insert(0, str(src_root))

# Repository imports
from app.data.repositories.course import CourseRepository
from app.data.repositories.course_skill import CourseSkillRepository
from app.data.repositories.skill import SkillRepository
from app.data.repositories.employee import EmployeeRepository

# Load environment variables
load_dotenv()
import getpass
import os

# Correct configuration
DEPLOYMENT = "text-embedding-3-small"      # deployment name in Azure
API_VERSION = "2023-05-15"                 # API version
AZURE_OPENAI_ENDPOINT = "https://psacodesprint2025.azure-api.net"  # base endpoint only

# SQLite DB connection
DB_PATH = Path(__file__).parents[2] / "data" / "database" / "app.db"
conn = sqlite3.connect(str(DB_PATH))

# Repository instances
course_repo = CourseRepository(conn)
course_skill_repo = CourseSkillRepository(conn)
skill_repo = SkillRepository(conn)
employee_repo = EmployeeRepository(conn)

# Optional: Persist FAISS index to disk
FAISS_INDEX_PATH = Path(__file__).parents[2] / "data" / "database" / "course_vectorstore"

# ----------------------
# Build / Load Vectorstore
# ----------------------
def get_employee_context(employee_id: str) -> dict:
    """
    Fetch a complete employee context (profile, readable skills, goals, courses).
    """
    employee = employee_repo.get_employee(employee_id)
    if not employee:
        raise ValueError(f"Employee {employee_id} not found")

    # Parse fields (your EmployeeRepository should already normalize JSON)
    skill_map = employee.get("skills", {})
    skill_names = []
    for skill_id in skill_map.keys():
        skill = skill_repo.get_skill(skill_id)
        if skill:
            skill_names.append(skill["name"])
    courses_enrolled = json.loads(employee.get("courses_enrolled_map", "{}"))
    goals = json.loads(employee.get("goals_set", "[]"))
    return {
        "profile": {
            "id": employee.get("id"),
            "name": employee.get("name"),
            "role": employee.get("role"),
            "department_id": employee.get("department_id"),
            "level": employee.get("level"),
            "points_current": employee.get("points_current"),
            "hire_date": employee.get("hire_date")
        },
        "skills": skill_names,
        "goals": employee.get("goals", []),
        "courses_enrolled": employee.get("courses_enrolled", {})
    }

def build_or_load_vectorstore() -> FAISS:
    # Initialize Azure OpenAI embeddings correctly
    embeddings = AzureOpenAIEmbeddings(
        model=DEPLOYMENT,
        azure_deployment=DEPLOYMENT,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        openai_api_version=API_VERSION,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )

    if FAISS_INDEX_PATH.exists():
        print("Loading existing FAISS vectorstore from disk...")
        try:
            vectorstore = FAISS.load_local(str(FAISS_INDEX_PATH), embeddings)
            print("Vectorstore loaded successfully!")
            return vectorstore
        except Exception as e:
            print(f"Failed to load vectorstore: {e}")
            print("Rebuilding vectorstore...")

    print("Building new FAISS vectorstore from DB...")
    courses = course_repo.list_courses() or []

    texts = []
    metadatas = []

    for course in courses:
        cid = course["id"]
        skills = course_skill_repo.get_skills_for_course(cid) or []
        skills_sorted = sorted(skills, key=lambda r: r.get("weight", 0), reverse=True)
        skill_names = [str(r.get("skill_name") or r.get("skill_id")) for r in skills_sorted]

        content_parts = [str(course.get("description") or "")]
        if skill_names:
            content_parts.append("Skills: " + ", ".join(skill_names))
        page_content = "\n\n".join([p for p in content_parts if p])

        metadata = {
            "id": str(cid),
            "title": str(course.get("title") or ""),
            "url": str(course.get("url") or ""),
            "skills": skill_names,
            "domain": str(course.get("domain") or ""),
            "active": int(course.get("active") or 0),
        }

        texts.append(page_content)
        metadatas.append(metadata)

    # Build vectorstore from texts + metadatas
    vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

    # Persist to disk
    try:
        vectorstore.save_local(str(FAISS_INDEX_PATH))
        print(f"Vectorstore saved to {FAISS_INDEX_PATH}")
    except Exception as e:
        print(f"Warning: Could not save vectorstore: {e}")

    return vectorstore

# ----------------------
# Load vectorstore once
# ----------------------
vectorstore = build_or_load_vectorstore()

# ----------------------
# Recommendation Tool
# ----------------------
def recommend_courses_tool(employee_skills: List[str], top_k: int = 3) -> List[Dict]:
    """
    Given a list of employee skills, return top_k course recommendations using vector similarity.
    """
    query_text = " ".join(employee_skills)
    docs = vectorstore.similarity_search(query_text, k=top_k)

    recommendations = []
    for doc in docs:
        recommendations.append({
            "title": doc.metadata["title"],
            "url": doc.metadata["url"],
            "skills": doc.metadata["skills"],
            "reason": f"This course matches the employee's skills: {', '.join(employee_skills)}"
        })
    return recommendations

# if __name__ == "__main__":
#     from tools import get_employee_context, recommend_courses_tool

#     employee_id = "EMP004"

#     print(f"=== Fetching Employee {employee_id} Context ===")
#     emp_context = get_employee_context(employee_id)

#     print("\n--- Employee Profile ---")
#     for k, v in emp_context["profile"].items():
#         print(f"{k}: {v}")

#     print("\n--- Employee Skills ---")
#     print(", ".join(emp_context["skills"]) or "No skills found")

#     print("\n--- Employee Goals ---")
#     print(", ".join(emp_context["goals"]) or "No goals found")

#     print("\n--- Courses Enrolled ---")
#     print(emp_context["courses_enrolled"] or "None")

#     # Generate course recommendations
#     print("\n=== Generating Course Recommendations ===")
#     skills_for_recommendation = emp_context["skills"]
#     recommendations = recommend_courses_tool(skills_for_recommendation, top_k=5)

#     if not recommendations:
#         print("No recommendations found.")
#     else:
#         for idx, rec in enumerate(recommendations, 1):
#             print(f"\n[{idx}] {rec['title']}")
#             print(f"URL: {rec['url']}")
#             print(f"Skills: {', '.join(rec['skills'])}")
#             print(f"Reason: {rec['reason']}")

if __name__ == "__main__":
    print(get_employee_context("EMP003"))
