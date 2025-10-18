"""
LangChain AzureOpenAI Embeddings example for PSA Hackathon
"""
import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()

# Correct configuration
DEPLOYMENT = "text-embedding-3-small"      # deployment name in Azure
API_VERSION = "2023-05-15"                 # API version
AZURE_OPENAI_ENDPOINT = "https://psacodesprint2025.azure-api.net"  # base endpoint only

# Create embeddings model
embeddings = AzureOpenAIEmbeddings(
    model=DEPLOYMENT,
    azure_deployment=DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_version=API_VERSION,
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  # ensure this is set
)

# Example
input_text = "The meaning of life is 42"
vector = embeddings.embed_query(input_text)
print(vector[:3])
