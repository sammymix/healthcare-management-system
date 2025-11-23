from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.config import get_db
from src.schemas.medical_record import MedicalRecord, MedicalRecordCreate, MedicalRecordUpdate
from src.crud import medical_record_crud

router = APIRouter()

@router.get("/", response_model=List[MedicalRecord])
def read_medical_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return medical_record_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/{record_id}", response_model=MedicalRecord)
def read_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = medical_record_crud.get(db, id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record

@router.post("/", response_model=MedicalRecord, status_code=201)
def create_medical_record(record: MedicalRecordCreate, db: Session = Depends(get_db)):
    return medical_record_crud.create(db, obj_in=record)

@router.get("/patient/{patient_id}", response_model=List[MedicalRecord])
def get_patient_records(patient_id: int, db: Session = Depends(get_db)):
    return medical_record_crud.get_by_patient(db, patient_id=patient_id)
