#!/usr/bin/env python3
"""
Fixed Streamlit Dashboard Runner
"""
import subprocess
import sys
import os

def main():
    print("🏥 Healthcare Management System - Fixed Dashboard")
    print("=" * 50)
    
    # First test if imports work
    try:
        from test_imports import test_imports
        test_imports()
    except:
        pass
    
    print("🚀 Launching Fixed Dashboard...")
    print("📊 Dashboard will open at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        # Use the fixed dashboard
        subprocess.run([
            "streamlit", "run", 
            "src/ui/streamlit_dashboard_fixed.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard server stopped")

if __name__ == "__main__":
    main()
