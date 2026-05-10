def assess_borrower_risk(user_profile):
    """Assess borrower risk from missed payments, DTI, credit score, and savings."""
    if not isinstance(user_profile, dict):
        return {"status": "error", "message": "user_profile must be an object."}

    try:
        monthly_income = float(user_profile.get("monthly_income", 0))
        monthly_expenses = float(user_profile.get("monthly_expenses", 0))
        credit_score = int(user_profile.get("credit_score", 0))
        missed_payments = int(user_profile.get("missed_payments_last_12m", 0))
        savings = float(user_profile.get("savings", 0))
        existing_loans = user_profile.get("existing_loans", [])
        total_emi = sum(float(loan.get("emi", 0)) for loan in existing_loans)
    except (TypeError, ValueError):
        return {"status": "error", "message": "Invalid numeric fields in user_profile."}

    if monthly_income <= 0:
        return {"status": "error", "message": "monthly_income must be greater than 0."}

    dti_ratio = total_emi / monthly_income
    savings_buffer_months = savings / monthly_expenses if monthly_expenses > 0 else 0

    score = 0
    factors = []

    if credit_score >= 750:
        factors.append("Strong credit score")
    elif credit_score >= 650:
        score += 1
        factors.append("Acceptable but not strong credit score")
    else:
        score += 2
        factors.append("Low credit score")

    if dti_ratio > 0.50:
        score += 2
        factors.append("High existing EMI burden")
    elif dti_ratio >= 0.30:
        score += 1
        factors.append("Moderate existing EMI burden")
    else:
        factors.append("Low existing EMI burden")

    if missed_payments > 2:
        score += 2
        factors.append("Multiple missed payments in the last 12 months")
    elif missed_payments > 0:
        score += 1
        factors.append("Some missed payments in the last 12 months")
    else:
        factors.append("Good repayment history")

    if savings_buffer_months < 2:
        score += 1
        factors.append("Limited savings buffer")
    else:
        factors.append("Adequate savings buffer")

    if score <= 1:
        risk_level = "Low"
    elif score <= 4:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "risk_level": risk_level,
        "factors": factors,
        "dti_ratio": round(dti_ratio, 2),
        "savings_buffer_months": round(savings_buffer_months, 1),
    }
