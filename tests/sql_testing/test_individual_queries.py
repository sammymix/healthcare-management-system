"""
Individual SQL Query Testing - For detailed analysis of each query
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.sql_queries.healthcare_queries import HealthcareSQLQueries

def test_specific_queries():
    """Test specific queries for detailed analysis"""
    tester = HealthcareSQLQueries()
    
    print("🔍 INDIVIDUAL QUERY TESTING")
    print("=" * 60)
    
    # Test specific complex queries
    complex_queries = [
        ("Window Function - Doctor Rankings", """
        SELECT 
            doctor_id,
            first_name || ' ' || last_name as doctor_name,
            specialization,
            appointment_count,
            RANK() OVER (ORDER BY appointment_count DESC) as rank_by_appointments
        FROM (
            SELECT 
                d.doctor_id,
                d.first_name,
                d.last_name,
                d.specialization,
                COUNT(a.appointment_id) as appointment_count
            FROM doctors d
            LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
            GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization
        ) doctor_stats
        ORDER BY rank_by_appointments;
        """),
        
        ("OLAP - Multi-dimensional Analysis", """
        SELECT 
            COALESCE(TO_CHAR(DATE_TRUNC('month', b.created_at), 'YYYY-MM'), 'All Months') as month,
            COALESCE(d.specialization, 'All Specializations') as specialization,
            COUNT(*) as bill_count,
            SUM(b.amount) as total_amount
        FROM billing b
        LEFT JOIN appointments a ON b.appointment_id = a.appointment_id
        LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
        GROUP BY GROUPING SETS (
            (DATE_TRUNC('month', b.created_at), d.specialization),
            (DATE_TRUNC('month', b.created_at)),
            (d.specialization),
            ()
        )
        ORDER BY month NULLS LAST, specialization NULLS LAST;
        """)
    ]
    
    for description, query in complex_queries:
        print(f"\n🎯 Testing: {description}")
        print("-" * 50)
        result = tester.execute_query(description, query)
        if result is not None:
            print(f"✅ Query executed successfully - {len(result)} rows returned")
    
    tester.close_connection()

if __name__ == "__main__":
    test_specific_queries()
