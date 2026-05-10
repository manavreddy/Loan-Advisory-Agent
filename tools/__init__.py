import json

from .assess_borrower_risk import assess_borrower_risk
from .calculate_dti import calculate_dti
from .calculate_emi import calculate_emi
from .check_loan_eligibility import check_loan_eligibility
from .get_user_profile import get_user_profile
from .simulate_repayment_plan import simulate_repayment_plan


TOOL_FUNCTIONS = {
    "get_user_profile": get_user_profile,
    "check_loan_eligibility": check_loan_eligibility,
    "calculate_emi": calculate_emi,
    "calculate_dti": calculate_dti,
    "simulate_repayment_plan": simulate_repayment_plan,
    "assess_borrower_risk": assess_borrower_risk,
}


def execute_tool(action: str, arguments: dict) -> str:
    """Route a tool call from the agent to the matching implementation."""
    try:
        if action not in TOOL_FUNCTIONS:
            result = {"status": "error", "message": f"Unknown tool: {action}"}
        else:
            result = TOOL_FUNCTIONS[action](**(arguments or {}))

        return json.dumps(result)
    except TypeError as e:
        return json.dumps({"status": "error", "message": f"Invalid tool arguments: {e}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Exception during execution: {e}"})
