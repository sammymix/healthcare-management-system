from sqlalchemy import Column, String, Date, Text, DateTime, Integer
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10))
    phone = Column(String(15), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    address = Column(Text)
    emergency_contact = Column(String(15))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="patient")
    medical_records = relationship("MedicalRecord", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")
    bills = relationship("Billing", back_populates="patient")

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"
