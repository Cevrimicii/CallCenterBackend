from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User

class ServicePurchase(SQLModel, table=True):
    __tablename__ = "service_purchase"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    service_type: str = Field(max_length=50)  # SMS, Email, Call
    count: int = Field(default=0, ge=0)
    unit_price: float = Field(ge=0)
    purchase_price: float = Field(ge=0)
    purchase_date: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(default=None)
    is_used: bool = Field(default=False)
    
    # İlişkiler
    user: Optional["User"] = Relationship()