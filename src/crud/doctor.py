from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.doctor import Doctor
from src.schemas.doctor import DoctorCreate, DoctorUpdate
from .base import CRUDBase

class CRUDDoctor(CRUDBase[Doctor, DoctorCreate, DoctorUpdate]):
    def __init__(self):
        super().__init__(Doctor)
    
    def get_by_email(self, db: Session, email: str) -> Optional[Doctor]:
        return db.query(Doctor).filter(Doctor.email == email).first()

    def get_by_phone(self, db: Session, phone: str) -> Optional[Doctor]:
        return db.query(Doctor).filter(Doctor.phone == phone).first()

    def get_by_license(self, db: Session, license_number: str) -> Optional[Doctor]:
        return db.query(Doctor).filter(Doctor.license_number == license_number).first()

    def get_by_specialization(
        self, db: Session, specialization: str, skip: int = 0, limit: int = 100
    ) -> List[Doctor]:
        return (
            db.query(Doctor)
            .filter(Doctor.specialization == specialization)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_doctors(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Doctor]:
        return (
            db.query(Doctor)
            .filter(Doctor.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_by_name(
        self, db: Session, name: str, skip: int = 0, limit: int = 100
    ) -> List[Doctor]:
        return (
            db.query(Doctor)
            .filter(
                (Doctor.first_name.ilike(f"%{name}%")) |
                (Doctor.last_name.ilike(f"%{name}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
