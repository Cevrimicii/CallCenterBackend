from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.package import Package
    from app.models.remaininguses import RemainingUses
    from app.models.subscription import Subscription
    from app.models.invoice import Invoice

class User(SQLModel, table=True):
    __tablename__ = "user"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    phone_number: str = Field(max_length=20, unique=True, index=True)
    email: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # İlişkiler
    remaining_uses: List["RemainingUses"] = Relationship(back_populates="user")
    subscriptions: List["Subscription"] = Relationship(back_populates="user")
    invoices: List["Invoice"] = Relationship(back_populates="user")