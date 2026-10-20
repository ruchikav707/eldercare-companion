from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=150)
    appointment_at: datetime
    location: str | None = Field(default=None, max_length=255)
    preparation_notes: str | None = None


class AppointmentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=150)
    appointment_at: datetime | None = None
    location: str | None = Field(default=None, max_length=255)
    preparation_notes: str | None = None