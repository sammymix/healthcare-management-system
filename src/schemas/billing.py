from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class BillingBase(BaseModel):
    patient_id: int
    appointment_id: int
    service_date: date
    amount: float
    status: str = "Pending"
    insurance_info: Optional[str] = None

class BillingCreate(BillingBase):
    pass

class BillingUpdate(BillingBase):
    status: Optional[str] = None
    amount: Optional[float] = None

class BillingInDB(BillingBase):
    bill_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Billing(BillingInDB):
    pass
