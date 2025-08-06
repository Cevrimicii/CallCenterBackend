from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.package import Package
from app.models.remaininguses import RemainingUses

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str
    phone_number: str
    package_id: Optional[int] = Field(default=None, foreign_key="package.id")
    package: Optional[Package] = Relationship(back_populates="users")
    contract_start_date: Optional[datetime] = Field(default=None)
    contract_end_date: Optional[datetime] = Field(default=None)
    remaining_uses: List["RemainingUses"] = Relationship(back_populates="user")