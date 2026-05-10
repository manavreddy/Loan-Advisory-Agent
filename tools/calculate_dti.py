def calculate_dti(user_profile):
    """Calculate debt-to-income ratio from existing EMIs and monthly income."""
    if not isinstance(user_profile, dict):
        return {"status": "error", "message": "user_profile must be an object."}

    try:
        monthly_income = float(user_profile.get("monthly_income", 0))
        existing_loans = user_profile.get("existing_loans", [])
        total_emi = sum(float(loan.get("emi", 0)) for loan in existing_loans)
    except (TypeError, ValueError):
        return {"status": "error", "message": "Invalid numeric fields in user_profile."}

    if monthly_income <= 0:
        return {"status": "error", "message": "monthly_income must be greater than 0."}

    dti_ratio = total_emi / monthly_income
    if dti_ratio < 0.30:
        risk = "Low"
    elif dti_ratio <= 0.50:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "dti_ratio": round(dti_ratio, 2),
        "risk": risk,
    }
