from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.config import get_db
from src.schemas.billing import Billing, BillingCreate, BillingUpdate
from src.crud import billing_crud

router = APIRouter()

@router.get("/", response_model=List[Billing])
def read_billing_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return billing_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/{bill_id}", response_model=Billing)
def read_billing_record(bill_id: int, db: Session = Depends(get_db)):
    bill = billing_crud.get(db, id=bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Billing record not found")
    return bill

@router.post("/", response_model=Billing, status_code=201)
def create_billing_record(billing: BillingCreate, db: Session = Depends(get_db)):
    return billing_crud.create(db, obj_in=billing)

@router.get("/patient/{patient_id}", response_model=List[Billing])
def get_patient_billing(patient_id: int, db: Session = Depends(get_db)):
    return billing_crud.get_by_patient(db, patient_id=patient_id)

@router.get("/revenue/total")
def get_total_revenue(db: Session = Depends(get_db)):
    total = billing_crud.get_total_revenue(db)
    return {"total_revenue": float(total)}
