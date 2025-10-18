import os
import json
import urllib.request
from dotenv import load_dotenv
load_dotenv()

# Set your deployment/model info
DEPLOYMENT = "gpt-4.1-nano"
API_VERSION = "2025-01-01-preview"
API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "API_KEY_HERE")

url = f"https://psacodesprint2025.azure-api.net/openai/deployments/{DEPLOYMENT}/chat/completions?api-version={API_VERSION}"

headers = {
    'Content-Type': 'application/json',
    "Cache-Control" : "no-cache",
    'api-key': API_KEY,
}

body = {
    "messages": [
        {"role": "user", "content": "can you tell me an IT joke in 20 words?"}
    ],
    "model": DEPLOYMENT,
    "max_tokens": 128,
    "temperature": 1,
    "top_p": 1,
    "n": 1
}

if API_KEY == "API_KEY_HERE":
    print("Please set PRIMARY_API_KEY in your .env file or environment.")
    exit(1)

try:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, headers=headers, data=data, method="POST")
    with urllib.request.urlopen(req) as response:
        print("Status:", response.getcode())
        resp_data = response.read().decode()
        print("Response:", resp_data)
        # Optionally parse JSON and print just the message
        try:
            resp_json = json.loads(resp_data)
            print("AI says:", resp_json["choices"][0]["message"]["content"])
        except Exception:
            pass
except Exception as e:
    print("Error:", e)