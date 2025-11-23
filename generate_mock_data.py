import random
from datetime import date, datetime, timedelta
from database.config import SessionLocal
from src.models.patient import Patient
from src.models.doctor import Doctor
from src.models.appointment import Appointment
from src.models.medical_record import MedicalRecord
from src.models.prescription import Prescription
from src.models.billing import Billing
from src.models.inventory import Inventory
from src.crud import patient_crud, doctor_crud, appointment_crud
from src.schemas.patient import PatientCreate
from src.schemas.doctor import DoctorCreate
from src.schemas.appointment import AppointmentCreate
from src.schemas.medical_record import MedicalRecordCreate
from src.schemas.prescription import PrescriptionCreate
from src.schemas.billing import BillingCreate
from src.schemas.inventory import InventoryCreate

# Sample data generators
FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", 
               "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
               "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
               "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
              "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
              "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"]

SPECIALIZATIONS = ["Cardiology", "Pediatrics", "Neurology", "Dermatology", "Orthopedics", 
                   "Psychiatry", "Oncology", "Gastroenterology", "Endocrinology", "Rheumatology",
                   "Urology", "Nephrology", "Pulmonology", "Hematology", "Infectious Disease"]

MEDICATIONS = ["Lisinopril", "Atorvastatin", "Metformin", "Amlodipine", "Metoprolol",
               "Omeprazole", "Losartan", "Albuterol", "Gabapentin", "Hydrochlorothiazide",
               "Sertraline", "Simvastatin", "Montelukast", "Escitalopram", "Fluticasone",
               "Levothyroxine", "Rosuvastatin", "Bupropion", "Trazodone", "Duloxetine"]

MEDICAL_CONDITIONS = ["Hypertension", "Diabetes", "Asthma", "Arthritis", "Depression",
                      "Anxiety", "Migraine", "COPD", "Hyperlipidemia", "Osteoporosis",
                      "GERD", "Hypothyroidism", "Back Pain", "Allergies", "Insomnia"]

INVENTORY_ITEMS = [
    ("Bandages", "Medical Supplies", 2.50),
    ("Syringes", "Medical Supplies", 0.75),
    ("Gloves", "Medical Supplies", 0.25),
    ("Antiseptic Wipes", "Medical Supplies", 0.50),
    ("Pain Relievers", "Medication", 15.99),
    ("Antibiotics", "Medication", 45.50),
    ("Vitamins", "Supplements", 12.75),
    ("Blood Pressure Monitor", "Equipment", 89.99),
    ("Thermometer", "Equipment", 25.50),
    ("First Aid Kit", "Medical Supplies", 35.00)
]

def generate_phone():
    return f"+1{random.randint(200, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"

def generate_email(first_name, last_name):
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
    return f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

def generate_doctor_email(first_name, last_name):
    hospitals = ["generalhospital", "citymedical", "communityhealth", "universitymedical"]
    return f"{first_name.lower()}.{last_name.lower()}@{random.choice(hospitals)}.com"

def generate_license_number():
    return f"MED{random.randint(100000, 999999)}"

def generate_patients(count=50):
    patients = []
    for i in range(count):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        patients.append(PatientCreate(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date(random.randint(1950, 2010), random.randint(1, 12), random.randint(1, 28)),
            gender=random.choice(["Male", "Female", "Other"]),
            phone=generate_phone(),
            email=generate_email(first_name, last_name),
            address=f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Pine'])} St, City, State",
            emergency_contact=generate_phone()
        ))
    return patients

def generate_doctors(count=15):
    doctors = []
    for i in range(count):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        doctors.append(DoctorCreate(
            first_name=first_name,
            last_name=last_name,
            specialization=random.choice(SPECIALIZATIONS),
            phone=generate_phone(),
            email=generate_doctor_email(first_name, last_name),
            license_number=generate_license_number(),
            hire_date=date(random.randint(2000, 2022), random.randint(1, 12), random.randint(1, 28)),
            is_active=random.choice([True, True, True, False])
        ))
    return doctors

def generate_appointments(patients, doctors, count=100):
    appointments = []
    for i in range(count):
        patient = random.choice(patients)
        doctor = random.choice([d for d in doctors if d.is_active])
        appointment_date = datetime.now() + timedelta(days=random.randint(-30, 90))
        appointments.append(AppointmentCreate(
            patient_id=patient.patient_id,
            doctor_id=doctor.doctor_id,
            appointment_date=appointment_date,
            status=random.choice(["Scheduled", "Completed", "Cancelled", "No-show"]),
            reason=random.choice(["Regular checkup", "Follow-up", "Emergency", "Consultation", "Routine exam"])
        ))
    return appointments

def generate_medical_records(patients, doctors, count=80):
    records = []
    for i in range(count):
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        visit_date = date.today() - timedelta(days=random.randint(1, 365))
        records.append(MedicalRecordCreate(
            patient_id=patient.patient_id,
            doctor_id=doctor.doctor_id,
            visit_date=visit_date,
            diagnosis=random.choice(MEDICAL_CONDITIONS),
            treatment=random.choice(["Medication", "Therapy", "Surgery", "Lifestyle changes"]),
            notes=f"Patient presented with symptoms. Recommended {random.choice(['rest', 'exercise', 'diet changes'])}.",
            follow_up_date=visit_date + timedelta(days=random.randint(30, 90)) if random.choice([True, False]) else None
        ))
    return records

