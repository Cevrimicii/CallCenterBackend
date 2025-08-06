from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import List, Optional,Dict

from app.models.user import User

class Package(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str # ev interneti mobil telefon
    details: Dict[str, str] = Field(sa_column=Column(JSON))
    commitment: str
    users: List["User"] = Relationship(back_populates="package")