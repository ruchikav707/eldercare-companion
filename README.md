# ElderCare Companion

## Project Overview & Short Description
ElderCare Companion is an empathetic, voice-inspired simulated Alexa+ experience designed specifically for senior citizens. It simplifies daily life management by allowing elderly users to manage appointments and check their daily schedules through natural, respectful dialogue.

## Problem Being Solved
Senior citizens often struggle with complex digital interfaces, remembering appointment times, keeping track of daily events, or navigating cluttered calendars. ElderCare Companion eliminates digital friction by offering a patient, warm, and natural conversational assistant that handles scheduling without complex menus or typing.

## Target Users
- **Primary Users:** Senior citizens and elderly individuals seeking simple schedule management.
- **Secondary Users:** Family members or caregivers checking appointment plans.

## Current MVP Features
- **Appointment Management:** View all appointments (including statuses like scheduled and cancelled), schedule new appointments via REST or chat agent, and soft-cancel appointments via REST.
- **Daily Plans:** Retrieve summarized daily schedules for a specific date via `GET /appointments/daily-plan?date=YYYY-MM-DD`.
- **AI Chat & Conversation:** Conversational agent integration via `POST /agent/chat` supporting list, daily plan, creation, clarification, and explicit session memory confirmation.
- **Natural Conversation & Safety:** Patient, respectful tone with robust clarification prompts, explicit confirmation before state-changing actions, and strict medical-safety guardrails.

## Simulated Alexa+ Experience
The application simulates an advanced Alexa+ conversational ecosystem tailored for hackathon demonstration. It bridges natural language understanding with a structured backend database to emulate an ambient voice assistant.

## Architecture
The system follows a decoupled client-server architecture:
- **Frontend:** React dashboard (built by Siya) providing a clean visual interface for appointments.
- **Backend:** FastAPI REST API (built by Ruchika) handling request validation and MySQL database operations.
- **AI Layer:** Conversational agent workflow and prompt design (planned and documented by Prachi), routing user intents through the currently implemented tools (`list_appointments`, `get_daily_plan`, `create_appointment`). Note: AI-based update and cancel tools are planned and not implemented yet (updates/cancellations currently work via REST APIs).

## Technologies Used
- **Backend:** Python, FastAPI, Pydantic, MySQL, Uvicorn
- **Frontend:** React, JavaScript, CSS
- **AI & Documentation:** LLM System Prompts, Markdown Specs, Git Workflow

## Backend API Endpoints
- `GET /appointments` - Retrieve all appointments (including current statuses).
- `POST /appointments` - Create a new appointment.
- `PUT /appointments/{id}` - Update specific appointment fields (`title`, `appointment_at`, `location`, `preparation_notes`).
- `DELETE /appointments/{id}` (Soft-cancel) - Update appointment status to `cancelled`.
- `GET /appointments/daily-plan?date=YYYY-MM-DD` - Retrieve the summarized schedule for a specific date.
- `POST /agent/chat` - Interact with the conversational AI agent backend.

## Medical-Safety Limitations
- The assistant **does not** diagnose medical symptoms or recommend medicines, dosages, or treatments.
- The assistant **does not** replace professional medical advice or doctors.
- In case of emergency or severe symptoms, the assistant directs users to India's public emergency number **112**.
- The current MVP does **not** feature medicine reminders, family coordination, emergency calling, or direct IoT/Alexa device integration.

## Team Members & Responsibilities
- **Ruchika:** Backend API development, MySQL database integration, and request validation.
- **Siya:** React appointment dashboard frontend.
- **Prachi:** AI workflow planning, system prompt engineering, test conversation specs, friction logging, and testing checklists.

## Basic Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/ruchikav707/eldercare-companion.git
cd eldercare-companion
```

### 2. Backend setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Update the newly created `.env` file with your MySQL credentials and Gemini API key.

### 3. Frontend setup

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```