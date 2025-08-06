from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User

class RemainingUses(SQLModel, table=True):
    __tablename__ = "remaining_uses"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    service_type: str = Field(max_length=100)  # SMS, Email, Call
    remaining_count: int = Field(default=0, ge=0)
    total_allocated: int = Field(default=0, ge=0)    
    last_reset_date: Optional[datetime] = Field(default=None)
    expires_at: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # İlişkiler
    user: Optional["User"] = Relationship(back_populates="remaining_uses")