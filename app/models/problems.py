from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Problem(SQLModel, table=True):
    __tablename__ = "problem"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    location: str = Field(max_length=200)
    problem: str = Field(max_length=1000)
    estimated_completion_time: datetime
    status: str = Field(default="pending", max_length=50)  # pending, in_progress, completed
    priority: str = Field(default="medium", max_length=20)  # low, medium, high, critical
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
