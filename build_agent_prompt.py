import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

with (ROOT_DIR / "tools.json").open("r", encoding="utf-8") as f:
    TOOLS = json.load(f)

with (ROOT_DIR / "data" / "users.json").open("r", encoding="utf-8") as f:
    USERS = json.load(f)


def get_user_data(user_id: str):
    normalized_user_id = str(user_id).strip().upper()
    for user in USERS:
        if str(user.get("user_id", "")).strip().upper() == normalized_user_id:
            return user
    return {}


def build_agent_prompt(agent_name: str, user_id: str):

    user_data = get_user_data(user_id)

    return f"""
    You are the {agent_name} agent.

    Your job:
    1. Understand the user query
    2. Analyze borrower data
    3. Select required tools
    4. Extract inputs for each tool
    5. Return ONLY valid JSON

    BORROWER DATA:
    {json.dumps(user_data, indent=2)}

    AVAILABLE TOOLS:
    {json.dumps(TOOLS, indent=2)}

    RULES:
    - Use only available tools
    - Do not invent parameters
    - Use borrower data whenever relevant
    - If information is missing, set value as null
    - Return strictly valid JSON
    - Do not explain anything
    - Do not generate conversational responses
    - Give the tool's inputs in the same order as it is in the available tools.

    OUTPUT FORMAT:

    {{
      "tools": [
        {{
          "name": "tool_name",
          "inputs": {{
            "param1": value,
            "param2": value
          }}
        }}
      ]
    }}
"""
