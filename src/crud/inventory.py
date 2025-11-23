from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date
from src.models.inventory import Inventory
from src.schemas.inventory import InventoryCreate, InventoryUpdate
from .base import CRUDBase

class CRUDInventory(CRUDBase[Inventory, InventoryCreate, InventoryUpdate]):
    def __init__(self):
        super().__init__(Inventory)
    
    def get_low_stock(
        self, db: Session, threshold: int = 20, skip: int = 0, limit: int = 100
    ) -> List[Inventory]:
        return (
            db.query(Inventory)
            .filter(Inventory.quantity <= threshold)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_category(
        self, db: Session, category: str, skip: int = 0, limit: int = 100
    ) -> List[Inventory]:
        return (
            db.query(Inventory)
            .filter(Inventory.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_expired_items(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Inventory]:
        return (
            db.query(Inventory)
            .filter(Inventory.expiration_date <= date.today())
            .offset(skip)
            .limit(limit)
            .all()
        )

inventory = CRUDInventory()
