from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    status: str = "Scheduled"
    reason: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    status: Optional[str] = None

class AppointmentInDB(AppointmentBase):
    appointment_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Appointment(AppointmentInDB):
    pass
