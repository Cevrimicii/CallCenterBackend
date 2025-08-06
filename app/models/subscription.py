from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.package import Package

class Subscription(SQLModel, table=True):
    __tablename__ = "subscription"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    package_id: int = Field(foreign_key="package.id", index=True)
    
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = Field(default=None)  # varsa taahhüt sonu
    contract_months: Optional[int] = Field(default=None, ge=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # İlişkiler - circular import'u önlemek için TYPE_CHECKING kullanıyoruz
    user: Optional["User"] = Relationship(back_populates="subscriptions")
    package: Optional["Package"] = Relationship(back_populates="subscriptions")