#!/usr/bin/env python3
"""
Test all imports and database connection
"""
import sys
import os

# Add project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🔍 Testing Imports and Database Connection...")
print("=" * 50)

try:
    from database.config import SessionLocal
    print("✅ database.config imported successfully")
    
    from src.models import Patient, Doctor
    print("✅ src.models imported successfully")
    
    from sqlalchemy import func, text
    print("✅ SQLAlchemy imported successfully")
    
    # Test database connection
    db = SessionLocal()
    result = db.execute(text("SELECT COUNT(*) FROM patients"))
    patient_count = result.scalar()
    print(f"✅ Database connected! Patient count: {patient_count}")
    
    db.close()
    print("🎉 All tests passed! Dashboard should work now.")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\n💡 Solution: Make sure you're running from the project root directory")
    print("Current directory:", current_dir)
    print("Python path:", sys.path)
except Exception as e:
    print(f"❌ Error: {e}")
