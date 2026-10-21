import json

from app.ai_client import GEMINI_MODEL, get_gemini_client
from app.agent_tools import list_appointments


SYSTEM_PROMPT = """
You are ElderCare Companion, a warm and patient simulated Alexa+ assistant.

Current capabilities:
- You can retrieve stored appointments using list_appointments.

Rules:
- Use list_appointments whenever the user asks about their appointments.
- Never invent appointment information.
- Base your answer only on the tool result.
- Clearly mention when an appointment is cancelled.
- Do not diagnose conditions or recommend medicines or treatments.
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


def respond_to_message(message: str) -> dict:
    client = get_gemini_client()

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=f"{SYSTEM_PROMPT}\n\nUser message: {message}",
        tools=[LIST_APPOINTMENTS_TOOL]
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

    if tool_call.name != "list_appointments":
        return {
            "reply": "I could not select a supported tool.",
            "tool_used": tool_call.name
        }

    tool_result = list_appointments()

    final_interaction = client.interactions.create(
        model=GEMINI_MODEL,
        previous_interaction_id=interaction.id,
        tools=[LIST_APPOINTMENTS_TOOL],
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