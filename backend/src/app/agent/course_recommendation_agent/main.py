# main.py
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from tools import recommend_courses_tool
from system_prompt import SYSTEM_PROMPT

# Load environment
load_dotenv()
DEPLOYMENT = os.getenv("DEPLOYMENT")
API_VERSION = os.getenv("API_VERSION")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY

# Initialize Azure LLM
llm = AzureChatOpenAI(
    azure_deployment=DEPLOYMENT,
    api_version=API_VERSION,
    temperature=0.3,
    max_tokens=500
)

# Wrap tool as callable for LangChain
def recommend_courses_agent_tool(employee_skills):
    return recommend_courses_tool(employee_skills)

# Create the agent
agent = create_agent(
    model=llm,
    tools=[recommend_courses_agent_tool],
    system_prompt=SYSTEM_PROMPT
)

# Example usage
employee_skills = [
    "Cloud Architecture",
    "Cloud DevOps & Automation",
    "Securing Cloud Infrastructure"
]

response = agent.invoke({
    "messages": [
        {"role": "user", "content": f"Recommend courses for an employee with skills: {employee_skills}"}
    ]
})

print("Agent Response:", response.messages.content)
