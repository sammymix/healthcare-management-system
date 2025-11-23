from database.config import SessionLocal
from src.crud import patient, doctor
from src.schemas.patient import PatientCreate
from src.schemas.doctor import DoctorCreate
from datetime import date

db = SessionLocal()

try:
    print("🧪 Testing Fixed CRUD Operations...")
    
    # Test 1: Check if methods exist
    print("1. Checking CRUD methods...")
    print(f"   Patient has 'create': {hasattr(patient, 'create')}")
    print(f"   Patient has 'get_multi': {hasattr(patient, 'get_multi')}")
    print(f"   Doctor has 'create': {hasattr(doctor, 'create')}")
    print(f"   Doctor has 'get_multi': {hasattr(doctor, 'get_multi')}")
    
    # Test 2: Create a patient
    print("\\n2. Creating patient...")
    patient_data = PatientCreate(
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1985, 3, 15),
        gender="Male",
        phone="+1234567890",
        email="john.doe@example.com"
    )
    
    new_patient = patient.create(db, obj_in=patient_data)
    print(f"✅ Created patient: {new_patient.first_name} {new_patient.last_name} (ID: {new_patient.patient_id})")
    
    # Test 3: Create a doctor
    print("\\n3. Creating doctor...")
    doctor_data = DoctorCreate(
        first_name="Sarah",
        last_name="Wilson",
        specialization="Pediatrics",
        phone="+1234567891",
        email="sarah.wilson@hospital.com",
        license_number="MED123456",
        hire_date=date(2019, 5, 20)
    )
    
    new_doctor = doctor.create(db, obj_in=doctor_data)
    print(f"✅ Created doctor: Dr. {new_doctor.first_name} {new_doctor.last_name} (ID: {new_doctor.doctor_id})")
    
    # Test 4: List records
    print("\\n4. Listing records...")
    patients = patient.get_multi(db)
    doctors = doctor.get_multi(db)
    
    print(f"📊 Total Patients: {len(patients)}")
    print(f"📊 Total Doctors: {len(doctors)}")
    
    print("\\n🎉 CRUD operations working successfully!")
    
except Exception as e:
    print(f"\\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
