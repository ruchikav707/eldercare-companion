import json
from datetime import date

from app.ai_client import GEMINI_MODEL, get_gemini_client
from app.agent_tools import get_daily_plan, list_appointments


SYSTEM_PROMPT = """
You are ElderCare Companion, a warm and patient simulated Alexa+ assistant.

Available capabilities:
- Use list_appointments to retrieve every stored appointment.
- Use get_daily_plan to retrieve scheduled appointments for one date.

Rules:
- Use list_appointments when the user asks for all appointments.
- Use get_daily_plan when the user asks about a particular date,
  today, tomorrow or a daily plan.
- Never invent appointment information.
- Base appointment answers only on tool results.
- Clearly mention when an appointment is cancelled.
- Never diagnose conditions or recommend medicines or treatments.
- Keep responses clear, respectful and concise.
"""


LIST_APPOINTMENTS_TOOL = {
    "type": "function",
    "name": "list_appointments",
    "description": (
        "Retrieves every stored appointment, including scheduled and "
        "cancelled appointments, ordered by date and time."
    ),
    "parameters": {
        "type": "object",
        "properties": {}
    }
}


GET_DAILY_PLAN_TOOL = {
    "type": "function",
    "name": "get_daily_plan",
    "description": (
        "Retrieves scheduled appointments for one specific calendar date."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "Calendar date in YYYY-MM-DD format"
            }
        },
        "required": ["date"]
    }
}


AVAILABLE_TOOLS = [
    LIST_APPOINTMENTS_TOOL,
    GET_DAILY_PLAN_TOOL
]


def execute_tool(tool_name: str, arguments: dict) -> dict:
    if tool_name == "list_appointments":
        return list_appointments()

    if tool_name == "get_daily_plan":
        return get_daily_plan(arguments["date"])

    return {
        "error": f"Unsupported tool: {tool_name}"
    }


def respond_to_message(message: str) -> dict:
    client = get_gemini_client()
    current_date = date.today().isoformat()

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=(
            f"{SYSTEM_PROMPT}\n\n"
            f"Current date: {current_date}\n"
            f"User message: {message}"
        ),
        tools=AVAILABLE_TOOLS
    )

    tool_call = next(
        (
            step
            for step in interaction.steps
            if step.type == "function_call"
        ),
        None
    )

    if tool_call is None:
        return {
            "reply": interaction.output_text,
            "tool_used": None
        }

    tool_result = execute_tool(
        tool_call.name,
        tool_call.arguments
    )

    final_interaction = client.interactions.create(
        model=GEMINI_MODEL,
        previous_interaction_id=interaction.id,
        tools=AVAILABLE_TOOLS,
        input=[
            {
                "type": "function_result",
                "name": tool_call.name,
                "call_id": tool_call.id,
                "result": [
                    {
                        "type": "text",
                        "text": json.dumps(tool_result)
                    }
                ]
            }
        ]
    )

    return {
        "reply": final_interaction.output_text,
        "tool_used": tool_call.name
    }