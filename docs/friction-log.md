# ElderCare Companion: Friction Log

This document records development and testing hurdles, bugs, and workflow roadblocks encountered during the ElderCare Companion MVP development lifecycle.

---

## Log Entry 1: PowerShell `mysql` Command Not Recognized

- **Task Attempted:** Accessing the MySQL command-line utility directly from the PowerShell terminal.
- **Steps Taken:** Typed `mysql -u root -p` in the terminal.
- **Expected Result:** The MySQL prompt should open immediately.
- **Actual Result:** PowerShell reported that `mysql` was not recognized as a cmdlet, function, script file, or executable program.
- **Severity:** Low
- **Workaround:** Used MySQL Workbench or added the MySQL `bin` directory to the Windows PATH environment variable.
- **Suggested Improvement:** Include Windows and PowerShell PATH configuration instructions in the onboarding documentation.

---

## Log Entry 2: Ambiguous Natural Language Appointment Updates

- **Task Attempted:** Evaluating how future AI update tools should handle multiple matching appointments, such as two doctor visits on the same day.
- **Steps Taken:** Analyzed possible edge cases for natural-language update and cancellation requests.
- **Expected Result:** A clear design that prevents the wrong appointment from being modified.
- **Actual Result:** This was identified as a design risk because AI update and cancellation tools are not implemented in the current MVP.
- **Severity:** Medium (Design Risk)
- **Workaround:** Kept AI update and cancellation actions outside the MVP. These operations currently use explicit REST API calls.
- **Suggested Improvement:** A future AI update workflow should first call `list_appointments()` and ask the user for clarification when multiple records match.

---

## Log Entry 3: Gemini Model Version 404 Error for New Users

- **Task Attempted:** Integrating the LLM chat endpoint (`POST /agent/chat`) using `gemini-2.5-flash`.
- **Steps Taken:** Initialized the Gemini client and sent test prompts.
- **Expected Result:** The selected Gemini model should return a successful response.
- **Actual Result:** A 404 error reported that the selected model was unavailable for new API users.
- **Severity:** High
- **Workaround:** Changed the model identifier to `gemini-3.8-flash`.
- **Suggested Improvement:** Clearly document current model availability and recommended fallback models.

---

## Log Entry 4: Gemini Free-Tier Quota Blocked AI-Agent Testing

- **Date:** October 22, 2026
- **Category:** Third-party AI dependency; not an Amazon or Alexa+ issue
- **Task Attempted:** Testing the ElderCare AI agent through the FastAPI `POST /agent/chat` endpoint.

### Steps Taken

1. Started the FastAPI backend with Uvicorn.
2. Opened the Swagger UI.
3. Sent a normal appointment request to `/agent/chat`.
4. Waited several minutes while the request continued loading.
5. Added an HTTP timeout and reduced automatic retry attempts.
6. Tested Gemini directly without FastAPI, MySQL, or agent tools.
7. Received a `429 RESOURCE_EXHAUSTED` error.

- **Expected Result:** Gemini should interpret the user's request, select the appropriate appointment tool, and return a response within a few seconds.
- **Actual Result:** The Gemini 3.8 Flash free-tier quota of 20 requests was exhausted. The API requested that testing resume after approximately 12 hours. Automatic retries also caused the request to appear frozen before the error was identified.
- **Severity:** High during final testing because AI-agent workflows could not be tested or recorded until the quota reset.

### Workaround

- Paused unnecessary AI testing until the quota reset.
- Added a 30-second HTTP timeout and limited retry attempts.
- Added a deterministic India-specific emergency guardrail that does not depend on Gemini.
- Planned the final demonstration tests carefully to conserve API quota.

- **Suggested Improvement:** The developer dashboard and SDK documentation could display per-model quota usage and reset times more clearly. Quota errors should also be returned quickly, with clearer timeout and retry configuration examples.