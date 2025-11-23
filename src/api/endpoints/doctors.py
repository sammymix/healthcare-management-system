from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database.config import get_db
from src.schemas.doctor import Doctor, DoctorCreate, DoctorUpdate
from src.crud import doctor_crud

router = APIRouter()

@router.get("/", response_model=List[Doctor])
def read_doctors(
    skip: int = 0,
    limit: int = 100,
    specialization: Optional[str] = None,
    active_only: bool = True,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve doctors with optional filtering.
    """
    if specialization:
        return doctor_crud.get_by_specialization(db, specialization=specialization, skip=skip, limit=limit)
    elif active_only:
        return doctor_crud.get_active_doctors(db, skip=skip, limit=limit)
    elif search:
        return doctor_crud.search_by_name(db, name=search, skip=skip, limit=limit)
    else:
        return doctor_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/{doctor_id}", response_model=Doctor)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get a specific doctor by ID.
    """
    doctor = doctor_crud.get(db, id=doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID {doctor_id} not found"
        )
    return doctor

@router.post("/", response_model=Doctor, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    """
    Create a new doctor.
    """
    # Check if phone already exists
    if doctor_crud.get_by_phone(db, phone=doctor.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor with this phone number already exists"
        )
    
    # Check if email already exists
    if doctor_crud.get_by_email(db, email=doctor.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor with this email already exists"
        )
    
    # Check if license number already exists
    if doctor_crud.get_by_license(db, license_number=doctor.license_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor with this license number already exists"
        )
    
    return doctor_crud.create(db, obj_in=doctor)

@router.put("/{doctor_id}", response_model=Doctor)
def update_doctor(
    doctor_id: int,
    doctor_update: DoctorUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a doctor's information.
    """
    doctor = doctor_crud.get(db, id=doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID {doctor_id} not found"
        )
    
    return doctor_crud.update(db, db_obj=doctor, obj_in=doctor_update)

@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Delete a doctor.
    """
    doctor = doctor_crud.get(db, id=doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID {doctor_id} not found"
        )
    
    doctor_crud.remove(db, id=doctor_id)
    return {"message": "Doctor deleted successfully"}

@router.get("/specializations/", response_model=List[str])
def get_specializations(db: Session = Depends(get_db)):
    """
    Get all available doctor specializations.
    """
    specializations = db.query(Doctor.specialization).distinct().all()
    return [spec[0] for spec in specializations]

@router.get("/{doctor_id}/appointments", response_model=List[dict])
def get_doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get all appointments for a specific doctor.
    """
    from src.crud import appointment_crud
    appointments = appointment_crud.get_by_doctor(db, doctor_id=doctor_id)
    return appointments
