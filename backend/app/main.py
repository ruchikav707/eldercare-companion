import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_database_connection
from app.schemas import AppointmentCreate, AppointmentUpdate

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


@app.put("/appointments/{appointment_id}")
def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate
):
    changes = appointment.model_dump(exclude_none=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update"
        )

    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM appointments WHERE id = %s",
            (appointment_id,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )

        set_clause = ", ".join(
            f"{field} = %s" for field in changes
        )

        values = list(changes.values())
        values.append(appointment_id)

        query = f"""
            UPDATE appointments
            SET {set_clause}
            WHERE id = %s
        """

        cursor.execute(query, tuple(values))
        connection.commit()

        return {
            "message": "Appointment updated successfully",
            "id": appointment_id,
            "updated_fields": list(changes.keys())
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()  

        

@app.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int):
    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT status FROM appointments WHERE id = %s",
            (appointment_id,)
        )

        appointment = cursor.fetchone()

        if appointment is None:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )

        if appointment[0] == "cancelled":
            return {
                "message": "Appointment is already cancelled",
                "id": appointment_id
            }

        cursor.execute(
            """
                UPDATE appointments
                SET status = 'cancelled'
                WHERE id = %s
            """,
            (appointment_id,)
        )

        connection.commit()

        return {
            "message": "Appointment cancelled successfully",
            "id": appointment_id
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


@app.get("/appointments/daily-plan")
def get_daily_plan(date: datetime.date):
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
                SELECT
                    id,
                    title,
                    appointment_at,
                    location,
                    preparation_notes,
                    status
                FROM appointments
                WHERE DATE(appointment_at) = %s
                    AND status = 'scheduled'
                ORDER BY appointment_at ASC
            """,
            (date,)
        )

        appointments = cursor.fetchall()

        return {
            "date": date,
            "total_appointments": len(appointments),
            "appointments": appointments
        }

    finally:
        cursor.close()
        connection.close()
