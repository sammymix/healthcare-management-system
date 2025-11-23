from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.config import get_db
from src.schemas.inventory import Inventory, InventoryCreate, InventoryUpdate
from src.crud import inventory_crud

router = APIRouter()

@router.get("/", response_model=List[Inventory])
def read_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return inventory_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=Inventory)
def read_inventory_item(item_id: int, db: Session = Depends(get_db)):
    item = inventory_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item

@router.post("/", response_model=Inventory, status_code=201)
def create_inventory_item(item: InventoryCreate, db: Session = Depends(get_db)):
    return inventory_crud.create(db, obj_in=item)

@router.get("/low-stock/", response_model=List[Inventory])
def get_low_stock(threshold: int = 20, db: Session = Depends(get_db)):
    return inventory_crud.get_low_stock(db, threshold=threshold)

@router.get("/category/{category}", response_model=List[Inventory])
def get_by_category(category: str, db: Session = Depends(get_db)):
    return inventory_crud.get_by_category(db, category=category)
