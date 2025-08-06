from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import Optional,Dict

from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import Optional, Dict
from datetime import datetime

from app.models.user import User

class RemainingUses(SQLModel, table=True):
    __tablename__ = "remaining_uses"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    service_type: str = Field(max_length=100)
    remaining_count: int = Field(default=0, ge=0)
    total_allocated: int = Field(default=0, ge=0)
    # last_reset_date: Optional[datetime] = Field(default=None)
    expires_at: Optional[datetime] = Field(default=None)
    user: Optional[User] = Relationship(back_populates="remaining_uses")