# ElderCare Companion: Testing & QA Checklist

This checklist defines the test cases required to verify the MVP functionality of the ElderCare Companion, while clearly distinguishing implemented features from planned future extensions.

---

## Part 1: Implemented MVP Features (Ready for Testing)

### 1. Viewing Appointments
- [ ] User can view all appointments (`list_appointments()`), including both scheduled and cancelled statuses.
- [ ] Database returns correct records formatted for the frontend dashboard.

### 2. Daily Plan
- [ ] User can request a schedule summary for a specific date (`get_daily_plan(date)`).
- [ ] Agent correctly parses temporal references like "tomorrow" into `YYYY-MM-DD` format.

### 3. Creating Appointments
- [ ] User can provide complete details (title, date/time, location, preparation notes).
- [ ] **Confirmation Rule:** Agent must summarize the action and ask for explicit confirmation *before* calling `create_appointment()`.
- [ ] Record is successfully inserted into MySQL with `status = 'scheduled'`.

### 4. Updating Appointments
- [ ] User can update allowed fields (`title`, `appointment_at`, `location`, `preparation_notes`).
- [ ] **Confirmation Rule:** Agent must ask for explicit confirmation before calling `update_appointment()`.
- [ ] **Security Rule:** Agent never attempts to update protected fields (`id`, `status` directly, `created_at`, `updated_at`).

### 5. Cancelling Appointments
- [ ] User can request appointment cancellation.
- [ ] **Confirmation Rule:** Agent asks for confirmation before calling `cancel_appointment()`.
- [ ] **Soft-Cancellation:** Record status updates to `cancelled` in MySQL (row is not permanently deleted).

### 6. Clarification & Missing Information
- [ ] Agent never guesses missing dates or times; asks clarifying questions instead.
- [ ] When multiple appointments match a query, agent lists options and asks the user to clarify.

### 7. Medical-Safety Guardrails
- [ ] Agent refuses to diagnose symptoms or recommend medicine dosages/treatments.
- [ ] When acute danger or severe symptoms are described, agent triggers the emergency override and provides India's public emergency number **112**.

---

## Part 2: Planned Features (Not Implemented in Current MVP)
*Note: The following features are outside the scope of the current hackathon MVP and are not currently implemented:*
- [ ] Medicine management / dosage schedules
- [ ] Real automated push notifications or reminders
- [ ] Family coordination / caregiver alerts
- [ ] Direct emergency service calling or dispatching
- [ ] Full voice support / hardware Alexa device integration
- [ ] Model Context Protocol (MCP) servers