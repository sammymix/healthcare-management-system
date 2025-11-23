from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date
from src.models.prescription import Prescription
from src.schemas.prescription import PrescriptionCreate, PrescriptionUpdate
from .base import CRUDBase

class CRUDPrescription(CRUDBase[Prescription, PrescriptionCreate, PrescriptionUpdate]):
    def __init__(self):
        super().__init__(Prescription)
    
    def get_by_patient(
        self, db: Session, patient_id: int, skip: int = 0, limit: int = 100
    ) -> List[Prescription]:
        return (
            db.query(Prescription)
            .filter(Prescription.patient_id == patient_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_doctor(
        self, db: Session, doctor_id: int, skip: int = 0, limit: int = 100
    ) -> List[Prescription]:
        return (
            db.query(Prescription)
            .filter(Prescription.doctor_id == doctor_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_prescriptions(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Prescription]:
        return (
            db.query(Prescription)
            .filter(
                (Prescription.end_date.is_(None)) | 
                (Prescription.end_date >= date.today())
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

prescription = CRUDPrescription()
