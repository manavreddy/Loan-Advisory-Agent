import json
from pathlib import Path


USERS_FILE = Path(__file__).resolve().parents[1] / "data" / "users.json"


def get_user_profile(user_id):
    """Return a borrower profile by user_id."""
    if not user_id:
        return {"status": "error", "message": "user_id is required."}

    try:
        with USERS_FILE.open("r", encoding="utf-8") as file:
            users = json.load(file)
    except FileNotFoundError:
        return {"status": "error", "message": "data/users.json was not found."}
    except json.JSONDecodeError:
        return {"status": "error", "message": "users.json is not valid JSON."}

    normalized_user_id = str(user_id).strip().upper()
    for user in users:
        if str(user.get("user_id", "")).strip().upper() == normalized_user_id:
            return {
                "status": "success",
                "borrower_profile": user,
                "loan_history": user.get("existing_loans", []),
                "risk_info": {
                    "risk_profile": user.get("risk_profile"),
                    "credit_score": user.get("credit_score"),
                    "missed_payments_last_12m": user.get("missed_payments_last_12m"),
                    "employment_stability_years": user.get("employment_stability_years"),
                },
            }

    return {"status": "error", "message": f"User not found: {user_id}"}
