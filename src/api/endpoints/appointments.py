from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database.config import get_db
from src.schemas.appointment import Appointment, AppointmentCreate, AppointmentUpdate
from src.crud import appointment_crud

router = APIRouter()

@router.get("/", response_model=List[Appointment])
def read_appointments(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    upcoming: bool = False,
    db: Session = Depends(get_db)
):
    """
    Retrieve appointments with optional filtering.
    """
    if status:
        return appointment_crud.get_by_status(db, status=status, skip=skip, limit=limit)
    elif upcoming:
        return appointment_crud.get_upcoming_appointments(db, skip=skip, limit=limit)
    else:
        return appointment_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/{appointment_id}", response_model=Appointment)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Get a specific appointment by ID.
    """
    appointment = appointment_crud.get(db, id=appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    return appointment

@router.post("/", response_model=Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    """
    Create a new appointment.
    """
    # Check if patient exists
    from src.crud import patient_crud
    patient = patient_crud.get(db, id=appointment.patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {appointment.patient_id} not found"
        )
    
    # Check if doctor exists and is active
    from src.crud import doctor_crud
    doctor = doctor_crud.get(db, id=appointment.doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID {appointment.doctor_id} not found"
        )
    if not doctor.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot schedule appointment with inactive doctor"
        )
    
    return appointment_crud.create(db, obj_in=appointment)

@router.put("/{appointment_id}", response_model=Appointment)
def update_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an appointment.
    """
    appointment = appointment_crud.get(db, id=appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    
    return appointment_crud.update(db, db_obj=appointment, obj_in=appointment_update)

@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Delete an appointment.
    """
    appointment = appointment_crud.get(db, id=appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    
    appointment_crud.remove(db, id=appointment_id)
    return {"message": "Appointment deleted successfully"}

@router.get("/patient/{patient_id}", response_model=List[Appointment])
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    """
    Get all appointments for a specific patient.
    """
    return appointment_crud.get_by_patient(db, patient_id=patient_id)

@router.get("/doctor/{doctor_id}", response_model=List[Appointment])
def get_doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get all appointments for a specific doctor.
    """
    return appointment_crud.get_by_doctor(db, doctor_id=doctor_id)
