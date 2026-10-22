
import json
import os
import re
from datetime import date, datetime, time, timedelta

from app.agent_tools import (
    create_appointment,
    get_daily_plan,
    list_appointments
)
from app.ai_client import GEMINI_MODEL, get_gemini_client


DEMO_MODE = os.getenv("DEMO_MODE", "false").casefold() == "true"


EMERGENCY_PHRASES = (
    "severe chest pain",
    "trouble breathing",
    "difficulty breathing",
    "cannot breathe",
    "can't breathe",
    "not breathing",
    "unconscious",
    "heavy bleeding"
)


def get_emergency_response(message: str) -> dict | None:
    """Return immediate India-specific guidance for clear emergencies."""

    normalized_message = message.casefold()

    emergency_detected = any(
        phrase in normalized_message
        for phrase in EMERGENCY_PHRASES
    )

    if not emergency_detected:
        return None

    return {
        "reply": (
            "This may be an emergency. If you are in India, "
            "call 112 immediately or ask someone nearby to call. "
            "Go to the nearest emergency department now. "
            "I cannot contact emergency services for you. "
            "Please do not wait for a response from this assistant."
        ),
        "tool_used": None,
        "confirmation_required": False
    }


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
- The intended users are located in India.
- If the user describes severe symptoms or immediate danger, clearly
  advise them to call India's emergency number 112 or go to the nearest
  emergency department immediately.
- Never mention 911 unless the user explicitly says they are in a country
  where 911 is the correct emergency number.
- Never claim that you contacted or dispatched emergency services.
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
DEMO_DRAFTS: dict[str, dict] = {}


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


def clean_assistant_reply(reply: str) -> str:
    """Remove simple Markdown formatting unsupported by the chat UI."""

    return (
        reply
        .replace("**", "")
        .replace("__", "")
        .strip()
    )


def format_time(appointment_at: str) -> str:
    """Convert an ISO date-time into an easy-to-read time."""

    parsed_datetime = datetime.fromisoformat(appointment_at)
    return parsed_datetime.strftime("%I:%M %p").lstrip("0")


def format_daily_plan(tool_result: dict, day_label: str) -> str:
    """Turn the real daily-plan tool result into a friendly reply."""

    appointments = tool_result.get("appointments", [])

    if not appointments:
        return f"You have no appointments scheduled for {day_label}."

    if len(appointments) == 1:
        appointment = appointments[0]
        reply = (
            f"You have one appointment scheduled for {day_label}: "
            f"{appointment['title']} at "
            f"{format_time(appointment['appointment_at'])}"
        )

        if appointment.get("location"):
            reply += f" at {appointment['location']}"

        if appointment.get("preparation_notes"):
            reply += f". Remember: {appointment['preparation_notes']}"

        return reply + "."

    lines = [
        f"You have {len(appointments)} appointments scheduled for "
        f"{day_label}:"
    ]

    for appointment in appointments:
        line = (
            f"- {appointment['title']} at "
            f"{format_time(appointment['appointment_at'])}"
        )

        if appointment.get("location"):
            line += f" at {appointment['location']}"

        lines.append(line)

    return "\n".join(lines)


def extract_time(message: str) -> time | None:
    """Read a simple time such as 2 PM or 10:30 AM."""

    match = re.search(
        r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b",
        message,
        flags=re.IGNORECASE
    )

    if match is None:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    period = match.group(3).casefold()

    if hour < 1 or hour > 12 or minute > 59:
        return None

    if period == "pm" and hour != 12:
        hour += 12
    elif period == "am" and hour == 12:
        hour = 0

    return time(hour=hour, minute=minute)