def generate_prescriptions(patients, doctors, count=60):
    prescriptions = []
    for i in range(count):
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        start_date = date.today() - timedelta(days=random.randint(1, 180))
        prescriptions.append(PrescriptionCreate(
            patient_id=patient.patient_id,
            doctor_id=doctor.doctor_id,
            medication_name=random.choice(MEDICATIONS),
            dosage=f"{random.randint(1, 5)}00 mg",
            frequency=random.choice(["Once daily", "Twice daily", "Three times daily", "As needed"]),
            start_date=start_date,
            end_date=start_date + timedelta(days=random.randint(30, 90)) if random.choice([True, False]) else None
        ))
    return prescriptions

def generate_billing(patients, appointments, count=70):
    billing = []
    appointment_ids = [a.appointment_id for a in appointments if a.status == "Completed"]
    for i in range(count):
        if not appointment_ids:
            break
        patient = random.choice(patients)
        appointment_id = random.choice(appointment_ids)
        appointment_ids.remove(appointment_id)
        
        billing.append(BillingCreate(
            patient_id=patient.patient_id,
            appointment_id=appointment_id,
            service_date=date.today() - timedelta(days=random.randint(1, 60)),
            amount=round(random.uniform(50, 500), 2),
            status=random.choice(["Pending", "Paid", "Insurance Claim"]),
            insurance_info=random.choice(["Blue Cross", "Aetna", "UnitedHealth", "Cigna", "Medicare"])
        ))
    return billing

def generate_inventory(count=30):
    inventory = []
    for i in range(count):
        item_name, category, base_price = random.choice(INVENTORY_ITEMS)
        inventory.append(InventoryCreate(
            item_name=item_name,
            category=category,
            quantity=random.randint(10, 200),
            unit_price=round(base_price * random.uniform(0.8, 1.2), 2),
            expiration_date=date.today() + timedelta(days=random.randint(30, 730)) if category == "Medication" else None,
            supplier=random.choice(["MedSupply Co", "HealthCorp", "PharmaDist", "Medical Imports"])
        ))
    return inventory

def main():
    db = SessionLocal()
    
    try:
        print("🏥 Generating Comprehensive Mock Data for Healthcare System...")
        
        # Clear existing data using model classes
        print("\\n1. Clearing existing data...")
        db.query(Billing).delete()
        db.query(Prescription).delete()
        db.query(MedicalRecord).delete()
        db.query(Appointment).delete()
        db.query(Inventory).delete()
        db.query(Patient).delete()
        db.query(Doctor).delete()
        db.commit()
        
        # Generate and insert patients
        print("2. Generating patients...")
        patient_schemas = generate_patients(20)  # Reduced for testing
        patients = []
        for patient_data in patient_schemas:
            try:
                patient = patient_crud.create(db, obj_in=patient_data)
                patients.append(patient)
            except Exception as e:
                print(f"   Skipped duplicate patient: {e}")
        print(f"   ✅ Created {len(patients)} patients")
        
        # Generate and insert doctors
        print("3. Generating doctors...")
        doctor_schemas = generate_doctors(8)  # Reduced for testing
        doctors = []
        for doctor_data in doctor_schemas:
            try:
                doctor = doctor_crud.create(db, obj_in=doctor_data)
                doctors.append(doctor)
            except Exception as e:
                print(f"   Skipped duplicate doctor: {e}")
        print(f"   ✅ Created {len(doctors)} doctors")
        
        # Generate and insert appointments
        print("4. Generating appointments...")
        appointment_schemas = generate_appointments(patients, doctors, 30)  # Reduced for testing
        appointments = []
        for appointment_data in appointment_schemas:
            appointment = appointment_crud.create(db, obj_in=appointment_data)
            appointments.append(appointment)
        print(f"   ✅ Created {len(appointments)} appointments")
        
        # Generate and insert medical records
        print("5. Generating medical records...")
        medical_record_schemas = generate_medical_records(patients, doctors, 25)
        for record_data in medical_record_schemas:
            db_obj = MedicalRecord(**record_data.model_dump())
            db.add(db_obj)
        db.commit()
        print(f"   ✅ Created {len(medical_record_schemas)} medical records")
        
        # Generate and insert prescriptions
        print("6. Generating prescriptions...")
        prescription_schemas = generate_prescriptions(patients, doctors, 20)
        for prescription_data in prescription_schemas:
            db_obj = Prescription(**prescription_data.model_dump())
            db.add(db_obj)
        db.commit()
        print(f"   ✅ Created {len(prescription_schemas)} prescriptions")
        
        # Generate and insert billing
        print("7. Generating billing records...")
        billing_schemas = generate_billing(patients, appointments, 15)
        for billing_data in billing_schemas:
            db_obj = Billing(**billing_data.model_dump())
            db.add(db_obj)
        db.commit()
        print(f"   ✅ Created {len(billing_schemas)} billing records")
        
        # Generate and insert inventory
        print("8. Generating inventory...")
        inventory_schemas = generate_inventory(10)
        for inventory_data in inventory_schemas:
            db_obj = Inventory(**inventory_data.model_dump())
            db.add(db_obj)
        db.commit()
        print(f"   ✅ Created {len(inventory_schemas)} inventory items")
        
        # Final statistics
        print("\\n📊 MOCK DATA GENERATION COMPLETE!")
        print("=" * 50)
        print(f"Patients: {len(patients)}")
        print(f"Doctors: {len(doctors)}")
        print(f"Appointments: {len(appointments)}")
        print(f"Medical Records: {len(medical_record_schemas)}")
        print(f"Prescriptions: {len(prescription_schemas)}")
        print(f"Billing Records: {len(billing_schemas)}")
        print(f"Inventory Items: {len(inventory_schemas)}")
        print("=" * 50)
        print("🎉 Database is now populated with realistic healthcare data!")
        
    except Exception as e:
        print(f"❌ Error generating mock data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()