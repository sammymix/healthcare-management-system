from sqlalchemy import Column, Integer, String, Date, Numeric, Text, DateTime
from database.config import Base
from datetime import datetime

class Inventory(Base):
    __tablename__ = "inventory"

    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(100), nullable=False)
    category = Column(String(50))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2))
    expiration_date = Column(Date)
    supplier = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Inventory {self.item_id} - {self.item_name} (Qty: {self.quantity})>"
