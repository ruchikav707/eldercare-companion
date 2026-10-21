from app.database import get_database_connection
from datetime import date as Date


def list_appointments() -> dict:
    """Return all stored appointments ordered by date and time."""

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
                    status,
                    created_at,
                    updated_at
                FROM appointments
                ORDER BY appointment_at ASC
            """
        )

        appointments = cursor.fetchall()

        for appointment in appointments:
            for field in ("appointment_at", "created_at", "updated_at"):
                value = appointment.get(field)

                if value is not None:
                    appointment[field] = value.isoformat()

        return {
            "total_appointments": len(appointments),
            "appointments": appointments
        }

    finally:
        cursor.close()
        connection.close()


def get_daily_plan(plan_date: str) -> dict:
    """Return scheduled appointments for one date in YYYY-MM-DD format."""

    try:
        selected_date = Date.fromisoformat(plan_date)

    except ValueError:
        return {
            "error": "Date must use YYYY-MM-DD format"
        }

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
            (selected_date,)
        )

        appointments = cursor.fetchall()

        for appointment in appointments:
            appointment["appointment_at"] = (
                appointment["appointment_at"].isoformat()
            )

        return {
            "date": selected_date.isoformat(),
            "total_appointments": len(appointments),
            "appointments": appointments
        }

    finally:
        cursor.close()
        connection.close()