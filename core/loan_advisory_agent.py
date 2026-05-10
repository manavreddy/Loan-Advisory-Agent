import json
import os

from ollama import Client
from build_agent_prompt import build_agent_prompt

client = Client(
        host='https://ollama.com',
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )
MODEL = os.getenv("OLLAMA_MODEL")
def loan_advisory_agent(message: str, user_id : str):

    messages = [
        {
            "role": "system",
            "content": """
            You are a Loan Advisory Agent.

            Your responsibilities:
            - Loan recommendations
            - Interest comparisons
            - EMI discussions
            - Tenure guidance
            - Borrowing affordability analysis

            Behavior rules:
            - Be analytical
            - Be financially grounded
            - Focus only on loan advisory workflows
            - Generate relevant tool calls
            """
        },
        {
            "role": "system",
            "content": build_agent_prompt("Loan Advisory", user_id)
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
