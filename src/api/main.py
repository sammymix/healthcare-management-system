from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.config import get_db
from src.schemas import *
from src.crud import *

# Create FastAPI application
app = FastAPI(
    title="Healthcare Management System API",
    description="A comprehensive REST API for managing healthcare operations including patients, doctors, appointments, medical records, prescriptions, billing, and inventory.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "Welcome to Healthcare Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "patients": "/patients/",
            "doctors": "/doctors/",
            "appointments": "/appointments/",
            "medical_records": "/medical-records/",
            "prescriptions": "/prescriptions/",
            "billing": "/billing/",
            "inventory": "/inventory/"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "message": "Healthcare API is running"}

# Include routers
from src.api.endpoints import patients, doctors, appointments, medical_records, prescriptions, billing, inventory

app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(medical_records.router, prefix="/medical-records", tags=["Medical Records"])
app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(billing.router, prefix="/billing", tags=["Billing"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
