from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.medical_record import MedicalRecord
from src.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate
from .base import CRUDBase

class CRUDMedicalRecord(CRUDBase[MedicalRecord, MedicalRecordCreate, MedicalRecordUpdate]):
    def __init__(self):
        super().__init__(MedicalRecord)
    
    def get_by_patient(
        self, db: Session, patient_id: int, skip: int = 0, limit: int = 100
    ) -> List[MedicalRecord]:
        return (
            db.query(MedicalRecord)
            .filter(MedicalRecord.patient_id == patient_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_doctor(
        self, db: Session, doctor_id: int, skip: int = 0, limit: int = 100
    ) -> List[MedicalRecord]:
        return (
            db.query(MedicalRecord)
            .filter(MedicalRecord.doctor_id == doctor_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

medical_record = CRUDMedicalRecord()
