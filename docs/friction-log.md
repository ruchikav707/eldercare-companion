# ElderCare Companion Friction Log

This log records technical difficulties encountered while building and testing
the ElderCare Companion prototype.

## Entry 1 — Gemini free-tier quota blocked AI-agent testing

**Date:** October 22, 2026

**Category:** Third-party AI dependency — not an Amazon or Alexa+ issue

**Task attempted:**  
Test the ElderCare AI agent through the FastAPI `POST /agent/chat` endpoint.

**Steps taken:**

1. Started the FastAPI backend with Uvicorn.
2. Opened the Swagger UI.
3. Sent a normal appointment request to `/agent/chat`.
4. Waited several minutes, but the request continued loading.
5. Added an HTTP timeout and reduced automatic retry attempts.
6. Tested Gemini directly without FastAPI, MySQL or agent tools.
7. Received `429 RESOURCE_EXHAUSTED`.

**Expected result:**  
Gemini should interpret the user’s request, select the correct appointment
tool and return a response within a few seconds.

**Actual result:**  
The Gemini 3.8 Flash free-tier quota of 20 requests was exhausted. The API
requested that we retry after approximately 12 hours. Automatic retry
behaviour also made the request appear frozen before the error was identified.

**Severity:**  
High during final testing because AI-agent workflows could not be tested or
recorded until the quota reset.

**Workaround:**

- Paused unnecessary AI testing until the quota reset.
- Added a 30-second HTTP timeout and limited retry attempts.
- Added a deterministic emergency guardrail that returns India-specific
  emergency guidance without depending on Gemini.
- Planned the final demo tests carefully to conserve the remaining quota.

**Suggested improvement:**  
The developer dashboard and SDK documentation could display per-model quota
usage and reset time more prominently. Quota errors should also be returned
quickly instead of appearing as a long-running request, with clearer examples
showing how to configure timeout and retry behaviour.