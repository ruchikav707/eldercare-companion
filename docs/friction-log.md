# ElderCare Companion: Friction Log

This document records development and testing hurdles, bugs, or workflow roadblocks encountered during the MVP development lifecycle.

---

## Log Entry 1: FastAPI Database Connection Initialization
- **Task Attempted:** Connecting the FastAPI backend to the local MySQL database (`eldercare_db`).
- **Steps Taken:** Configured `.env` file credentials and executed `uvicorn app.main:app --reload`.
- **Expected Result:** Instant successful connection pool establishment with MySQL.
- **Actual Result:** Initial connection timeout due to MySQL service not running locally on the default port.
- **Severity:** Medium
- **Workaround:** Started the MySQL service locally via Windows Services / XAMPP before launching Uvicorn.
- **Suggested Improvement:** Add automated database connection health checks and clearer startup error messaging in `backend/app/database.py`.

---

## Log Entry 2: Ambiguous Natural Language Appointment Matching
- **Task Attempted:** Defining how the AI agent handles multiple appointments on the same day (e.g., two doctor visits).
- **Steps Taken:** Tested agent behavior when a user says *"Change my doctor appointment"*.
- **Expected Result:** Agent immediately updates one without asking.
- **Actual Result:** Without clarification, the agent risked updating the wrong record.
- **Severity:** High (Data integrity risk)
- **Workaround:** Implemented strict disambiguation rules in the system prompt requiring the agent to call `list_appointments()` and ask the user to specify which appointment they mean.
- **Suggested Improvement:** Pass appointment IDs or descriptive time slots directly into conversational prompts when multiple matches occur.