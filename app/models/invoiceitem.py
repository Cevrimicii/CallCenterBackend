from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.invoice import Invoice

class InvoiceItem(SQLModel, table=True):
    __tablename__ = "invoice_item"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoice.id", index=True)

    service_type: str = Field(max_length=50)  # SMS, Email, Call
    description: str = Field(max_length=500)
    quantity: int = Field(ge=0)
    unit_price: float = Field(ge=0)
    total_price: float = Field(ge=0)
    tax_rate: Optional[float] = Field(default=0.18, ge=0, le=1)  # KDV oranı

    # İlişkiler
    invoice: Optional["Invoice"] = Relationship(back_populates="items")