from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database.config import get_db
from src.schemas.patient import Patient, PatientCreate, PatientUpdate
from src.crud import patient_crud

router = APIRouter()

@router.get("/", response_model=List[Patient])
def read_patients(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    gender: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve patients with optional filtering and search.
    """
    if search:
        return patient_crud.search_by_name(db, name=search, skip=skip, limit=limit)
    elif gender:
        return patient_crud.get_multi_by_gender(db, gender=gender, skip=skip, limit=limit)
    else:
        return patient_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/{patient_id}", response_model=Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Get a specific patient by ID.
    """
    patient = patient_crud.get(db, id=patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    return patient

@router.post("/", response_model=Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """
    Create a new patient.
    """
    # Check if phone already exists
    if patient_crud.get_by_phone(db, phone=patient.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient with this phone number already exists"
        )
    
    # Check if email already exists (if provided)
    if patient.email and patient_crud.get_by_email(db, email=patient.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient with this email already exists"
        )
    
    return patient_crud.create(db, obj_in=patient)

@router.put("/{patient_id}", response_model=Patient)
def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a patient's information.
    """
    patient = patient_crud.get(db, id=patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    return patient_crud.update(db, db_obj=patient, obj_in=patient_update)

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Delete a patient.
    """
    patient = patient_crud.get(db, id=patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    patient_crud.remove(db, id=patient_id)
    return {"message": "Patient deleted successfully"}

@router.get("/{patient_id}/appointments", response_model=List[dict])
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    """
    Get all appointments for a specific patient.
    """
    from src.crud import appointment_crud
    appointments = appointment_crud.get_by_patient(db, patient_id=patient_id)
    return appointments

@router.get("/{patient_id}/medical-records", response_model=List[dict])
def get_patient_medical_records(patient_id: int, db: Session = Depends(get_db)):
    """
    Get all medical records for a specific patient.
    """
    from src.crud import medical_record_crud
    records = medical_record_crud.get_by_patient(db, patient_id=patient_id)
    return records
