from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.invoiceitem import InvoiceItem
    from app.models.user import User

class Invoice(SQLModel, table=True):
    __tablename__ = "invoice"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    invoice_number: str = Field(max_length=50, unique=True, index=True)
    
    billing_period_start: datetime
    billing_period_end: datetime
    total_amount: float = Field(default=0, ge=0)
    status: str = Field(default="pending", max_length=20)  # pending, paid, canceled, overdue
    due_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    paid_at: Optional[datetime] = Field(default=None)

    # İlişkiler
    user: Optional["User"] = Relationship(back_populates="invoices")
    items: List["InvoiceItem"] = Relationship(back_populates="invoice")