import os

from ollama import Client

client = Client(
        host='https://ollama.com',
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )
MODEL = os.getenv("OLLAMA_MODEL")
# print("FUCK YOU: ", MODEL)

def supervisor(message: str, user_id: str) -> str:

    messages = [
        {
            "role": "system",
            "content": """
You are a supervisor routing agent.

Your responsibility:
- Understand the borrower query
- Route the query to the correct specialized agent

Available agents:
- LOAN_ADVISORY
    Handles:
    - Loan recommendations
    - EMI discussions
    - Interest comparisons
    - Borrowing guidance

- REPAYMENT
    Handles:
    - EMI repayment workflows
    - Missed payments
    - Repayment simulations
    - Restructuring discussions

- ELIGIBILITY
    Handles:
    - Loan eligibility assessment
    - Creditworthiness analysis
    - Risk evaluation
    - Debt-to-income analysis

- VERIFICATION
    Handles:
    - KYC verification
    - Identity validation
    - Compliance procedures
    - Required document checks

RULES:
- Choose exactly ONE agent
- Return ONLY the agent name
- Do not explain anything
"""
        },
        {
            "role": "user",
            "content": f"""
USER ID:
{user_id}

MESSAGE:
{message}
"""
        }
    ]

    response = client.chat(
        model=MODEL,
        messages=messages,
        stream=False
    )

    output = response["message"]["content"].strip().lower()

    if "repayment" in output:
        return "repayment"

    if "eligibility" in output:
        return "eligibility"

    if "verification" in output:
        return "verification"

    return "loan_advisory"


# agent = supervisor(
#     "I missed my EMI payment and need a new repayment plan",
#     "U001"
# )

# print(agent)
