from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from src.models.appointment import Appointment
from src.schemas.appointment import AppointmentCreate, AppointmentUpdate
from .base import CRUDBase

class CRUDAppointment(CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate]):
    def __init__(self):
        super().__init__(Appointment)
    
    def get_by_patient(
        self, db: Session, patient_id: int, skip: int = 0, limit: int = 100
    ) -> List[Appointment]:
        return (
            db.query(Appointment)
            .filter(Appointment.patient_id == patient_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_doctor(
        self, db: Session, doctor_id: int, skip: int = 0, limit: int = 100
    ) -> List[Appointment]:
        return (
            db.query(Appointment)
            .filter(Appointment.doctor_id == doctor_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, status: str, skip: int = 0, limit: int = 100
    ) -> List[Appointment]:
        return (
            db.query(Appointment)
            .filter(Appointment.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_upcoming_appointments(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Appointment]:
        return (
            db.query(Appointment)
            .filter(and_(
                Appointment.appointment_date >= datetime.now(),
                Appointment.status == "Scheduled"
            ))
            .offset(skip)
            .limit(limit)
            .all()
        )
