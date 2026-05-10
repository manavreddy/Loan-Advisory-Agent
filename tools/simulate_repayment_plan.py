from .calculate_emi import calculate_emi


def simulate_repayment_plan(amount, months, interest_rate):
    """Return EMI, total payable, and interest paid for a repayment plan."""
    try:
        amount = float(amount)
        months = int(months)
        interest_rate = float(interest_rate)
    except (TypeError, ValueError):
        return {"status": "error", "message": "Invalid numeric arguments."}

    emi = calculate_emi(amount, interest_rate, months)
    if isinstance(emi, dict) and emi.get("status") == "error":
        return emi

    total_payable = round(emi * months, 2)
    interest_paid = round(total_payable - amount, 2)

    return {
        "emi": emi,
        "total_payable": total_payable,
        "interest_paid": interest_paid,
    }
