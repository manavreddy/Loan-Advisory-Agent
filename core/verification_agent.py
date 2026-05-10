import json
import os

from ollama import Client
from build_agent_prompt import build_agent_prompt

client = Client(
        host='https://ollama.com',
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )
MODEL = os.getenv("OLLAMA_MODEL")

def verification_agent(message: str, user_id : str):

    messages = [
        {
            "role": "system",
            "content": """
You are a Verification Agent.

Your responsibilities:
- Identity verification
- KYC workflows
- Compliance procedures
- Document validation

Behavior rules:
- Maintain a formal tone
- Be strict and compliance-oriented
- Do not provide financial advice
- Stay only within verification workflows
- Focus on extracting required tool calls
"""
        },
        {
            "role": "system",
            "content": build_agent_prompt("Verification", user_id)
        },
        {
            "role": "user",
            "content": message
        }
    ]

    response = client.chat(
        model=MODEL,
        messages=messages,
        stream=False,
        format="json"
    )

    return json.loads(response["message"]["content"])
