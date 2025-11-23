from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    phone: str
    email: EmailStr
    license_number: str
    hire_date: date
    is_active: bool = True

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class DoctorInDB(DoctorBase):
    doctor_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Doctor(DoctorInDB):
    pass
