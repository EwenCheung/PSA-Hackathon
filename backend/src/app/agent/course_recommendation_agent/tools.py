# tools.py
import json
from typing import List, Dict
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document

# Load courses
with open("courses.json", "r") as f:
    course_data = json.load(f)

# Convert courses to documents
documents = [
    Document(
        page_content=course["description"],
        metadata={
            "title": course["title"],
            "url": course["url"],
            "skills": course["skills"],
            "domain": course["domain"]
        }
    )
    for course in course_data
]

# Create embeddings and FAISS vectorstore
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")  # Azure-compatible
vectorstore = FAISS.from_documents(documents, embeddings)

# Tool function for LangChain agent
def recommend_courses_tool(employee_skills: List[str], top_k: int = 3) -> List[Dict]:
    """
    Recommend courses using vector search based on employee skills.
    """
    query = " ".join(employee_skills)
    docs = vectorstore.similarity_search(query, k=top_k)

    recommendations = []
    for doc in docs:
        recommendations.append({
            "title": doc.metadata["title"],
            "url": doc.metadata["url"],
            "reason": f"This course matches the employee's skills: {', '.join(employee_skills)}"
        })
    return recommendations
