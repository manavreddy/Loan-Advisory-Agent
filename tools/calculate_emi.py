def calculate_emi(principal, rate, tenure_months):
    """Calculate monthly EMI using reducing-balance interest."""
    try:
        principal = float(principal)
        annual_rate = float(rate)
        tenure_months = int(tenure_months)
    except (TypeError, ValueError):
        return {"status": "error", "message": "Invalid numeric arguments."}

    if principal <= 0:
        return {"status": "error", "message": "principal must be greater than 0."}
    if tenure_months <= 0:
        return {"status": "error", "message": "tenure_months must be greater than 0."}
    if annual_rate < 0:
        return {"status": "error", "message": "rate cannot be negative."}

    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        return round(principal / tenure_months, 2)

    emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months)
    emi = emi / (((1 + monthly_rate) ** tenure_months) - 1)
    return round(emi, 2)
