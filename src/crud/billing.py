from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.billing import Billing
from src.schemas.billing import BillingCreate, BillingUpdate
from .base import CRUDBase

class CRUDBilling(CRUDBase[Billing, BillingCreate, BillingUpdate]):
    def __init__(self):
        super().__init__(Billing)
    
    def get_by_patient(
        self, db: Session, patient_id: int, skip: int = 0, limit: int = 100
    ) -> List[Billing]:
        return (
            db.query(Billing)
            .filter(Billing.patient_id == patient_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, status: str, skip: int = 0, limit: int = 100
    ) -> List[Billing]:
        return (
            db.query(Billing)
            .filter(Billing.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_total_revenue(self, db: Session) -> float:
        result = db.query(func.sum(Billing.amount)).filter(Billing.status == 'Paid').scalar()
        return result or 0.0

billing = CRUDBilling()
