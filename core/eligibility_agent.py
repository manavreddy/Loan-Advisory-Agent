import json
import os

from ollama import Client
from build_agent_prompt import build_agent_prompt

client = Client(
        host='https://ollama.com',
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )
MODEL = os.getenv("OLLAMA_MODEL")

def eligibility_agent(message: str, user_id : str):

    messages = [
        {
            "role": "system",
            "content": """
You are an Eligibility Agent.

Your responsibilities:
- Loan eligibility assessment
- Risk analysis
- Creditworthiness evaluation
- Debt-to-income analysis

Behavior rules:
- Be financially logical
- Be risk-aware
- Avoid unsupported assumptions
- Focus only on eligibility-related workflows
"""
        },
        {
            "role": "system",
            "content": build_agent_prompt("Eligibility", user_id)
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
