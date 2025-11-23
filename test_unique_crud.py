from database.config import SessionLocal
from src.crud import patient_crud, doctor_crud
from src.schemas.patient import PatientCreate
from src.schemas.doctor import DoctorCreate
from datetime import date
import random

db = SessionLocal()

try:
    print("🧪 Testing CRUD with Unique Data...")
    
    # Generate unique phone numbers
    patient_phone = f"+1{random.randint(1000000000, 9999999999)}"
    doctor_phone = f"+1{random.randint(1000000000, 9999999999)}"
    
    # Test 1: Create a patient
    print("1. Creating patient...")
    patient_data = PatientCreate(
        first_name="Test",
        last_name="Patient",
        date_of_birth=date(1990, 1, 1),
        gender="Other",
        phone=patient_phone,
        email=f"test.patient.{random.randint(1000,9999)}@example.com"
    )
    
    new_patient = patient_crud.create(db, obj_in=patient_data)
    print(f"✅ Created patient: {new_patient.first_name} {new_patient.last_name} (ID: {new_patient.patient_id})")
    
    # Test 2: Create a doctor
    print("2. Creating doctor...")
    doctor_data = DoctorCreate(
        first_name="Test",
        last_name="Doctor",
        specialization="General Medicine",
        phone=doctor_phone,
        email=f"test.doctor.{random.randint(1000,9999)}@hospital.com",
        license_number=f"MED{random.randint(100000,999999)}",
        hire_date=date(2020, 1, 1)
    )
    
    new_doctor = doctor_crud.create(db, obj_in=doctor_data)
    print(f"✅ Created doctor: Dr. {new_doctor.first_name} {new_doctor.last_name} (ID: {new_doctor.doctor_id})")
    
    # Test 3: List records
    print("3. Listing records...")
    patients = patient_crud.get_multi(db)
    doctors = doctor_crud.get_multi(db)
    
    print(f"📊 Total Patients: {len(patients)}")
    print(f"📊 Total Doctors: {len(doctors)}")
    
    # Test 4: Search functionality
    print("4. Testing search...")
    search_results = patient_crud.search_by_name(db, name="Test")
    print(f"🔍 Found {len(search_results)} patients with 'Test'")
    
    # Test 5: Specialization filter
    print("5. Testing doctor filter...")
    general_doctors = doctor_crud.get_by_specialization(db, specialization="General Medicine")
    print(f"👨‍⚕️ Found {len(general_doctors)} General Medicine doctors")
    
    print("\\n🎉 ALL CRUD OPERATIONS WORKING PERFECTLY!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
