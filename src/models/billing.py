from sqlalchemy import Column, Integer, Date, Numeric, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime

class Billing(Base):
    __tablename__ = "billing"

    bill_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    appointment_id = Column(Integer, ForeignKey("appointments.appointment_id"))
    service_date = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="Pending")
    insurance_info = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="bills")
    appointment = relationship("Appointment", back_populates="bills")

    def __repr__(self):
        return f"<Billing {self.bill_id} - ${self.amount} - {self.status}>"
