from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_database_connection
from app.schemas import AppointmentCreate

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


@app.post("/appointments", status_code=201)
def create_appointment(appointment: AppointmentCreate):
    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO appointments
                (title, appointment_at, location, preparation_notes)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            appointment.title,
            appointment.appointment_at,
            appointment.location,
            appointment.preparation_notes
        )

        cursor.execute(query, values)
        connection.commit()

        return {
            "message": "Appointment created successfully",
            "id": cursor.lastrowid
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()        

