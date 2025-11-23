import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Fix Python path to find our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

try:
    from database.config import SessionLocal
    from src.models import Patient, Doctor, Appointment, MedicalRecord, Prescription, Billing, Inventory
    from sqlalchemy import func, text
    IMPORT_SUCCESS = True
except ImportError as e:
    st.error(f"Import Error: {e}")
    IMPORT_SUCCESS = False

class HealthcareDashboard:
    def __init__(self):
        if IMPORT_SUCCESS:
            self.db = SessionLocal()
        else:
            self.db = None
        self.setup_page()
    
    def setup_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Healthcare Management System",
            page_icon="🏥",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        if not IMPORT_SUCCESS:
            st.error("❌ Cannot connect to database. Please check your setup.")
            return
    
    def setup_sidebar(self):
        """Create sidebar with navigation and filters"""
        st.sidebar.title("🏥 Navigation")
        
        # Main navigation
        page = st.sidebar.radio(
            "Go to",
            ["Dashboard", "Patient Management", "Doctor Management", 
             "Appointments", "Medical Records", "Inventory", "Analytics"]
        )
        
        return page
    
    def display_dashboard(self):
        """Main dashboard with KPIs and overview"""
        st.markdown('<h1 style="font-size: 2.5rem; color: #1f77b4; text-align: center;">🏥 Healthcare Management Dashboard</h1>', unsafe_allow_html=True)
        
        # Key Performance Indicators
        self.display_kpis()
        st.markdown("---")
        
        # Main content in columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.display_patient_demographics()
            self.display_appointment_metrics()
        
        with col2:
            self.display_doctor_status()
            self.display_inventory_alerts()
    
    def display_kpis(self):
        """Display Key Performance Indicators"""
        # Calculate metrics
        total_patients = self.db.query(Patient).count()
        total_doctors = self.db.query(Doctor).filter(Doctor.is_active == True).count()
        total_appointments = self.db.query(Appointment).count()
        
        # Revenue calculation
        revenue_result = self.db.query(Billing.amount).filter(Billing.status == 'Paid').all()
        total_revenue = sum([r[0] for r in revenue_result]) if revenue_result else 0
        
        # Today's appointments
        today = datetime.now().date()
        todays_appointments = self.db.query(Appointment).filter(
            Appointment.appointment_date == today
        ).count()
        
        # Display KPIs
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Patients", total_patients)
        
        with col2:
            st.metric("Active Doctors", total_doctors)
        
        with col3:
            st.metric("Total Appointments", total_appointments)
        
        with col4:
            st.metric("Today's Appointments", todays_appointments)
        
        with col5:
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
    
    def display_patient_demographics(self):
        """Display patient demographic charts"""
        st.subheader("👥 Patient Demographics")
        
        # Gender distribution
        gender_data = self.db.query(
            Patient.gender, 
            func.count(Patient.patient_id)
        ).group_by(Patient.gender).all()
        
        if gender_data:
            gender_df = pd.DataFrame(gender_data, columns=['Gender', 'Count'])
            fig = px.pie(
                gender_df, 
                values='Count', 
                names='Gender', 
                title='Patient Gender Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Age distribution
        patients = self.db.query(Patient).all()
        ages = []
        for patient in patients:
            if patient.date_of_birth:
                age = datetime.now().year - patient.date_of_birth.year
                ages.append(age)
        
        if ages:
            age_df = pd.DataFrame(ages, columns=['Age'])
            fig = px.histogram(
                age_df, 
                x='Age', 
                title='Patient Age Distribution',
                nbins=10
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def display_appointment_metrics(self):
        """Display appointment-related metrics"""
        st.subheader("📅 Appointment Analytics")
        
        # Appointment status distribution
        status_data = self.db.query(
            Appointment.status,
            func.count(Appointment.appointment_id)
        ).group_by(Appointment.status).all()
        
        if status_data:
            status_df = pd.DataFrame(status_data, columns=['Status', 'Count'])
            fig = px.bar(
                status_df,
                x='Status',
                y='Count',
                title='Appointments by Status'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def display_doctor_status(self):
        """Display doctor information and status"""
        st.subheader("👨‍⚕️ Doctor Overview")
        
        # Active doctors by specialization
        spec_data = self.db.query(
            Doctor.specialization,
            func.count(Doctor.doctor_id)
        ).filter(Doctor.is_active == True).group_by(Doctor.specialization).all()
        
        if spec_data:
            spec_df = pd.DataFrame(spec_data, columns=['Specialization', 'Count'])
            fig = px.pie(
                spec_df,
                values='Count',
                names='Specialization',
                title='Doctors by Specialization'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def display_inventory_alerts(self):
        """Display inventory status and alerts"""
        st.subheader("📦 Inventory Status")
        
        # Low stock alert
        low_stock = self.db.query(Inventory).filter(Inventory.quantity < 20).all()
        
        if low_stock:
            st.warning(f"🚨 {len(low_stock)} items are running low on stock!")
            
            low_stock_data = []
            for item in low_stock:
                low_stock_data.append({
                    'Item': item.item_name,
                    'Current Stock': item.quantity,
                    'Category': item.category
                })
            
            st.dataframe(pd.DataFrame(low_stock_data), use_container_width=True)
        else:
            st.success("✅ All inventory items are sufficiently stocked")
    
    def display_patient_management(self):
        """Patient management interface"""
        st.title("👥 Patient Management")
        
        patients = self.db.query(Patient).all()
        
        # Display patients in a nice table
        patient_data = []
        for patient in patients:
            # Calculate age
            age = "N/A"
            if patient.date_of_birth:
                age = datetime.now().year - patient.date_of_birth.year
            
            patient_data.append({
                'ID': patient.patient_id,
                'Name': f"{patient.first_name} {patient.last_name}",
                'Age': age,
                'Gender': patient.gender,
                'Phone': patient.phone,
                'Email': patient.email
            })
        
        if patient_data:
            df = pd.DataFrame(patient_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No patients found in the database.")
    
    def display_doctor_management(self):
        """Doctor management interface"""
        st.title("👨‍⚕️ Doctor Management")
        
        doctors = self.db.query(Doctor).all()
        
        # Display doctors
        doctor_data = []
        for doctor in doctors:
            doctor_data.append({
                'ID': doctor.doctor_id,
                'Name': f"Dr. {doctor.first_name} {doctor.last_name}",
                'Specialization': doctor.specialization,
                'Phone': doctor.phone,
                'Email': doctor.email,
                'Status': 'Active' if doctor.is_active else 'Inactive'
            })
        
        if doctor_data:
            st.dataframe(pd.DataFrame(doctor_data), use_container_width=True)
        else:
            st.info("No doctors found in the database.")
    
    def run(self):
        """Main method to run the dashboard"""
        if not IMPORT_SUCCESS:
            st.error("""
            ❌ Cannot import database modules. Please check:
            1. Database is running
            2. All models are properly defined
            3. Python path is correctly set
            """)
            return
        
        try:
            page = self.setup_sidebar()
            
            if page == "Dashboard":
                self.display_dashboard()
            elif page == "Patient Management":
                self.display_patient_management()
            elif page == "Doctor Management":
                self.display_doctor_management()
            elif page == "Appointments":
                st.title("📅 Appointments Management")
                st.info("Appointments management page - to be implemented")
            elif page == "Medical Records":
                st.title("🏥 Medical Records")
                st.info("Medical records management page - to be implemented")
            elif page == "Inventory":
                st.title("📦 Inventory Management")
                st.info("Inventory management page - to be implemented")
            elif page == "Analytics":
                st.title("📊 Advanced Analytics")
                st.info("Advanced analytics page - to be implemented")
                
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Please make sure your database is running and contains data.")
        finally:
            if self.db:
                self.db.close()

if __name__ == "__main__":
    dashboard = HealthcareDashboard()
    dashboard.run()
