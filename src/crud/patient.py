from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.patient import Patient
from src.schemas.patient import PatientCreate, PatientUpdate
from .base import CRUDBase

class CRUDPatient(CRUDBase[Patient, PatientCreate, PatientUpdate]):
    def __init__(self):
        super().__init__(Patient)
    
    def get_by_email(self, db: Session, email: str) -> Optional[Patient]:
        return db.query(Patient).filter(Patient.email == email).first()

    def get_by_phone(self, db: Session, phone: str) -> Optional[Patient]:
        return db.query(Patient).filter(Patient.phone == phone).first()

    def search_by_name(
        self, db: Session, name: str, skip: int = 0, limit: int = 100
    ) -> List[Patient]:
        return (
            db.query(Patient)
            .filter(
                (Patient.first_name.ilike(f"%{name}%")) |
                (Patient.last_name.ilike(f"%{name}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_gender(
        self, db: Session, gender: str, skip: int = 0, limit: int = 100
    ) -> List[Patient]:
        return (
            db.query(Patient)
            .filter(Patient.gender == gender)
            .offset(skip)
            .limit(limit)
            .all()
        )
