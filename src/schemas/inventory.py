from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class InventoryBase(BaseModel):
    item_name: str
    category: Optional[str] = None
    quantity: int
    unit_price: Optional[float] = None
    expiration_date: Optional[date] = None
    supplier: Optional[str] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    item_name: Optional[str] = None
    quantity: Optional[int] = None

class InventoryInDB(InventoryBase):
    item_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Inventory(InventoryInDB):
    pass
