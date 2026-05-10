import json

from tools import execute_tool


def _parse_tool_output(raw_output):
    if isinstance(raw_output, str):
        try:
            return json.loads(raw_output)
        except json.JSONDecodeError:
            return raw_output
    return raw_output


def _normalize_sub_agent_output(sub_agent_output):
    if isinstance(sub_agent_output, str):
        return json.loads(sub_agent_output)

    if isinstance(sub_agent_output, list):
        return {"tools": sub_agent_output}

    if isinstance(sub_agent_output, dict):
        if "tools" in sub_agent_output:
            return sub_agent_output
        if "name" in sub_agent_output:
            return {"tools": [sub_agent_output]}

    raise ValueError(
        "Expected JSON object with a 'tools' list, a single tool object, or a list of tool objects."
    )


def implement_tools(sub_agent_output):
    """
    Execute tool calls selected by a sub-agent.

    Expected input:
    {
      "tools": [
        {
          "name": "calculate_emi",
          "inputs": {
            "principal": 500000,
            "rate": 11.5,
            "tenure_months": 36
          }
        }
      ]
    }

    Returns:
    {
      "results": [
        {
          "tool_name": "calculate_emi",
          "input_name": "calculate_emi_input",
          "inputs": {...},
          "output": 16488.0
        }
      ]
    }
    """
    normalized_output = _normalize_sub_agent_output(sub_agent_output)
    tool_calls = normalized_output.get("tools", [])

    if not isinstance(tool_calls, list):
        raise ValueError("'tools' must be a list.")

    results = []
    for index, tool_call in enumerate(tool_calls, start=1):
        if not isinstance(tool_call, dict):
            results.append(
                {
                    "tool_name": None,
                    "input_name": f"tool_{index}_input",
                    "inputs": None,
                    "output": {
                        "status": "error",
                        "message": "Tool call must be an object.",
                    },
                }
            )
            continue

        tool_name = tool_call.get("name") or tool_call.get("tool_name")
        inputs = tool_call.get("inputs", {})
        input_name = tool_call.get("input_name") or f"{tool_name or 'tool'}_input"

        if not isinstance(inputs, dict):
            results.append(
                {
                    "tool_name": tool_name,
                    "input_name": input_name,
                    "inputs": inputs,
                    "output": {
                        "status": "error",
                        "message": "Tool inputs must be an object.",
                    },
                }
            )
            continue

        raw_output = execute_tool(tool_name, inputs)
        results.append(
            {
                "tool_name": tool_name,
                "input_name": input_name,
                "inputs": inputs,
                "output": _parse_tool_output(raw_output),
            }
        )

    return {"results": results}
