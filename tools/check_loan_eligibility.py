def check_loan_eligibility(user_profile):
    """Check basic loan eligibility from income, expenses, credit, and liabilities."""
    if not isinstance(user_profile, dict):
        return {"status": "error", "message": "user_profile must be an object."}

    try:
        monthly_income = float(user_profile.get("monthly_income", 0))
        monthly_expenses = float(user_profile.get("monthly_expenses", 0))
        credit_score = int(user_profile.get("credit_score", 0))
        missed_payments = int(user_profile.get("missed_payments_last_12m", 0))
        existing_loans = user_profile.get("existing_loans", [])
    except (TypeError, ValueError):
        return {"status": "error", "message": "Invalid numeric fields in user_profile."}

    if monthly_income <= 0:
        return {"eligible": False, "reason": "Monthly income must be greater than zero."}

    total_existing_emi = sum(float(loan.get("emi", 0)) for loan in existing_loans)
    total_obligations = monthly_expenses + total_existing_emi
    obligation_ratio = total_obligations / monthly_income

    reasons = []
    if credit_score < 650:
        reasons.append("Credit score is below the preferred threshold.")
    if obligation_ratio > 0.65:
        reasons.append("Existing expenses and EMI burden are high compared with income.")
    if missed_payments > 2:
        reasons.append("Recent missed payments indicate repayment risk.")

    if reasons:
        return {"eligible": False, "reason": " ".join(reasons)}

    return {
        "eligible": True,
        "reason": "Stable income, acceptable credit score, and manageable liabilities.",
    }
