from core.eligibility_agent import eligibility_agent
from core.loan_advisory_agent import loan_advisory_agent
from core.repayment_agent import repayment_agent
from core.response_generation import generate_response
from core.supervisor import supervisor
from tools.implement_tools import implement_tools
from core.verification_agent import verification_agent


AGENTS = {
    "loan_advisory": loan_advisory_agent,
    "repayment": repayment_agent,
    "eligibility": eligibility_agent,
    "verification": verification_agent,
}


def _normalize_agent_names(agent_names):
    if isinstance(agent_names, str):
        return [agent_names.strip().lower()]

    if isinstance(agent_names, list):
        return [str(agent_name).strip().lower() for agent_name in agent_names]

    return ["loan_advisory"]


def orchestrate(query: str, user_id: str):
    """
    Run the complete loan advisory pipeline.

    Flow:
    1. Supervisor selects the required sub-agent.
    2. Selected sub-agent returns tool calls in JSON format.
    3. Tool calls are executed.
    4. Response generation summarizes user data and tool outputs into the final answer.
    """
    selected_agents = _normalize_agent_names(supervisor(query, user_id))

    sub_agent_outputs = []
    tool_outputs = []

    for agent_name in selected_agents:
        agent = AGENTS.get(agent_name, loan_advisory_agent)
        sub_agent_output = agent(query, user_id)
        implemented_output = implement_tools(sub_agent_output)

        sub_agent_outputs.append(
            {
                "agent_name": agent_name,
                "tool_calls": sub_agent_output,
            }
        )
        tool_outputs.append(
            {
                "agent_name": agent_name,
                "tool_outputs": implemented_output,
            }
        )

    final_response = generate_response(
        initial_query=query,
        user_id=user_id,
        tool_outputs={
            "selected_agents": selected_agents,
            "sub_agent_outputs": sub_agent_outputs,
            "tool_outputs": tool_outputs,
        },
    )

    return final_response


def orchestration(query: str, user_id: str):
    return orchestrate(query, user_id)
