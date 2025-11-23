from sqlalchemy import Column, Integer, Date, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    record_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"))
    visit_date = Column(Date, nullable=False)
    diagnosis = Column(Text)
    treatment = Column(Text)
    notes = Column(Text)
    follow_up_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="medical_records")
    doctor = relationship("Doctor", back_populates="medical_records")

    def __repr__(self):
        return f"<MedicalRecord {self.record_id} for Patient {self.patient_id}>"
