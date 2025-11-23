from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    medication_name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(PrescriptionBase):
    medication_name: Optional[str] = None
    start_date: Optional[date] = None

class PrescriptionInDB(PrescriptionBase):
    prescription_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Prescription(PrescriptionInDB):
    pass
