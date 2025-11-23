from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class MedicalRecordBase(BaseModel):
    patient_id: int
    doctor_id: int
    visit_date: date
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(MedicalRecordBase):
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None

class MedicalRecordInDB(MedicalRecordBase):
    record_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MedicalRecord(MedicalRecordInDB):
    pass
