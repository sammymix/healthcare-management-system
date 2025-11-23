# Import all models here for easy access
from .patient import Patient
from .doctor import Doctor
from .appointment import Appointment
from .medical_record import MedicalRecord
from .prescription import Prescription
from .billing import Billing
from .inventory import Inventory

# This will help with Alembic migrations
__all__ = [
    "Patient", 
    "Doctor", 
    "Appointment", 
    "MedicalRecord", 
    "Prescription", 
    "Billing", 
    "Inventory"
]
