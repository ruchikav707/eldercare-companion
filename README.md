# ElderCare Companion

## Project Overview & Short Description
ElderCare Companion is an empathetic, voice-first (simulated Alexa+) conversational AI companion designed specifically for senior citizens. It simplifies daily life management by allowing elderly users to manage appointments and check their daily schedules through natural, respectful dialogue.

## Problem Being Solved
Senior citizens often struggle with complex digital interfaces, remembering appointment times, keeping track of daily events, or navigating cluttered calendars. ElderCare Companion eliminates digital friction by offering a patient, warm, and natural conversational assistant that handles scheduling without complex menus or typing.

## Target Users
- **Primary Users:** Senior citizens and elderly individuals seeking simple schedule management.
- **Secondary Users:** Family members or caregivers checking appointment plans.

## Current MVP Features
- **Appointment Management:** View all appointments (including statuses like scheduled and cancelled), schedule new appointments, update appointment details (title, time, location, preparation notes), and soft-cancel appointments.
- **Daily Plans:** Retrieve summarized daily schedules for any target date.
- **Natural Conversation & Safety:** Patient, respectful tone with robust clarification prompts, explicit confirmation before state-changing actions, and strict medical-safety guardrails.

## Simulated Alexa+ Experience
The application simulates an advanced Alexa+ conversational ecosystem tailored for hackathon demonstration. It bridges natural language understanding with a structured backend database to emulate an ambient voice assistant.

## Architecture
The system follows a decoupled client-server architecture:
- **Frontend:** React dashboard (built by Siya) providing a clean visual interface for appointments.
- **Backend:** FastAPI REST API (built by Ruchika) handling request validation and MySQL database operations.
- **AI Layer:** Conversational agent workflow and system prompt routing user intents through validated tool definitions (`list_appointments`, `create_appointment`, `update_appointment`, `cancel_appointment`, `get_daily_plan`).

## Technologies Used
- **Backend:** Python, FastAPI, Pydantic, MySQL, Uvicorn
- **Frontend:** React, JavaScript, CSS
- **AI & Documentation:** LLM System Prompts, Markdown Specs, Git Workflow

## Backend API Endpoints
- `GET /appointments` - Retrieve all appointments (including current statuses).
- `POST /appointments` - Create a new appointment.
- `PUT /appointments/{id}` - Update specific appointment fields (`title`, `appointment_at`, `location`, `preparation_notes`).
- `DELETE /appointments/{id}` (Soft-cancel) - Update appointment status to `cancelled`.
- `GET /daily-plan` - Retrieve the summarized schedule for a specific date.

## Medical-Safety Limitations
- The assistant **does not** diagnose medical symptoms or recommend medicines, dosages, or treatments.
- The assistant **does not** replace professional medical advice or doctors.
- In case of emergency or severe symptoms, the assistant directs users to India's public emergency number **112**.
- The current MVP does **not** feature medicine reminders, family coordination, emergency calling, or direct IoT/Alexa device integration.

## Team Members & Responsibilities
- **Ruchika:** Backend API development, MySQL database integration, and request validation.
- **Siya:** React appointment dashboard frontend.
- **You (AI & Documentation Lead):** AI workflow planning, system prompt engineering, test conversation specs, friction logging, and testing checklists.

## Basic Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ruchikav707/eldercare-companion.git](https://github.com/ruchikav707/eldercare-companion.git)
   cd eldercare-companion