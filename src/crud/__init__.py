from .patient import CRUDPatient
from .doctor import CRUDDoctor
from .appointment import CRUDAppointment
from .medical_record import CRUDMedicalRecord
from .prescription import CRUDPrescription
from .billing import CRUDBilling
from .inventory import CRUDInventory

# Create instances
patient_crud = CRUDPatient()
doctor_crud = CRUDDoctor()
appointment_crud = CRUDAppointment()
medical_record_crud = CRUDMedicalRecord()
prescription_crud = CRUDPrescription()
billing_crud = CRUDBilling()
inventory_crud = CRUDInventory()

__all__ = [
    "patient_crud", "doctor_crud", "appointment_crud", 
    "medical_record_crud", "prescription_crud", "billing_crud", 
    "inventory_crud"
]
