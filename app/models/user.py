from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.package import Package

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str
    phone_number: str
    package_id: int | None = Field(default=None, foreign_key="package.id")
    package: Package | None = Relationship()