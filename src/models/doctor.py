from sqlalchemy import Column, String, Date, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime

class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    specialization = Column(String(100), nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    hire_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")
    medical_records = relationship("MedicalRecord", back_populates="doctor")
    prescriptions = relationship("Prescription", back_populates="doctor")

    def __repr__(self):
        return f"<Doctor {self.first_name} {self.last_name} ({self.specialization})>"
