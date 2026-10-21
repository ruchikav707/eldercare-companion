import json
from datetime import date

from app.agent_tools import (
    create_appointment,
    get_daily_plan,
    list_appointments
)
from app.ai_client import GEMINI_MODEL, get_gemini_client


SYSTEM_PROMPT = """
You are ElderCare Companion, a warm and patient simulated Alexa+ assistant.

Available capabilities:
- Use list_appointments to retrieve every stored appointment.
- Use get_daily_plan to retrieve scheduled appointments for one date.
- Use create_appointment to prepare a new appointment.

Appointment creation rules:
- A title, date and time are required.
- Ask a clarifying question if any required detail is missing.
- Never guess a missing date or time.
- When all required information is available, call create_appointment.
- The backend will request confirmation before saving the appointment.
- Never claim an appointment was saved before receiving a successful
  tool result.

General rules:
- Never invent appointment information.
- Base appointment answers only on tool results.
- Clearly mention when an appointment is cancelled.
- Never diagnose medical conditions.
- Never recommend medicines, dosages or treatments.
- Encourage professional or emergency help when appropriate.
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


CREATE_APPOINTMENT_TOOL = {
    "type": "function",
    "name": "create_appointment",
    "description": (
        "Prepares a new appointment after the title, date and time "
        "have been provided. The backend requests confirmation before saving."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Name or purpose of the appointment"
            },
            "appointment_at": {
                "type": "string",
                "description": (
                    "Appointment date and time in "
                    "YYYY-MM-DDTHH:MM:SS format"
                )
            },
            "location": {
                "type": "string",
                "description": "Optional appointment location"
            },
            "preparation_notes": {
                "type": "string",
                "description": "Optional preparation instructions"
            }
        },
        "required": ["title", "appointment_at"]
    }
}


AVAILABLE_TOOLS = [
    LIST_APPOINTMENTS_TOOL,
    GET_DAILY_PLAN_TOOL,
    CREATE_APPOINTMENT_TOOL
]


SESSION_INTERACTIONS: dict[str, str] = {}
PENDING_ACTIONS: dict[str, dict] = {}


CONFIRMATION_WORDS = {
    "yes",
    "yes please",
    "confirm",
    "confirmed",
    "please do",
    "do it",
    "yeah",
    "yup"
}


REJECTION_WORDS = {
    "no",
    "no thanks",
    "cancel",
    "stop",
    "do not",
    "don't"
}


def normalize_message(message: str) -> str:
    """Prepare a short reply for confirmation checking."""

    return message.strip().lower().rstrip(".!")


def execute_read_tool(tool_name: str, arguments: dict) -> dict:
    """Execute tools that only read information from the database."""

    if tool_name == "list_appointments":
        return list_appointments()

    if tool_name == "get_daily_plan":
        return get_daily_plan(arguments["date"])

    return {
        "error": f"Unsupported read tool: {tool_name}"
    }


def build_confirmation_message(arguments: dict) -> str:
    """Create a clear appointment summary before saving it."""

    return (
        "I’m ready to create this appointment:\n\n"
        f"- Title: {arguments['title']}\n"
        f"- Date and time: {arguments['appointment_at']}\n"
        f"- Location: {arguments.get('location') or 'Not provided'}\n"
        "- Preparation notes: "
        f"{arguments.get('preparation_notes') or 'None'}\n\n"
        "Should I save it? Please reply yes or no."
    )


def complete_pending_action(
    message: str,
    session_id: str
) -> dict:
    """Handle confirmation or rejection of a pending appointment."""

    normalized_message = normalize_message(message)
    pending_action = PENDING_ACTIONS[session_id]

    if normalized_message in REJECTION_WORDS:
        PENDING_ACTIONS.pop(session_id, None)
        SESSION_INTERACTIONS.pop(session_id, None)

        return {
            "reply": "Okay, I did not create the appointment.",
            "tool_used": None,
            "confirmation_required": False
        }

    if normalized_message not in CONFIRMATION_WORDS:
        return {
            "reply": (
                "The appointment has not been saved yet. "
                "Please reply yes to save it or no to cancel."
            ),
            "tool_used": "create_appointment",
            "confirmation_required": True
        }

    tool_result = create_appointment(
        **pending_action["arguments"]
    )

    PENDING_ACTIONS.pop(session_id, None)

    if "error" in tool_result:
        SESSION_INTERACTIONS.pop(session_id, None)

        return {
            "reply": tool_result["error"],
            "tool_used": "create_appointment",
            "confirmation_required": False
        }

    client = get_gemini_client()

    try:
        final_interaction = client.interactions.create(
            model=GEMINI_MODEL,
            previous_interaction_id=pending_action["interaction_id"],
            tools=AVAILABLE_TOOLS,
            input=[
                {
                    "type": "function_result",
                    "name": pending_action["tool_name"],
                    "call_id": pending_action["call_id"],
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(tool_result)
                        }
                    ]
                }
            ]
        )

        SESSION_INTERACTIONS[session_id] = final_interaction.id
        reply = final_interaction.output_text

    except Exception:
        SESSION_INTERACTIONS.pop(session_id, None)
        reply = (
            "Your appointment was created successfully. "
            f"Its appointment ID is {tool_result['id']}."
        )

    return {
        "reply": reply,
        "tool_used": "create_appointment",
        "confirmation_required": False
    }


def respond_to_message(
    message: str,
    session_id: str
) -> dict:
    """Respond to one message while preserving session context."""

    if session_id in PENDING_ACTIONS:
        return complete_pending_action(message, session_id)

    client = get_gemini_client()
    previous_interaction_id = SESSION_INTERACTIONS.get(session_id)

    if previous_interaction_id:
        interaction = client.interactions.create(
            model=GEMINI_MODEL,
            previous_interaction_id=previous_interaction_id,
            input=message,
            tools=AVAILABLE_TOOLS
        )

    else:
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

    SESSION_INTERACTIONS[session_id] = interaction.id

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
            "tool_used": None,
            "confirmation_required": False
        }

    arguments = dict(tool_call.arguments)

    if tool_call.name == "create_appointment":
        PENDING_ACTIONS[session_id] = {
            "tool_name": tool_call.name,
            "arguments": arguments,
            "interaction_id": interaction.id,
            "call_id": tool_call.id
        }

        return {
            "reply": build_confirmation_message(arguments),
            "tool_used": "create_appointment",
            "confirmation_required": True
        }

    tool_result = execute_read_tool(
        tool_call.name,
        arguments
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

    SESSION_INTERACTIONS[session_id] = final_interaction.id

    return {
        "reply": final_interaction.output_text,
        "tool_used": tool_call.name,
        "confirmation_required": False
    }