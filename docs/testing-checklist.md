# ElderCare Companion: Testing & QA Checklist

This checklist defines the test cases required to verify the MVP functionality of the ElderCare Companion, while clearly distinguishing implemented features from planned future extensions.

---

## Part 1: Implemented MVP Features (Ready for Testing)

### 1. Backend REST Endpoints
- [ ] `GET /appointments` retrieves all appointments including their statuses.
- [ ] `GET /appointments/daily-plan?date=YYYY-MM-DD` retrieves the daily plan for the specified date.
- [ ] `POST /appointments` creates a new appointment.
- [ ] `PUT /appointments/{id}` updates allowed fields (`title`, `appointment_at`, `location`, `preparation_notes`).
- [ ] `DELETE /appointments/{id}` performs a soft-cancellation (`status = 'cancelled'`).

### 2. Completed AI Agent Tests (`POST /agent/chat`)
- [ ] **Listing Appointments:** User asks to view all appointments and the agent successfully returns them.
- [ ] **Daily Plan:** User asks about schedule on a specific date and agent invokes `get_daily_plan`.
- [ ] **Understanding Relative Dates:** Agent correctly interprets relative terms like "tomorrow".
- [ ] **Missing-Time Clarification:** Agent refuses to guess missing time/date and asks a clarifying question.
- [ ] **Session Memory:** Agent maintains multi-turn context across conversation turns.
- [ ] **Yes Confirmation:** User responds "Yes" to a proposed creation action and the record is successfully created.
- [ ] **No Rejection:** User responds "No" and the agent creates nothing.

### 3. Medical-Safety Guardrails
- [ ] Agent refuses to diagnose symptoms or recommend medicine dosages/treatments.
- [ ] When acute danger or severe symptoms are described, agent triggers the emergency override and provides India's public emergency number **112**.

---

## Part 2: Planned Features (Not Implemented in Current MVP)
*Note: The following features are outside the scope of the current hackathon MVP and are not currently implemented:*
- [ ] AI-based appointment update tool (`update_appointment` via agent chat)
- [ ] AI-based appointment cancellation tool (`cancel_appointment` via agent chat)
- [ ] Multiple-match appointment disambiguation handling via AI chat
- [ ] Medicine management / dosage schedules
- [ ] Real automated push notifications or reminders
- [ ] Family coordination / caregiver alerts
- [ ] Direct emergency service calling or dispatching
- [ ] Full voice support / hardware Alexa device integration
- [ ] Model Context Protocol (MCP) servers