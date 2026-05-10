# Loan Advisory Agent

A small Python project that routes a borrower query to a specialist agent, runs selected financial tools, and generates a final response using Ollama.

This is a prototype/demo workflow. It uses sample borrower data from `data/users.json` and should not be treated as production financial advice or a real loan approval system.

## What It Does

The main flow is:

1. `core/supervisor.py` chooses one sub-agent for the user query.
2. One of the sub-agents creates tool calls:
   - `loan_advisory_agent`
   - `repayment_agent`
   - `eligibility_agent`
   - `verification_agent`
3. `tools/implement_tools.py` executes those tool calls.
4. `core/response_generation.py` combines the original query, user data, and tool outputs into a final answer.

The orchestration entry point is:

```python
from core.orchestrator import orchestrate

response = orchestrate(
    query="Can I afford the requested home renovation loan?",
    user_id="U001"
)
```

## Project Structure

```text
core/
  orchestrator.py           # End-to-end pipeline
  supervisor.py             # Routes query to an agent
  loan_advisory_agent.py    # Loan guidance tool-call agent
  repayment_agent.py        # Repayment tool-call agent
  eligibility_agent.py      # Eligibility/risk tool-call agent
  verification_agent.py     # Verification tool-call agent
  response_generation.py    # Final answer generation

tools/
  get_user_profile.py
  check_loan_eligibility.py
  calculate_emi.py
  calculate_dti.py
  simulate_repayment_plan.py
  assess_borrower_risk.py
  implement_tools.py

data/
  users.json                # Sample borrower profiles

tools.json                  # Tool descriptions for agent prompts
build_agent_prompt.py       # Builds prompts using tools + user data
main.py                     # Example run
```

## Setup

Create and activate a virtual environment if needed:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Install dependencies:

```powershell
pip install ollama
```

The current agent files use Ollama's Python client with:

```python
host="https://ollama.com"
```

So set these environment variables before running:

```powershell
$env:OLLAMA_API_KEY="your_ollama_api_key"
$env:OLLAMA_MODEL="your_model_name"
```

Do not commit real API keys.

## Run Example

`main.py` contains a simple example:

```powershell
python main.py
```

It currently runs:

```python
user_id = "U001"
query = "Can I afford the requested home renovation loan? Please check EMI, eligibility, and risk."
```

## Tools

The available deterministic tools are:

- `get_user_profile(user_id)`
- `check_loan_eligibility(user_profile)`
- `calculate_emi(principal, rate, tenure_months)`
- `calculate_dti(user_profile)`
- `simulate_repayment_plan(amount, months, interest_rate)`
- `assess_borrower_risk(user_profile)`

Tool metadata is stored in `tools.json`.

## Notes

- User data is sample data only.
- Tool outputs are simple rule-based calculations.
- The final response depends on the configured Ollama model.
- The project is intended for local experimentation with agent orchestration.

## Future Improvements

- Add proper RAG over loan policy documents in `data/` or `RAG/`.
- Use retrieved policy context in the supervisor, sub-agents, and final response generator.
- Return structured errors when an agent produces invalid JSON.
- Add tests for tools and orchestration flow.
- Move model/client configuration into one shared config file.
- Add a small CLI or API wrapper around `orchestrate(query, user_id)`.
- Add logging for selected agent, tool calls, and tool outputs.
