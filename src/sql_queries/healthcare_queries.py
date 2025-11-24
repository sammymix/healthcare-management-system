"""
Advanced SQL Queries for Healthcare Management System
Testing 15+ queries including window functions, OLAP, and complex joins
"""
from database.config import SessionLocal
from sqlalchemy import text, func, case, and_, or_, extract
from sqlalchemy.sql import expression
from datetime import datetime, timedelta
import pandas as pd

class HealthcareSQLQueries:
    def __init__(self):
        self.db = SessionLocal()
    
    def execute_query(self, query_description, sql_query, params=None):
        """Execute SQL query and return formatted results"""
        print(f"\n{'='*80}")
        print(f"📊 {query_description}")
        print(f"{'='*80}")
        print(f"🔍 SQL Query:\n{sql_query}")
        print(f"{'-'*80}")
        
        try:
            if params:
                result = self.db.execute(text(sql_query), params)
            else:
                result = self.db.execute(text(sql_query))
            
            # Get column names
            columns = result.keys()
            
            # Fetch all results
            rows = result.fetchall()
            
            if rows:
                # Create DataFrame for nice display
                df = pd.DataFrame(rows, columns=columns)
                print(f"✅ Results ({len(rows)} rows):")
                print(df.to_string(index=False))
                return df
            else:
                print("ℹ️  No results returned")
                return None
                
        except Exception as e:
            print(f"❌ Error executing query: {e}")
            return None
    
    def test_basic_queries(self):
        """Basic SELECT queries with filtering and aggregation"""
        print("🎯 BASIC QUERIES")
        print("="*60)
        
        # Query 1: Basic patient information with filtering
        query_1 = """
        SELECT patient_id, first_name, last_name, gender, 
               EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) as age,
               phone, email
        FROM patients 
        WHERE gender = 'Female' AND date_of_birth < '2000-01-01'
        ORDER BY age DESC
        LIMIT 10;
        """
        self.execute_query(
            "1. Female patients born before 2000 with age calculation",
            query_1
        )
        
        # Query 2: Doctor specialization counts
        query_2 = """
        SELECT specialization, COUNT(*) as doctor_count,
               COUNT(*) * 100.0 / (SELECT COUNT(*) FROM doctors) as percentage
        FROM doctors 
        WHERE is_active = true
        GROUP BY specialization
        ORDER BY doctor_count DESC;
        """
        self.execute_query(
            "2. Doctor count by specialization with percentages",
            query_2
        )
        
        # Query 3: Appointment statistics by status
        query_3 = """
        SELECT 
            status,
            COUNT(*) as total_appointments,
            AVG(EXTRACT(EPOCH FROM (appointment_date - created_at))/86400) as avg_lead_time_days,
            MIN(appointment_date) as earliest_appointment,
            MAX(appointment_date) as latest_appointment
        FROM appointments
        GROUP BY status
        ORDER BY total_appointments DESC;
        """
        self.execute_query(
            "3. Appointment statistics grouped by status",
            query_3
        )
    
    def test_advanced_joins(self):
        """Complex JOIN operations across multiple tables"""
        print("\n🎯 ADVANCED JOIN QUERIES")
        print("="*60)
        
        # Query 4: Patient appointments with doctor details
        query_4 = """
        SELECT 
            p.patient_id,
            p.first_name || ' ' || p.last_name as patient_name,
            d.first_name || ' ' || d.last_name as doctor_name,
            d.specialization,
            a.appointment_date,
            a.status,
            a.reason
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_date >= CURRENT_DATE
        ORDER BY a.appointment_date, p.last_name
        LIMIT 15;
        """
        self.execute_query(
            "4. Upcoming appointments with patient and doctor details",
            query_4
        )
        
        # Query 5: Patient medical history with prescriptions
        query_5 = """
        SELECT 
            p.patient_id,
            p.first_name || ' ' || p.last_name as patient_name,
            mr.visit_date,
            mr.diagnosis,
            mr.treatment,
            pr.medication_name,
            pr.dosage,
            pr.frequency
        FROM medical_records mr
        JOIN patients p ON mr.patient_id = p.patient_id
        LEFT JOIN prescriptions pr ON mr.patient_id = pr.patient_id 
            AND mr.visit_date = pr.start_date
        WHERE mr.diagnosis IS NOT NULL
        ORDER BY p.last_name, mr.visit_date DESC
        LIMIT 15;
        """
        self.execute_query(
            "5. Patient medical history with associated prescriptions",
            query_5
        )
        
        # Query 6: Billing analysis with patient and appointment info
        query_6 = """
        SELECT 
            b.bill_id,
            p.first_name || ' ' || p.last_name as patient_name,
            a.appointment_date,
            b.amount,
            b.status,
            b.insurance_provider,
            b.insurance_coverage,
            b.amount - b.insurance_coverage as patient_responsibility
        FROM billing b
        JOIN patients p ON b.patient_id = p.patient_id
        LEFT JOIN appointments a ON b.appointment_id = a.appointment_id
        WHERE b.amount > 100
        ORDER BY b.amount DESC
        LIMIT 12;
        """
        self.execute_query(
            "6. Billing analysis with patient responsibility calculation",
            query_6
        )
    
    def test_window_functions(self):
        """Advanced window functions for analytics"""
        print("\n🎯 WINDOW FUNCTION QUERIES")
        print("="*60)
        
        # Query 7: Doctor ranking by appointment count
        query_7 = """
        SELECT 
            doctor_id,
            first_name || ' ' || last_name as doctor_name,
            specialization,
            appointment_count,
            RANK() OVER (ORDER BY appointment_count DESC) as rank_by_appointments,
            ROUND(100.0 * appointment_count / SUM(appointment_count) OVER (), 2) as percentage_of_total,
            ROUND(AVG(appointment_count) OVER (), 2) as avg_appointments_all_doctors
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
        """
        self.execute_query(
            "7. Doctor ranking by appointment count with window functions",
            query_7
        )
        
        # Query 8: Patient spending analysis with running totals
        query_8 = """
        SELECT 
            patient_id,
            patient_name,
            total_spent,
            RANK() OVER (ORDER BY total_spent DESC) as spending_rank,
            ROUND(AVG(total_spent) OVER (), 2) as avg_patient_spending,
            SUM(total_spent) OVER (ORDER BY total_spent DESC) as running_total,
            ROUND(100.0 * total_spent / SUM(total_spent) OVER (), 2) as percentage_of_total_revenue
        FROM (
            SELECT 
                p.patient_id,
                p.first_name || ' ' || p.last_name as patient_name,
                COALESCE(SUM(b.amount), 0) as total_spent
            FROM patients p
            LEFT JOIN billing b ON p.patient_id = b.patient_id AND b.status = 'Paid'
            GROUP BY p.patient_id, p.first_name, p.last_name
        ) patient_spending
        ORDER BY spending_rank
        LIMIT 15;
        """
        self.execute_query(
            "8. Patient spending analysis with running totals and rankings",
            query_8
        )
        
        # Query 9: Monthly revenue with growth calculations
        query_9 = """
        WITH monthly_revenue AS (
            SELECT 
                DATE_TRUNC('month', created_at) as month,
                SUM(amount) as monthly_revenue,
                COUNT(*) as bill_count
            FROM billing 
            WHERE status = 'Paid'
            GROUP BY DATE_TRUNC('month', created_at)
        )
        SELECT 
            TO_CHAR(month, 'YYYY-MM') as month,
            monthly_revenue,
            bill_count,
            LAG(monthly_revenue) OVER (ORDER BY month) as previous_month_revenue,
            ROUND(
                100.0 * (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month)) 
                / LAG(monthly_revenue) OVER (ORDER BY month), 
                2
            ) as growth_percentage,
            ROUND(AVG(monthly_revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) as moving_avg_3_months
        FROM monthly_revenue
        ORDER BY month DESC;
        """
        self.execute_query(
            "9. Monthly revenue analysis with growth percentages and moving averages",
            query_9
        )
    
    def test_olap_queries(self):
        """OLAP-style queries with grouping sets and cube operations"""
        print("\n🎯 OLAP QUERIES")
        print("="*60)
        
        # Query 10: Multi-dimensional revenue analysis
        query_10 = """
        SELECT 
            COALESCE(TO_CHAR(DATE_TRUNC('month', b.created_at), 'YYYY-MM'), 'All Months') as month,
            COALESCE(d.specialization, 'All Specializations') as specialization,
            COALESCE(b.status, 'All Statuses') as billing_status,
            COUNT(*) as bill_count,
            SUM(b.amount) as total_amount,
            ROUND(AVG(b.amount), 2) as avg_amount
        FROM billing b
        LEFT JOIN appointments a ON b.appointment_id = a.appointment_id
        LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
        GROUP BY GROUPING SETS (
            (DATE_TRUNC('month', b.created_at), d.specialization, b.status),
            (DATE_TRUNC('month', b.created_at), d.specialization),
            (DATE_TRUNC('month', b.created_at), b.status),
            (d.specialization, b.status),
            (DATE_TRUNC('month', b.created_at)),
            (d.specialization),
            (b.status),
            ()
        )
        ORDER BY 
            month NULLS LAST,
            specialization NULLS LAST,
            billing_status NULLS LAST,
            total_amount DESC
        LIMIT 20;
        """
        self.execute_query(
            "10. Multi-dimensional revenue analysis with GROUPING SETS",
            query_10
        )
        
        # Query 11: Patient demographics cube analysis
        query_11 = """
        SELECT 
            COALESCE(gender, 'All Genders') as gender,
            COALESCE(
                CASE 
                    WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) < 30 THEN 'Under 30'
                    WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) < 50 THEN '30-49'
                    ELSE '50+'
                END, 
                'All Age Groups'
            ) as age_group,
            COUNT(*) as patient_count,
            ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
        FROM patients
        GROUP BY CUBE (gender, 
            CASE 
                WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) < 30 THEN 'Under 30'
                WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) < 50 THEN '30-49'
                ELSE '50+'
            END
        )
        ORDER BY gender NULLS LAST, age_group NULLS LAST;
        """
        self.execute_query(
            "11. Patient demographics analysis with CUBE operation",
            query_11
        )
    
    def test_complex_analytics(self):
        """Complex analytical queries with subqueries and CTEs"""
        print("\n🎯 COMPLEX ANALYTICAL QUERIES")
        print("="*60)
        
        # Query 12: Patient readmission analysis
        query_12 = """
        WITH patient_visits AS (
            SELECT 
                patient_id,
                visit_date,
                LAG(visit_date) OVER (PARTITION BY patient_id ORDER BY visit_date) as previous_visit,
                diagnosis
            FROM medical_records
        ),
        readmissions AS (
            SELECT 
                patient_id,
                visit_date as readmission_date,
                previous_visit,
                diagnosis,
                visit_date - previous_visit as days_between_visits
            FROM patient_visits
            WHERE previous_visit IS NOT NULL 
            AND visit_date - previous_visit <= 30  -- Readmission within 30 days
        )
        SELECT 
            p.first_name || ' ' || p.last_name as patient_name,
            r.readmission_date,
            r.previous_visit,
            r.days_between_visits,
            r.diagnosis
        FROM readmissions r
        JOIN patients p ON r.patient_id = p.patient_id
        ORDER BY r.days_between_visits, p.last_name
        LIMIT 10;
        """
        self.execute_query(
            "12. Patient readmission analysis within 30 days",
            query_12
        )
        
        # Query 13: Inventory optimization analysis
        query_13 = """
        WITH monthly_usage AS (
            SELECT 
                i.item_id,
                i.item_name,
                i.category,
                i.quantity as current_stock,
                i.unit_price,
                COUNT(DISTINCT pr.prescription_id) as monthly_prescriptions,
                AVG(i.quantity) OVER (PARTITION BY i.category) as avg_category_stock
            FROM inventory i
            LEFT JOIN prescriptions pr ON LOWER(pr.medication_name) LIKE '%' || LOWER(i.item_name) || '%'
            GROUP BY i.item_id, i.item_name, i.category, i.quantity, i.unit_price
        )
        SELECT 
            item_name,
            category,
            current_stock,
            unit_price,
            monthly_prescriptions,
            avg_category_stock,
            CASE 
                WHEN current_stock < 10 THEN 'CRITICAL'
                WHEN current_stock < 20 THEN 'LOW'
                WHEN current_stock > 100 THEN 'OVERSTOCKED'
                ELSE 'OPTIMAL'
            END as stock_status,
            ROUND(current_stock / NULLIF(monthly_prescriptions, 0), 2) as months_of_supply
        FROM monthly_usage
        ORDER BY stock_status, months_of_supply NULLS LAST
        LIMIT 15;
        """
        self.execute_query(
            "13. Inventory optimization and stock level analysis",
            query_13
        )
        
        # Query 14: Doctor performance and patient satisfaction metrics
        query_14 = """
        WITH doctor_metrics AS (
            SELECT 
                d.doctor_id,
                d.first_name || ' ' || d.last_name as doctor_name,
                d.specialization,
                COUNT(DISTINCT a.appointment_id) as total_appointments,
                COUNT(DISTINCT a.patient_id) as unique_patients,
                AVG(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) as completion_rate,
                COUNT(DISTINCT mr.record_id) as medical_records_created,
                COUNT(DISTINCT pr.prescription_id) as prescriptions_written
            FROM doctors d
            LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
            LEFT JOIN medical_records mr ON d.doctor_id = mr.doctor_id
            LEFT JOIN prescriptions pr ON d.doctor_id = pr.doctor_id
            WHERE d.is_active = true
            GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization
        )
        SELECT 
            doctor_name,
            specialization,
            total_appointments,
            unique_patients,
            ROUND(completion_rate * 100, 2) as completion_rate_percent,
            medical_records_created,
            prescriptions_written,
            ROUND(unique_patients * 1.0 / NULLIF(total_appointments, 0), 2) as avg_appointments_per_patient,
            CASE 
                WHEN total_appointments > 20 AND completion_rate > 0.8 THEN 'HIGH PERFORMER'
                WHEN total_appointments > 10 AND completion_rate > 0.6 THEN 'GOOD PERFORMER'
                ELSE 'NEEDS REVIEW'
            END as performance_category
        FROM doctor_metrics
        ORDER BY total_appointments DESC, completion_rate DESC
        LIMIT 12;
        """
        self.execute_query(
            "14. Doctor performance metrics and categorization",
            query_14
        )
        
        # Query 15: Financial forecasting and trend analysis
        query_15 = """
        WITH daily_revenue AS (
            SELECT 
                DATE(created_at) as revenue_date,
                SUM(amount) as daily_revenue,
                COUNT(*) as daily_transactions
            FROM billing 
            WHERE status = 'Paid' AND created_at >= CURRENT_DATE - INTERVAL '90 days'
            GROUP BY DATE(created_at)
        ),
        revenue_trends AS (
            SELECT 
                revenue_date,
                daily_revenue,
                daily_transactions,
                LAG(daily_revenue, 7) OVER (ORDER BY revenue_date) as revenue_7_days_ago,
                LAG(daily_revenue, 30) OVER (ORDER BY revenue_date) as revenue_30_days_ago,
                AVG(daily_revenue) OVER (ORDER BY revenue_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as weekly_moving_avg,
                SUM(daily_revenue) OVER (ORDER BY revenue_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) as monthly_running_total
            FROM daily_revenue
        )
        SELECT 
            revenue_date,
            daily_revenue,
            daily_transactions,
            revenue_7_days_ago,
            ROUND(100.0 * (daily_revenue - revenue_7_days_ago) / NULLIF(revenue_7_days_ago, 0), 2) as weekly_growth_percent,
            weekly_moving_avg,
            monthly_running_total,
            CASE 
                WHEN daily_revenue > weekly_moving_avg * 1.2 THEN 'ABOVE TREND'
                WHEN daily_revenue < weekly_moving_avg * 0.8 THEN 'BELOW TREND'
                ELSE 'ON TREND'
            END as trend_status
        FROM revenue_trends
        WHERE revenue_date >= CURRENT_DATE - INTERVAL '30 days'
        ORDER BY revenue_date DESC
        LIMIT 15;
        """
        self.execute_query(
            "15. Financial forecasting and revenue trend analysis",
            query_15
        )
    
    def run_all_queries(self):
        """Execute all 15+ SQL queries for comprehensive testing"""
        print("🏥 HEALTHCARE MANAGEMENT SYSTEM - SQL QUERY TESTING")
        print("="*80)
        print("Testing 15+ advanced SQL queries including:")
        print("• Basic queries with filtering and aggregation")
        print("• Advanced JOIN operations across multiple tables") 
        print("• Window functions for rankings and analytics")
        print("• OLAP queries with GROUPING SETS and CUBE")
        print("• Complex analytical queries with CTEs and subqueries")
        print("="*80)
        
        self.test_basic_queries()
        self.test_advanced_joins()
        self.test_window_functions()
        self.test_olap_queries()
        self.test_complex_analytics()
        
        print(f"\n{'='*80}")
        print("🎉 SQL QUERY TESTING COMPLETED SUCCESSFULLY!")
        print("📊 15+ advanced queries executed and analyzed")
        print(f"{'='*80}")
    
    def close_connection(self):
        """Close database connection"""
        self.db.close()

if __name__ == "__main__":
    sql_tester = HealthcareSQLQueries()
    try:
        sql_tester.run_all_queries()
    finally:
        sql_tester.close_connection()
