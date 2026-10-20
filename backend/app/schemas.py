from datetime import datetime

from pydantic import BaseModel, Field


class AppointmentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    appointment_at: datetime
    location: str | None = Field(default=None, max_length=255)
    preparation_notes: str | None = None