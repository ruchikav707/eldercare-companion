# ElderCare Companion: Friction Log

This document records development and testing hurdles, bugs, or workflow roadblocks encountered during the MVP development lifecycle.

---

## Log Entry 1: PowerShell `mysql` Command Not Recognized
- **Task Attempted:** Accessing the MySQL command-line utility directly from the PowerShell terminal.
- **Steps Taken:** Typed `mysql -u root -p` in the terminal.
- **Expected Result:** MySQL prompt opens immediately.
- **Actual Result:** PowerShell threw an error stating that `mysql` is not recognized as the name of a cmdlet, function, script file, or operable program.
- **Severity:** Low
- **Workaround:** Used XAMPP / MySQL Workbench GUI / added the MySQL bin directory to the Windows Environment PATH variables.
- **Suggested Improvement:** Document local path setup instructions for Windows / PowerShell developers in the onboarding guide.

---

## Log Entry 2: Design Risk - Ambiguous Natural Language Appointment Updates (Planned Feature)
- **Task Attempted:** Evaluating how future AI-based update tools will handle multiple matching appointments (e.g., two doctor visits on the same day).
- **Steps Taken:** Analyzed potential edge cases for future natural language update execution.
- **Expected Result:** Clear design specification preventing unintended record updates.
- **Actual Result:** Identified as a potential design risk since AI update/cancel tools are not yet implemented in the current MVP.
- **Severity:** Medium (Design Risk)
- **Workaround:** Kept AI update/cancel features out of the MVP scope; updates currently go through explicit REST API calls.
- **Suggested Improvement:** Require the future AI update workflow to call `list_appointments()` and prompt the user for clarification before modifying any records.

---

## Log Entry 3: Gemini Model Version 404 Error for New Users
- **Task Attempted:** Integrating the LLM chat endpoint (`POST /agent/chat`) using `gemini-2.5-flash`.
- **Steps Taken:** Initialized the Gemini client and sent test prompt payloads.
- **Expected Result:** Successful model response without authentication or model-not-found errors.
- **Actual Result:** Received a 404 error indicating the specified model version was unavailable for new API user tiers.
- **Severity:** High
- **Workaround:** Switched the model identifier to `gemini-3.8-flash`.
- **Suggested Improvement:** Document model compatibility and fallback tiers clearly in configuration notes.