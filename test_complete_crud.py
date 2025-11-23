from database.config import SessionLocal
from src.crud import patient, doctor
from src.schemas.patient import PatientCreate
from src.schemas.doctor import DoctorCreate
from datetime import date

# Create database session
db = SessionLocal()

try:
    print("🧪 Testing Complete CRUD System...")
    
    # Test 1: Create a new patient
    print("\\n1. Testing Patient Creation...")
    patient_data = PatientCreate(
        first_name="Alice",
        last_name="Johnson",
        date_of_birth=date(1990, 5, 15),
        gender="Female",
        phone="+1555123456",
        email="alice.johnson@example.com",
        address="789 Pine St, City, State",
        emergency_contact="+1555987654"
    )
    
    new_patient = patient.create(db, obj_in=patient_data)
    print(f"✅ Created patient: {new_patient.first_name} {new_patient.last_name} (ID: {new_patient.patient_id})")
    
    # Test 2: Create a new doctor
    print("\\n2. Testing Doctor Creation...")
    doctor_data = DoctorCreate(
        first_name="Michael",
        last_name="Brown",
        specialization="Neurology",
        phone="+1555123457",
        email="michael.brown@hospital.com",
        license_number="MED789012",
        hire_date=date(2018, 8, 20),
        is_active=True
    )
    
    new_doctor = doctor.create(db, obj_in=doctor_data)
    print(f"✅ Created doctor: Dr. {new_doctor.first_name} {new_doctor.last_name} (ID: {new_doctor.doctor_id})")
    
    # Test 3: Get patient by ID
    print("\\n3. Testing Get Patient by ID...")
    found_patient = patient.get(db, id=new_patient.patient_id)
    if found_patient:
        print(f"✅ Found patient: {found_patient.first_name} {found_patient.last_name}")
    else:
        print("❌ Patient not found")
    
    # Test 4: Search patients
    print("\\n4. Testing Patient Search...")
    search_results = patient.search_by_name(db, name="John")
    print(f"✅ Found {len(search_results)} patients with 'John'")
    for p in search_results:
        print(f"   - {p.first_name} {p.last_name}")
    
    # Test 5: Get doctors by specialization
    print("\\n5. Testing Doctor Specialization Filter...")
    neurologists = doctor.get_by_specialization(db, specialization="Neurology")
    print(f"✅ Found {len(neurologists)} neurologists")
    for d in neurologists:
        print(f"   - Dr. {d.first_name} {d.last_name}")
    
    print("\\n🎉 Complete CRUD system tested successfully!")
    
except Exception as e:
    print(f"❌ Error during CRUD testing: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
