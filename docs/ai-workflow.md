# ElderCare Companion: AI Workflow & Agent Architecture

## 1. The AI Agent's Purpose & MVP Scope
The ElderCare Companion is a conversational AI assistant designed for the simulated Alexa+ hackathon track. Its purpose is to help elderly users manage their appointments and daily schedules through natural, empathetic dialogue. 
- **MVP Scope Note:** The current MVP promises only appointments and daily plans. Medicine management, real reminders, family coordination, emergency calling, MCP, and real Alexa integration are not part of the current MVP.

## 2. What Makes the Project Agentic
Unlike a traditional chatbot that only relies on pre-trained conversational weights, this agent is **agentic** because it can:
- Parse user intent from natural language.
- Select and execute specific tools (functions) dynamically.
- Read, create, update, and soft-cancel structured records in the MySQL database (`eldercare_db`).
- Maintain multi-turn conversational context to handle follow-up requests (e.g., changing appointment times).
- Fall back on safety rules and clarification prompts when user requests are ambiguous or unsafe.

## 3. Supported User Intentions
The ElderCare Companion recognizes the following core user goals:
- **Schedule an Appointment:** Booking a new medical, personal, or family appointment.
- **Check All Appointments:** Listing all appointments (including their current statuses) without a date filter.
- **Check Daily Plan:** Asking what is scheduled for a specific date (today, tomorrow, or a specific date using `get_daily_plan(date)`).
- **Update Appointment Details:** Modifying the title, time (`appointment_at`), location, or preparation notes of an existing appointment.
- **Cancel Appointment:** Changing an appointment's status to `cancelled` (soft-cancellation; the database record is not permanently deleted).
- **General Inquiries / Safety Checks:** Handling everyday questions while respecting strict medical and safety guardrails.

## 4. Tool Definitions and Required Parameters
To fulfill user intentions, the agent has access to the following 5 core tools:

### 1. `list_appointments()`
- **Purpose:** Retrieve all appointments, including their current statuses.
- **Parameters:** None.

### 2. `create_appointment(title, appointment_at, location, preparation_notes)`
- **Purpose:** Store a new appointment in the database.
- **Parameters:**
  - `title` (string): Short title/name of the appointment.
  - `appointment_at` (string, ISO datetime format `YYYY-MM-DDTHH:MM:SS`): Date and time of the event.
  - `location` (string): Venue or hospital name.
  - `preparation_notes` (string, optional): Notes or items to bring.

### 3. `update_appointment(id, fields_to_change)`
- **Purpose:** Modify specific fields of an existing appointment.
- **Parameters:**
  - `id` (integer): The unique appointment ID.
  - `fields_to_change` (object/dict): Key-value pairs to update. **Restriction:** The agent may update only `title`, `appointment_at`, `location`, or `preparation_notes`. The agent must never update `id`, `status` directly, `created_at`, or `updated_at`.

### 4. `cancel_appointment(id)`
- **Purpose:** Soft-cancel an appointment by changing its status to `cancelled`. (The database record is never permanently deleted).
- **Parameters:**
  - `id` (integer): The unique appointment ID.

### 5. `get_daily_plan(date)`
- **Purpose:** Retrieve the summarized schedule/daily plan for a particular date.
- **Parameters:**
  - `date` (string, YYYY-MM-DD): The target date for the summary.

## 5. Decision Rules for Selecting Tools
The agent uses the following logical mapping to choose the correct tool:
- If the user asks for *all* appointments without a date → Call `list_appointments()`.
- If the user asks about what is coming up or scheduled on a specific day (today, tomorrow, or a date) → Call `get_daily_plan(date)`.
- If the user wants to add a new event → Ask for explicit confirmation first, then call `create_appointment(...)`.
- If the user wants to change allowed fields of an existing event → Ask for explicit confirmation first, then call `update_appointment(id, fields_to_change)`.
- If the user wants to cancel an event → Ask for explicit confirmation first, then call `cancel_appointment(id)`.

## 6. Clarification & Confirmation Rules
The agent must follow strict behavioral guardrails before executing tools:
- **Never Guess Missing Dates or Times:** The agent must never guess a missing date or time and must ask a clarifying question.
- **Ambiguous Matches:** If multiple appointments could match the user's request, the agent may use `list_appointments()` to inspect records and must ask which appointment the user means.
- **Mandatory Confirmation:** The agent must ask for explicit confirmation before creating, updating, or cancelling an appointment.

## 7. Safety Rules
ElderCare Companion operates under strict medical and safety guardrails:
- **The Agent Must NOT:**
  - Diagnose any medical condition or recommend medicines, dosages, or treatments.
  - Replace a doctor or professional medical advice.
  - Claim that it contacted or dispatched emergency services.
- **Emergency Handling:** Use India's emergency number `112` when advising the user to contact local emergency services in case of severe symptoms or acute danger.

## 8. Test Conversations
Detailed agent behaviour, confirmation, clarification, safety and database-change test cases are documented in `docs/test-conversations.md`.