from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import Optional,Dict

class Package(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    details: Dict[str, str] = Field(sa_column=Column(JSON))
    commitment: str