from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import List, Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.subscription import Subscription

class Package(SQLModel, table=True):
    __tablename__ = "package"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    type: str = Field(max_length=50) # mobile package modem internet
    details: Dict[str, str] = Field(sa_column=Column(JSON))
    commitment: str = Field(max_length=50)  # 12 ay, 24 ay, yok
    monthly_fee: Optional[float] = Field(default=0, ge=0)
    is_active: bool = Field(default=True)
    
    # İlişkiler
    subscriptions: List["Subscription"] = Relationship(back_populates="package")