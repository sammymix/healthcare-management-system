#!/usr/bin/env python3
"""
Test database connection and models
"""
from database.config import SessionLocal
from sqlalchemy import text

def test_database_connection():
    """Test if database is accessible"""
    try:
        db = SessionLocal()
        # Use text() for raw SQL in SQLAlchemy 2.0
        result = db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_models():
    """Test if models can be imported and queried"""
    try:
        from src.models import Patient, Doctor
        db = SessionLocal()
        
        patient_count = db.query(Patient).count()
        doctor_count = db.query(Doctor).count()
        
        db.close()
        
        print(f"✅ Models imported successfully!")
        print(f"📊 Patient count: {patient_count}")
        print(f"👨‍⚕️ Doctor count: {doctor_count}")
        return True
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Healthcare Database...")
    print("=" * 40)
    
    connection_ok = test_database_connection()
    models_ok = test_models()
    
    if connection_ok and models_ok:
        print("🎉 All tests passed! Database is ready.")
    else:
        print("💥 Some tests failed. Please check your setup.")