def respond_in_demo_mode(message: str, session_id: str) -> dict:
    """Run reliable demo workflows with real tools and no Gemini request."""

    normalized_message = normalize_message(message)

    if session_id in DEMO_DRAFTS:
        selected_time = extract_time(message)

        if selected_time is None:
            return {
                "reply": (
                    "Please tell me the appointment time, for example "
                    "2 PM or 10:30 AM."
                ),
                "tool_used": None,
                "confirmation_required": False
            }

        draft = DEMO_DRAFTS.pop(session_id)
        appointment_datetime = datetime.combine(
            date.fromisoformat(draft["date"]),
            selected_time
        )

        arguments = {
            "title": draft["title"],
            "appointment_at": appointment_datetime.isoformat(),
            "location": draft.get("location"),
            "preparation_notes": draft.get("preparation_notes")
        }

        PENDING_ACTIONS[session_id] = {
            "tool_name": "create_appointment",
            "arguments": arguments,
            "demo_mode": True
        }

        return {
            "reply": build_confirmation_message(arguments),
            "tool_used": "create_appointment",
            "confirmation_required": True
        }

    if "tomorrow" in normalized_message and any(
        word in normalized_message
        for word in ("what", "plan", "schedule", "scheduled")
    ) and not any(
        word in normalized_message
        for word in ("add", "book", "create", "dentist")
    ):
        tomorrow = date.today() + timedelta(days=1)
        tool_result = get_daily_plan(tomorrow.isoformat())

        return {
            "reply": format_daily_plan(tool_result, "tomorrow"),
            "tool_used": "get_daily_plan",
            "confirmation_required": False
        }

    if any(
        phrase in normalized_message
        for phrase in ("schedule a dentist", "book a dentist", "add a dentist")
    ):
        tomorrow = date.today() + timedelta(days=1)
        selected_time = extract_time(message)

        if selected_time is None:
            DEMO_DRAFTS[session_id] = {
                "title": "Dentist appointment",
                "date": tomorrow.isoformat()
            }

            return {
                "reply": (
                    "What time would you like to schedule your dentist "
                    "appointment for tomorrow?"
                ),
                "tool_used": None,
                "confirmation_required": False
            }

        appointment_datetime = datetime.combine(tomorrow, selected_time)
        arguments = {
            "title": "Dentist appointment",
            "appointment_at": appointment_datetime.isoformat(),
            "location": None,
            "preparation_notes": None
        }

        PENDING_ACTIONS[session_id] = {
            "tool_name": "create_appointment",
            "arguments": arguments,
            "demo_mode": True
        }

        return {
            "reply": build_confirmation_message(arguments),
            "tool_used": "create_appointment",
            "confirmation_required": True
        }

    if "appointment" in normalized_message and any(
        word in normalized_message
        for word in ("show", "list", "all")
    ):
        tool_result = list_appointments()
        appointments = tool_result.get("appointments", [])

        if not appointments:
            reply = "You do not have any stored appointments."
        else:
            reply = (
                f"You have {len(appointments)} stored appointments. "
                "They are displayed on your appointment dashboard."
            )

        return {
            "reply": reply,
            "tool_used": "list_appointments",
            "confirmation_required": False
        }

    return {
        "reply": (
            "Demo mode currently supports checking tomorrow's schedule "
            "and scheduling a dentist appointment for tomorrow."
        ),
        "tool_used": None,
        "confirmation_required": False
    }


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

    if pending_action.get("demo_mode"):
        SESSION_INTERACTIONS.pop(session_id, None)

        appointment = tool_result["appointment"]
        reply = (
            f"Your {appointment['title'].lower()} was saved successfully "
            f"for {format_time(appointment['appointment_at'])}."
        )

        return {
            "reply": reply,
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
        reply = clean_assistant_reply(final_interaction.output_text)

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

    emergency_response = get_emergency_response(message)

    if emergency_response is not None:
        PENDING_ACTIONS.pop(session_id, None)
        SESSION_INTERACTIONS.pop(session_id, None)
        return emergency_response

    if session_id in PENDING_ACTIONS:
        return complete_pending_action(message, session_id)

    if DEMO_MODE:
        return respond_in_demo_mode(message, session_id)

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
            "reply": clean_assistant_reply(interaction.output_text),
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
        "reply": clean_assistant_reply(final_interaction.output_text),
        "tool_used": tool_call.name,
        "confirmation_required": False
    }
