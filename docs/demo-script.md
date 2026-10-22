# ElderCare Companion: Demo-Video Script & Submission Guide

- **Event:** Build, Ship, Shape: Amazon Developer Hackathon 2026
- **Track:** Alexa+ project track (simulated Alexa+ experience route)
- **Team Members:** Ruchika (FastAPI, MySQL, AI integration), Siya (React frontend, Dashboard), Prachi (AI workflow planning, Testing, Documentation)
- **Target Duration:** ~2 minutes 42 seconds (Optimized for a safe margin under the 3-minute hard limit; edit out AI response waiting times during editing).

---

## Scene-by-Scene Breakdown

### Scene 1: Opening Hook & Problem
- **Timestamp:** 0:00 – 0:18
- **Speaker:** Prachi
- **What Appears on Screen:** Title slide presenting ElderCare Companion, the scheduling problem, and our vision for conversational accessibility.
- **Exact Spoken Narration:** "Digital calendars are often packed with tiny buttons and confusing menus. For many older adults, managing appointments or checking daily schedules can feel stressful and frustrating."
- **User Message:** N/A (Intro slide)
- **Expected Assistant Response:** N/A

### Scene 2: Solution Overview
- **Timestamp:** 0:18 – 0:35
- **Speaker:** Siya
- **What Appears on Screen:** The solution overview slide introducing the simulated Alexa+ experience, natural dialogue, and safety guardrails.
- **Exact Spoken Narration:** "Meet ElderCare Companion. Built for the Alexa+ track, it is a simulated Alexa+ experience providing a warm, simple conversational interface for older adults to manage their schedules easily."
- **User Message:** N/A (App overview)
- **Expected Assistant Response:** N/A

### Scene 3: Live Workflow — Daily Plan
- **Timestamp:** 0:35 – 0:56
- **Speaker:** Ruchika
- **What Appears on Screen:** Simulated Alexa+ chat interface showing the user query and assistant response. (Note: Terminal or debug screens are omitted).
- **Exact Spoken Narration:** "Let us see it in action. First, checking tomorrow's schedule. The AI agent automatically selects the get_daily_plan tool to fetch database information."
- **User Message:** "What do I have scheduled for tomorrow?"
- **Expected Assistant Response:** (Note: Treatment as expected behavior rather than exact wording) "You have a doctor's appointment tomorrow at 10:00 AM at City Care Clinic." (Ensure database is pre-loaded with this exact test data prior to recording).

### Scene 4: Live Workflow — Clarification
- **Timestamp:** 0:56 – 1:20
- **Speaker:** Prachi
- **What Appears on Screen:** Chat interface. User adds an appointment request without specifying the time. The agent maintains short-term session context and asks a clarifying question.
- **Exact Spoken Narration:** "Next, adding a new appointment. Notice how the user omits the time. The agent maintains short-term session context and intelligently asks for the missing information."
- **User Message:** "Schedule a dentist appointment tomorrow."
- **Expected Assistant Response:** "I can schedule your dentist appointment for tomorrow. What time would you like to set it for?"

### Scene 5: Live Workflow — Confirmation & Dashboard
- **Timestamp:** 1:20 – 1:52
- **Speaker:** Siya
- **What Appears on Screen:** Chat interface showing the user providing the time ("At 2 PM."), the agent summarizing and asking for confirmation, user typing "Yes", and the React dashboard automatically refreshing to display the saved appointment.
- **Exact Spoken Narration:** "The user provides the time. The agent summarizes the details, asks for explicit confirmation, and upon receiving 'yes', stores the confirmed appointment in MySQL. After the appointment is saved, the React dashboard automatically refreshes and displays it."
- **User Message:** "At 2 PM." (Followed by "Yes" after confirmation prompt)
- **Expected Assistant Response:** "Appointment saved successfully!" React dashboard automatically refreshes and displays the new dentist appointment.

### Scene 6: Safety Guardrail
- **Timestamp:** 1:52 – 2:10
- **Speaker:** Prachi
- **What Appears on Screen:** Chat interface demonstrating the medical safety rule when reporting severe symptoms.
- **Exact Spoken Narration:** "ElderCare Companion uses a deterministic emergency guardrail before the AI call. It never diagnoses conditions or recommends medication. When severe symptoms are detected, it immediately provides India-focused emergency guidance using 112 and clearly states that it cannot contact emergency services."
- **User Message:** "I have severe chest pain and trouble breathing."
- **Expected Assistant Response:** "This may be an emergency. If you are in India, call 112 immediately or ask someone nearby to call. Go to the nearest emergency department now. I cannot contact emergency services for you. Please do not wait for a response from this assistant."

### Scene 7: Architecture
- **Timestamp:** 2:10 – 2:30
- **Speaker:** Ruchika
- **What Appears on Screen:** Architecture diagram: React Frontend → FastAPI Backend → Gemini AI Agent → Agent Tools → MySQL Database → Response.
- **Exact Spoken Narration:** "The React interface sends the user’s message to FastAPI. The Gemini-powered agent understands the goal, selects an allowed tool, and the tool safely reads from or writes to MySQL. FastAPI then returns the result to the interface."
- **User Message:** N/A (Architecture diagram)
- **Expected Assistant Response:** N/A

### Scene 8: Closing & Team
- **Timestamp:** 2:30 – 2:42
- **Speaker:** Prachi
- **What Appears on Screen:** Closing slide with team names (Ruchika, Siya, Prachi), project name, and hackathon details.
- **Exact Spoken Narration:** "ElderCare Companion brings simplicity and peace of mind to older adults. Thank you for watching our submission for the Amazon Developer Hackathon 2026!"
- **User Message:** N/A (Closing slide)
- **Expected Assistant Response:** N/A

---

## Pre-Recording Action Plan
1. **Database Preparation:** Populate MySQL with a scheduled doctor appointment for tomorrow at 10:00 AM at City Care Clinic. Ensure the dentist test slot is clear before the creation sequence.
2. **Video Editing Tip:** Cut out any network/API loading pauses so the final video flows smoothly within the ~2:42 target window.
3. **Team Rehearsal:** Run through the complete workflow once together before hitting record to verify timing and smooth speaker handoffs.
4. **Demo Reset:** Remove the dentist appointment created during rehearsal, restart the FastAPI backend to clear temporary session memory, and refresh the React frontend before recording.