from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import List, Optional,Dict

from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import Optional, Dict
from datetime import datetime

from app.models.invoice import Invoice

class InvoiceItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoice.id")

    service_type: str  # SMS, Email, Call
    description: str
    quantity: int
    unit_price: float
    total_price: float

    invoice: Optional[Invoice] = Relationship(back_populates="items")