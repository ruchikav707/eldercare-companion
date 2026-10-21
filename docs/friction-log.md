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
- **Task Attempted:** Defining how the AI agent handles multiple appointments on the same day (e.g., two doctor visits) during an update request.
- **Steps Taken:** Tested agent behavior when a user says *"Change my doctor appointment"*.
- **Expected Result:** Agent asks for clarification instead of updating immediately.
- **Actual Result:** Initial conversational flow risked modifying the wrong record without proper prompt constraints.
- **Severity:** High (Data integrity risk)
- **Workaround:** Enforced strict disambiguation rules in the system prompt requiring the agent to ask clarifying questions before proceeding.
- **Suggested Improvement:** Pass explicit appointment IDs or descriptive time slots into conversational prompts when multiple matches occur.

---

## Log Entry 3: Gemini Model Version 404 Error for New Users
- **Task Attempted:** Integrating the LLM chat endpoint (`POST /agent/chat`) using `gemini-2.5-flash`.
- **Steps Taken:** Initialized the Gemini client and sent test prompt payloads.
- **Expected Result:** Successful model response without authentication or model-not-found errors.
- **Actual Result:** Received a 404 error indicating the specified model version was unavailable for new API user tiers.
- **Severity:** High
- **Workaround:** Switched the model identifier to `gemini-3.8-flash`.
- **Suggested Improvement:** Document model compatibility and fallback tiers clearly in configuration notes.