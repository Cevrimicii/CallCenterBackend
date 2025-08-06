from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import List, Optional,Dict

from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import Optional, Dict
from datetime import datetime

from app.models.invoiceitem import InvoiceItem
from app.models.user import User

class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    billing_period_start: datetime
    billing_period_end: datetime
    is_paid: bool = Field(default=True)
    total_amount: float = Field(default=0)
    status: str = Field(default="pending")  # pending, paid, canceled
    created_at: datetime = Field(default_factory=datetime.utcnow)
    paid_at: Optional[datetime] = Field(default=None)

    user: Optional[User] = Relationship(back_populates="invoices")
    items: List["InvoiceItem"] = Relationship(back_populates="invoice")