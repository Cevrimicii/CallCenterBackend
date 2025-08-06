from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.package import Package
    from app.models.user import User

class PackageChangeRequest(SQLModel, table=True):
    __tablename__ = "package_change_request"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    current_package_id: Optional[int] = Field(default=None, foreign_key="package.id")
    requested_package_id: int = Field(foreign_key="package.id")
    status: str = Field(default="pending", max_length=20)  # pending, approved, rejected
    reason: Optional[str] = Field(default=None, max_length=500)
    admin_notes: Optional[str] = Field(default=None, max_length=1000)
    requested_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = Field(default=None)

    # İlişkiler
    user: Optional["User"] = Relationship()
    requested_package: Optional["Package"] = Relationship(
        foreign_keys=[requested_package_id]
    )
    current_package: Optional["Package"] = Relationship(
        foreign_keys=[current_package_id]
    )