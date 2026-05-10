import json
import os
from pathlib import Path

from ollama import Client

client = Client(
        host='https://ollama.com',
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )
USERS_FILE = Path(__file__).resolve().parents[1] / "data" / "users.json"
MODEL = os.getenv("OLLAMA_MODEL")


def _load_user_data(user_id: str):
    with USERS_FILE.open("r", encoding="utf-8") as file:
        users = json.load(file)

    normalized_user_id = str(user_id).strip().upper()
    for user in users:
        if str(user.get("user_id", "")).strip().upper() == normalized_user_id:
            return user

    return {}


def _normalize_tool_outputs(tool_outputs):
    if isinstance(tool_outputs, str):
        try:
            return json.loads(tool_outputs)
        except json.JSONDecodeError:
            return {"raw_tool_output": tool_outputs}

    return tool_outputs


def generate_response(initial_query: str, user_id: str, tool_outputs):
    """
    Generate the final borrower-facing response using the original query,
    borrower profile, and JSON output returned by implemented tools.
    """
    user_data = _load_user_data(user_id)
    normalized_tool_outputs = _normalize_tool_outputs(tool_outputs)

    messages = [
        {
            "role": "system",
            "content": """
You are the final response generation agent for a loan advisory system.

Your job:
- Answer the user's original question using borrower data and tool outputs.
- Summarize tool results clearly.
- Keep the response financially grounded and borrower-friendly.
- Use only the provided borrower data and tool outputs.
- Do not invent numbers, eligibility decisions, risk levels, or repayment values.
- If tool data is missing or insufficient, say what information is missing.
- Keep the answer concise and practical.
- Do not expose raw JSON unless the user explicitly asks for JSON.
"""
        },
        {
            "role": "user",
            "content": f"""
USER ID:
{user_id}

INITIAL USER QUERY:
{initial_query}

BORROWER DATA FROM data/users.json:
{json.dumps(user_data, indent=2)}

TOOL OUTPUTS:
{json.dumps(normalized_tool_outputs, indent=2)}

INSTRUCTION:
Write the final response to the user. Summarize the relevant tool outputs and directly answer the initial query.
"""
        }
    ]

    response = client.chat(
        model=MODEL,
        messages=messages,
        stream=False
    )

    return response["message"]["content"].strip()


def response_generation(initial_query: str, user_id: str, tool_outputs):
    return generate_response(initial_query, user_id, tool_outputs)
