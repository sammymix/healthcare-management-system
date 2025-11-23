from database.config import SessionLocal
from src.crud import patient_crud, doctor_crud, appointment_crud
from src.schemas.appointment import AppointmentCreate
from datetime import datetime
import random

db = SessionLocal()

try:
    print("🧪 Testing Advanced CRUD Features...")
    
    # Get existing patients and doctors
    patients = patient_crud.get_multi(db)
    doctors = doctor_crud.get_multi(db)
    
    print(f"📊 Working with {len(patients)} patients and {len(doctors)} doctors")
    
    if patients and doctors:
        # Test 1: Create an appointment
        print("1. Creating appointment...")
        patient = patients[0]
        doctor = doctors[0]
        
        appointment_data = AppointmentCreate(
            patient_id=patient.patient_id,
            doctor_id=doctor.doctor_id,
            appointment_date=datetime(2024, 12, 25, 10, 0, 0),
            status="Scheduled",
            reason="Annual checkup"
        )
        
        new_appointment = appointment_crud.create(db, obj_in=appointment_data)
        print(f"✅ Created appointment: ID {new_appointment.appointment_id}")
        
        # Test 2: Get appointments by patient
        print("2. Testing patient appointments...")
        patient_appointments = appointment_crud.get_by_patient(db, patient_id=patient.patient_id)
        print(f"📅 Patient has {len(patient_appointments)} appointments")
        
        # Test 3: Get appointments by doctor
        print("3. Testing doctor appointments...")
        doctor_appointments = appointment_crud.get_by_doctor(db, doctor_id=doctor.doctor_id)
        print(f"📅 Doctor has {len(doctor_appointments)} appointments")
        
        # Test 4: Test search by email/phone
        print("4. Testing search by contact...")
        found_patient = patient_crud.get_by_email(db, email=patient.email)
        if found_patient:
            print(f"🔍 Found patient by email: {found_patient.first_name} {found_patient.last_name}")
        
        found_doctor = doctor_crud.get_by_phone(db, phone=doctor.phone)
        if found_doctor:
            print(f"🔍 Found doctor by phone: Dr. {found_doctor.first_name} {found_doctor.last_name}")
    
    print("\\n🎉 ADVANCED CRUD FEATURES WORKING!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
