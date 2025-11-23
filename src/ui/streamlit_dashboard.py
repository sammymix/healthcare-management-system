import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.config import SessionLocal
from src.models import Patient, Doctor, Appointment, MedicalRecord, Prescription, Billing, Inventory
from sqlalchemy import func, text

class HealthcareDashboard:
    def __init__(self):
        self.db = SessionLocal()
        self.setup_page()
    
    def setup_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Healthcare Management System",
            page_icon="🏥",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #1f77b4;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def setup_sidebar(self):
        """Create sidebar with navigation and filters"""
        st.sidebar.title("🏥 Navigation")
        
        # Main navigation
        page = st.sidebar.radio(
            "Go to",
            ["Dashboard", "Patient Management", "Doctor Management", 
             "Appointments", "Medical Records", "Inventory", "Analytics"]
        )
        
        # Quick filters
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Quick Filters")
        
        # Date range filter
        today = datetime.now()
        start_date = st.sidebar.date_input("Start Date", today - timedelta(days=30))
        end_date = st.sidebar.date_input("End Date", today)
        
        # Status filter
        status_filter = st.sidebar.multiselect(
            "Appointment Status",
            ["Scheduled", "Completed", "Cancelled", "No-show"],
            default=["Scheduled", "Completed"]
        )
        
        return page, start_date, end_date, status_filter
    
    def display_dashboard(self):
        """Main dashboard with KPIs and overview"""
        st.markdown('<h1 class="main-header">🏥 Healthcare Management Dashboard</h1>', unsafe_allow_html=True)
        
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
            st.metric(
                "Total Patients", 
                total_patients, 
                delta=f"+{self.get_patient_growth()}%"
            )
        
        with col2:
            st.metric(
                "Active Doctors", 
                total_doctors,
                delta="+2" if total_doctors > 8 else "0"
            )
        
        with col3:
            st.metric(
                "Total Appointments", 
                total_appointments,
                delta=f"+{self.get_appointment_growth()}%"
            )
        
        with col4:
            st.metric(
                "Today's Appointments", 
                todays_appointments,
                delta=f"+{todays_appointments - 2}" if todays_appointments > 2 else "0"
            )
        
        with col5:
            st.metric(
                "Total Revenue", 
                f"${total_revenue:,.2f}",
                delta=f"+${(total_revenue * 0.1):.2f}"
            )
    
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
                title='Patient Gender Distribution',
                color_discrete_sequence=px.colors.qualitative.Set3
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
                nbins=10,
                color_discrete_sequence=['#2E86AB']
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
                title='Appointments by Status',
                color='Status',
                color_discrete_sequence=px.colors.qualitative.Pastel
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
                title='Doctors by Specialization',
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Doctor list
        doctors = self.db.query(Doctor).filter(Doctor.is_active == True).all()
        doctor_list = []
        for doctor in doctors:
            doctor_list.append({
                'Name': f"Dr. {doctor.first_name} {doctor.last_name}",
                'Specialization': doctor.specialization,
                'Phone': doctor.phone,
                'Email': doctor.email
            })
        
        if doctor_list:
            st.dataframe(pd.DataFrame(doctor_list), use_container_width=True)
    
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
                    'Category': item.category,
                    'Status': 'CRITICAL' if item.quantity < 10 else 'LOW'
                })
            
            st.dataframe(pd.DataFrame(low_stock_data), use_container_width=True)
        else:
            st.success("✅ All inventory items are sufficiently stocked")
        
        # Inventory value summary
        inventory_value = self.db.query(
            func.sum(Inventory.quantity * Inventory.unit_price)
        ).scalar()
        
        if inventory_value:
            st.metric("Total Inventory Value", f"${inventory_value:,.2f}")
    
    def display_patient_management(self):
        """Patient management interface"""
        st.title("👥 Patient Management")
        
        # Patient list with search
        search_term = st.text_input("🔍 Search patients by name:")
        
        if search_term:
            patients = self.db.query(Patient).filter(
                (Patient.first_name.ilike(f"%{search_term}%")) |
                (Patient.last_name.ilike(f"%{search_term}%"))
            ).all()
        else:
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
                'Email': patient.email,
                'Blood Type': patient.blood_type or 'Unknown'
            })
        
        if patient_data:
            df = pd.DataFrame(patient_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No patients found matching your search criteria.")
    
    def display_doctor_management(self):
        """Doctor management interface"""
        st.title("👨‍⚕️ Doctor Management")
        
        # Doctor list with filters
        col1, col2 = st.columns(2)
        
        with col1:
            specialization_filter = st.selectbox(
                "Filter by specialization:",
                ["All"] + [spec[0] for spec in self.db.query(Doctor.specialization).distinct().all()]
            )
        
        with col2:
            status_filter = st.selectbox(
                "Filter by status:",
                ["All", "Active", "Inactive"]
            )
        
        # Build query based on filters
        query = self.db.query(Doctor)
        
        if specialization_filter != "All":
            query = query.filter(Doctor.specialization == specialization_filter)
        
        if status_filter == "Active":
            query = query.filter(Doctor.is_active == True)
        elif status_filter == "Inactive":
            query = query.filter(Doctor.is_active == False)
        
        doctors = query.all()
        
        # Display doctors
        doctor_data = []
        for doctor in doctors:
            doctor_data.append({
                'ID': doctor.doctor_id,
                'Name': f"Dr. {doctor.first_name} {doctor.last_name}",
                'Specialization': doctor.specialization,
                'Phone': doctor.phone,
                'Email': doctor.email,
                'Status': 'Active' if doctor.is_active else 'Inactive',
                'License': doctor.license_number
            })
        
        if doctor_data:
            st.dataframe(pd.DataFrame(doctor_data), use_container_width=True)
        else:
            st.info("No doctors found matching your criteria.")
    
    def get_patient_growth(self):
        """Calculate patient growth percentage (mock data)"""
        return 12  # Mock growth percentage
    
    def get_appointment_growth(self):
        """Calculate appointment growth percentage (mock data)"""
        return 15  # Mock growth percentage
    
    def run(self):
        """Main method to run the dashboard"""
        try:
            page, start_date, end_date, status_filter = self.setup_sidebar()
            
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
            st.error(f"Error connecting to database: {e}")
            st.info("Please make sure your database is running and properly configured")
        finally:
            self.db.close()

if __name__ == "__main__":
    dashboard = HealthcareDashboard()
    dashboard.run()
