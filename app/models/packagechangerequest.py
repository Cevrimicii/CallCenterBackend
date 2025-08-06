from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import List, Optional,Dict

from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import Optional, Dict
from datetime import datetime

from app.models.invoice import Invoice
from app.models.package import Package
from app.models.user import User

class PackageChangeRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    requested_package_id: int = Field(foreign_key="package.id")
    status: str = Field(default="pending")  # pending, approved, rejected
    requested_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship()
    requested_package: Optional[Package] = Relationship()