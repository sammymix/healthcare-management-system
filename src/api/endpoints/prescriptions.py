from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.config import get_db
from src.schemas.prescription import Prescription, PrescriptionCreate, PrescriptionUpdate
from src.crud import prescription_crud

router = APIRouter()

@router.get("/", response_model=List[Prescription])
def read_prescriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return prescription_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/{prescription_id}", response_model=Prescription)
def read_prescription(prescription_id: int, db: Session = Depends(get_db)):
    prescription = prescription_crud.get(db, id=prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription

@router.post("/", response_model=Prescription, status_code=201)
def create_prescription(prescription: PrescriptionCreate, db: Session = Depends(get_db)):
    return prescription_crud.create(db, obj_in=prescription)

@router.get("/patient/{patient_id}", response_model=List[Prescription])
def get_patient_prescriptions(patient_id: int, db: Session = Depends(get_db)):
    return prescription_crud.get_by_patient(db, patient_id=patient_id)

@router.get("/active/", response_model=List[Prescription])
def get_active_prescriptions(db: Session = Depends(get_db)):
    return prescription_crud.get_active_prescriptions(db)
