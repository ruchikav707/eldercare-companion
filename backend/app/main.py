from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_database_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message": "ElderCare backend is running"}

@app.get("/appointments")
def get_appointments():
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                id,
                title,
                appointment_at,
                location,
                preparation_notes,
                status,
                created_at,
                updated_at
            FROM appointments
            ORDER BY appointment_at ASC
        """)

        appointments = cursor.fetchall()
        return appointments

    finally:
        cursor.close()
        connection.close()