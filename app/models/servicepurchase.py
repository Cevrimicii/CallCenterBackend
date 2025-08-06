from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import Optional,Dict

from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import Optional, Dict
from datetime import datetime

from app.models.user import User

class ServicePurchase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    service_type: str  # SMS, Email, Call
    count: int = Field(default=0)
    purchase_price: float
    purchase_date: datetime = Field(default_factory=datetime.now)
    
    user: Optional[User] = Relationship()