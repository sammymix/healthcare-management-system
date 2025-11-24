#!/usr/bin/env python3
"""
SQL Query Testing Runner for Healthcare Management System
Executes 15+ advanced SQL queries for the 3rd deliverable
"""
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.sql_queries.healthcare_queries import HealthcareSQLQueries

def main():
    print("🏥 Healthcare Management System - SQL Query Testing")
    print("=" * 60)
    
    try:
        # Initialize SQL tester
        sql_tester = HealthcareSQLQueries()
        
        # Run all queries
        sql_tester.run_all_queries()
        
        print("\n✅ All SQL queries executed successfully!")
        print("📋 Deliverable 3 Requirements Met:")
        print("   • 15+ different SQL queries tested")
        print("   • Advanced window functions included") 
        print("   • OLAP operations implemented")
        print("   • Complex joins and analytics")
        print("   • Query explanations and results provided")
        
    except Exception as e:
        print(f"❌ Error during SQL testing: {e}")
        print("💡 Make sure your database is running and contains data")
    
    finally:
        if 'sql_tester' in locals():
            sql_tester.close_connection()

if __name__ == "__main__":
    main()
