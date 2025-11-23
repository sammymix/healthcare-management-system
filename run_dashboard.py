#!/usr/bin/env python3
"""
Streamlit Dashboard Runner for Healthcare Management System
"""
import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'plotly', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_missing_packages(missing_packages):
    """Install missing packages"""
    if missing_packages:
        print(f"📦 Installing missing packages: {', '.join(missing_packages)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("✅ Packages installed successfully!")

def test_database_connection():
    """Test database connection with proper SQLAlchemy 2.0 syntax"""
    try:
        from database.config import SessionLocal
        from sqlalchemy import text
        
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))  # Fixed: using text() for raw SQL
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    print("🏥 Healthcare Management System - Dashboard")
    print("=" * 50)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        install_missing_packages(missing)
    
    # Check if database is accessible
    if not test_database_connection():
        print("Please make sure your database is running and properly configured.")
        return
    
    print("✅ Database connection successful!")
    
    # Launch Streamlit dashboard
    print("🚀 Launching Streamlit Dashboard...")
    print("📊 Dashboard will open in your web browser")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            "streamlit", "run", 
            "src/ui/streamlit_dashboard.py",
            "--server.port=8501",
            "--server.address=0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard server stopped")

if __name__ == "__main__":
    main()
