"""
LangChain AzureChatOpenAI agent example for PSA Hackathon

This script demonstrates how to use AzureChatOpenAI with LangChain for chat completions.
"""
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Load environment variables from .env
load_dotenv()
import getpass
import os

DEPLOYMENT = os.getenv("DEPLOYMENT")
API_VERSION = os.getenv("API_VERSION")
URL = f"https://psacodesprint2025.azure-api.net/openai/deployments/{DEPLOYMENT}/chat/completions?api-version={API_VERSION}"
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")


# https://python.langchain.com/docs/integrations/chat/azure_chat_openai/
# https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.azure.AzureChatOpenAI.html

llm = AzureChatOpenAI(
    azure_deployment="gpt-4.1-nano",  # Your deployment name
    api_version="2025-01-01-preview",  # Your API version
    temperature=0.7,
    max_tokens=128,
)

messages = [
    ("system", "You are a helpful assistant that tells IT jokes in 20 words."),
    ("human", "Can you tell me an IT joke in 20 words?")
]

ai_msg = llm.invoke(messages)
print("AI Response:", ai_msg.content)

# Example: Chaining with a prompt template
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
    ("human", "{input}"),
])

chain = prompt | llm
result = chain.invoke({
    "input_language": "English",
    "output_language": "German",
    "input": "I love programming.",
})
print("Chain Response:", result.content)



# Agent
# https://docs.langchain.com/oss/python/langchain/quickstart
print("\n--- Agent Example ---\n")
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
response =agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

# print("Agent Response:", response.messages.content)
print("Agent Response:", response)