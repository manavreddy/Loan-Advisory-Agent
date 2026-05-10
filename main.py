from core.orchestrator import orchestrate


def main():
    user_id = "U001"
    query = "Can I afford the requested home renovation loan? Please check EMI, eligibility, and risk."

    response = orchestrate(query=query, user_id=user_id)
    print(response)


if __name__ == "__main__":
    main()
