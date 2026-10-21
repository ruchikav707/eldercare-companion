from app.database import get_database_connection


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