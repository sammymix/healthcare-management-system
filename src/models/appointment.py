from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime

class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"))
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="Scheduled")
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    bills = relationship("Billing", back_populates="appointment")

    def __repr__(self):
        return f"<Appointment {self.appointment_id} - {self.status}>"
